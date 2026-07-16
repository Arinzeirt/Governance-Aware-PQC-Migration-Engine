import threading
import traceback

from engine.assessment_engine import engine
from engine.runtime import runtime


class AssessmentRunner:

    def __init__(self):

        self.thread = None
        self.running = False

    def start(
        self,
        target_type,
        target,
    ):

        if self.running:
            return False

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            args=(
                target_type,
                target,
            ),
            daemon=True,
        )

        self.thread.start()

        return True

    def _run(
        self,
        target_type,
        target,
    ):

        try:

            engine.run(
                target_type,
                target,
            )

        except Exception as e:

            runtime.log(
                f"ENGINE ERROR: {type(e).__name__}: {e}"
            )

            traceback.print_exc()

            runtime.fail()

        finally:

            self.running = False

    def is_running(self):

        return self.running


runner = AssessmentRunner()
