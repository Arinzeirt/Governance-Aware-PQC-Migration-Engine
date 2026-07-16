def infer_threat_level(inventory):
    high_count = sum(1 for item in inventory if item.get("priority") == "High")

    if high_count >= 3:
        return "HIGH"
    elif high_count >= 1:
        return "MEDIUM"
    return "LOW"


def infer_governance_status(inventory):
    under_review = sum(
        1 for item in inventory
        if item.get("migration_status") == "Under Review"
    )

    if under_review > 0:
        return "PENDING"
    return "VALID"


def infer_coverage_status(inventory):
    gaps = sum(
        1 for item in inventory
        if item.get("coverage_status") in ["Horizon Short", "Not Yet Assessed"]
    )

    if gaps > 0:
        return "PARTIAL"
    return "ADEQUATE"


def infer_migration_mode(inventory):
    high_count = sum(1 for item in inventory if item.get("priority") == "High")
    coverage_gaps = sum(
        1 for item in inventory
        if item.get("coverage_status") == "Horizon Short"
    )

    if high_count > 0 or coverage_gaps > 0:
        return "HYBRID"

    return "CLASSICAL"
