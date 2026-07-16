import json
from collections import Counter
from pathlib import Path


INVENTORY_FILE = Path("inventory.json")


def load_inventory():

    if not INVENTORY_FILE.exists():
        return []

    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


def get_dashboard_metrics():

    inventory = load_inventory()

    if not inventory:

        return {
            "total_assets": 0,
            "average_readiness": 0,
            "high_priority": 0,
            "medium_priority": 0,
            "low_priority": 0,
            "phase1": 0,
            "phase2": 0,
            "phase3": 0,
        }

    total_assets = len(inventory)

    average_readiness = round(
        sum(item.get("readiness_score", 0) for item in inventory)
        / total_assets
    )

    return {

        "total_assets": total_assets,

        "average_readiness": average_readiness,

        "high_priority": sum(
            1 for item in inventory
            if item.get("priority") == "High"
        ),

        "medium_priority": sum(
            1 for item in inventory
            if item.get("priority") == "Medium"
        ),

        "low_priority": sum(
            1 for item in inventory
            if item.get("priority") == "Low"
        ),

        "phase1": sum(
            1 for item in inventory
            if item.get("migration_phase") == "Phase 1"
        ),

        "phase2": sum(
            1 for item in inventory
            if item.get("migration_phase") == "Phase 2"
        ),

        "phase3": sum(
            1 for item in inventory
            if item.get("migration_phase") == "Phase 3"
        ),
    }


def get_priority_distribution():

    inventory = load_inventory()

    return dict(
        Counter(
            item.get("priority", "Unknown")
            for item in inventory
        )
    )


def get_phase_distribution():

    inventory = load_inventory()

    return dict(
        Counter(
            item.get("migration_phase", "Unknown")
            for item in inventory
        )
    )


def get_business_zone_distribution():

    inventory = load_inventory()

    return dict(
        Counter(
            item.get("business_zone", "Unknown")
            for item in inventory
        )
    )


def get_asset_type_distribution():

    inventory = load_inventory()

    return dict(
        Counter(
            item.get("asset_type", "Unknown")
            for item in inventory
        )
    )


def get_compliance_distribution():

    inventory = load_inventory()

    return dict(
        Counter(
            item.get("compliance_risk", "Unknown")
            for item in inventory
        )
    )


def get_enterprise_intelligence():

    inventory = load_inventory()

    return {

        "inventory": inventory,

        "metrics": get_dashboard_metrics(),

        "priority": get_priority_distribution(),

        "phases": get_phase_distribution(),

        "business": get_business_zone_distribution(),

        "asset_types": get_asset_type_distribution(),

        "compliance": get_compliance_distribution(),

    }


if __name__ == "__main__":

    intelligence = get_enterprise_intelligence()

    print(json.dumps(intelligence, indent=4))
