from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


BRAND = colors.HexColor("#1f4e79")
ACCENT = colors.HexColor("#2ca58d")
LIGHT_BG = colors.HexColor("#f4f8fb")
DARK_TEXT = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#6b7280")


def _sar(value):
    try:
        return f"{float(value):,.0f} SAR"
    except (TypeError, ValueError):
        return "0 SAR"


def _pct(value):
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "0.0%"


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.6 * cm, 1.1 * cm, "CFO AI PRO - Decision support report, not a final credit decision")
    canvas.drawRightString(A4[0] - 1.6 * cm, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()


def _section_title(text, styles):
    return Paragraph(text, styles["SectionTitle"])


def _metric_cards(metrics, health):
    data = [
        [
            Paragraph("<b>Financial Health</b><br/>" + f'{health.get("score", 0)}/100<br/>{health.get("status", "N/A")}', _card_style()),
            Paragraph("<b>Total Revenue</b><br/>" + _sar(metrics.get("total_sales", 0)), _card_style()),
            Paragraph("<b>Net Profit</b><br/>" + _sar(metrics.get("net_profit", 0)), _card_style()),
        ],
        [
            Paragraph("<b>Profit Margin</b><br/>" + _pct(metrics.get("profit_margin", 0)), _card_style()),
            Paragraph("<b>Expense Ratio</b><br/>" + f'{float(metrics.get("expense_ratio", 0)):.1%}', _card_style()),
            Paragraph("<b>Overdue Ratio</b><br/>" + f'{float(metrics.get("overdue_ratio", 0)):.1%}', _card_style()),
        ],
    ]
    table = Table(data, colWidths=[5.3 * cm, 5.3 * cm, 5.3 * cm], rowHeights=[2.2 * cm, 2.2 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d9e5ef")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def _card_style():
    return ParagraphStyle(
        "CardText",
        fontName="Helvetica",
        fontSize=10,
        leading=16,
        textColor=DARK_TEXT,
        alignment=TA_CENTER,
    )


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=BRAND,
        alignment=TA_CENTER,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "Subtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=18,
    ))
    styles.add(ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=BRAND,
        spaceBefore=10,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "BodyClean",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        "Callout",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=DARK_TEXT,
        backColor=colors.HexColor("#eef8f5"),
        borderColor=ACCENT,
        borderWidth=0.8,
        borderPadding=10,
        spaceBefore=6,
        spaceAfter=12,
    ))
    return styles


def _decision_table(best_decision):
    rows = [
        ["Recommended Action", str(best_decision.get("Decision", "N/A"))],
        ["Category", str(best_decision.get("Category", "N/A"))],
        ["Scenario Value", f'{best_decision.get("Value", 0)}%'],
        ["Expected Profit", _sar(best_decision.get("Expected Profit", 0))],
        ["Profit Change", _sar(best_decision.get("Profit Change", 0))],
        ["Financial Health After Scenario", str(best_decision.get("Health", "N/A"))],
        ["Execution Risk", str(best_decision.get("Risk", "N/A"))],
        ["Confidence", str(best_decision.get("Confidence", "N/A"))],
    ]
    table = Table(rows, colWidths=[6.4 * cm, 9.6 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BRAND),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("TEXTCOLOR", (1, 0), (1, -1), DARK_TEXT),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8dee9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def generate_pdf(metrics, health, best_decision):
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
    styles = _build_styles()
    today = datetime.now().strftime("%Y-%m-%d")

    story = [
        Paragraph("CFO AI PRO", styles["ReportTitle"]),
        Paragraph(f"Executive Financial Decision Report - Generated {today}", styles["Subtitle"]),
        _metric_cards(metrics, health),
        Spacer(1, 12),
        _section_title("Executive Recommendation", styles),
        Paragraph(
            "CFO AI PRO recommends the highest-ranked scenario based on projected profit, financial health, execution risk, and confidence. This report is designed for management review and should be combined with human judgment before implementation.",
            styles["Callout"],
        ),
        KeepTogether([
            _section_title("Recommended Scenario", styles),
            _decision_table(best_decision),
        ]),
        Spacer(1, 10),
        _section_title("Why This Matters", styles),
        Paragraph(
            "The selected scenario produced the strongest decision score among the tested options. The recommendation is evidence-based, but it is not a guaranteed result. Management should validate market demand, operational capacity, and cash-flow impact before committing.",
            styles["BodyClean"],
        ),
        Spacer(1, 8),
        _section_title("Management Advice", styles),
        Paragraph(
            "Run the recommended action as a controlled pilot first. Track weekly revenue, gross margin, overdue invoices, and expense movement. If the pilot improves profit without weakening financial health, scale gradually.",
            styles["BodyClean"],
        ),
        Spacer(1, 8),
        Paragraph(
            "<b>Note:</b> This is a decision-support report generated from uploaded or demo Excel data. Final financing decisions require bank review, supporting documents, and human assessment.",
            styles["BodyClean"],
        ),
    ]

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return output_path
