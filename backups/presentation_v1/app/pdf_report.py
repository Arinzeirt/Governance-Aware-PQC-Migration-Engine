import json
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)


def count_value(items, field, value):
    return sum(1 for i in items if i.get(field) == value)


def build_pdf_report(
    inventory_path="inventory.json",
    output_path="reports/pqc_executive_report.pdf"
):
    inventory_path = Path(inventory_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(exist_ok=True)

    if not inventory_path.exists():
        raise FileNotFoundError("inventory.json not found. Run a scan first.")

    inventory = json.loads(inventory_path.read_text())
    classified = [i for i in inventory if i.get("finding_type") == "classification"]

    total = len(classified)
    high = count_value(classified, "priority", "High")
    medium = count_value(classified, "priority", "Medium")
    low = count_value(classified, "priority", "Low")

    dora_high = count_value(classified, "dora_impact", "High")
    pci_high = count_value(classified, "pci_impact", "High")
    elevated_compliance = count_value(classified, "compliance_risk", "Elevated")

    readiness_scores = [
        i.get("readiness_score") for i in classified
        if i.get("readiness_score") is not None
    ]
    avg_readiness = round(sum(readiness_scores) / len(readiness_scores), 2) if readiness_scores else 0

    deadlines = [i.get("recommended_deadline") for i in classified if i.get("recommended_deadline")]
    recommended_deadline = min(deadlines) if deadlines else "Not Available"

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=42,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleCustom", parent=styles["Title"], fontSize=22, textColor=colors.HexColor("#0f172a"))
    heading = ParagraphStyle("HeadingCustom", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor("#1e3a8a"), spaceBefore=12, spaceAfter=8)
    body = ParagraphStyle("BodyCustom", parent=styles["BodyText"], fontSize=9, leading=13)

    story = []

    story.append(Paragraph("PQC Migration Readiness Assessment Report", title))
    story.append(Paragraph("Governance, Business Impact, and Regulatory Migration Intelligence", styles["Heading3"]))
    story.append(Spacer(1, 0.2 * inch))

    meta = [
        ["Assessment Target", "Streple Backend"],
        ["Generated", datetime.now().strftime("%Y-%m-%d %H:%M")],
        ["Report Type", "Executive Security Assessment"],
        ["Prepared By", "PQC Migration Engine"],
    ]

    table = Table(meta, colWidths=[150, 330])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Executive Summary", heading))
    story.append(Paragraph(
        "This report summarizes post-quantum cryptographic migration readiness, business impact, regulatory exposure, governance status, and recommended migration urgency based on the scanned application codebase.",
        body
    ))

    summary = [
        ["Metric", "Value"],
        ["Affected Systems / Findings", total],
        ["High Priority Findings", high],
        ["Medium Priority Findings", medium],
        ["Low Priority Findings", low],
        ["Average Readiness Score", f"{avg_readiness}/100"],
        ["DORA High Impact Findings", dora_high],
        ["PCI DSS High Impact Findings", pci_high],
        ["Elevated Compliance Risk Findings", elevated_compliance],
        ["Recommended Migration Deadline", recommended_deadline],
    ]

    table = Table(summary, colWidths=[270, 210])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(table)

    story.append(Paragraph("Business Impact Summary", heading))

    business_rows = [["Asset", "Business Zone", "Throughput", "Latency", "Criticality"]]
    for item in classified:
        business_rows.append([
            Paragraph(item.get("classification", ""), body),
            item.get("business_zone", ""),
            item.get("throughput_class", ""),
            item.get("latency_sensitivity", ""),
            item.get("asset_criticality", ""),
        ])

    table = Table(business_rows, colWidths=[135, 110, 95, 70, 70], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    story.append(PageBreak())

    story.append(Paragraph("Regulatory Impact Assessment", heading))

    regulatory_rows = [["Asset", "DORA", "PCI DSS", "NIST PQC", "Risk", "Deadline"]]
    for item in classified:
        regulatory_rows.append([
            Paragraph(item.get("classification", ""), body),
            item.get("dora_impact", ""),
            item.get("pci_impact", ""),
            item.get("nist_alignment", ""),
            item.get("compliance_risk", ""),
            item.get("recommended_deadline", ""),
        ])

    table = Table(regulatory_rows, colWidths=[140, 60, 70, 80, 70, 60], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    story.append(Paragraph("Top Priority Migration Actions", heading))

    priority_rows = [["Asset", "Owner", "Phase", "Recommendation"]]
    for item in classified:
        if item.get("priority") == "High":
            priority_rows.append([
                item.get("classification", ""),
                item.get("owner", ""),
                item.get("migration_phase", ""),
                Paragraph(item.get("recommendation", ""), body)
            ])

    table = Table(priority_rows, colWidths=[120, 90, 70, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    story.append(PageBreak())
    story.append(Paragraph("Detailed Technical Findings", heading))

    detailed_rows = [["Asset", "Priority", "Coverage", "Owner", "Status", "Recommendation"]]
    for item in classified:
        detailed_rows.append([
            Paragraph(item.get("classification", ""), body),
            item.get("priority", ""),
            item.get("coverage_status", ""),
            item.get("owner", ""),
            item.get("migration_status", ""),
            Paragraph(item.get("recommendation", ""), body),
        ])

    table = Table(detailed_rows, colWidths=[95, 55, 75, 75, 75, 105], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    doc.build(story)
    return output_path


if __name__ == "__main__":
    output = build_pdf_report()
    print(f"PDF report generated: {output}")
