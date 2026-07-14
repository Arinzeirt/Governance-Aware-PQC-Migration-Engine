class WorkflowStep:

    def __init__(

        self,

        key,

        title,

        progress,

    ):

        self.key = key

        self.title = title

        self.progress = progress


class WorkflowEngine:

    def __init__(self):

        self.steps = [

            WorkflowStep(
                "INITIALIZE",
                "Initializing Assessment",
                5,
            ),

            WorkflowStep(
                "TARGET",
                "Resolving Assessment Target",
                15,
            ),

            WorkflowStep(
                "DISCOVERY",
                "Scanning Repository",
                40,
            ),

            WorkflowStep(
                "INVENTORY",
                "Building Inventory",
                70,
            ),

            WorkflowStep(
                "REPORT",
                "Generating Executive Report",
                90,
            ),

            WorkflowStep(
                "COMPLETE",
                "Assessment Complete",
                100,
            ),

        ]

        self.reset()

    def reset(self):

        self.position = 0

        self.started = False

        self.finished = False

    @property
    def current(self):

        return self.steps[self.position]

    def advance(self):

        if self.position < len(self.steps) - 1:

            self.position += 1

        else:

            self.finished = True

    def begin(self):

        self.started = True


workflow = WorkflowEngine()

