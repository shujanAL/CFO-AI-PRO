from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(metrics, health, best_decision):

    doc = SimpleDocTemplate("Executive_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>CFO AI PRO</b>", styles["Title"])
    )

    story.append(
        Paragraph("Executive Financial Report", styles["Heading1"])
    )

    story.append(
        Paragraph(f"Financial Health: {health['status']}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Revenue: {metrics['total_sales']:,.0f} SAR", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Net Profit: {metrics['net_profit']:,.0f} SAR", styles["BodyText"])
    )

    story.append(
        Paragraph(
            f"Recommended Decision: {best_decision['Decision']}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Expected Profit: {best_decision['Expected Profit']:,.0f} SAR",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return "Executive_Report.pdf"