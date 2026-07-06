from pages.dashboard import show as dashboard
from pages.assessment import show as assessment
from pages.migration import show as migration
from pages.reports import show as reports
from pages.inventory import show as inventory
from pages.repository import show as repository
from pages.research import show as research
from pages.about import show as about


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
    ROUTES.get(page, dashboard)()
