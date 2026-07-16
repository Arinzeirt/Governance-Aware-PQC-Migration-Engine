import sys
import time
from pathlib import Path
from datetime import datetime

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service


PIPELINE = [
    "Environment Validation",
    "Cryptographic Discovery",
    "Asset Classification",
    "Migration Readiness",
    "Governance Analysis",
    "Executive Decision",
]


def create_session():

    return "PQC-" + datetime.now().strftime("%Y%m%d-%H%M%S")


def run_assessment(target="."):

    session = create_session()

    service.begin(target)

    while not service.complete:

        service.next_step()

        state = service.get_state()

        runtime = {

            "session": session,

            "progress": state["progress"],

            "stage": state["stage"],

            "operation": state["stage"],

            "completed": PIPELINE[:service.stage_index],

            "current": state["stage"],

            "pending": PIPELINE[service.stage_index + 1:],

            "log": state["logs"][-8:],

            "inventory": state["inventory"],

            "analytics": state["analytics"],

            "decision": state["decision"]

        }

        # ---------- Runtime Store ----------
        st.session_state.app["assessment"]["running"] = True
        st.session_state.app["assessment"]["complete"] = state["complete"]
        st.session_state.app["assessment"]["state"] = runtime
        # -----------------------------------

        yield runtime

        time.sleep(0.6)

    final_state = service.get_state()

    st.session_state.app["assessment"]["running"] = False
    st.session_state.app["assessment"]["complete"] = True
    st.session_state.app["assessment"]["state"] = {

        "session": session,

        "progress": final_state["progress"],

        "stage": final_state["stage"],

        "operation": final_state["stage"],

        "completed": PIPELINE,

        "current": final_state["stage"],

        "pending": [],

        "log": final_state["logs"][-8:],

        "inventory": final_state["inventory"],

        "analytics": final_state["analytics"],

        "decision": final_state["decision"]

    }

    yield st.session_state.app["assessment"]["state"]
