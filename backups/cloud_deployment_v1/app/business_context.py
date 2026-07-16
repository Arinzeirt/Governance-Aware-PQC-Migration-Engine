def infer_business_zone(item):

    text = (
        item.get("file", "")
        + " "
        + item.get("classification", "")
    ).lower()

    if any(x in text for x in [
        "wallet",
        "payment",
        "transaction",
        "settlement"
    ]):
        return "Critical Payments"

    if any(x in text for x in [
        "jwt",
        "auth",
        "authentication"
    ]):
        return "Customer Authentication"

    if any(x in text for x in [
        "api",
        "webhook"
    ]):
        return "API Gateway"

    return "Internal Operations"


def infer_throughput_class(zone):

    mapping = {
        "Critical Payments": "High Throughput",
        "Settlement Infrastructure": "High Throughput",
        "API Gateway": "Medium Throughput",
        "Customer Authentication": "Medium Throughput",
        "Internal Operations": "Low Throughput",
        "Archive Systems": "Low Throughput",
    }

    return mapping.get(zone, "Low Throughput")


def infer_latency_sensitivity(zone):

    mapping = {
        "Critical Payments": "Critical",
        "Settlement Infrastructure": "Critical",
        "API Gateway": "Elevated",
        "Customer Authentication": "Elevated",
        "Internal Operations": "Normal",
        "Archive Systems": "Normal",
    }

    return mapping.get(zone, "Normal")


def infer_asset_criticality(zone):

    mapping = {
        "Critical Payments": "Critical",
        "Settlement Infrastructure": "Critical",
        "API Gateway": "High",
        "Customer Authentication": "High",
        "Internal Operations": "Medium",
        "Archive Systems": "Low",
    }

    return mapping.get(zone, "Medium")
