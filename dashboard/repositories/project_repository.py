from dashboard.domain.project import Project


class ProjectRepository:

    def __init__(self):

        self._projects = {}

    def add(self, project: Project):

        self._projects[
            project.project_id
        ] = project

    def get(self, project_id: str):

        return self._projects.get(
            project_id
        )

    def list(self):

        return list(
            self._projects.values()
        )


repository = ProjectRepository()
