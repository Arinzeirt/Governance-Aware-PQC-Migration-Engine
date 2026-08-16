import streamlit as st
from datetime import datetime

from domain.environment import Environment


def _ensure_app_state():

    if "app" not in st.session_state:

        st.session_state.app = {

            "presentation_mode": True,

            "assessment": {
                "running": False,
                "complete": False,
                "started": False,
                "ui_loaded": False,
                "state": None,
            },

            "dashboard": {
                "loaded": False,
                "last_refresh": None,
            },

            "migration": {
                "loaded": False,
                "active_view": "overview",
                "filters": {},
            },

            "inventory": {
                "loaded": False,
                "last_sync": None,
            },

            "reports": {
                "loaded": False,
                "last_generated": None,
                "available": [],
            },

            "research": {
                "loaded": False,
                "active_section": "overview",
                "filters": {},
            },

            "navigation": {
                "selected_page": "dashboard",
                "history": [],
            },

            "environment": {
                "environment_id": None,
                "organization_id": None,
                "name": "Primary Environment",
                "status": "Not Connected",
                "created_at": None,
                "last_sync": None,
                "sources": [],
                "visibility": {
                    "systems": 0,
                    "applications": 0,
                    "data_assets": 0,
                    "cryptographic_assets": 0,
                    "certificates": 0,
                },
                "discovery_gaps": 0,
            },
        }


def initialize_environment(
    organization_id="",
    name="Primary Environment",
):

    _ensure_app_state()

    environment = st.session_state.app[
        "environment"
    ]

    if not environment["environment_id"]:

        model = Environment(
            organization_id=organization_id,
            name=name,
        )

        environment["environment_id"] = (
            model.environment_id
        )

        environment["organization_id"] = (
            organization_id
        )

        environment["name"] = name

        environment["status"] = model.status

        environment["created_at"] = (
            model.created_at
        )

    return environment


def get_environment():

    _ensure_app_state()

    return st.session_state.app[
        "environment"
    ]


def update_environment_status(status):

    environment = get_environment()

    environment["status"] = status


def record_sync():

    environment = get_environment()

    environment["last_sync"] = datetime.utcnow()

    environment["status"] = "Connected"


def add_source(
    name,
    source_type,
    provider="",
):

    environment = get_environment()

    source = {
        "source_id": (
            f"{source_type.lower()}-"
            f"{len(environment['sources']) + 1}"
        ),
        "name": name,
        "source_type": source_type,
        "provider": provider,
        "status": "Connected",
        "last_sync": datetime.utcnow(),
    }

    environment["sources"].append(
        source
    )

    return source


def set_visibility(
    systems=None,
    applications=None,
    data_assets=None,
    cryptographic_assets=None,
    certificates=None,
):

    environment = get_environment()

    visibility = environment[
        "visibility"
    ]

    values = {
        "systems": systems,
        "applications": applications,
        "data_assets": data_assets,
        "cryptographic_assets": cryptographic_assets,
        "certificates": certificates,
    }

    for key, value in values.items():

        if value is not None:

            visibility[key] = value
