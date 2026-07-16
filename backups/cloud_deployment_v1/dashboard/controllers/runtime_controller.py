import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service

from components.assessment_runner import run_assessment


class RuntimeController:

    def __init__(self):

        self._runtime = None

    def start(self, target="."):

        return run_assessment(target)

    def current_state(self):

        return service.get_state()

    def complete(self):

        return service.get_state()["complete"]


controller = RuntimeController()
