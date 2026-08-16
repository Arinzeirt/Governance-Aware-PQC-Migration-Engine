import streamlit as st


def _navigate(page):

    st.session_state.page = page
    st.rerun()


def show():

    if not st.session_state.get(
        "eqmp_authenticated",
        False,
    ):

        st.session_state.page = "login"
        st.rerun()

    organisation = st.session_state.get(
        "eqmp_organisation",
        "Organisation",
    )

    # =====================================================
    # Environment
    # =====================================================

    from components.environment import (
        initialize_environment,
        get_environment,
    )

    environment = initialize_environment(
        organization_id=st.session_state.get(
            "eqmp_organisation_id",
            "",
        ),
        name=st.session_state.get(
            "eqmp_organisation_name",
            "Primary Environment",
        ),
    )

    st.markdown(
        """
<div style="
    font-size:0.72rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
    margin-bottom:8px;
">
ENVIRONMENT
</div>
""",
        unsafe_allow_html=True,
    )

    environment_left, environment_right = st.columns(
        [1.4, 1],
        gap="medium",
    )

    with environment_left:

        status = environment.get(
            "status",
            "Not Connected",
        )

        status_class = (
            "connected"
            if status == "Connected"
            else "pending"
        )

        status_text = (
            "Connected"
            if status == "Connected"
            else "Not Connected"
        )

        st.markdown(
            f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:15px;
    min-height:112px;
">

<div style="
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:9px;
">

<div style="
    font-size:0.90rem;
    font-weight:800;
    color:#F5F7FA;
">
{environment.get("name", "Primary Environment")}
</div>

<div class="eqmp-env-status {status_class}">
● {status_text}
</div>

</div>

<div style="
    font-size:0.67rem;
    line-height:1.5;
    color:#8FA1B5;
">
The enterprise environment is the EQMP oversight boundary.
Discovery sources contribute evidence to this environment;
no individual vendor becomes the system of record.
</div>

</div>

<style>

.eqmp-env-status {{
    font-size:0.62rem;
    font-weight:700;
}}

.eqmp-env-status.connected {{
    color:#22C55E;
}}

.eqmp-env-status.pending {{
    color:#8FA1B5;
}}

</style>
""",
            unsafe_allow_html=True,
        )

    with environment_right:

        visibility = environment.get(
            "visibility",
            {},
        )

        active_sources = len(
            environment.get(
                "sources",
                [],
            )
        )

        st.markdown(
            f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:15px;
    min-height:112px;
">

<div style="
    font-size:0.62rem;
    letter-spacing:1px;
    color:#7F91A6;
    font-weight:750;
    margin-bottom:10px;
">
ENVIRONMENT VISIBILITY
</div>

<div style="
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
">

<div>
<div style="
    font-size:0.85rem;
    font-weight:750;
    color:#F5F7FA;
">
{visibility.get("systems", 0)}
</div>
<div style="
    font-size:0.57rem;
    color:#718096;
">
Systems
</div>
</div>

<div>
<div style="
    font-size:0.85rem;
    font-weight:750;
    color:#F5F7FA;
">
{visibility.get("applications", 0)}
</div>
<div style="
    font-size:0.57rem;
    color:#718096;
">
Applications
</div>
</div>

<div>
<div style="
    font-size:0.85rem;
    font-weight:750;
    color:#F5F7FA;
">
{visibility.get("cryptographic_assets", 0)}
</div>
<div style="
    font-size:0.57rem;
    color:#718096;
">
Cryptographic Assets
</div>
</div>

<div>
<div style="
    font-size:0.85rem;
    font-weight:750;
    color:#F5F7FA;
">
{active_sources}
</div>
<div style="
    font-size:0.57rem;
    color:#718096;
">
Active Sources
</div>
</div>

</div>

</div>
""",
            unsafe_allow_html=True,
        )

    # =====================================================
    # Discovery Sources
    # =====================================================

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="
    font-size:0.72rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
    margin-bottom:5px;
">
DISCOVERY SOURCES
</div>

<div style="
    font-size:0.72rem;
    color:#8FA1B5;
    line-height:1.45;
    margin-bottom:12px;
">
Connect approved sources of enterprise evidence to build
visibility without surrendering oversight to a vendor.
</div>
""",
        unsafe_allow_html=True,
    )

    source_left, source_right = st.columns(
        2,
        gap="medium",
    )

    sources = [
        (
            "Enterprise Directory",
            "Asset and system inventory",
            "Directory",
        ),
        (
            "Cryptographic Scanner",
            "Cryptographic asset discovery",
            "Scanner",
        ),
        (
            "Cloud Environment",
            "Cloud infrastructure visibility",
            "Cloud",
        ),
        (
            "Evidence Repository",
            "Architecture and supporting evidence",
            "Evidence",
        ),
    ]

    for index, (
        name,
        description,
        source_type,
    ) in enumerate(sources):

        column = (
            source_left
            if index % 2 == 0
            else source_right
        )

        with column:

            connected = any(
                source.get("source_type") == source_type
                and source.get("status") == "Connected"
                for source in environment.get(
                    "sources",
                    [],
                )
            )

            source_status = (
                "Connected"
                if connected
                else "Not Connected"
            )

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.09);
    border-radius:7px;
    padding:11px 12px;
    margin-bottom:8px;
">

<div style="
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
">

<div>

<div style="
    font-size:0.70rem;
    font-weight:700;
    color:#D5DCE5;
">
{name}
</div>

<div style="
    font-size:0.59rem;
    color:#718096;
    margin-top:4px;
">
{description}
</div>

</div>

<div style="
    font-size:0.57rem;
    color:{'#22C55E' if connected else '#718096'};
    white-space:nowrap;
">
● {source_status}
</div>

</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # =====================================================
    # Environment Overview
    # =====================================================


    st.markdown(
        """
<div style="
    font-size:0.72rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
    margin-bottom:8px;
">
ENVIRONMENT OVERVIEW
</div>
""",
        unsafe_allow_html=True,
    )

    systems, applications, data, cryptography = st.columns(
        4,
        gap="small",
    )

    overview_cards = [
        (
            systems,
            "SYSTEMS",
            "Not connected",
            "Environment discovery required",
        ),
        (
            applications,
            "APPLICATIONS",
            "Not connected",
            "Application inventory required",
        ),
        (
            data,
            "DATA",
            "Not established",
            "Data classification required",
        ),
        (
            cryptography,
            "CRYPTOGRAPHY",
            "Limited visibility",
            "Cryptographic discovery required",
        ),
    ]

    for column, label, value, detail in overview_cards:

        with column:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:14px;
    min-height:108px;
">

<div style="
    font-size:0.64rem;
    letter-spacing:1px;
    color:#7F91A6;
    font-weight:750;
    margin-bottom:8px;
">
{label}
</div>

<div style="
    font-size:0.98rem;
    font-weight:800;
    color:#F5F7FA;
">
{value}
</div>

<div style="
    font-size:0.70rem;
    line-height:1.4;
    color:#8FA1B5;
    margin-top:5px;
">
{detail}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # =====================================================
    # Discovery Coverage
    # =====================================================

    st.markdown(
        '<div style="height:22px"></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.35, 1],
        gap="medium",
    )

    with left:

        st.markdown(
            """
<div style="
    font-size:0.95rem;
    font-weight:750;
    margin-bottom:9px;
">
Discovery Coverage
</div>
""",
            unsafe_allow_html=True,
        )

        coverage = [
            (
                "Technology environment",
                0,
                "No technical evidence connected",
            ),
            (
                "Cryptographic environment",
                0,
                "No cryptographic inventory connected",
            ),
            (
                "Certificates & PKI",
                0,
                "Certificate evidence not connected",
            ),
            (
                "System dependencies",
                0,
                "Dependency relationships not established",
            ),
        ]

        for label, percentage, detail in coverage:

            st.markdown(
                f"""
<div style="
    margin-bottom:13px;
">

<div style="
    display:flex;
    justify-content:space-between;
    font-size:0.72rem;
    margin-bottom:5px;
">

<span style="color:#C9D2DD;">
{label}
</span>

<span style="color:#7F91A6;">
{percentage}%
</span>

</div>

<div style="
    height:5px;
    background:#202632;
    border-radius:5px;
    overflow:hidden;
">

<div style="
    width:{percentage}%;
    height:100%;
    background:#2F81F7;
">
</div>

</div>

<div style="
    font-size:0.64rem;
    color:#66778C;
    margin-top:4px;
">
{detail}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # =====================================================
    # Discovery Sources
    # =====================================================

    with right:

        st.markdown(
            """
<div style="
    font-size:0.95rem;
    font-weight:750;
    margin-bottom:9px;
">
Discovery Sources
</div>
""",
            unsafe_allow_html=True,
        )

        sources = [
            (
                "Directory",
                "Import enterprise asset and system inventories.",
            ),
            (
                "Scanner",
                "Connect technical discovery and cryptographic scanning.",
            ),
            (
                "Evidence",
                "Upload architecture, certificate and system evidence.",
            ),
        ]

        for title, description in sources:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.08);
    border-radius:7px;
    padding:11px 13px;
    margin-bottom:7px;
">

<div style="
    font-size:0.79rem;
    font-weight:700;
    color:#D9E0E8;
">
{title}
</div>

<div style="
    font-size:0.67rem;
    color:#7F91A6;
    line-height:1.4;
    margin-top:4px;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # =====================================================
    # Open Discovery Gaps
    # =====================================================

    st.markdown(
        '<div style="height:10px"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="
    font-size:0.95rem;
    font-weight:750;
    margin-bottom:9px;
">
Open Discovery Gaps
</div>

<div style="
    border:1px solid rgba(255,255,255,.08);
    border-radius:8px;
    padding:14px;
">

<div style="
    display:grid;
    grid-template-columns:1.5fr 1fr 1fr;
    gap:10px;
    font-size:0.68rem;
    color:#7F91A6;
    font-weight:700;
    margin-bottom:8px;
">
<span>Discovery requirement</span>
<span>Current state</span>
<span>Impact</span>
</div>

<div style="
    display:grid;
    grid-template-columns:1.5fr 1fr 1fr;
    gap:10px;
    font-size:0.72rem;
    color:#C9D2DD;
    padding:8px 0;
    border-top:1px solid rgba(255,255,255,.06);
">
<span>Enterprise asset inventory</span>
<span>Not connected</span>
<span>High</span>
</div>

<div style="
    display:grid;
    grid-template-columns:1.5fr 1fr 1fr;
    gap:10px;
    font-size:0.72rem;
    color:#C9D2DD;
    padding:8px 0;
    border-top:1px solid rgba(255,255,255,.06);
">
<span>Cryptographic inventory</span>
<span>Not established</span>
<span>High</span>
</div>

<div style="
    display:grid;
    grid-template-columns:1.5fr 1fr 1fr;
    gap:10px;
    font-size:0.72rem;
    color:#C9D2DD;
    padding:8px 0;
    border-top:1px solid rgba(255,255,255,.06);
">
<span>Certificate / PKI inventory</span>
<span>Not connected</span>
<span>Medium</span>
</div>

<div style="
    display:grid;
    grid-template-columns:1.5fr 1fr 1fr;
    gap:10px;
    font-size:0.72rem;
    color:#C9D2DD;
    padding:8px 0;
    border-top:1px solid rgba(255,255,255,.06);
">
<span>System dependencies</span>
<span>Not established</span>
<span>High</span>
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "Return to Command Center",
        key="discovery_return",
    ):
        _navigate("command_center")
