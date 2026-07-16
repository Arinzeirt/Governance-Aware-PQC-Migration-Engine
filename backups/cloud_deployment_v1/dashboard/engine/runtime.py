from datetime import datetime


class RuntimeManager:

    def __init__(self):

        self.reset()

    def reset(self):

        #
        # Session
        #

        self.running = False
        self.paused = False
        self.cancelled = False

        self.status = "Ready"
        self.stage = "Idle"
        self.progress = 0

        self.started_at = None

        self.refresh_counter = 0

        #
        # Repository
        #

        self.repository_name = ""
        self.repository_type = ""

        #
        # Scan
        #

        self.current_file = ""
        self.files_scanned = 0
        self.total_files = 0

        #
        # Statistics
        #

        self.inventory_records = 0

        self.findings = 0
        self.critical = 0
        self.medium = 0
        self.low = 0

        #
        # Runtime UI
        #

        self.discoveries = []
        self.activity = []

    #
    # --------------------------------------------------
    # Session Lifecycle
    # --------------------------------------------------
    #

    def start(self):

        self.running = True
        self.paused = False
        self.cancelled = False

        self.started_at = datetime.now()

        self.status = "Running"

        self.log(

            "Assessment Started"

        )

    def finish(self):

        self.running = False

        self.status = "Completed"

        self.progress = 100

        self.log(

            "Assessment Completed"

        )

    def fail(self):

        self.running = False

        self.status = "Failed"

        self.log(

            "Assessment Failed"

        )

    def pause(self):

        self.paused = True

        self.status = "Paused"

        self.log(

            "Assessment Paused"

        )

    def resume(self):

        self.paused = False

        self.status = "Running"

        self.log(

            "Assessment Resumed"

        )

    #
    # --------------------------------------------------
    # Repository
    # --------------------------------------------------
    #

    def set_repository(

        self,

        name,

        repo_type,

    ):

        self.repository_name = name
        self.repository_type = repo_type

    #
    # --------------------------------------------------
    # Scanner
    # --------------------------------------------------
    #

    def update_scan(

        self,

        file,

        current,

        total,

    ):

        self.current_file = file

        self.files_scanned = current

        self.total_files = total

        self.refresh()

    #
    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------
    #

    def update_statistics(

        self,

        **kwargs,

    ):

        if "inventory" in kwargs:

            self.inventory_records = kwargs["inventory"]

        if "findings" in kwargs:

            self.findings = kwargs["findings"]

        if "critical" in kwargs:

            self.critical = kwargs["critical"]

        if "medium" in kwargs:

            self.medium = kwargs["medium"]

        if "low" in kwargs:

            self.low = kwargs["low"]

        self.refresh()

    #
    # --------------------------------------------------
    # Discoveries
    # --------------------------------------------------
    #

    def add_discovery(

        self,

        title,

        file,

        severity="Medium",

    ):

        self.findings += 1

        if severity == "High":

            self.critical += 1

        elif severity == "Medium":

            self.medium += 1

        else:

            self.low += 1

        self.discoveries.insert(

            0,

            {

                "title": title,

                "file": file,

                "severity": severity,

            },

        )

        self.discoveries = self.discoveries[:15]

        self.refresh()

    #
    # --------------------------------------------------
    # Timeline
    # --------------------------------------------------
    #

    def log(

        self,

        message,

    ):

        self.activity.insert(

            0,

            {

                "time": datetime.now().strftime(

                    "%H:%M:%S"

                ),

                "message": message,

            },

        )

        self.activity = self.activity[:25]

        self.refresh()

    #
    # --------------------------------------------------
    # Runtime Messaging
    # --------------------------------------------------
    #

    def emit(

        self,

        message,

        progress=None,

        stage=None,

        log=True,

    ):

        if progress is not None:

            self.progress = progress

        if stage is not None:

            self.stage = stage

        #
        # Notify UI
        #

        self.refresh()

        #
        # Optional timeline logging
        #

        if log and message:

            self.log(message)

    #
    # --------------------------------------------------
    # Runtime Refresh
    # --------------------------------------------------
    #

    def refresh(self):

        self.refresh_counter += 1

    #
    # --------------------------------------------------
    # Runtime Clock
    # --------------------------------------------------
    #

    def elapsed(self):

        if not self.started_at:

            return "00:00"

        seconds = int(

            (

                datetime.now()

                - self.started_at

            ).total_seconds()

        )

        minutes = seconds // 60

        seconds %= 60

        return f"{minutes:02}:{seconds:02}"

    #
    # --------------------------------------------------
    # New Assessment
    # --------------------------------------------------
    #

    def new_assessment(self):

        self.reset()


runtime = RuntimeManager()

