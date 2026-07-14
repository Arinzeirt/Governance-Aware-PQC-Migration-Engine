from components.executive_summary import show as show_summary
from components.executive_kpis import show as show_kpis
from components.quick_actions import show as show_actions
from components.executive_workspace import show as show_workspace
from components.footer import show as show_footer


def show():

    #
    # Executive Summary
    #
    show_summary()

    #
    # Executive KPIs
    #
    show_kpis()

    #
    # Recommended Next Steps
    #
    show_actions()

    #
    # Enterprise Workspace
    #
    show_workspace()

    #
    # Footer
    #
    show_footer()

