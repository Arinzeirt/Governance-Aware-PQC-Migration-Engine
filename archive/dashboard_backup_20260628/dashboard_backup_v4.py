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
st.caption("Governance-aware cryptographic discovery, classification, recommendation, and migration tracking.")

inventory_path = Path("inventory.json")

if not inventory_path.exists():
    st.warning("No inventory.json found. Run a scan first.")
    st.code("python app/main.py ~/Downloads/streple-backend-main")
    st.stop()

with open(inventory_path, "r") as f:
    inventory = json.load(f)

df = pd.DataFrame(inventory)

st.sidebar.title("Filters")
filtered_df = df.copy()

def apply_filter(column, label):
    global filtered_df
    if column in df.columns:
        values = sorted(df[column].dropna().unique())
        selected = st.sidebar.multiselect(label, values, default=values)
        filtered_df = filtered_df[filtered_df[column].isin(selected)]

apply_filter("priority", "Priority")
apply_filter("asset_type", "Asset Type")
apply_filter("owner", "Owner")
apply_filter("migration_status", "Migration Status")

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
high_priority = len(filtered_df[filtered_df.get("priority") == "High"]) if "priority" in filtered_df else 0
medium_priority = len(filtered_df[filtered_df.get("priority") == "Medium"]) if "priority" in filtered_df else 0
low_priority = len(filtered_df[filtered_df.get("priority") == "Low"]) if "priority" in filtered_df else 0

planned = len(filtered_df[filtered_df.get("migration_status") == "Planned"]) if "migration_status" in filtered_df else 0
under_review = len(filtered_df[filtered_df.get("migration_status") == "Under Review"]) if "migration_status" in filtered_df else 0
monitor = len(filtered_df[filtered_df.get("migration_status") == "Monitor"]) if "migration_status" in filtered_df else 0

if "readiness_score" in filtered_df.columns:
    readiness_scores = filtered_df["readiness_score"].dropna()

    if len(readiness_scores) > 0:
        score = round(readiness_scores.mean())
    else:
        score = 0
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

if "priority" in filtered_df.columns:
    high_df = filtered_df[filtered_df["priority"] == "High"]

    if not high_df.empty:
        action_columns = [
            "file",
            "classification",
            "asset_type",
            "recommendation",
            "timeline",
            "owner",
            "approver",
            "evidence",
            "migration_status"
        ]

        available_action_columns = [col for col in action_columns if col in high_df.columns]
        st.dataframe(high_df[available_action_columns], use_container_width=True)
    else:
        st.success("No high-priority findings match the selected filters.")
else:
    st.info("No priority information available.")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Priority",
    "Migration Status",
    "Asset Types",
    "Governance Owners",
    "Governance Queue"
])

with tab1:
    st.subheader("Priority Distribution")
    if "priority" in filtered_df.columns and not filtered_df.empty:
        priority_counts = filtered_df["priority"].value_counts().reset_index()
        priority_counts.columns = ["Priority", "Count"]
        fig = px.pie(priority_counts, names="Priority", values="Count", title="Findings by Priority")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No priority data available.")

with tab2:
    st.subheader("Migration Status Distribution")
    if "migration_status" in filtered_df.columns and not filtered_df.empty:
        status_counts = filtered_df["migration_status"].value_counts().reset_index()
        status_counts.columns = ["Migration Status", "Count"]
        fig = px.bar(status_counts, x="Migration Status", y="Count", title="Findings by Migration Status")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No migration status data available.")

with tab3:
    st.subheader("Asset Type Breakdown")
    if "asset_type" in filtered_df.columns and not filtered_df.empty:
        asset_counts = filtered_df["asset_type"].value_counts().reset_index()
        asset_counts.columns = ["Asset Type", "Count"]
        fig = px.bar(asset_counts, x="Asset Type", y="Count", title="Findings by Asset Type")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No asset type data available.")

with tab4:
    st.subheader("Owner Workload")
    if "owner" in filtered_df.columns and not filtered_df.empty:
        owner_counts = filtered_df["owner"].value_counts().reset_index()
        owner_counts.columns = ["Owner", "Count"]
        fig = px.bar(owner_counts, x="Owner", y="Count", title="Findings by Owner")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No owner data available.")

with tab5:
    st.subheader("Governance Queue")

    queue_columns = [
    "file",
    "classification",
    "readiness_score",
    "urgency",
    "coverage_status",
    "priority",
    "owner",
    "approver",
    "evidence",
    "migration_status",
    "timeline"
]

    available_queue_columns = [col for col in queue_columns if col in filtered_df.columns]

    if available_queue_columns and not filtered_df.empty:
        governance_queue = filtered_df[available_queue_columns].copy()

        if "priority" in governance_queue.columns:
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            governance_queue["priority_order"] = governance_queue["priority"].map(priority_order)
            governance_queue = governance_queue.sort_values("priority_order")
            governance_queue = governance_queue.drop(columns=["priority_order"])

        st.dataframe(governance_queue, use_container_width=True)
    else:
        st.info("No governance queue records available.")

st.divider()

st.subheader("Governance View")

governance_columns = [
    "file",
    "asset_type",
    "classification",
    "readiness_score",
    "urgency",
    "coverage_status",
    "priority",
    "owner",
    "approver",
    "evidence",
    "migration_status"
]

available_governance_columns = [col for col in governance_columns if col in filtered_df.columns]

if available_governance_columns and not filtered_df.empty:
    st.dataframe(filtered_df[available_governance_columns], use_container_width=True)
else:
    st.info("No governance records match the selected filters.")

st.divider()

st.divider()

st.subheader("Priority Migration Actions")

action_columns = [
    "classification",
    "asset_type",
    "priority",
    "owner",
    "readiness_score",
    "migration_status",
    "recommendation"
]

available_action_columns = [
    col for col in action_columns if col in filtered_df.columns
]

if available_action_columns and not filtered_df.empty:
    action_view = filtered_df[available_action_columns].copy()

    if "readiness_score" in action_view.columns:
        action_view = action_view.sort_values(
            by="readiness_score",
            ascending=True
        )

    st.dataframe(action_view, use_container_width=True)
else:
    st.info("No priority migration actions available.")
