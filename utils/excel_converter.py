from io import BytesIO
from datetime import datetime, timedelta
import re

import pandas as pd


TARGET_COLUMNS = {
    "Company": ["Company Name", "Industry", "City", "Employees", "Start Date"],
    "Sales": ["Date", "Customer", "Category", "Amount", "Payment Method"],
    "Expenses": ["Date", "Category", "Amount", "Description"],
    "Invoices": ["Customer", "Issue Date", "Due Date", "Amount", "Status"],
    "Employees": ["Department", "Salary", "Hire Date"],
}


KEYWORDS = {
    ("Sales", "Date"): ["date", "sales date", "transaction date", "order date", "تاريخ"],
    ("Sales", "Customer"): ["customer", "client", "buyer", "name", "عميل", "العميل"],
    ("Sales", "Category"): ["category", "type", "product", "service", "الفئة", "نوع"],
    ("Sales", "Amount"): ["revenue", "sales", "income", "amount", "total", "price", "value", "مبيعات", "إيراد", "ايراد", "مبلغ"],
    ("Sales", "Payment Method"): ["payment", "method", "channel", "طريقة"],
    ("Expenses", "Date"): ["date", "expense date", "transaction date", "تاريخ"],
    ("Expenses", "Category"): ["category", "type", "expense type", "cost type", "الفئة", "نوع"],
    ("Expenses", "Amount"): ["cost", "expense", "spending", "amount", "total", "paid", "مصروف", "تكلفة", "مبلغ"],
    ("Expenses", "Description"): ["description", "details", "notes", "memo", "وصف", "ملاحظات"],
    ("Invoices", "Customer"): ["customer", "client", "عميل", "العميل"],
    ("Invoices", "Issue Date"): ["invoice date", "issue date", "date", "تاريخ الفاتورة", "تاريخ"],
    ("Invoices", "Due Date"): ["due date", "deadline", "تاريخ الاستحقاق", "استحقاق"],
    ("Invoices", "Amount"): ["invoice amount", "amount", "total", "value", "مبلغ", "قيمة"],
    ("Invoices", "Status"): ["paid", "unpaid", "overdue", "status", "حالة", "مدفوع", "متأخر"],
    ("Employees", "Department"): ["department", "team", "division", "إدارة", "ادارة", "قسم"],
    ("Employees", "Salary"): ["salary", "payroll", "wage", "compensation", "راتب", "رواتب"],
    ("Employees", "Hire Date"): ["hire date", "joining date", "start date", "تاريخ التوظيف", "تاريخ"],
    ("Company", "Company Name"): ["company", "company name", "business", "name", "شركة", "اسم الشركة"],
    ("Company", "Industry"): ["industry", "sector", "قطاع", "نشاط"],
    ("Company", "City"): ["city", "location", "مدينة", "موقع"],
    ("Company", "Employees"): ["employees", "headcount", "staff", "موظفين", "عدد الموظفين"],
    ("Company", "Start Date"): ["start date", "founded", "established", "تأسيس", "البداية"],
}

SHEET_HINTS = {
    "Sales": ["sales", "revenue", "income", "orders", "مبيعات", "إيرادات", "ايرادات"],
    "Expenses": ["expense", "expenses", "cost", "spending", "مصروف", "مصروفات", "تكاليف"],
    "Invoices": ["invoice", "invoices", "billing", "فاتورة", "فواتير"],
    "Employees": ["employee", "employees", "payroll", "staff", "hr", "موظف", "موظفين", "رواتب"],
    "Company": ["company", "profile", "about", "شركة", "بيانات"],
}


def _norm(value):
    value = str(value).strip().lower()
    value = re.sub(r"[_\-./]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


def _score_column(column_name, keywords):
    normalized = _norm(column_name)
    best = 0
    for keyword in keywords:
        keyword = _norm(keyword)
        if normalized == keyword:
            best = max(best, 100)
        elif keyword in normalized or normalized in keyword:
            best = max(best, 85)
        else:
            parts = [part for part in keyword.split() if len(part) > 2]
            if parts and all(part in normalized for part in parts):
                best = max(best, 70)
    return best


def _sheet_hint_score(sheet_name, target_sheet):
    normalized = _norm(sheet_name)
    return 25 if any(_norm(hint) in normalized for hint in SHEET_HINTS[target_sheet]) else 0


def _read_workbook(file_obj):
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    excel = pd.ExcelFile(file_obj)
    sheets = {}
    for sheet_name in excel.sheet_names:
        df = pd.read_excel(excel, sheet_name=sheet_name)
        df = df.dropna(how="all")
        sheets[sheet_name] = df
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    return sheets


def _best_mapping_for_sheet(target_sheet, sheets):
    best_sheet = None
    best_mapping = {}
    best_score = -1

    for source_sheet, df in sheets.items():
        if df.empty and target_sheet != "Company":
            continue
        used_columns = set()
        mapping = {}
        score = _sheet_hint_score(source_sheet, target_sheet)

        for target_column in TARGET_COLUMNS[target_sheet]:
            candidates = []
            for source_column in df.columns:
                if source_column in used_columns:
                    continue
                column_score = _score_column(source_column, KEYWORDS.get((target_sheet, target_column), []))
                if column_score:
                    candidates.append((column_score, source_column))

            if candidates:
                column_score, source_column = sorted(candidates, reverse=True)[0]
                used_columns.add(source_column)
                mapping[target_column] = (source_sheet, source_column, min(100, column_score + _sheet_hint_score(source_sheet, target_sheet)))
                score += column_score

        if score > best_score:
            best_sheet = source_sheet
            best_mapping = mapping
            best_score = score

    return best_sheet, best_mapping, best_score


def _series_or_default(df, source_column, default, rows):
    if source_column and source_column in df.columns:
        return df[source_column].reset_index(drop=True)
    return pd.Series([default] * rows)


def _clean_amount(series):
    return pd.to_numeric(series.astype(str).str.replace(",", "", regex=False).str.replace("SAR", "", regex=False), errors="coerce").fillna(0)


def _clean_date(series, default=None):
    default = default or datetime.today()
    return pd.to_datetime(series, errors="coerce").fillna(default)


def _normalize_status(value):
    text = _norm(value)
    if any(word in text for word in ["overdue", "late", "متأخر", "متاخر"]):
        return "Overdue"
    if any(word in text for word in ["paid", "مدفوع"]) and "unpaid" not in text:
        return "Paid"
    return "Unpaid"


def _build_sheet(target_sheet, sheets, mapping):
    source_sheet = next((item[0] for item in mapping.values()), None)
    source_df = sheets.get(source_sheet, pd.DataFrame()).copy()
    rows = max(len(source_df), 1 if target_sheet == "Company" else 0)

    if target_sheet == "Company":
        today = pd.Timestamp(datetime.today().date())
        return pd.DataFrame({
            "Company Name": [_series_or_default(source_df, mapping.get("Company Name", (None, None, 0))[1], "Uploaded Company", 1).iloc[0]],
            "Industry": [_series_or_default(source_df, mapping.get("Industry", (None, None, 0))[1], "General", 1).iloc[0]],
            "City": [_series_or_default(source_df, mapping.get("City", (None, None, 0))[1], "Unknown", 1).iloc[0]],
            "Employees": [_clean_amount(_series_or_default(source_df, mapping.get("Employees", (None, None, 0))[1], 0, 1)).iloc[0]],
            "Start Date": [today],
        })

    if rows == 0:
        return pd.DataFrame(columns=TARGET_COLUMNS[target_sheet])

    today = pd.Timestamp(datetime.today().date())
    if target_sheet == "Sales":
        return pd.DataFrame({
            "Date": _clean_date(_series_or_default(source_df, mapping.get("Date", (None, None, 0))[1], today, rows), today),
            "Customer": _series_or_default(source_df, mapping.get("Customer", (None, None, 0))[1], "Unknown Customer", rows).fillna("Unknown Customer"),
            "Category": _series_or_default(source_df, mapping.get("Category", (None, None, 0))[1], "General", rows).fillna("General"),
            "Amount": _clean_amount(_series_or_default(source_df, mapping.get("Amount", (None, None, 0))[1], 0, rows)),
            "Payment Method": _series_or_default(source_df, mapping.get("Payment Method", (None, None, 0))[1], "Unknown", rows).fillna("Unknown"),
        })

    if target_sheet == "Expenses":
        return pd.DataFrame({
            "Date": _clean_date(_series_or_default(source_df, mapping.get("Date", (None, None, 0))[1], today, rows), today),
            "Category": _series_or_default(source_df, mapping.get("Category", (None, None, 0))[1], "General", rows).fillna("General"),
            "Amount": _clean_amount(_series_or_default(source_df, mapping.get("Amount", (None, None, 0))[1], 0, rows)),
            "Description": _series_or_default(source_df, mapping.get("Description", (None, None, 0))[1], "", rows).fillna(""),
        })

    if target_sheet == "Invoices":
        issue = _clean_date(_series_or_default(source_df, mapping.get("Issue Date", (None, None, 0))[1], today, rows), today)
        due = _clean_date(_series_or_default(source_df, mapping.get("Due Date", (None, None, 0))[1], today + timedelta(days=30), rows), today + timedelta(days=30))
        status_source = _series_or_default(source_df, mapping.get("Status", (None, None, 0))[1], "Unpaid", rows)
        return pd.DataFrame({
            "Customer": _series_or_default(source_df, mapping.get("Customer", (None, None, 0))[1], "Unknown Customer", rows).fillna("Unknown Customer"),
            "Issue Date": issue,
            "Due Date": due,
            "Amount": _clean_amount(_series_or_default(source_df, mapping.get("Amount", (None, None, 0))[1], 0, rows)),
            "Status": status_source.fillna("Unpaid").map(_normalize_status),
        })

    if target_sheet == "Employees":
        return pd.DataFrame({
            "Department": _series_or_default(source_df, mapping.get("Department", (None, None, 0))[1], "General", rows).fillna("General"),
            "Salary": _clean_amount(_series_or_default(source_df, mapping.get("Salary", (None, None, 0))[1], 0, rows)),
            "Hire Date": _clean_date(_series_or_default(source_df, mapping.get("Hire Date", (None, None, 0))[1], today, rows), today),
        })

    return pd.DataFrame(columns=TARGET_COLUMNS[target_sheet])


def convert_to_cfo_template(file_obj):
    sheets = _read_workbook(file_obj)
    mappings = {}
    preview_rows = []
    converted = {}

    for target_sheet in TARGET_COLUMNS:
        _source_sheet, mapping, score = _best_mapping_for_sheet(target_sheet, sheets)
        mappings[target_sheet] = mapping
        converted[target_sheet] = _build_sheet(target_sheet, sheets, mapping)
        for target_column in TARGET_COLUMNS[target_sheet]:
            source_sheet, source_column, confidence = mapping.get(target_column, ("-", "-", 0))
            preview_rows.append({
                "Target Sheet": target_sheet,
                "Target Column": target_column,
                "Source Sheet": source_sheet,
                "Source Column": source_column,
                "Confidence": confidence,
            })

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in converted.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)

    sales_ready = "Amount" in converted["Sales"] and converted["Sales"]["Amount"].sum() > 0
    expenses_ready = "Amount" in converted["Expenses"] and converted["Expenses"]["Amount"].sum() >= 0
    usable = sales_ready and expenses_ready

    return {
        "file": output,
        "mapping_preview": pd.DataFrame(preview_rows),
        "converted": converted,
        "usable": usable,
        "message": "Converted successfully." if usable else "Could not confidently identify enough sales and expense data.",
    }
