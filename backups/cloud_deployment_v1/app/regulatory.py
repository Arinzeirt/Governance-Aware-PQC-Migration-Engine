def assess_dora_impact(item):

    if (
        item.get("business_zone") == "Critical Payments"
        and item.get("coverage_status") == "Horizon Short"
    ):
        return "High"

    if item.get("asset_criticality") == "High":
        return "Medium"

    return "Low"


def assess_pci_impact(item):

    classification = item.get("classification", "")

    if any(x in classification for x in [
        "RSA",
        "Encryption",
        "Authentication",
        "Key"
    ]):
        return "High"

    return "Medium"


def assess_nist_alignment(item):

    if item.get("coverage_status") == "Horizon Short":
        return "Partial"

    if item.get("coverage_status") == "Covers":
        return "Strong"

    return "Partial"


def assess_compliance_risk(item):

    if (
        item.get("priority") == "High"
        and item.get("coverage_status") == "Horizon Short"
    ):
        return "Elevated"

    if item.get("priority") == "Medium":
        return "Moderate"

    return "Low"


def recommend_deadline(item):

    if (
        item.get("business_zone") == "Critical Payments"
        and item.get("coverage_status") == "Horizon Short"
    ):
        return "2028"

    if item.get("priority") == "High":
        return "2030"

    if item.get("priority") == "Medium":
        return "2032"

    return "2035"
