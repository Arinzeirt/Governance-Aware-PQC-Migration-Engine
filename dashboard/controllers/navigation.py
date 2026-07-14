from views.dashboard import show as dashboard
from views.assessment import show as assessment
from views.migration import show as migration
from views.reports import show as reports
from views.inventory import show as inventory
from views.repository import show as repository
from views.research import show as research
from views.about import show as about


ROUTES = {
    "dashboard": dashboard,
    "assessment": assessment,
    "migration": migration,
    "reports": reports,
    "inventory": inventory,
    "repository": repository,
    "research": research,
    "about": about,
}


def render(page):

    ROUTES.get(
        page,
        dashboard
    )()
