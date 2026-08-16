import streamlit as st

from theme.theme import load


# =========================================================
# Landing Components
# =========================================================

from components.landing.navigation import (
    show as navigation,
)

from components.landing.hero import (
    show as hero,
)

from components.landing.journey import (
    show as journey,
)

from components.landing.enterprise_value import (
    show as enterprise_value,
)

from components.landing.footer import (
    show as footer,
)


# =========================================================
# Shared Authenticated Shell
# =========================================================

from components.app_shell.shell import (
    show as app_shell,
)


# =========================================================
# Views
# =========================================================

from views.login import (
    show as login,
)

from views.command_center import (
    show as command_center,
)

from views.settings import (
    show as settings,
)

from views.discovery import (
    show as discovery,
)

from views.marketplace import (
    show as marketplace,
)

from views.migration import (
    show as migration,
)

from views.enterprise_assessment import (
    show as enterprise_assessment,
)

from views.research import (
    show as research,
)

from views.frameworks import (
    show as frameworks,
)

from views.asset_detail import (
    show as asset_detail,
)


# =========================================================
# Application Configuration
# =========================================================

st.set_page_config(
    page_title="Enterprise Quantum Migration Platform (EQMP)",
    page_icon="dashboard/assets/favicon.png",
    layout="wide",
)

load()


# =========================================================
# Route State
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "landing"


page = st.session_state.page


# =========================================================
# Public Landing
# =========================================================

if page == "landing":

    navigation()

    hero()

    journey()

    enterprise_value()

    footer()


# =========================================================
# Login
# =========================================================

elif page == "login":

    login()


# =========================================================
# Settings
#
# Settings is intentionally outside the four workspace
# navigation items. It is reached through the shell gear.
# =========================================================

elif page == "settings":

    settings()


# =========================================================
# Authenticated Workspace
# =========================================================

elif page == "command_center":

    app_shell(
        "Command Center",
        "Governance, accountability and quantum migration oversight.",
        command_center,
    )


elif page == "discovery":

    app_shell(
        "Discovery",
        "Establish what exists in the enterprise environment before migration decisions are made.",
        discovery,
    )


elif page == "marketplace":

    app_shell(
        "Marketplace",
        "Specialist partners aligned to enterprise quantum-readiness needs.",
        marketplace,
    )


elif page == "migration":

    app_shell(
        "Migration",
        "Governance-aware planning and migration execution.",
        migration,
    )


# =========================================================
# Public Enterprise Assessment
# =========================================================

elif page == "enterprise_assessment":

    enterprise_assessment()


# =========================================================
# Public Research
# =========================================================

elif page == "research":

    navigation()

    research()


# =========================================================
# Public Frameworks
# =========================================================

elif page == "frameworks":

    navigation()

    frameworks()


# =========================================================
# Asset Detail
# =========================================================

elif page == "asset_detail":

    navigation()

    asset_detail()


# =========================================================
# Unknown Route
# =========================================================

else:

    st.session_state.page = "landing"

    st.rerun()
