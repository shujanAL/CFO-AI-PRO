import pandas as pd

REQUIRED_STRUCTURE = {
    "Company": [
        "Company Name",
        "Industry",
        "City",
        "Employees",
        "Start Date"
    ],

    "Sales": [
        "Date",
        "Customer",
        "Category",
        "Amount",
        "Payment Method"
    ],

    "Expenses": [
        "Date",
        "Category",
        "Amount",
        "Description"
    ],

    "Invoices": [
        "Customer",
        "Issue Date",
        "Due Date",
        "Amount",
        "Status"
    ],

    "Employees": [
        "Department",
        "Salary",
        "Hire Date"
    ]
}


def validate_excel(file_path):

    try:
        excel = pd.ExcelFile(file_path)

    except Exception as e:
        return False, f"Cannot open Excel file.\n{e}"

    # Check sheets
    for sheet in REQUIRED_STRUCTURE:

        if sheet not in excel.sheet_names:
            return False, f"Missing sheet: {sheet}"

    # Check columns
    for sheet, required_columns in REQUIRED_STRUCTURE.items():

        df = pd.read_excel(file_path, sheet_name=sheet)

        for column in required_columns:

            if column not in df.columns:
                return False, f"Missing column '{column}' in sheet '{sheet}'"

    return True, "Excel template is completely valid."