from analytics import get_enterprise_intelligence
from decision_service import get_decision
from scanner import scan_directory


PIPELINE = [
    ("Environment Validation", 10),
    ("Cryptographic Discovery", 30),
    ("Asset Classification", 50),
    ("Migration Readiness", 70),
    ("Governance Analysis", 85),
    ("Executive Decision", 100),
]


class AssessmentService:

    def __init__(self):

        self.reset()

    def reset(self):

        self.started = False

        self.running = False
        self.complete = False

        self.target = None

        self.stage_index = -1
        self.current_stage = "Waiting"

        self.progress = 0

        self.inventory = []
        self.analytics = {}
        self.decision = {}

        self.logs = []

    def begin(self, target):

        if self.started:
            return

        self.reset()

        self.started = True

        self.running = True

        self.target = target

        self.logs.append("Assessment started.")

    def next_step(self):

        if self.complete:
            return

        self.stage_index += 1

        if self.stage_index >= len(PIPELINE):

            self.running = False
            self.complete = True

            self.logs.append(
                "Assessment completed successfully."
            )

            return

        stage, progress = PIPELINE[self.stage_index]

        self.current_stage = stage

        self.progress = progress

        self.logs.append(stage)

        if stage == "Cryptographic Discovery":

            self.inventory = scan_directory(self.target)

        elif stage == "Migration Readiness":

            self.analytics = get_enterprise_intelligence()

        elif stage == "Executive Decision":

            self.decision = get_decision()

    def get_state(self):

        return {

            "started": self.started,

            "running": self.running,

            "complete": self.complete,

            "progress": self.progress,

            "stage": self.current_stage,

            "inventory": self.inventory,

            "analytics": self.analytics,

            "decision": self.decision,

            "logs": self.logs,

        }


service = AssessmentService()
