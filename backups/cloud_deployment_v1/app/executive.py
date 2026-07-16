def generate_priority_actions(inventory):

    actions = []

    for item in inventory:

        if item.get("priority") == "High":

            actions.append({
                "asset": item.get("classification"),
                "owner": item.get("owner"),
                "action": item.get("recommendation"),
                "phase": item.get("migration_phase")
            })

    return actions


def generate_governance_risks(inventory):

    risks = []
    seen_assets = set()

    for item in inventory:

        asset = item.get("classification")

        if item.get("migration_status") == "Under Review" and asset not in seen_assets:

            risks.append({
                "asset": asset,
                "owner": item.get("owner"),
                "status": item.get("migration_status")
            })

            seen_assets.add(asset)

    return risks


def generate_90_day_plan():

    return [

        {
            "period": "Month 1",
            "action": "Validate cryptographic inventory and ownership assignments."
        },

        {
            "period": "Month 2",
            "action": "Review high-priority cryptographic assets and governance approvals."
        },

        {
            "period": "Month 3",
            "action": "Begin migration planning for assets with Horizon Short coverage."
        }

    ]
