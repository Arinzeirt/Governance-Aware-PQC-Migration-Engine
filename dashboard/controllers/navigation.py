from views.dashboard import show as dashboard
from views.enterprise_assessment import show as enterprise_assessment
from views.assessment import show as assessment
from views.migration import show as migration
from views.reports import show as reports
from views.inventory import show as inventory
from views.repository import show as repository
from views.research import show as research
from views.knowledge_library import show as knowledge_library
from views.asset_detail import show as asset_detail
from views.about import show as about
from views.emcw import show as emcw


ROUTES = {

    "dashboard": dashboard,

    #
    # Enterprise Assessment Platform
    #
    "enterprise_assessment": enterprise_assessment,

    #
    # Assessment Runtime Engine
    #
    "assessment": assessment,

    "migration": migration,

    "emcw": emcw,

    "reports": reports,

    "inventory": inventory,

    "repository": repository,

    "research": research,

    "knowledge_library": knowledge_library,

    "asset_detail": asset_detail,

    "about": about,

}


def render(page):

    ROUTES.get(
        page,
        dashboard,
    )()
