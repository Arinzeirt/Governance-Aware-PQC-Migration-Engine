import sys
import time
from pathlib import Path
from datetime import datetime

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

        completed = PIPELINE[:service.stage_index]

        current = state["stage"]

        pending = PIPELINE[service.stage_index + 1:]

        yield {

            "session": session,

            "progress": state["progress"],

            "stage": current,

            "operation": current,

            "completed": completed,

            "current": current,

            "pending": pending,

            "log": state["logs"][-8:],

            # Runtime Snapshot
            "inventory": state["inventory"],

            "analytics": state["analytics"],

            "decision": state["decision"]

        }

        time.sleep(0.6)
