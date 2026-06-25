import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="PQC Migration Engine",
    layout="wide"
)

st.title("PQC Migration Readiness Dashboard")
st.caption(
    "Governance-aware cryptographic discovery, classification, recommendation, and migration tracking."
)

inventory_path = Path("inventory.json")

if not inventory_path.exists():
    st.warning("No inventory.json found. Run a scan first.")
    st.code("python app/main.py ~/Downloads/streple-backend-main")
    st.stop()

with open(inventory_path, "r") as f:
    inventory = json.load(f)

df = pd.DataFrame(inventory)

# Keep only classified findings for dashboard analysis
classified_df = df[df["finding_type"] == "classification"].copy()

st.sidebar.title("Filters")
filtered_df = classified_df.copy()

with st.sidebar.expander("Priority", expanded=True):
    priorities = sorted(classified_df["priority"].dropna().unique())
    selected_priorities = st.multiselect(
        "Select Priority",
        priorities,
        default=priorities
    )
    filtered_df = filtered_df[filtered_df["priority"].isin(selected_priorities)]

with st.sidebar.expander("Asset Type", expanded=True):
    asset_types = sorted(classified_df["asset_type"].dropna().unique())
    selected_asset_types = st.multiselect(
        "Select Asset Type",
        asset_types,
        default=asset_types
    )
    filtered_df = filtered_df[filtered_df["asset_type"].isin(selected_asset_types)]

with st.sidebar.expander("Owner", expanded=True):
    owners = sorted(classified_df["owner"].dropna().unique())
    selected_owners = st.multiselect(
        "Select Owner",
        owners,
        default=owners
    )
    filtered_df = filtered_df[filtered_df["owner"].isin(selected_owners)]

with st.sidebar.expander("Migration Status", expanded=True):
    statuses = sorted(classified_df["migration_status"].dropna().unique())
    selected_statuses = st.multiselect(
        "Select Migration Status",
        statuses,
        default=statuses
    )
    filtered_df = filtered_df[filtered_df["migration_status"].isin(selected_statuses)]

st.sidebar.divider()

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="Download Filtered Inventory CSV",
    data=csv_data,
    file_name="pqc_filtered_inventory.csv",
    mime="text/csv"
)

st.subheader("Executive Summary")

total_findings = len(filtered_df)
high_priority = len(filtered_df[filtered_df["priority"] == "High"])
medium_priority = len(filtered_df[filtered_df["priority"] == "Medium"])
low_priority = len(filtered_df[filtered_df["priority"] == "Low"])

planned = len(filtered_df[filtered_df["migration_status"] == "Planned"])
under_review = len(filtered_df[filtered_df["migration_status"] == "Under Review"])
monitor = len(filtered_df[filtered_df["migration_status"] == "Monitor"])

if "readiness_score" in filtered_df.columns and not filtered_df.empty:
    score = round(filtered_df["readiness_score"].dropna().mean())
else:
    score = 0

if score >= 80:
    readiness_label = "Strong"
elif score >= 60:
    readiness_label = "Moderate"
elif score >= 40:
    readiness_label = "Weak"
else:
    readiness_label = "Critical"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Findings", total_findings)
col2.metric("High Priority", high_priority)
col3.metric("Medium Priority", medium_priority)
col4.metric("PQC Readiness Score", f"{score}/100")

col5, col6, col7 = st.columns(3)
col5.metric("Planned", planned)
col6.metric("Under Review", under_review)
col7.metric("Monitor", monitor)

st.info(
    f"Readiness Rating: {readiness_label}. "
    "The score reflects identified PQC migration priorities, governance status, and remediation readiness."
)

st.divider()

st.subheader("High-Priority Migration Actions")

high_df = filtered_df[filtered_df["priority"] == "High"]

if not high_df.empty:
    high_priority_view = high_df[
        [
            "classification",
            "asset_type",
            "readiness_score",
            "urgency",
            "migration_status",
            "recommendation",
            "owner",
            "approver"
        ]
    ].rename(columns={
        "classification": "Asset",
        "asset_type": "Asset Type",
        "readiness_score": "Readiness Score",
        "urgency": "Urgency",
        "migration_status": "Status",
        "recommendation": "Recommendation",
        "owner": "Owner",
        "approver": "Approver"
    })

    st.dataframe(high_priority_view, use_container_width=True)
else:
    st.success("No high-priority findings match the selected filters.")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Overview",
    "Findings",
    "Governance",
    "Roadmap",
    "Readiness",
    "Priority Actions",
    "Coverage",
    "Executive Decisions"
])

with tab1:
    st.subheader("Priority Distribution")
    if not filtered_df.empty:
        priority_counts = filtered_df["priority"].value_counts().reset_index()
        priority_counts.columns = ["Priority", "Count"]
        fig = px.pie(priority_counts, names="Priority", values="Count", title="Findings by Priority")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No priority data available.")
    st.markdown("### Governance Risks")

    governance_risk_df = filtered_df[
        filtered_df["migration_status"] == "Under Review"
    ].drop_duplicates(
        subset=["classification"]
    )

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

        st.dataframe(
            governance_risk_view,
            use_container_width=True
        )

    else:
        st.success("No governance risks identified.")

    st.markdown("### 90-Day Action Plan")

    action_plan = [
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
    ]

    st.dataframe(
        action_plan,
        use_container_width=True
    )

with tab2:
    st.subheader("Migration Status Distribution")
    if not filtered_df.empty:
        status_counts = filtered_df["migration_status"].value_counts().reset_index()
        status_counts.columns = ["Migration Status", "Count"]
        fig = px.bar(status_counts, x="Migration Status", y="Count", title="Findings by Migration Status")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No migration status data available.")

with tab3:
    st.subheader("Asset Type Breakdown")
    if not filtered_df.empty:
        asset_counts = filtered_df["asset_type"].value_counts().reset_index()
        asset_counts.columns = ["Asset Type", "Count"]
        fig = px.bar(asset_counts, x="Asset Type", y="Count", title="Findings by Asset Type")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No asset type data available.")

with tab4:
    st.subheader("Owner Workload")
    if not filtered_df.empty:
        owner_counts = filtered_df["owner"].value_counts().reset_index()
        owner_counts.columns = ["Owner", "Count"]
        fig = px.bar(owner_counts, x="Owner", y="Count", title="Findings by Owner")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No owner data available.")

with tab5:
    st.subheader("Governance Queue")

    queue_view = filtered_df[
        [
            "classification",
            "priority",
            "readiness_score",
            "urgency",
            "owner",
            "approver",
            "evidence",
            "migration_status",
            "timeline"
        ]
    ].rename(columns={
        "classification": "Asset",
        "priority": "Priority",
        "readiness_score": "Readiness Score",
        "urgency": "Urgency",
        "owner": "Owner",
        "approver": "Approver",
        "evidence": "Evidence Required",
        "migration_status": "Status",
        "timeline": "Timeline"
    })

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    queue_view["priority_order"] = queue_view["Priority"].map(priority_order)
    queue_view = queue_view.sort_values("priority_order").drop(columns=["priority_order"])

    st.dataframe(queue_view, use_container_width=True)
with tab6:

    st.subheader("Migration Roadmap")

    roadmap_view = filtered_df[
        [
            "migration_phase",
            "classification",
            "priority",
            "readiness_score",
            "urgency",
            "owner",
            "migration_status",
            "timeline"
        ]
    ].copy()

    roadmap_view = roadmap_view.rename(columns={
        "migration_phase": "Phase",
        "classification": "Asset",
        "priority": "Priority",
        "readiness_score": "Readiness Score",
        "urgency": "Urgency",
        "owner": "Owner",
        "migration_status": "Status",
        "timeline": "Timeline"
    })

    phase_order = {
        "Phase 1": 1,
        "Phase 2": 2,
        "Phase 3": 3
    }

    roadmap_view["phase_order"] = roadmap_view["Phase"].map(
        phase_order
    )

    roadmap_view = roadmap_view.sort_values(
        "phase_order"
    )

    roadmap_view = roadmap_view.drop(
        columns=["phase_order"]
    )

    st.dataframe(
        roadmap_view,
        use_container_width=True
    )

    st.markdown("### Migration Phase Guide")

    st.write(
        "**Phase 1:** Immediate migration planning."
    )

    st.write(
        "**Phase 2:** Prepare for migration."
    )

    st.write(
        "**Phase 3:** Monitor and review."
    )

st.divider()

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

st.divider()

st.subheader("Full Inventory")

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
with tab7:
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

        st.dataframe(
            coverage_view,
            use_container_width=True
        )

        st.markdown("### Coverage Meaning")
        st.write("**Covers:** Current mechanism is generally adequate for the assessed protection requirement.")
        st.write("**Horizon Short:** Current protection may not remain adequate over the required future protection horizon.")
        st.write("**Not Yet Assessed:** More information is required about algorithms, asset sensitivity, or security properties.")
    else:
        st.info("No coverage assessment records available.")
with tab8:

    st.subheader("Executive Decisions")
    st.markdown("### Top Priority Migration Actions")

    priority_df = filtered_df[
        filtered_df["priority"] == "High"
    ]

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

        st.dataframe(
            priority_view,
            use_container_width=True
        )

    else:
        st.info("No high-priority actions identified.")
