import uuid
from datetime import datetime


class AssessmentSession:

    def __init__(self):
        self.reset()

    def reset(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.state = "IDLE"
        self.created = datetime.now()
        self.target_type = ""
        self.target = ""
        self.finished = False
        self.failed = False

    def start(self, target_type, target):
        self.reset()
        self.state = "INITIALIZING"
        self.target_type = target_type
        self.target = target

    def transition(self, state):
        self.state = state

    def complete(self):
        self.state = "COMPLETED"
        self.finished = True

    def fail(self):
        self.state = "FAILED"
        self.failed = True


session = AssessmentSession()
