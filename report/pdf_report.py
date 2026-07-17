from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)

from utils.i18n import tr

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except Exception:  # Optional dependency; PDF still works without shaping.
    arabic_reshaper = None
    get_display = None


BRAND = colors.HexColor("#5b1235")
ACCENT = colors.HexColor("#b88954")
LIGHT_BG = colors.HexColor("#fbf7f0")
DARK_TEXT = colors.HexColor("#211827")
MUTED = colors.HexColor("#706777")

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def _register_unicode_fonts():
    global FONT_REGULAR, FONT_BOLD
    candidates = [
        (r"C:\Windows\Fonts\tahoma.ttf", r"C:\Windows\Fonts\tahomabd.ttf", "CFOArabic"),
        (r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf", "CFOArabic"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "CFOArabic"),
    ]
    for regular, bold, name in candidates:
        if Path(regular).exists():
            pdfmetrics.registerFont(TTFont(name, regular))
            FONT_REGULAR = name
            if Path(bold).exists():
                pdfmetrics.registerFont(TTFont(f"{name}-Bold", bold))
                FONT_BOLD = f"{name}-Bold"
            else:
                FONT_BOLD = name
            break


def _rtl(text, is_arabic):
    text = str(text)
    if is_arabic and arabic_reshaper and get_display:
        return get_display(arabic_reshaper.reshape(text))
    return text


def _sar(value, is_arabic=False):
    try:
        amount = f"{float(value):,.0f}"
    except (TypeError, ValueError):
        amount = "0"
    return f"{amount} ر.س" if is_arabic else f"{amount} SAR"


def _pct(value):
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "0.0%"


def _footer_factory(language="en"):
    is_arabic = language == "ar"

    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_REGULAR, 8)
        canvas.setFillColor(MUTED)
        note = (
            "CFO AI PRO - تقرير لدعم القرار وليس قرارًا ائتمانيًا نهائيًا"
            if is_arabic
            else "CFO AI PRO - Decision support report, not a final credit decision"
        )
        page = f"صفحة {doc.page}" if is_arabic else f"Page {doc.page}"
        canvas.drawString(1.6 * cm, 1.1 * cm, _rtl(note, is_arabic))
        canvas.drawRightString(A4[0] - 1.6 * cm, 1.1 * cm, _rtl(page, is_arabic))
        canvas.restoreState()

    return _footer


def _section_title(text, styles, is_arabic=False):
    return Paragraph(_rtl(text, is_arabic), styles["SectionTitle"])


def _card_style():
    return ParagraphStyle(
        "CardText",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=16,
        textColor=DARK_TEXT,
        alignment=TA_CENTER,
    )


def _card(label, value, is_arabic=False):
    return Paragraph(f"<b>{_rtl(label, is_arabic)}</b><br/>{_rtl(value, is_arabic)}", _card_style())


def _metric_cards(metrics, health, language="en"):
    is_arabic = language == "ar"
    labels = {
        "health": "الصحة المالية" if is_arabic else "Financial Health",
        "revenue": "إجمالي الإيرادات" if is_arabic else "Total Revenue",
        "profit": "صافي الربح" if is_arabic else "Net Profit",
        "margin": "هامش الربح" if is_arabic else "Profit Margin",
        "expenses": "نسبة المصروفات" if is_arabic else "Expense Ratio",
        "overdue": "نسبة الفواتير المتأخرة" if is_arabic else "Overdue Ratio",
    }
    health_status = tr(health.get("status", "N/A"), language) if is_arabic else health.get("status", "N/A")
    data = [
        [
            _card(labels["health"], f'{health.get("score", 0)}/100 - {health_status}', is_arabic),
            _card(labels["revenue"], _sar(metrics.get("total_sales", 0), is_arabic), is_arabic),
            _card(labels["profit"], _sar(metrics.get("net_profit", 0), is_arabic), is_arabic),
        ],
        [
            _card(labels["margin"], _pct(metrics.get("profit_margin", 0)), is_arabic),
            _card(labels["expenses"], f'{float(metrics.get("expense_ratio", 0)):.1%}', is_arabic),
            _card(labels["overdue"], f'{float(metrics.get("overdue_ratio", 0)):.1%}', is_arabic),
        ],
    ]
    table = Table(data, colWidths=[5.3 * cm, 5.3 * cm, 5.3 * cm], rowHeights=[2.2 * cm, 2.2 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#eadfd4")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def _build_styles(language="en"):
    is_arabic = language == "ar"
    alignment = TA_RIGHT if is_arabic else TA_LEFT
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName=FONT_BOLD,
        fontSize=24,
        leading=30,
        textColor=BRAND,
        alignment=TA_CENTER,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "Subtitle",
        parent=styles["BodyText"],
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=18,
    ))
    styles.add(ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=18,
        textColor=BRAND,
        alignment=alignment,
        spaceBefore=10,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "BodyClean",
        parent=styles["BodyText"],
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT,
        alignment=alignment,
    ))
    styles.add(ParagraphStyle(
        "Callout",
        parent=styles["BodyText"],
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=15,
        textColor=DARK_TEXT,
        alignment=alignment,
        backColor=colors.HexColor("#fff7ed"),
        borderColor=ACCENT,
        borderWidth=0.8,
        borderPadding=10,
        spaceBefore=6,
        spaceAfter=12,
    ))
    return styles


def _decision_table(best_decision, language="en"):
    is_arabic = language == "ar"
    labels = (
        [
            ("الإجراء المقترح", tr(best_decision.get("Decision", "N/A"), language)),
            ("الفئة", tr(best_decision.get("Category", "N/A"), language)),
            ("قيمة السيناريو", f'{best_decision.get("Value", 0)}%'),
            ("الربح المتوقع", _sar(best_decision.get("Expected Profit", 0), is_arabic)),
            ("تغير الربح", _sar(best_decision.get("Profit Change", 0), is_arabic)),
            ("الصحة المالية بعد السيناريو", tr(best_decision.get("Health", "N/A"), language)),
            ("مخاطر التنفيذ", tr(best_decision.get("Risk", "N/A"), language)),
            ("الثقة", {"High": "عالية", "Medium": "متوسطة", "Low": "منخفضة"}.get(best_decision.get("Confidence", "N/A"), best_decision.get("Confidence", "N/A"))),
        ]
        if is_arabic
        else [
            ("Recommended Action", best_decision.get("Decision", "N/A")),
            ("Category", best_decision.get("Category", "N/A")),
            ("Scenario Value", f'{best_decision.get("Value", 0)}%'),
            ("Expected Profit", _sar(best_decision.get("Expected Profit", 0), is_arabic)),
            ("Profit Change", _sar(best_decision.get("Profit Change", 0), is_arabic)),
            ("Financial Health After Scenario", best_decision.get("Health", "N/A")),
            ("Execution Risk", best_decision.get("Risk", "N/A")),
            ("Confidence", best_decision.get("Confidence", "N/A")),
        ]
    )
    rows = [[_rtl(label, is_arabic), _rtl(value, is_arabic)] for label, value in labels]
    table = Table(rows, colWidths=[6.4 * cm, 9.6 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BRAND),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("TEXTCOLOR", (1, 0), (1, -1), DARK_TEXT),
        ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
        ("FONTNAME", (1, 0), (1, -1), FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#eadfd4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT" if is_arabic else "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def generate_pdf(metrics, health, best_decision, language="en"):
    is_arabic = language == "ar"
    _register_unicode_fonts()
    output_path = "Executive_Report.pdf"
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
        title="CFO AI PRO Executive Report",
    )
    styles = _build_styles(language)
    today = datetime.now().strftime("%Y-%m-%d")

    if is_arabic:
        title = "CFO AI PRO"
        subtitle = f"تقرير القرار المالي التنفيذي - تاريخ الإنشاء {today}"
        rec_title = "التوصية التنفيذية"
        rec_body = (
            "يوصي CFO AI PRO بالسيناريو الأعلى ترتيبًا بناءً على الربح المتوقع، الصحة المالية، مخاطر التنفيذ، ومستوى الثقة. "
            "هذا التقرير مخصص لدعم قرار الإدارة ويجب دمجه مع الحكم البشري قبل التنفيذ."
        )
        scenario_title = "السيناريو المقترح"
        why_title = "لماذا هذا مهم؟"
        why_body = (
            "حقق السيناريو المختار أعلى درجة قرار بين الخيارات التي تم اختبارها. التوصية مبنية على الأدلة، لكنها ليست نتيجة مضمونة. "
            "ينبغي على الإدارة التحقق من الطلب في السوق، القدرة التشغيلية، وأثر التدفق النقدي قبل الالتزام."
        )
        advice_title = "نصيحة للإدارة"
        advice_body = (
            "ابدأ بتنفيذ الإجراء المقترح كتجربة محدودة. راقب الإيرادات أسبوعيًا، هامش الربح، الفواتير المتأخرة، وحركة المصروفات. "
            "إذا حسّنت التجربة الربح دون إضعاف الصحة المالية، يمكن التوسع تدريجيًا."
        )
        note = (
            "ملاحظة: هذا تقرير لدعم القرار تم إنشاؤه من بيانات Excel المرفوعة أو بيانات العرض. قرارات التمويل النهائية تتطلب مراجعة بنكية ومستندات داعمة وتقييمًا بشريًا."
        )
    else:
        title = "CFO AI PRO"
        subtitle = f"Executive Financial Decision Report - Generated {today}"
        rec_title = "Executive Recommendation"
        rec_body = (
            "CFO AI PRO recommends the highest-ranked scenario based on projected profit, financial health, execution risk, and confidence. "
            "This report is designed for management review and should be combined with human judgment before implementation."
        )
        scenario_title = "Recommended Scenario"
        why_title = "Why This Matters"
        why_body = (
            "The selected scenario produced the strongest decision score among the tested options. The recommendation is evidence-based, but it is not a guaranteed result. "
            "Management should validate market demand, operational capacity, and cash-flow impact before committing."
        )
        advice_title = "Management Advice"
        advice_body = (
            "Run the recommended action as a controlled pilot first. Track weekly revenue, gross margin, overdue invoices, and expense movement. "
            "If the pilot improves profit without weakening financial health, scale gradually."
        )
        note = (
            "<b>Note:</b> This is a decision-support report generated from uploaded or demo Excel data. Final financing decisions require bank review, supporting documents, and human assessment."
        )

    story = [
        Paragraph(_rtl(title, is_arabic), styles["ReportTitle"]),
        Paragraph(_rtl(subtitle, is_arabic), styles["Subtitle"]),
        _metric_cards(metrics, health, language),
        Spacer(1, 12),
        _section_title(rec_title, styles, is_arabic),
        Paragraph(_rtl(rec_body, is_arabic), styles["Callout"]),
        KeepTogether([
            _section_title(scenario_title, styles, is_arabic),
            _decision_table(best_decision, language),
        ]),
        Spacer(1, 10),
        _section_title(why_title, styles, is_arabic),
        Paragraph(_rtl(why_body, is_arabic), styles["BodyClean"]),
        Spacer(1, 8),
        _section_title(advice_title, styles, is_arabic),
        Paragraph(_rtl(advice_body, is_arabic), styles["BodyClean"]),
        Spacer(1, 8),
        Paragraph(_rtl(note, is_arabic) if is_arabic else note, styles["BodyClean"]),
    ]

    footer = _footer_factory(language)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output_path
