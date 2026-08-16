import streamlit as st


def _enterprise_configuration():
    """Administrator enterprise configuration workspace."""

    st.markdown(
        """
<div style="
    margin-bottom:20px;
">
<div style="
    font-size:1.65rem;
    font-weight:800;
    color:#F5F7FA;
">
Enterprise Configuration
</div>

<div style="
    color:#8FA1B5;
    font-size:0.86rem;
    margin-top:5px;
">
Define the enterprise context EQMP is responsible for overseeing.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "← Back to Settings",
        key="eqmp_enterprise_config_back",
    ):
        st.session_state["eqmp_settings_section"] = "overview"
        st.rerun()

    st.markdown(
        """
<div class="eqmp-settings-section">
<div class="eqmp-settings-title">
Enterprise Profile
</div>
<div class="eqmp-settings-description">
Establish the organisational context used across discovery,
risk assessment and migration governance.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="medium")

    with left:

        st.text_input(
            "Organisation Name",
            value=st.session_state.get(
                "eqmp_organisation_name",
                "EQMP Test Organisation",
            ),
            key="eqmp_enterprise_name",
        )

        st.text_input(
            "Industry",
            value=st.session_state.get(
                "eqmp_enterprise_industry",
                "",
            ),
            key="eqmp_enterprise_industry",
        )

        st.text_input(
            "Website",
            value=st.session_state.get(
                "eqmp_enterprise_website",
                "",
            ),
            key="eqmp_enterprise_website",
        )

    with right:

        st.text_input(
            "Country / Primary Jurisdiction",
            value=st.session_state.get(
                "eqmp_enterprise_country",
                "",
            ),
            key="eqmp_enterprise_country",
        )

        st.selectbox(
            "Enterprise Classification",
            [
                "Large Enterprise",
                "Mid-Market",
                "Financial Institution",
                "Public Sector",
                "Critical Infrastructure",
                "Other",
            ],
            key="eqmp_enterprise_classification",
        )

        st.selectbox(
            "Criticality Profile",
            [
                "Standard",
                "High",
                "Critical",
            ],
            key="eqmp_enterprise_criticality",
        )

    if st.button(
        "Save Enterprise Profile",
        key="eqmp_save_enterprise_profile",
    ):

        st.session_state[
            "eqmp_organisation_name"
        ] = st.session_state.get(
            "eqmp_enterprise_name",
            "EQMP Test Organisation",
        )

        st.success(
            "Enterprise profile updated."
        )

    st.markdown(
        """
<div class="eqmp-settings-section">
<div class="eqmp-settings-title">
Environment Oversight
</div>
<div class="eqmp-settings-description">
Define the environment EQMP will monitor and the sources that
provide enterprise visibility.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    environment_left, environment_right = st.columns(
        2,
        gap="medium",
    )

    with environment_left:

        st.selectbox(
            "Environment Connection",
            [
                "Not Connected",
                "Connected",
                "Connection Pending",
            ],
            key="eqmp_environment_connection",
        )

        st.selectbox(
            "Primary Discovery Source",
            [
                "Not Configured",
                "Repository Scanner",
                "Infrastructure Scanner",
                "Vendor-Powered Scanner",
                "Multiple Sources",
            ],
            key="eqmp_primary_discovery_source",
        )

    with environment_right:

        st.selectbox(
            "Active Vendor Scanner",
            [
                "None",
                "QuantumGenie",
                "Other Approved Vendor",
            ],
            key="eqmp_active_vendor_scanner",
        )

        st.selectbox(
            "Oversight Mode",
            [
                "Full EQMP Oversight",
                "Assessment Only",
                "Discovery Only",
            ],
            key="eqmp_environment_oversight_mode",
        )

    st.markdown(
        """
<div style="
    margin-top:10px;
    border:1px solid rgba(47,129,247,.30);
    border-left:2px solid #2F81F7;
    border-radius:7px;
    padding:12px;
    color:#8FA1B5;
    font-size:.70rem;
    line-height:1.5;
">
EQMP remains the governance and oversight layer. Connected
scanners and specialist vendors provide evidence and technical
capabilities; EQMP retains the enterprise-level view of
discovery, risk, ownership and migration decisions.
</div>
""",
        unsafe_allow_html=True,
    )


def _governance_configuration():
    """Administrator governance configuration workspace."""

    st.markdown(
        """
<div style="
    margin-bottom:20px;
">
<div style="
    font-size:1.65rem;
    font-weight:800;
    color:#F5F7FA;
">
Governance Configuration
</div>

<div style="
    color:#8FA1B5;
    font-size:0.86rem;
    margin-top:5px;
">
Define decision ownership, accountability and oversight controls.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "← Back to Settings",
        key="eqmp_governance_config_back",
    ):
        st.session_state["eqmp_settings_section"] = "overview"
        st.rerun()

    st.markdown(
        """
<div class="eqmp-settings-section">
<div class="eqmp-settings-title">
Decision Authority
</div>
<div class="eqmp-settings-description">
Define who owns and approves post-quantum migration decisions.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="medium")

    with left:

        st.text_input(
            "Executive Sponsor",
            value=st.session_state.get(
                "eqmp_executive_sponsor",
                "",
            ),
            key="eqmp_governance_executive_sponsor",
        )

        st.text_input(
            "PQC Programme Owner",
            value=st.session_state.get(
                "eqmp_pqc_programme_owner",
                "",
            ),
            key="eqmp_governance_pqc_owner",
        )

        st.text_input(
            "Security Owner",
            value=st.session_state.get(
                "eqmp_security_owner",
                "",
            ),
            key="eqmp_governance_security_owner",
        )

    with right:

        st.text_input(
            "Migration Programme Owner",
            value=st.session_state.get(
                "eqmp_migration_owner",
                "",
            ),
            key="eqmp_governance_migration_owner",
        )

        st.text_input(
            "Risk Acceptance Authority",
            value=st.session_state.get(
                "eqmp_risk_acceptance_authority",
                "",
            ),
            key="eqmp_governance_risk_authority",
        )

        st.selectbox(
            "Governance Model",
            [
                "Centralised",
                "Federated",
                "Hybrid",
            ],
            key="eqmp_governance_model",
        )

    st.markdown(
        """
<div class="eqmp-settings-section">
<div class="eqmp-settings-title">
Oversight Controls
</div>
<div class="eqmp-settings-description">
Define how EQMP should surface decisions, exceptions and
accountability gaps.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    control_left, control_right = st.columns(
        2,
        gap="medium",
    )

    with control_left:

        st.selectbox(
            "Governance Review Frequency",
            [
                "Monthly",
                "Quarterly",
                "Biannual",
            ],
            key="eqmp_governance_review_frequency",
        )

        st.toggle(
            "Require Migration Approval",
            value=True,
            key="eqmp_require_migration_approval",
        )

    with control_right:

        st.toggle(
            "Escalate Ownership Gaps",
            value=True,
            key="eqmp_escalate_ownership_gaps",
        )

        st.toggle(
            "Require Audit Evidence",
            value=True,
            key="eqmp_require_audit_evidence",
        )

    if st.button(
        "Save Governance Configuration",
        key="eqmp_save_governance_configuration",
    ):
        st.success(
            "Governance configuration updated."
        )


def _enterprise_governance_entry():
    """Entry point for administrator enterprise configuration domains."""

    st.markdown(
        """
<div style="
    margin-top:2px;
    margin-bottom:12px;
">
<div style="
    font-size:0.82rem;
    font-weight:750;
    color:#F5F7FA;
">
Enterprise Configuration
</div>

<div style="
    color:#8FA1B5;
    font-size:0.68rem;
    line-height:1.45;
    margin-top:4px;
">
Define the enterprise context, environment visibility and
governance controls used throughout EQMP.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    domains = [
        (
            "Organisation Overview",
            "Enterprise identity, business context and organisational profile.",
            "organisation",
        ),
        (
            "Technology Environment",
            "Applications, infrastructure, systems and technology landscape.",
            "technology",
        ),
        (
            "Environment Connections",
            "Cloud, on-premise, repositories, endpoints and connected sources.",
            "connections",
        ),
        (
            "Governance & Accountability",
            "Ownership, sponsorship and accountability across the programme.",
            "governance",
        ),
        (
            "Risk & Data Context",
            "Critical systems, sensitive data, longevity and risk context.",
            "risk",
        ),
        (
            "Compliance & Regulatory",
            "Regulatory obligations, standards, assurance and evidence requirements.",
            "compliance",
        ),
        (
            "Decision & Approval",
            "Decision authority, approvals, exceptions and risk acceptance.",
            "decision",
        ),
    ]

    # ---------------------------------------------------------
    # First row — four compact domains
    # ---------------------------------------------------------

    row_one = st.columns(
        4,
        gap="small",
    )

    for column, item in zip(
        row_one,
        domains[:4],
    ):

        title, description, section = item

        with column:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:7px;
    padding:11px;
    min-height:105px;
">

<div style="
    font-size:0.65rem;
    font-weight:750;
    color:#F5F7FA;
    line-height:1.25;
    margin-bottom:7px;
">
{title}
</div>

<div style="
    font-size:0.58rem;
    line-height:1.42;
    color:#718096;
    min-height:40px;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

            if st.button(
                "Configure →",
                key=f"eqmp_config_domain_{section}",
                use_container_width=True,
            ):

                st.session_state[
                    "eqmp_settings_section"
                ] = section

                st.rerun()

    # ---------------------------------------------------------
    # Second row — three domains
    # ---------------------------------------------------------

    row_two = st.columns(
        4,
        gap="small",
    )

    for column, item in zip(
        row_two[:3],
        domains[4:],
    ):

        title, description, section = item

        with column:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:7px;
    padding:11px;
    min-height:105px;
">

<div style="
    font-size:0.65rem;
    font-weight:750;
    color:#F5F7FA;
    line-height:1.25;
    margin-bottom:7px;
">
{title}
</div>

<div style="
    font-size:0.58rem;
    line-height:1.42;
    color:#718096;
    min-height:40px;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

            if st.button(
                "Configure →",
                key=f"eqmp_config_domain_{section}",
                use_container_width=True,
            ):

                st.session_state[
                    "eqmp_settings_section"
                ] = section

                st.rerun()

    st.markdown(
        '<div style="height:6px"></div>',
        unsafe_allow_html=True,
    )


def show():

    # =========================================================
    # Authentication / Role
    # =========================================================

    if not st.session_state.get(
        "eqmp_authenticated",
        False,
    ):

        st.session_state.page = "login"
        st.rerun()

    user_role = st.session_state.get(
        "eqmp_user_role",
        "user",
    )

    is_admin = user_role == "admin"

    # =========================================================
    # Personal Settings — Standard User
    # =========================================================

    if not is_admin:

        organisation = st.session_state.get(
            "eqmp_organisation_name",
            "EQMP Test Organisation",
        )

        email = st.session_state.get(
            "eqmp_user_email",
            "",
        )

        display_name = st.session_state.get(
            "eqmp_user_name",
            email.split("@")[0] if email else "EQMP User",
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header_left, header_right = st.columns(
            [8.5, 1.5],
            gap="small",
        )

        with header_left:

            st.markdown(
                f"""
<div style="
    margin-bottom:8px;
">

<div style="
    font-size:1.75rem;
    font-weight:800;
    color:#F5F7FA;
">
My Settings
</div>

<div style="
    color:#8FA1B5;
    font-size:0.88rem;
    margin-top:5px;
">
Manage your personal EQMP account settings.
</div>

</div>
""",
                unsafe_allow_html=True,
            )

        with header_right:

            st.markdown(
                """
<div style="
    display:flex;
    justify-content:flex-end;
    align-items:center;
    margin-top:8px;
">

<span style="
    font-size:0.68rem;
    color:#22C55E;
    letter-spacing:.5px;
">
● LIVE
</span>

</div>
""",
                unsafe_allow_html=True,
            )

            if st.button(
                "Sign Out",
                key="eqmp_user_sign_out",
                use_container_width=True,
            ):

                st.session_state[
                    "eqmp_authenticated"
                ] = False

                st.session_state.pop(
                    "eqmp_user_email",
                    None,
                )

                st.session_state.pop(
                    "eqmp_user_role",
                    None,
                )

                st.session_state.pop(
                    "eqmp_user_name",
                    None,
                )

                st.session_state.page = "landing"

                st.rerun()

        # -----------------------------------------------------
        # Return
        # -----------------------------------------------------

        if st.button(
            "← Return to Command Center",
            key="eqmp_user_return_command",
        ):

            st.session_state.page = "command_center"
            st.rerun()

        # -----------------------------------------------------
        # Profile
        # -----------------------------------------------------

        st.markdown(
            """
<div style="
    margin-top:22px;
    margin-bottom:9px;
    font-size:0.72rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
">
PROFILE
</div>
""",
            unsafe_allow_html=True,
        )

        profile_left, profile_right = st.columns(
            2,
            gap="medium",
        )

        with profile_left:

            new_name = st.text_input(
                "Display Name",
                value=display_name,
                key="eqmp_user_profile_name",
            )

            st.text_input(
                "Business Email",
                value=email,
                disabled=True,
                key="eqmp_user_profile_email",
            )

        with profile_right:

            st.text_input(
                "Organisation",
                value=organisation,
                disabled=True,
                key="eqmp_user_profile_organisation",
            )

            st.text_input(
                "Role",
                value="Organisation User",
                disabled=True,
                key="eqmp_user_profile_role",
            )

        if st.button(
            "Save Profile",
            key="eqmp_user_save_profile",
        ):

            st.session_state[
                "eqmp_user_name"
            ] = new_name

            st.success(
                "Profile updated."
            )

        # -----------------------------------------------------
        # Password
        # -----------------------------------------------------

        st.markdown(
            """
<div style="
    margin-top:22px;
    margin-bottom:9px;
    font-size:0.72rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
">
PASSWORD
</div>
""",
            unsafe_allow_html=True,
        )

        password_left, password_right = st.columns(
            2,
            gap="medium",
        )

        with password_left:

            st.text_input(
                "Current Password",
                type="password",
                key="eqmp_user_current_password",
            )

        with password_right:

            st.text_input(
                "New Password",
                type="password",
                key="eqmp_user_new_password",
            )

        st.text_input(
            "Confirm New Password",
            type="password",
            key="eqmp_user_confirm_password",
        )

        if st.button(
            "Update Password",
            key="eqmp_user_update_password",
        ):

            new_password = st.session_state.get(
                "eqmp_user_new_password",
                "",
            )

            confirm_password = st.session_state.get(
                "eqmp_user_confirm_password",
                "",
            )

            if not new_password:

                st.warning(
                    "Enter a new password."
                )

            elif new_password != confirm_password:

                st.error(
                    "New passwords do not match."
                )

            else:

                st.info(
                    "Password update will be applied "
                    "through the EQMP account service."
                )

        # -----------------------------------------------------
        # Personal Preferences
        # -----------------------------------------------------

        st.markdown(
            """
<div style="
    margin-top:22px;
    margin-bottom:9px;
    font-size:0.72rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
">
PERSONAL PREFERENCES
</div>
""",
            unsafe_allow_html=True,
        )

        st.checkbox(
            "Remember this device",
            value=True,
            key="eqmp_user_remember_device",
        )

        st.checkbox(
            "Show migration notifications",
            value=True,
            key="eqmp_user_migration_notifications",
        )

        return



    # =========================================================
    # Administrator Settings
    # =========================================================

    st.markdown(
        """
<style>

.eqmp-admin-section {
    margin-top:22px;
    margin-bottom:10px;
}

.eqmp-admin-section-label {
    font-size:.76rem;
    letter-spacing:1.15px;
    font-weight:750;
    color:#7F91A6;
}

.eqmp-admin-section-description {
    margin-top:4px;
    font-size:.69rem;
    line-height:1.45;
    color:#8FA1B5;
}

.eqmp-admin-card {
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:13px;
    margin-bottom:7px;
    min-height:108px;
    background:rgba(7,16,31,.18);
}

.eqmp-admin-card-title {
    font-size:.71rem;
    font-weight:750;
    color:#F5F7FA;
    margin-bottom:6px;
}

.eqmp-admin-card-description {
    font-size:.63rem;
    line-height:1.42;
    color:#718096;
    min-height:32px;
}

.eqmp-admin-card-status {
    margin-top:8px;
    font-size:.60rem;
    color:#8FA1B5;
}

.eqmp-admin-primary {
    border:1px solid rgba(47,129,247,.30);
    border-radius:8px;
    padding:15px;
    background:rgba(7,16,31,.20);
}

.eqmp-admin-primary-label {
    font-size:.70rem;
    letter-spacing:1px;
    font-weight:750;
    color:#7F91A6;
    margin-bottom:5px;
}

.eqmp-admin-primary-description {
    font-size:.66rem;
    line-height:1.45;
    color:#8FA1B5;
    margin-bottom:14px;
}

</style>
""",
        unsafe_allow_html=True,
    )

    # =========================================================
    # Header
    # =========================================================

    header_left, header_right = st.columns(
        [8.5, 1.5],
        gap="small",
    )

    with header_left:

        st.markdown(
            """
<div style="
    margin-bottom:8px;
">

<div style="
    font-size:1.75rem;
    font-weight:800;
    line-height:1.1;
    color:#F5F7FA;
">
Settings
</div>

<div style="
    color:#8FA1B5;
    font-size:0.88rem;
    margin-top:5px;
">
Master system configuration and administrative controls.
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with header_right:

        st.markdown(
            """
<div style="
    display:flex;
    justify-content:flex-end;
    align-items:center;
    margin-top:8px;
">

<span style="
    font-size:0.68rem;
    color:#22C55E;
    letter-spacing:.5px;
">
● SYSTEM LIVE
</span>

</div>
""",
            unsafe_allow_html=True,
        )

    if st.button(
        "← Command Center",
        key="settings_back",
    ):

        st.session_state.page = "command_center"
        st.rerun()

    # =========================================================
    # Configuration workspace routing
    # =========================================================

    settings_section = st.session_state.get(
        "eqmp_settings_section",
        "overview",
    )

    if settings_section != "overview":

        st.markdown(
            '<div style="height:8px"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "← Back to Settings",
            key="eqmp_settings_workspace_back",
        ):

            st.session_state[
                "eqmp_settings_section"
            ] = "overview"

            st.rerun()

        st.markdown(
            f"""
<div style="
    margin-top:16px;
    margin-bottom:18px;
">

<div style="
    font-size:1.35rem;
    font-weight:800;
    color:#F5F7FA;
">
{settings_section.replace("_", " ").title()}
</div>

<div style="
    color:#8FA1B5;
    font-size:.78rem;
    margin-top:5px;
">
Configuration workspace for the selected enterprise control area.
</div>

</div>
""",
            unsafe_allow_html=True,
        )

        # -----------------------------------------------------
        # Organisation
        # -----------------------------------------------------

        if settings_section == "organisation":

            st.markdown(
                """
<div class="eqmp-admin-primary">

<div class="eqmp-admin-primary-label">
ORGANISATION PROFILE
</div>

<div class="eqmp-admin-primary-description">
Define the enterprise identity and business context used
throughout EQMP.
</div>

</div>
""",
                unsafe_allow_html=True,
            )

            left, right = st.columns(
                2,
                gap="medium",
            )

            with left:

                st.text_input(
                    "Organisation Name",
                    value=st.session_state.get(
                        "eqmp_organisation_name",
                        "EQMP Test Organisation",
                    ),
                    key="eqmp_admin_org_name",
                )

                st.selectbox(
                    "Country / Primary Jurisdiction",
                    [
                        "Nigeria",
                        "United Kingdom",
                        "United States",
                        "European Union",
                        "Other",
                    ],
                    key="eqmp_admin_org_country",
                )

                st.text_input(
                    "Website",
                    key="eqmp_admin_org_website",
                )

            with right:

                st.selectbox(
                    "Industry",
                    [
                        "Financial Services",
                        "Banking",
                        "Insurance",
                        "Telecommunications",
                        "Healthcare",
                        "Government",
                        "Technology",
                        "Other",
                    ],
                    key="eqmp_admin_org_industry",
                )

                st.selectbox(
                    "Enterprise Classification",
                    [
                        "Large Enterprise",
                        "Mid-Market",
                        "Small Enterprise",
                        "Public Sector",
                    ],
                    key="eqmp_admin_org_classification",
                )

                st.selectbox(
                    "Business Criticality",
                    [
                        "Critical",
                        "High",
                        "Moderate",
                        "Standard",
                    ],
                    key="eqmp_admin_org_criticality",
                )

            if st.button(
                "Save Organisation Configuration",
                type="primary",
                key="eqmp_save_org_configuration",
            ):

                st.session_state[
                    "eqmp_organisation_name"
                ] = st.session_state.get(
                    "eqmp_admin_org_name",
                    "EQMP Test Organisation",
                )

                st.success(
                    "Organisation configuration saved."
                )

            return

        # -----------------------------------------------------
        # Technology
        # -----------------------------------------------------

        if settings_section == "technology":

            st.markdown(
                """
<div class="eqmp-admin-primary">

<div class="eqmp-admin-primary-label">
TECHNOLOGY ENVIRONMENT
</div>

<div class="eqmp-admin-primary-description">
Define the enterprise technology estate and the environments
that EQMP should consider during discovery and migration planning.
</div>

</div>
""",
                unsafe_allow_html=True,
            )

            st.selectbox(
                "Infrastructure Model",
                [
                    "Hybrid",
                    "Cloud",
                    "On-Premise",
                ],
                key="eqmp_admin_infrastructure_model",
            )

            left, right = st.columns(
                2,
                gap="medium",
            )

            with left:

                st.multiselect(
                    "Cloud Providers",
                    [
                        "Amazon Web Services",
                        "Microsoft Azure",
                        "Google Cloud",
                        "Oracle Cloud",
                        "Other",
                    ],
                    key="eqmp_admin_cloud_providers",
                )

            with right:

                st.multiselect(
                    "Technology Domains",
                    [
                        "Applications",
                        "Databases",
                        "Networks",
                        "Identity",
                        "Endpoints",
                        "PKI / Certificates",
                        "Data Platforms",
                        "Core Infrastructure",
                    ],
                    key="eqmp_admin_technology_domains",
                )

            st.multiselect(
                "Critical Technology Areas",
                [
                    "Payment Systems",
                    "Core Banking",
                    "Customer Platforms",
                    "Identity Infrastructure",
                    "Transaction Processing",
                    "Security Infrastructure",
                ],
                key="eqmp_admin_critical_areas",
            )

            if st.button(
                "Save Technology Configuration",
                type="primary",
                key="eqmp_save_technology",
            ):

                st.success(
                    "Technology environment configuration saved."
                )

            return

        # -----------------------------------------------------
        # Environment connections + vendors
        # -----------------------------------------------------

        if settings_section == "connections":

            st.markdown(
                """
<div class="eqmp-admin-primary">

<div class="eqmp-admin-primary-label">
ENVIRONMENT CONNECTIONS
</div>

<div class="eqmp-admin-primary-description">
Establish the evidence sources EQMP can oversee across the
enterprise environment.
</div>

</div>
""",
                unsafe_allow_html=True,
            )

            connection_groups = [
                (
                    "CLOUD ENVIRONMENTS",
                    [
                        "Amazon Web Services",
                        "Microsoft Azure",
                        "Google Cloud",
                    ],
                ),
                (
                    "ON-PREMISE ENVIRONMENT",
                    [
                        "Data Centre",
                    ],
                ),
                (
                    "CODE & REPOSITORIES",
                    [
                        "Git / Source Repository",
                    ],
                ),
                (
                    "CRYPTOGRAPHIC SOURCES",
                    [
                        "PKI / Certificates",
                    ],
                ),
            ]

            for group_name, sources in connection_groups:

                st.markdown(
                    f"""
<div style="
    margin-top:17px;
    margin-bottom:7px;
    font-size:.63rem;
    letter-spacing:1px;
    font-weight:750;
    color:#7F91A6;
">
{group_name}
</div>
""",
                    unsafe_allow_html=True,
                )

                for source in sources:

                    left, right = st.columns(
                        [4, 1],
                        gap="small",
                    )

                    with left:

                        st.markdown(
                            f"""
<div style="
    border:1px solid rgba(255,255,255,.08);
    border-radius:7px;
    padding:10px 11px;
    margin-bottom:6px;
">

<div style="
    font-size:.69rem;
    color:#D5DCE5;
    font-weight:650;
">
{source}
</div>

<div style="
    font-size:.58rem;
    color:#718096;
    margin-top:3px;
">
Not Connected
</div>

</div>
""",
                            unsafe_allow_html=True,
                        )

                    with right:

                        if st.button(
                            "Connect",
                            key=f"eqmp_connect_{source}",
                            use_container_width=True,
                        ):

                            st.info(
                                f"{source} connection workflow."
                            )

            st.markdown(
                """
<div style="
    margin-top:24px;
    margin-bottom:8px;
    font-size:.68rem;
    letter-spacing:1px;
    font-weight:750;
    color:#7F91A6;
">
VENDOR & SPECIALIST TOOLS
</div>
""",
                unsafe_allow_html=True,
            )

            vendor_left, vendor_right = st.columns(
                [3, 1],
                gap="medium",
            )

            with vendor_left:

                st.markdown(
                    """
<div class="eqmp-admin-card">

<div class="eqmp-admin-card-title">
Approved Vendor Connections
</div>

<div class="eqmp-admin-card-description">
Specialist scanners and technology capabilities approved
for use within the organisation's EQMP oversight model.
</div>

<div class="eqmp-admin-card-status">
0 Connected
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

            with vendor_right:

                if st.button(
                    "Manage Vendor Connections →",
                    key="eqmp_manage_vendor_connections",
                    use_container_width=True,
                ):

                    st.info(
                        "Vendor connection management workspace."
                    )

            return

        # -----------------------------------------------------
        # Governance
        # -----------------------------------------------------

        if settings_section == "governance":

            left, right = st.columns(
                2,
                gap="medium",
            )

            with left:

                st.text_input(
                    "Executive Sponsor",
                    key="eqmp_admin_exec_sponsor",
                )

                st.text_input(
                    "PQC Programme Owner",
                    key="eqmp_admin_pqc_owner",
                )

                st.text_input(
                    "Security Owner",
                    key="eqmp_admin_security_owner",
                )

            with right:

                st.text_input(
                    "Migration Owner",
                    key="eqmp_admin_migration_owner",
                )

                st.selectbox(
                    "Governance Model",
                    [
                        "Centralised",
                        "Federated",
                        "Hybrid",
                    ],
                    key="eqmp_admin_governance_model",
                )

                st.selectbox(
                    "Review Frequency",
                    [
                        "Monthly",
                        "Quarterly",
                        "Biannual",
                    ],
                    key="eqmp_admin_review_frequency",
                )

            st.checkbox(
                "Escalate ownership gaps",
                value=True,
                key="eqmp_admin_escalate_ownership",
            )

            st.checkbox(
                "Require governance evidence",
                value=True,
                key="eqmp_admin_require_governance_evidence",
            )

            if st.button(
                "Save Governance Configuration",
                type="primary",
                key="eqmp_save_governance",
            ):

                st.success(
                    "Governance configuration saved."
                )

            return

        # -----------------------------------------------------
        # Risk
        # -----------------------------------------------------

        if settings_section == "risk":

            st.multiselect(
                "Critical Data Categories",
                [
                    "Customer Data",
                    "Financial Data",
                    "Intellectual Property",
                    "Authentication Data",
                    "Regulatory Data",
                    "Operational Data",
                ],
                key="eqmp_admin_critical_data",
            )

            st.selectbox(
                "Expected Data Longevity",
                [
                    "Less than 5 years",
                    "5–10 years",
                    "10–20 years",
                    "20+ years",
                ],
                key="eqmp_admin_data_longevity",
            )

            st.multiselect(
                "Critical Systems",
                [
                    "Payment Systems",
                    "Core Banking",
                    "Identity Systems",
                    "Customer Platforms",
                    "Critical Infrastructure",
                ],
                key="eqmp_admin_critical_systems",
            )

            st.selectbox(
                "Enterprise Risk Tolerance",
                [
                    "Low",
                    "Moderate",
                    "High",
                ],
                key="eqmp_admin_risk_tolerance",
            )

            if st.button(
                "Save Risk Configuration",
                type="primary",
                key="eqmp_save_risk",
            ):

                st.success(
                    "Risk and data configuration saved."
                )

            return

        # -----------------------------------------------------
        # Compliance
        # -----------------------------------------------------

        if settings_section == "compliance":

            st.multiselect(
                "Applicable Frameworks",
                [
                    "ISO 27001",
                    "NIST",
                    "PCI DSS",
                    "SOC 2",
                    "NDPA",
                    "GDPR",
                    "Other",
                ],
                key="eqmp_admin_compliance_frameworks",
            )

            st.multiselect(
                "Regulatory Jurisdictions",
                [
                    "Nigeria",
                    "United Kingdom",
                    "European Union",
                    "United States",
                    "Other",
                ],
                key="eqmp_admin_regulatory_jurisdictions",
            )

            st.selectbox(
                "Assurance Requirement",
                [
                    "Standard",
                    "Enhanced",
                    "Strict",
                ],
                key="eqmp_admin_assurance_requirement",
            )

            st.checkbox(
                "Require evidence for governance decisions",
                value=True,
                key="eqmp_admin_compliance_evidence",
            )

            if st.button(
                "Save Compliance Configuration",
                type="primary",
                key="eqmp_save_compliance",
            ):

                st.success(
                    "Compliance configuration saved."
                )

            return

        # -----------------------------------------------------
        # Decision and approval
        # -----------------------------------------------------

        if settings_section == "decision":

            left, right = st.columns(
                2,
                gap="medium",
            )

            with left:

                st.text_input(
                    "Migration Decision Authority",
                    key="eqmp_admin_decision_authority",
                )

                st.text_input(
                    "Risk Acceptance Authority",
                    key="eqmp_admin_risk_acceptance",
                )

            with right:

                st.text_input(
                    "Exception Authority",
                    key="eqmp_admin_exception_authority",
                )

                st.selectbox(
                    "Approval Model",
                    [
                        "Risk-Based Approval",
                        "Committee Approval",
                        "Executive Approval",
                    ],
                    key="eqmp_admin_approval_model",
                )

            st.checkbox(
                "Require approval before migration execution",
                value=True,
                key="eqmp_admin_require_migration_approval",
            )

            st.checkbox(
                "Require evidence before approval",
                value=True,
                key="eqmp_admin_require_approval_evidence",
            )

            st.checkbox(
                "Escalate unresolved exceptions",
                value=True,
                key="eqmp_admin_escalate_exceptions",
            )

            st.markdown(
                """
<div style="
    margin-top:22px;
    padding:14px;
    border:1px solid rgba(255,255,255,.08);
    border-radius:8px;
">

<div style="
    font-size:.67rem;
    letter-spacing:.8px;
    color:#7F91A6;
    font-weight:750;
    margin-bottom:9px;
">
DECISION FLOW
</div>

<div style="
    font-size:.70rem;
    color:#AEBCCE;
    line-height:1.8;
">
Discovery → Assessment → Recommendation → Approval → Migration → Validation
</div>

</div>
""",
                unsafe_allow_html=True,
            )

            if st.button(
                "Save Decision Configuration",
                type="primary",
                key="eqmp_save_decision",
            ):

                st.success(
                    "Decision and approval configuration saved."
                )

            return

    # =========================================================
    # Enterprise Configuration
    # =========================================================

    st.markdown(
        """
<div class="eqmp-admin-section">

<div class="eqmp-admin-section-label">
ENTERPRISE CONFIGURATION
</div>

<div class="eqmp-admin-section-description">
Core organisational and operational context for EQMP.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    # =========================================================
    # Organisation Overview — full width
    # =========================================================

    st.markdown(
        """
<div class="eqmp-admin-primary">

<div class="eqmp-admin-primary-label">
ORGANISATION OVERVIEW
</div>

<div class="eqmp-admin-primary-description">
Define the enterprise identity and business context used
throughout EQMP.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    org_left, org_right = st.columns(
        2,
        gap="medium",
    )

    with org_left:

        st.text_input(
            "Organisation Name",
            value=st.session_state.get(
                "eqmp_organisation_name",
                "EQMP Test Organisation",
            ),
            key="eqmp_admin_overview_org_name",
        )

        st.selectbox(
            "Country / Primary Jurisdiction",
            [
                "Nigeria",
                "United Kingdom",
                "United States",
                "European Union",
                "Other",
            ],
            key="eqmp_admin_overview_country",
        )

    with org_right:

        st.selectbox(
            "Industry",
            [
                "Financial Services",
                "Banking",
                "Insurance",
                "Telecommunications",
                "Healthcare",
                "Government",
                "Technology",
                "Other",
            ],
            key="eqmp_admin_overview_industry",
        )

        st.selectbox(
            "Enterprise Classification",
            [
                "Large Enterprise",
                "Mid-Market",
                "Small Enterprise",
                "Public Sector",
            ],
            key="eqmp_admin_overview_classification",
        )

    org_left, org_right = st.columns(
        2,
        gap="medium",
    )

    with org_left:

        st.text_input(
            "Website",
            key="eqmp_admin_overview_website",
        )

    with org_right:

        st.selectbox(
            "Business Criticality",
            [
                "Critical",
                "High",
                "Moderate",
                "Standard",
            ],
            key="eqmp_admin_overview_criticality",
        )

    if st.button(
        "Save Organisation Configuration",
        type="primary",
        key="eqmp_admin_overview_save",
    ):

        st.session_state[
            "eqmp_organisation_name"
        ] = st.session_state.get(
            "eqmp_admin_overview_org_name",
            "EQMP Test Organisation",
        )

        st.success(
            "Organisation configuration saved."
        )

    # =========================================================
    # Additional Enterprise Configuration
    # =========================================================

    st.markdown(
        """
<div class="eqmp-admin-section">

<div class="eqmp-admin-section-label">
ADDITIONAL ENTERPRISE CONFIGURATION
</div>

<div class="eqmp-admin-section-description">
Configure the enterprise environment, governance, risk,
compliance and decision controls used by EQMP.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    cards = [
        (
            "Technology Environment",
            "Enterprise technology estate, infrastructure and critical systems.",
            "Partially Configured",
            "technology",
            "Configure Technology →",
        ),
        (
            "Environment Connections",
            "Cloud, on-premise, repositories and evidence sources.",
            "0 Connected",
            "connections",
            "Connect Environment →",
        ),
        (
            "Governance & Accountability",
            "Ownership, sponsorship, accountability and programme oversight.",
            "Attention Required",
            "governance",
            "Configure Governance →",
        ),
        (
            "Compliance & Regulatory",
            "Regulatory obligations, standards, assurance and evidence.",
            "Not Configured",
            "compliance",
            "Configure Compliance →",
        ),
        (
            "Risk & Data Context",
            "Critical systems, data longevity and enterprise risk.",
            "Not Configured",
            "risk",
            "Configure Risk →",
        ),
        (
            "Decision & Approval",
            "Decision authority, approval pathways and risk acceptance.",
            "Not Established",
            "decision",
            "Configure Decisions →",
        ),
    ]

    for index in range(0, len(cards), 2):

        columns = st.columns(
            2,
            gap="medium",
        )

        for column, card in zip(
            columns,
            cards[index:index + 2],
        ):

            title, description, status, section, action = card

            with column:

                st.markdown(
                    f"""
<div class="eqmp-admin-card">

<div class="eqmp-admin-card-title">
{title}
</div>

<div class="eqmp-admin-card-description">
{description}
</div>

<div class="eqmp-admin-card-status">
{status}
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

                if st.button(
                    action,
                    key=f"eqmp_admin_action_{section}",
                    use_container_width=True,
                ):

                    st.session_state[
                        "eqmp_settings_section"
                    ] = section

                    st.rerun()

    # =========================================================
    # System Configuration
    # =========================================================

    st.markdown(
        """
<div class="eqmp-admin-section">

<div class="eqmp-admin-section-label">
SYSTEM CONFIGURATION
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        2,
        gap="medium",
    )

    with left:

        st.selectbox(
            "Platform Environment",
            [
                "Development",
                "Staging",
                "Production",
            ],
            index=0,
            key="eqmp_environment",
        )

    with right:

        st.selectbox(
            "Assessment Mode",
            [
                "Enterprise",
                "Demonstration",
            ],
            index=0,
            key="eqmp_assessment_mode",
        )

    left, right = st.columns(
        2,
        gap="medium",
    )

    with left:

        st.selectbox(
            "Default Access Model",
            [
                "Provisioned Access",
                "Organisation Managed",
            ],
            index=0,
            key="eqmp_access_model",
        )

    with right:

        st.text_input(
            "Platform Name",
            value="Enterprise Quantum Migration Platform",
            key="eqmp_platform_name",
        )

    # =========================================================
    # Assessment Engine
    # =========================================================

    st.markdown(
        """
<div class="eqmp-admin-section">

<div class="eqmp-admin-section-label">
ASSESSMENT ENGINE
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        2,
        gap="medium",
    )

    with left:

        st.selectbox(
            "Risk Model",
            [
                "Governance-aware",
                "Standard",
            ],
            index=0,
            key="eqmp_risk_model",
        )

        st.selectbox(
            "Risk Threshold",
            [
                "Default",
                "Conservative",
                "Strict",
            ],
            index=0,
            key="eqmp_risk_threshold",
        )

    with right:

        st.toggle(
            "Data Longevity Analysis",
            value=True,
            key="eqmp_data_longevity",
        )

        st.toggle(
            "Migration Timeline Estimation",
            value=True,
            key="eqmp_migration_timeline",
        )

    # =========================================================
    # Access & Accounts
    # =========================================================

    st.markdown(
        """
<div class="eqmp-admin-section">

<div class="eqmp-admin-section-label">
ACCESS & ACCOUNTS
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        2,
        gap="medium",
    )

    with left:

        st.markdown(
            """
<div class="eqmp-admin-card">

<div class="eqmp-admin-card-title">
Active Accounts
</div>

<div class="eqmp-admin-card-description">
Provisioned access to the EQMP environment.
</div>

<div class="eqmp-admin-card-status">
1 Administrator · 1 User · 1 Testing
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with right:

        if st.button(
            "Manage Accounts →",
            key="eqmp_manage_accounts",
            use_container_width=True,
        ):

            st.info(
                "Account management workspace."
            )

