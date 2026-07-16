from components.wizard import show_wizard
from components.progress import show_progress
from components.summary import show_summary
from components.enterprise_intelligence import show_enterprise_intelligence

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import sys
import subprocess

sys.path.append("app")

from decision import (
    infer_threat_level,
    infer_governance_status,
    infer_coverage_status,
    infer_migration_mode
)


st.set_page_config(
    page_title="PQC Migration Command Center",
    layout="wide"
)
if "screen" not in st.session_state:
    st.session_state.screen = "wizard"

if st.session_state.screen == "wizard":
    show_wizard()
    st.stop()

elif st.session_state.screen == "progress":
    show_progress()
    st.stop()

elif st.session_state.screen == "summary":
    show_summary()
    st.stop()

# If we reach here, continue into the existing dashboard

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1320px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2937;
}

[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #e5e7eb !important;
}

[data-testid="stSidebar"] button {
    background-color: #1f2937 !important;
    color: #ffffff !important;
    border: 1px solid #374151 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] button:hover {
    background-color: #374151 !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stDownloadButton button {
    background-color: #1f2937 !important;
    color: #ffffff !important;
    border: 1px solid #374151 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {
    color: #111827 !important;
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #111827 !important;
}

[data-testid="stSidebar"] [role="button"] {
    color: #e5e7eb !important;
}

.app-badge {
    display: inline-block;
    border: 1px solid #cbd5e1;
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #334155;
    background: #ffffff;
}

.soft-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 10px rgba(15,23,42,0.06);
}

.stat-card {
    background: #ffffff;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 10px rgba(15,23,42,0.06);
    min-height: 108px;
}

.stat-label {
    font-size: 0.82rem;
    color: #64748b;
    margin-bottom: 4px;
}

.stat-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0f172a;
}

.stat-note {
    font-size: 0.76rem;
    color: #64748b;
}

.panel-title {
    font-size: 1.15rem;
    font-weight: 750;
    color: #0f172a;
    margin-bottom: 4px;
}

.panel-subtitle {
    font-size: 0.84rem;
    color: #64748b;
    margin-bottom: 16px;
}

.inner-box {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 14px;
    background: #ffffff;
    margin-bottom: 12px;
}

.inner-label {
    font-size: 0.78rem;
    color: #64748b;
    margin-bottom: 3px;
}

.inner-value {
    font-size: 1rem;
    font-weight: 750;
    color: #0f172a;
}

.logic-row {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 12px;
    background: #ffffff;
    margin-bottom: 10px;
    font-size: 0.88rem;
}

.small-muted {
    color: #64748b;
    font-size: 0.88rem;
}

.red-text {
    color: #dc2626;
    font-weight: 800;
}

.amber-text {
    color: #d97706;
    font-weight: 800;
}

.green-text {
    color: #059669;
    font-weight: 800;
}

.hr-light {
    border-top: 1px solid #e2e8f0;
    margin: 14px 0;
}
</style>
""", unsafe_allow_html=True)


inventory_path = Path("inventory.json")

if not inventory_path.exists():
    inventory = []
    df = pd.DataFrame()
    classified_df = pd.DataFrame()
    fresh_state = True
else:
    with open(inventory_path, "r") as f:
        inventory = json.load(f)

    df = pd.DataFrame(inventory)

    if df.empty:
        classified_df = pd.DataFrame()
        fresh_state = True
    else:
        classified_df = df[df["finding_type"] == "classification"].copy()
        fresh_state = classified_df.empty


if fresh_state:
    st.info("Fresh state: no inventory loaded. Enter a local folder path and run a PQC scan to generate findings.")

    st.markdown("### Scan Target")

    scan_col1, scan_col2 = st.columns([4, 1])

    with scan_col1:
        scan_path = st.text_input(
            "Enter local folder path",
            value="~/Downloads/streple-backend-main",
            help="Example: ~/Downloads/streple-backend-main"
        )

    with scan_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_scan = st.button(
            "Run PQC Scan",
            use_container_width=True,
            key="fresh_run_scan"
        )

    if run_scan:
        resolved_path = str(Path(scan_path).expanduser())

        if not Path(resolved_path).exists():
            st.error(f"Path does not exist: {resolved_path}")
        else:
            with st.spinner("Running PQC scan..."):
                result = subprocess.run(
                    [
                        sys.executable,
                        "app/main.py",
                        resolved_path
                    ],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:
                st.success("Scan completed. Inventory and report updated.")
                st.rerun()
            else:
                st.error("Scan failed.")
                st.code(result.stderr)

    st.stop()


st.sidebar.title("PQC Command Center")

filtered_df = classified_df.copy()

st.sidebar.markdown("### Scan & Export")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="pqc_filtered_inventory.csv",
    mime="text/csv",
    use_container_width=True
)

if Path("inventory.json").exists():
    st.sidebar.download_button(
        label="Download Full Inventory",
        data=Path("inventory.json").read_text(),
        file_name="inventory.json",
        mime="application/json",
        use_container_width=True
    )

if Path("reports/pqc_report.txt").exists():
    st.sidebar.download_button(
        label="Download PQC Report",
        data=Path("reports/pqc_report.txt").read_text(),
        file_name="pqc_report.txt",
        mime="text/plain",
        use_container_width=True
    )

if Path("reports/pqc_executive_report.pdf").exists():
    with open("reports/pqc_executive_report.pdf", "rb") as pdf_file:
        st.sidebar.download_button(
            label="Download Executive PDF",
            data=pdf_file.read(),
            file_name="pqc_executive_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.sidebar.divider()

st.sidebar.markdown("### Quick Filters")

high_only = st.sidebar.checkbox("High Priority Only")
phase1_only = st.sidebar.checkbox("Phase 1 Only")
coverage_gap_only = st.sidebar.checkbox("Coverage Gaps Only")

if high_only:
    filtered_df = filtered_df[filtered_df["priority"] == "High"]

if phase1_only:
    filtered_df = filtered_df[filtered_df["migration_phase"] == "Phase 1"]

if coverage_gap_only:
    filtered_df = filtered_df[filtered_df["coverage_status"] != "Covers"]

st.sidebar.divider()

with st.sidebar.expander("Advanced Filters", expanded=False):

    priorities = sorted(classified_df["priority"].dropna().unique())
    selected_priorities = st.multiselect(
        "Priority",
        priorities,
        default=priorities
    )
    filtered_df = filtered_df[filtered_df["priority"].isin(selected_priorities)]

    asset_types = sorted(classified_df["asset_type"].dropna().unique())
    selected_asset_types = st.multiselect(
        "Asset Type",
        asset_types,
        default=asset_types
    )
    filtered_df = filtered_df[filtered_df["asset_type"].isin(selected_asset_types)]

    owners = sorted(classified_df["owner"].dropna().unique())
    selected_owners = st.multiselect(
        "Owner",
        owners,
        default=owners
    )
    filtered_df = filtered_df[filtered_df["owner"].isin(selected_owners)]

    statuses = sorted(classified_df["migration_status"].dropna().unique())
    selected_statuses = st.multiselect(
        "Migration Status",
        statuses,
        default=statuses
    )
    filtered_df = filtered_df[filtered_df["migration_status"].isin(selected_statuses)]

st.sidebar.divider()

st.sidebar.caption(
    "Filters update the command center, decision state, roadmap, governance view, and analytics."
)

total_findings = len(filtered_df)
high_priority = len(filtered_df[filtered_df["priority"] == "High"])
medium_priority = len(filtered_df[filtered_df["priority"] == "Medium"])
low_priority = len(filtered_df[filtered_df["priority"] == "Low"])

planned = len(filtered_df[filtered_df["migration_status"] == "Planned"])
under_review = len(filtered_df[filtered_df["migration_status"] == "Under Review"])
monitor = len(filtered_df[filtered_df["migration_status"] == "Monitor"])

coverage_gaps = len(filtered_df[filtered_df["coverage_status"] != "Covers"])
phase1_assets = len(filtered_df[filtered_df["migration_phase"] == "Phase 1"])

readiness_scores = filtered_df["readiness_score"].dropna() if "readiness_score" in filtered_df.columns else []
score = round(readiness_scores.mean()) if len(readiness_scores) > 0 else 0

if score >= 80:
    readiness_label = "STRONG"
elif score >= 60:
    readiness_label = "MODERATE"
elif score >= 40:
    readiness_label = "WEAK"
else:
    readiness_label = "CRITICAL"

runtime_mode = infer_migration_mode(filtered_df.to_dict("records"))

inferred_threat_level = infer_threat_level(
    filtered_df.to_dict("records")
)

governance_summary = infer_governance_status(
    filtered_df.to_dict("records")
)

coverage_summary = infer_coverage_status(
    filtered_df.to_dict("records")
)

threat_horizon = (
    "ELEVATED"
    if inferred_threat_level in ["MEDIUM", "HIGH"]
    else "NORMAL"
)

if coverage_gaps > 0 or high_priority > 0:
    inferred_protection_horizon = "10 YEARS"
elif medium_priority > 0:
    inferred_protection_horizon = "5 YEARS"
else:
    inferred_protection_horizon = "1 YEAR"

evidence_ready_auto = (
    "evidence" in filtered_df.columns
    and filtered_df["evidence"].notna().any()
)

compliance_ready_auto = Path("reports/pqc_report.txt").exists()

governance_ready_auto = governance_summary == "VALID"


header_left, header_right = st.columns([4, 1])

with header_left:
    st.markdown("""
    <h1 style="margin-bottom: 0.25rem;">PQC Migration Command Center</h1>
    <p class="small-muted" style="max-width: 850px;">
    Governance-aware post-quantum cryptographic migration decision support for digital financial infrastructure.
    </p>
    """, unsafe_allow_html=True)

with header_right:
    st.markdown("""
    <div style="text-align: right; padding-top: 10px;">
        <span class="app-badge">Research Prototype v0.10</span>
    </div>
    """, unsafe_allow_html=True)


st.markdown("")

with st.container(border=True):
    st.markdown("### Scan Target")

    scan_col1, scan_col2 = st.columns([4, 1])

    with scan_col1:
        scan_path = st.text_input(
            "Enter local folder path",
            value="~/Downloads/streple-backend-main",
            help="Example: ~/Downloads/streple-backend-main"
        )

    with scan_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_scan = st.button(
            "Run PQC Scan",
            use_container_width=True
        )

        clear_scan = st.button(
            "Clear Scan",
            use_container_width=True
        )

    if clear_scan:
        for target_file in [
            Path("inventory.json"),
            Path("reports/pqc_report.txt")
        ]:
            if target_file.exists():
                target_file.unlink()

        st.success("Scan cleared. System returned to fresh state.")
        st.rerun()

    if run_scan:
        resolved_path = str(Path(scan_path).expanduser())

        if not Path(resolved_path).exists():
            st.error(f"Path does not exist: {resolved_path}")
        else:
            with st.spinner("Running PQC scan..."):
                result = subprocess.run(
                    [
                        sys.executable,
                        "app/main.py",
                        resolved_path
                    ],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:
                st.success("Scan completed. Inventory and report updated.")
                st.code(result.stdout[-2000:])
                st.rerun()
            else:
                st.error("Scan failed.")
                st.code(result.stderr)

st.markdown("")

top1, top2, top3, top4 = st.columns(4)

top1.markdown(f"""
<div class="stat-card">
    <div class="stat-label">Current Mode</div>
    <div class="stat-value">{runtime_mode}</div>
    <div class="stat-note">Recommended operating state</div>
</div>
""", unsafe_allow_html=True)

top2.markdown(f"""
<div class="stat-card">
    <div class="stat-label">Threat Horizon</div>
    <div class="stat-value">{threat_horizon}</div>
    <div class="stat-note">Based on PQC exposure</div>
</div>
""", unsafe_allow_html=True)

top3.markdown(f"""
<div class="stat-card">
    <div class="stat-label">Governance Status</div>
    <div class="stat-value">{governance_summary}</div>
    <div class="stat-note">Ownership and review posture</div>
</div>
""", unsafe_allow_html=True)

top4.markdown(f"""
<div class="stat-card">
    <div class="stat-label">Coverage Status</div>
    <div class="stat-value">{coverage_summary}</div>
    <div class="stat-note">Protection adequacy view</div>
</div>
""", unsafe_allow_html=True)


st.markdown("")


main_left, main_right = st.columns([2, 1])

with main_left:
    with st.container(border=True):
        st.markdown("### Runtime Inputs")
        st.caption("Adjust decision variables while retaining the current inventory-driven architecture.")

        input_col1, input_col2 = st.columns(2)

        threat_level = inferred_threat_level
        protection_horizon = inferred_protection_horizon
        governance_ready = governance_ready_auto
        compliance_ready = compliance_ready_auto
        audit_ready = evidence_ready_auto

        with input_col1:
            st.text_input(
                "Threat Level",
                value=threat_level,
                disabled=True,
                help="Automatically inferred from scan findings and priority levels."
            )

            st.text_input(
                "Protection Horizon",
                value=protection_horizon,
                disabled=True,
                help="Automatically inferred from coverage gaps and migration priority."
            )

        with input_col2:
            st.checkbox(
                "Governance Approved",
                value=governance_ready,
                disabled=True,
                help="Remains unchecked when governance approval or owner action is still pending."
            )

            st.checkbox(
                "Compliance Ready",
                value=compliance_ready,
                disabled=True,
                help="Checked when a PQC report has been generated."
            )

            st.checkbox(
                "Evidence / Audit Ready",
                value=audit_ready,
                disabled=True,
                help="Checked when evidence requirements exist in the generated inventory."
            )

        st.markdown("#### Migration Scenario State")

        if coverage_gaps > 0 or threat_level in ["HIGH", "CRITICAL"]:
            active_scenario = "High Exposure"
        elif not governance_ready or not compliance_ready or not audit_ready:
            active_scenario = "Governance Block"
        elif threat_level == "MEDIUM":
            active_scenario = "Hybrid"
        else:
            active_scenario = "Stable"

        scenario_1, scenario_2, scenario_3, scenario_4 = st.columns(4)

        scenario_1.button(
            "Stable",
            use_container_width=True,
            disabled=(active_scenario != "Stable")
        )

        scenario_2.button(
            "Hybrid",
            use_container_width=True,
            disabled=(active_scenario != "Hybrid")
        )

        scenario_3.button(
            "Governance Block",
            use_container_width=True,
            disabled=(active_scenario != "Governance Block")
        )

        scenario_4.button(
            "High Exposure",
            use_container_width=True,
            disabled=(active_scenario != "High Exposure")
        )

        st.caption(f"Current scenario inferred from findings: {active_scenario}")

    st.markdown("")

    assess_col1, assess_col2, assess_col3, assess_col4, assess_col5 = st.columns(5)

    assess_col1.metric("Assets", total_findings, "Classified")
    assess_col2.metric("High Priority", high_priority, "Near-term")
    assess_col3.metric("Coverage Gaps", coverage_gaps, "Review")
    assess_col4.metric("Phase 1", phase1_assets, "Immediate")
    assess_col5.metric("Readiness", f"{score}/100", readiness_label)


with main_right:
    with st.container(border=True):
        st.markdown("### Migration Decision")
        st.caption("Decision engine evaluates inventory, coverage, governance, and runtime assumptions.")

        if coverage_gaps > 0 or threat_level in ["HIGH", "CRITICAL"] or protection_horizon == "10 YEARS":
            decision = "Activate Hybrid PQC Planning"
            decision_reason = "Coverage gaps, exposure pressure, or long protection horizon require hybrid migration planning."
            state_label = "ACTION REQUIRED"
            confidence = 85
            next_action = "Begin Phase 1 migration planning."
        elif not governance_ready or not compliance_ready or not audit_ready:
            decision = "Hold Migration Pending Governance Validation"
            decision_reason = "Governance, compliance, or evidence readiness is incomplete."
            state_label = "REVIEW REQUIRED"
            confidence = 65
            next_action = "Validate ownership, approvals, and evidence."
        else:
            decision = "Monitor Current Migration State"
            decision_reason = "No immediate migration trigger is active under current assumptions."
            state_label = "MONITOR"
            confidence = 55
            next_action = "Continue periodic cryptographic review."

        st.markdown("**Migration State**")

        if state_label == "MONITOR":
            st.success(state_label)
        elif state_label == "REVIEW REQUIRED":
            st.warning(state_label)
        else:
            st.error(state_label)

        st.markdown("**Decision**")
        st.write(decision)

        st.markdown("**Confidence**")
        st.progress(confidence / 100)
        st.caption(f"{confidence}% confidence")

        st.markdown("**Reason**")
        st.write(decision_reason)

        st.markdown("**Next Action**")
        st.write(next_action)


st.markdown("")

logic_col, audit_col = st.columns(2)

with logic_col:
    with st.container(border=True):
        st.markdown("### State Logic")
        st.caption("Decision states used by the governance-aware migration engine.")

        st.markdown("**CLASSICAL:** Low threat or incomplete migration pressure.")
        st.markdown("**HYBRID:** Elevated threat, coverage gap, or long protection horizon requiring transition planning.")
        st.markdown("**PQC:** Strong governance, compliance readiness, and migration preparedness.")
        st.markdown("**REVIEW:** Governance, compliance, or audit evidence remains incomplete.")

with audit_col:
    now = datetime.now().strftime("%H:%M:%S")

    with st.container(border=True):
        st.markdown("### Decision Trace")
        st.caption("Recent explainability trace generated from current dashboard state.")

        st.write(f"[{now}] Inventory loaded from inventory.json.")
        st.write(f"[{now}] Coverage gaps detected: {coverage_gaps}.")
        st.write(f"[{now}] Phase 1 assets identified: {phase1_assets}.")
        st.write(f"[{now}] Decision generated: {decision}.")


st.markdown("")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Executive Decisions",
    "Migration Roadmap",
    "Governance",
    "Coverage",
    "Business Impact",
    "Regulatory Impact",
    "Asset Inventory",
    "Analytics"
])


with tab1:
    st.subheader("Executive Decisions")

    show_enterprise_intelligence()


    st.markdown("### Top Priority Migration Actions")

    priority_df = filtered_df[filtered_df["priority"] == "High"]

    if not priority_df.empty:
        priority_view = priority_df[
            [
                "classification",
                "owner",
                "migration_phase",
                "recommendation"
            ]
        ].copy()

        priority_view.columns = [
            "Asset",
            "Owner",
            "Migration Phase",
            "Recommendation"
        ]

        st.dataframe(priority_view, use_container_width=True)
    else:
        st.info("No high-priority actions identified.")

    st.markdown("### Governance Risks")

    governance_risk_df = filtered_df[
        filtered_df["migration_status"] == "Under Review"
    ].drop_duplicates(subset=["classification"])

    if not governance_risk_df.empty:
        governance_risk_view = governance_risk_df[
            [
                "classification",
                "owner",
                "migration_status"
            ]
        ].copy()

        governance_risk_view.columns = [
            "Asset",
            "Owner",
            "Status"
        ]

        st.dataframe(governance_risk_view, use_container_width=True)
    else:
        st.success("No governance risks identified.")

    st.markdown("### 90-Day Action Plan")

    action_plan = pd.DataFrame([
        {
            "Period": "Month 1",
            "Action": "Validate cryptographic inventory and ownership assignments."
        },
        {
            "Period": "Month 2",
            "Action": "Review high-priority cryptographic assets and governance approvals."
        },
        {
            "Period": "Month 3",
            "Action": "Begin migration planning for assets with Horizon Short coverage."
        }
    ])

    st.dataframe(action_plan, use_container_width=True)


with tab2:
    st.subheader("Migration Roadmap")

    roadmap_columns = [
        "migration_phase",
        "classification",
        "priority",
        "readiness_score",
        "urgency",
        "owner",
        "migration_status",
        "timeline",
        "recommendation"
    ]

    available_roadmap_columns = [
        col for col in roadmap_columns if col in filtered_df.columns
    ]

    if available_roadmap_columns and not filtered_df.empty:
        roadmap_view = filtered_df[available_roadmap_columns].copy()

        roadmap_view = roadmap_view.rename(columns={
            "migration_phase": "Phase",
            "classification": "Asset",
            "priority": "Priority",
            "readiness_score": "Readiness Score",
            "urgency": "Urgency",
            "owner": "Owner",
            "migration_status": "Status",
            "timeline": "Timeline",
            "recommendation": "Recommendation"
        })

        phase_order = {
            "Phase 1": 1,
            "Phase 2": 2,
            "Phase 3": 3
        }

        roadmap_view["phase_order"] = roadmap_view["Phase"].map(phase_order)
        roadmap_view = roadmap_view.sort_values(["phase_order", "Priority"])
        roadmap_view = roadmap_view.drop(columns=["phase_order"])

        st.dataframe(roadmap_view, use_container_width=True)

        st.markdown("### Phase Meaning")
        st.write("**Phase 1:** High-priority assets requiring near-term migration planning.")
        st.write("**Phase 2:** Medium-priority assets requiring review and preparation.")
        st.write("**Phase 3:** Low-priority assets requiring monitoring or periodic review.")
    else:
        st.info("No migration roadmap data available.")


with tab3:
    st.subheader("Governance View")

    governance_view = filtered_df[
        [
            "classification",
            "asset_type",
            "owner",
            "approver",
            "evidence",
            "migration_status"
        ]
    ].rename(columns={
        "classification": "Asset",
        "asset_type": "Asset Type",
        "owner": "Owner",
        "approver": "Approver",
        "evidence": "Evidence Required",
        "migration_status": "Status"
    })

    st.dataframe(governance_view, use_container_width=True)


with tab4:
    st.subheader("Coverage Assessment")

    coverage_columns = [
        "classification",
        "asset_type",
        "coverage_status",
        "coverage_reason",
        "readiness_score",
        "urgency",
        "owner",
        "migration_phase"
    ]

    available_coverage_columns = [
        col for col in coverage_columns if col in filtered_df.columns
    ]

    if available_coverage_columns and not filtered_df.empty:
        coverage_view = filtered_df[available_coverage_columns].copy()

        coverage_view = coverage_view.rename(columns={
            "classification": "Asset",
            "asset_type": "Asset Type",
            "coverage_status": "Coverage Status",
            "coverage_reason": "Coverage Reason",
            "readiness_score": "Readiness Score",
            "urgency": "Urgency",
            "owner": "Owner",
            "migration_phase": "Migration Phase"
        })

        st.dataframe(coverage_view, use_container_width=True)

        st.markdown("### Coverage Meaning")
        st.write("**Covers:** Current mechanism is generally adequate for the assessed protection requirement.")
        st.write("**Horizon Short:** Current protection may not remain adequate over the required future protection horizon.")
        st.write("**Not Yet Assessed:** More information is required about algorithms, asset sensitivity, or security properties.")
    else:
        st.info("No coverage assessment records available.")


with tab5:
    st.subheader("Business Impact View")

    business_columns = [
        "classification",
        "business_zone",
        "throughput_class",
        "latency_sensitivity",
        "asset_criticality",
        "priority",
        "coverage_status",
        "migration_phase"
    ]

    available_business_columns = [
        col for col in business_columns if col in filtered_df.columns
    ]

    if available_business_columns and not filtered_df.empty:
        business_view = filtered_df[available_business_columns].copy()

        business_view = business_view.rename(columns={
            "classification": "Asset",
            "business_zone": "Business Zone",
            "throughput_class": "Throughput Class",
            "latency_sensitivity": "Latency Sensitivity",
            "asset_criticality": "Asset Criticality",
            "priority": "Priority",
            "coverage_status": "Coverage Status",
            "migration_phase": "Migration Phase"
        })

        st.dataframe(business_view, use_container_width=True)

        st.markdown("### Business Context Meaning")
        st.write("**Business Zone:** Operational area affected by the cryptographic asset.")
        st.write("**Throughput Class:** Estimated transaction or request-processing sensitivity.")
        st.write("**Latency Sensitivity:** Estimated tolerance for migration-related performance overhead.")
        st.write("**Asset Criticality:** Business impact level inferred from the asset context.")
    else:
        st.info("No business impact records available.")


with tab6:
    st.subheader("Regulatory Impact View")

    regulatory_columns = [
        "classification",
        "business_zone",
        "dora_impact",
        "pci_impact",
        "nist_alignment",
        "compliance_risk",
        "recommended_deadline",
        "priority",
        "coverage_status",
        "migration_phase"
    ]

    available_regulatory_columns = [
        col for col in regulatory_columns if col in filtered_df.columns
    ]

    if available_regulatory_columns and not filtered_df.empty:
        regulatory_view = filtered_df[available_regulatory_columns].copy()

        regulatory_view = regulatory_view.rename(columns={
            "classification": "Asset",
            "business_zone": "Business Zone",
            "dora_impact": "DORA Impact",
            "pci_impact": "PCI DSS Impact",
            "nist_alignment": "NIST PQC Alignment",
            "compliance_risk": "Compliance Risk",
            "recommended_deadline": "Recommended Deadline",
            "priority": "Priority",
            "coverage_status": "Coverage Status",
            "migration_phase": "Migration Phase"
        })

        st.dataframe(
            regulatory_view,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Regulatory Interpretation")
        st.write("**DORA Impact:** Operational resilience exposure inferred from asset criticality and protection coverage.")
        st.write("**PCI DSS Impact:** Payment and authentication security exposure inferred from encryption, key management, and authentication assets.")
        st.write("**NIST PQC Alignment:** Alignment posture inferred from coverage and migration readiness.")
        st.write("**Recommended Deadline:** Suggested migration planning deadline inferred from priority, coverage, and business context.")
    else:
        st.info("No regulatory impact records available.")


with tab7:
    st.subheader("Asset Inventory")

    inventory_view = filtered_df[
        [
            "classification",
            "asset_type",
            "priority",
            "readiness_score",
            "urgency",
            "coverage_status",
            "owner",
            "migration_status",
            "recommendation"
        ]
    ].rename(columns={
        "classification": "Asset",
        "asset_type": "Asset Type",
        "priority": "Priority",
        "readiness_score": "Readiness Score",
        "urgency": "Urgency",
        "coverage_status": "Coverage Status",
        "owner": "Owner",
        "migration_status": "Status",
        "recommendation": "Recommendation"
    })

    st.dataframe(inventory_view, use_container_width=True)


with tab8:
    st.subheader("Analytics")

    analytics_col1, analytics_col2 = st.columns(2)

    with analytics_col1:
        priority_counts = filtered_df["priority"].value_counts().reset_index()
        priority_counts.columns = ["Priority", "Count"]
        fig = px.pie(
            priority_counts,
            names="Priority",
            values="Count",
            title="Findings by Priority"
        )
        st.plotly_chart(fig, use_container_width=True)

    with analytics_col2:
        status_counts = filtered_df["migration_status"].value_counts().reset_index()
        status_counts.columns = ["Migration Status", "Count"]
        fig = px.bar(
            status_counts,
            x="Migration Status",
            y="Count",
            title="Findings by Migration Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    analytics_col3, analytics_col4 = st.columns(2)

    with analytics_col3:
        asset_counts = filtered_df["asset_type"].value_counts().reset_index()
        asset_counts.columns = ["Asset Type", "Count"]
        fig = px.bar(
            asset_counts,
            x="Asset Type",
            y="Count",
            title="Findings by Asset Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with analytics_col4:
        owner_counts = filtered_df["owner"].value_counts().reset_index()
        owner_counts.columns = ["Owner", "Count"]
        fig = px.bar(
            owner_counts,
            x="Owner",
            y="Count",
            title="Findings by Owner"
        )
        st.plotly_chart(fig, use_container_width=True)
