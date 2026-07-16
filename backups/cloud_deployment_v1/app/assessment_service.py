from analytics import get_enterprise_intelligence
from decision_service import get_decision
from environment_validation import validate_environment
from enterprise_scan import run_enterprise_scan


PIPELINE = [
    ("Environment Validation", 10),
    ("Enterprise Scan", 40),
    ("Migration Readiness", 65),
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

        self.environment = {}
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

        if stage == "Environment Validation":

            self.environment = validate_environment(self.target)

            env = self.environment

            self.logs.append(
                f"Target verified: {env['target']}"
            )

            self.logs.append(
                f"Files discovered: {env['file_count']}"
            )

            self.logs.append(
                f"Languages: {', '.join(env['languages']) or 'Unknown'}"
            )

            self.logs.append(
                f"Repository: {'Git' if env['git_repository'] else 'Not Detected'}"
            )

            self.logs.append(
                f"Estimated size: {env['estimated_size_mb']} MB"
            )

        elif stage == "Enterprise Scan":

            result = run_enterprise_scan(self.target)

            self.inventory = result["inventory"]

            self.logs.extend(result["activity"])

        elif stage == "Migration Readiness":

            self.analytics = get_enterprise_intelligence()

            self.logs.append(
                "Migration readiness analysis completed."
            )

        elif stage == "Executive Decision":

            self.decision = get_decision()

            self.logs.append(
                "Executive decision generated."
            )

    def get_state(self):

        return {

            "started": self.started,
            "running": self.running,
            "complete": self.complete,

            "progress": self.progress,
            "stage": self.current_stage,

            "environment": self.environment,
            "inventory": self.inventory,
            "analytics": self.analytics,
            "decision": self.decision,

            "logs": self.logs,

        }


service = AssessmentService()
