from analytics import get_enterprise_intelligence

from decision import (
    infer_threat_level,
    infer_governance_status,
    infer_coverage_status,
    infer_migration_mode,
)


def get_decision():

    intelligence = get_enterprise_intelligence()

    inventory = intelligence["inventory"]

    metrics = intelligence["metrics"]

    threat = infer_threat_level(inventory)

    governance = infer_governance_status(inventory)

    coverage = infer_coverage_status(inventory)

    mode = infer_migration_mode(inventory)

    readiness = metrics["average_readiness"]

    if readiness >= 80:

        strategy = "FULL PQC MIGRATION"

        confidence = "96%"

        status = "HEALTHY"

    elif readiness >= 60:

        strategy = "HYBRID PQC MIGRATION"

        confidence = "92%"

        status = "MONITOR"

    else:

        strategy = "PLANNING REQUIRED"

        confidence = "81%"

        status = "ACTION REQUIRED"

    return {

        "strategy": strategy,

        "confidence": confidence,

        "metrics": metrics,

        "mode": mode,

        "threat": threat,

        "governance": governance,

        "coverage": coverage,

        "health": {

            "threat": threat,

            "governance": governance,

            "coverage": coverage,

            "readiness": readiness,

            "status": status,

        },

        "evidence": [

            f"Assets Analysed: {metrics['total_assets']}",

            f"High Priority Assets: {metrics['high_priority']}",

            f"Average Readiness: {readiness}",

            f"Threat Level: {threat}",

            f"Governance: {governance}",

            f"Coverage: {coverage}",

            f"Migration Mode: {mode}"

        ],

        "recommendation":
        "Review governance, prioritise Phase 1 assets, and begin hybrid migration planning."

    }

