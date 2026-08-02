from dashboard.domain.organization import Organization


class OrganizationRepository:

    def __init__(self):

        self._organizations = {}

    def add(self, organization: Organization):

        self._organizations[
            organization.organization_id
        ] = organization

    def get(self, organization_id: str):

        return self._organizations.get(
            organization_id
        )

    def list(self):

        return list(
            self._organizations.values()
        )


repository = OrganizationRepository()
