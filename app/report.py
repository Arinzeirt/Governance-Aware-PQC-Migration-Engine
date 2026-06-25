from executive import (
    generate_priority_actions,
    generate_governance_risks,
    generate_90_day_plan
)

def generate_report(inventory):

    report_lines = []

    total_findings = len(inventory)
    high_priority = sum(1 for item in inventory if item.get("priority") == "High")
    medium_priority = sum(1 for item in inventory if item.get("priority") == "Medium")
    low_priority = sum(1 for item in inventory if item.get("priority") == "Low")

    planned = sum(1 for item in inventory if item.get("migration_status") == "Planned")
    under_review = sum(1 for item in inventory if item.get("migration_status") == "Under Review")
    monitor = sum(1 for item in inventory if item.get("migration_status") == "Monitor")

    readiness_scores = [
        item.get("readiness_score")
        for item in inventory
        if item.get("readiness_score") is not None
    ]

    average_readiness = round(sum(readiness_scores) / len(readiness_scores), 2) if readiness_scores else 0

    high_urgency = sum(1 for item in inventory if item.get("urgency") == "High")
    medium_urgency = sum(1 for item in inventory if item.get("urgency") == "Medium")
    low_urgency = sum(1 for item in inventory if item.get("urgency") == "Low")

    priority_actions = generate_priority_actions(inventory)
    governance_risks = generate_governance_risks(inventory)
    ninety_day_plan = generate_90_day_plan()

    report_lines.append("PQC Migration Readiness Report")
    report_lines.append("=" * 32)
    report_lines.append("")

    report_lines.append("Executive Summary")
    report_lines.append("-" * 17)
    report_lines.append(f"Total Findings: {total_findings}")
    report_lines.append(f"High Priority Findings: {high_priority}")
    report_lines.append(f"Medium Priority Findings: {medium_priority}")
    report_lines.append(f"Low Priority Findings: {low_priority}")
    report_lines.append("")
    report_lines.append(f"Average Readiness Score: {average_readiness}/100")
    report_lines.append(f"High Urgency Findings: {high_urgency}")
    report_lines.append(f"Medium Urgency Findings: {medium_urgency}")
    report_lines.append(f"Low Urgency Findings: {low_urgency}")
    report_lines.append("")
    report_lines.append(f"Migration Status - Planned: {planned}")
    report_lines.append(f"Migration Status - Under Review: {under_review}")
    report_lines.append(f"Migration Status - Monitor: {monitor}")
    report_lines.append("")

    report_lines.append("Executive Recommendations")
    report_lines.append("-" * 25)
    report_lines.append("")

    report_lines.append("Top Priority Migration Actions")
    report_lines.append("")

    if priority_actions:
        for index, action in enumerate(priority_actions, start=1):
            report_lines.append(f"{index}. Asset: {action['asset']}")
            report_lines.append(f"   Owner: {action['owner']}")
            report_lines.append(f"   Phase: {action['phase']}")
            report_lines.append(f"   Recommended Action: {action['action']}")
            report_lines.append("")
    else:
        report_lines.append("No high-priority migration actions identified.")
        report_lines.append("")

    report_lines.append("Governance Risks")
    report_lines.append("")

    if governance_risks:
        for index, risk in enumerate(governance_risks, start=1):
            report_lines.append(f"{index}. Asset: {risk['asset']}")
            report_lines.append(f"   Owner: {risk['owner']}")
            report_lines.append(f"   Status: {risk['status']}")
            report_lines.append("")
    else:
        report_lines.append("No governance risks currently identified.")
        report_lines.append("")

    report_lines.append("90-Day Action Plan")
    report_lines.append("")

    for item in ninety_day_plan:
        report_lines.append(f"{item['period']}: {item['action']}")

    report_lines.append("")
    report_lines.append("Detailed Findings")
    report_lines.append("-" * 17)
    report_lines.append("")

    if not inventory:
        report_lines.append("No cryptographic indicators were found.")
    else:
        for item in inventory:
            report_lines.append(f"File: {item['file']}")
            report_lines.append(f"Finding Type: {item['finding_type']}")

            if item["finding_type"] == "keyword":
                report_lines.append(f"Algorithm/Indicator: {item['algorithm']}")
                report_lines.append(f"Risk: {item['risk']}")
                report_lines.append(f"PQC Status: {item['pqc_status']}")
                report_lines.append(f"Reason: {item['reason']}")

            elif item["finding_type"] == "classification":
                report_lines.append(f"Pattern: {item['pattern']}")
                report_lines.append(f"Asset Type: {item['asset_type']}")
                report_lines.append(f"Classification: {item['classification']}")
                report_lines.append(f"PQC Relevance: {item['pqc_relevance']}")
                report_lines.append(f"Readiness Score: {item['readiness_score']}/100")
                report_lines.append(f"Urgency: {item['urgency']}")
                report_lines.append(f"Coverage Status: {item['coverage_status']}")
                report_lines.append(f"Coverage Reason: {item['coverage_reason']}")
                report_lines.append(f"Migration Direction: {item['migration_direction']}")
                report_lines.append(f"Priority: {item['priority']}")
                report_lines.append(f"Recommendation: {item['recommendation']}")
                report_lines.append(f"Timeline: {item['timeline']}")
                report_lines.append(f"Migration Phase: {item['migration_phase']}")
                report_lines.append(f"Owner: {item['owner']}")
                report_lines.append(f"Criticality: {item['criticality']}")
                report_lines.append(f"Approver: {item['approver']}")
                report_lines.append(f"Evidence Required: {item['evidence']}")
                report_lines.append(f"Migration Status: {item['migration_status']}")

            report_lines.append("-" * 32)

    with open("reports/pqc_report.txt", "w") as f:
        f.write("\n".join(report_lines))
