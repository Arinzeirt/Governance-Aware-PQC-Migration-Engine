import uuid

from project.project import AssessmentProject


class AssessmentProjectManager:
    """
    Central manager for enterprise Assessment Projects.
    """

    def __init__(self):

        self._assessments = {}

        self._current_id = None

    #
    # Create Assessment
    #

    def create_assessment(
        self,
        name: str,
        repository: str = "",
        repository_type: str = "",
    ):

        project = AssessmentProject()

        project.project_id = str(uuid.uuid4())

        project.name = name

        project.repository = repository

        project.repository_type = repository_type

        project.status = "Assessment"

        self._assessments[
            project.project_id
        ] = project

        self._current_id = project.project_id

        return project

    #
    # Current Assessment
    #

    @property
    def current(self):

        if self._current_id is None:

            return None

        return self._assessments.get(
            self._current_id
        )

    #
    # Lookup
    #

    def get_assessment(
        self,
        project_id: str,
    ):

        return self._assessments.get(
            project_id
        )

    #
    # Registry
    #

    def list_assessments(self):

        return list(
            self._assessments.values()
        )

    #
    # State
    #

    def has_assessment(self):

        return self.current is not None

    #
    # Close Current
    #

    def close_assessment(self):

        self._current_id = None

    #
    # Reset Everything
    #

    def reset(self):

        self._assessments.clear()

        self._current_id = None


manager = AssessmentProjectManager()
