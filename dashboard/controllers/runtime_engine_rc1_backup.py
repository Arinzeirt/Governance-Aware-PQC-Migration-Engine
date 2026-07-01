import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service


def update_runtime(target="."):

    assessment = st.session_state.app["assessment"]

    if not assessment["running"] and not assessment["complete"]:

        service.begin(target)

        service.next_step()

    elif service.running:

        service.next_step()

    state = service.get_state()

    assessment["running"] = state["running"]
    assessment["complete"] = state["complete"]
    assessment["state"] = state

    return state
