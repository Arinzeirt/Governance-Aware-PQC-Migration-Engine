from scanner import scan_directory
from inventory import save_inventory
from report import generate_report


def run_enterprise_scan(target):

    activity = []

    activity.append("Enterprise scan started.")

    findings = scan_directory(target)

    activity.append(
        f"Files containing cryptographic indicators: {len(findings)}"
    )

    inventory = save_inventory(findings)

    activity.append(
        f"Inventory generated: {len(inventory)} assets"
    )

    generate_report(inventory)

    activity.append(
        "Executive assessment report generated."
    )

    return {

        "inventory": inventory,

        "activity": activity,

        "findings": findings

    }
