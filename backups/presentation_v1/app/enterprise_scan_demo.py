from scanner import scan_directory
from inventory import save_inventory


def run_demo_scan(target):

    findings = scan_directory(target)

    #
    # Demo mode:
    # only analyse the first 100 files containing findings.
    #
    limited = {}

    for index, item in enumerate(findings.items()):

        if index >= 100:
            break

        file_path, matches = item

        limited[file_path] = matches

    inventory = save_inventory(limited)

    return {

        "inventory": inventory,

        "findings": limited,

        "activity": [

            "Executive assessment completed.",

            f"Assets discovered: {len(inventory)}"

        ]

    }
