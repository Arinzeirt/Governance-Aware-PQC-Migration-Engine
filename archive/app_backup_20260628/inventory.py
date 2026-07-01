from coverage import assess_coverage
from roadmap import assign_phase
from business_context import (
    infer_business_zone,
    infer_throughput_class,
    infer_latency_sensitivity,
    infer_asset_criticality
)
from regulatory import (
    assess_dora_impact,
    assess_pci_impact,
    assess_nist_alignment,
    assess_compliance_risk,
    recommend_deadline
)
import json
from risk import assess_risk
from recommendations import get_recommendation
from governance import get_governance
from readiness import assess_readiness


def save_inventory(findings):

    inventory = []

    for file_path, matches in findings.items():

        for match in matches:

            if match["type"] == "keyword":

                algorithm = match["value"]
                risk_info = assess_risk(algorithm)

                inventory.append({
                    "file": file_path,
                    "finding_type": "keyword",
                    "algorithm": algorithm,
                    "risk": risk_info["risk"],
                    "pqc_status": risk_info["pqc_status"],
                    "reason": risk_info["reason"]
                })

            elif match["type"] == "classification":

                item = match["value"]

                recommendation = get_recommendation(
                    item["classification"]
                )

                governance = get_governance(
                    item["classification"]
                )

                readiness = assess_readiness(
                    item["classification"]
                )

                coverage = assess_coverage(
                    item["classification"]
                )

                business_zone = infer_business_zone({
                    "file": file_path,
                    "classification": item["classification"],
                    "asset_type": item["asset_type"]
                })

                throughput_class = infer_throughput_class(business_zone)
                latency_sensitivity = infer_latency_sensitivity(business_zone)
                asset_criticality = infer_asset_criticality(business_zone)

                context_item = {
                    "classification": item["classification"],
                    "priority": recommendation["priority"],
                    "coverage_status": coverage["coverage_status"],
                    "business_zone": business_zone,
                    "asset_criticality": asset_criticality
                }

                dora_impact = assess_dora_impact(context_item)
                pci_impact = assess_pci_impact(context_item)
                nist_alignment = assess_nist_alignment(context_item)
                compliance_risk = assess_compliance_risk(context_item)
                recommended_deadline = recommend_deadline(context_item)

                inventory.append({
                    "file": file_path,
                    "finding_type": "classification",
                    "pattern": item["pattern"],
                    "asset_type": item["asset_type"],
                    "classification": item["classification"],
                    "pqc_relevance": item["pqc_relevance"],
                    "migration_direction": item["migration_direction"],
                    "priority": recommendation["priority"],
                    "recommendation": recommendation["recommendation"],
                    "timeline": recommendation["timeline"],
                    "owner": governance["owner"],
                    "criticality": governance["criticality"],
                    "approver": governance["approver"],
                    "evidence": governance["evidence"],
                    "migration_status": governance["migration_status"],
                    "readiness_score": readiness["readiness_score"],
                    "urgency": readiness["urgency"],
                    "coverage_status": coverage["coverage_status"],
                    "coverage_reason": coverage["coverage_reason"],
                    "migration_phase": assign_phase({
                        "priority": recommendation["priority"],
                        "coverage_status": coverage["coverage_status"],
                        "readiness_score": readiness["readiness_score"]
                    }),
                    "business_zone": business_zone,
                    "throughput_class": throughput_class,
                    "latency_sensitivity": latency_sensitivity,
                    "asset_criticality": asset_criticality,
                    "dora_impact": dora_impact,
                    "pci_impact": pci_impact,
                    "nist_alignment": nist_alignment,
                    "compliance_risk": compliance_risk,
                    "recommended_deadline": recommended_deadline
                })

    with open("inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

    return inventory
