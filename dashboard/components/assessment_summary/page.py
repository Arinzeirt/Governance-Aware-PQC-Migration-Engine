from .header import show as show_header
from .kpis import show as show_kpis
from .decision import show as show_decision
from .metadata import show as show_metadata
from .assets import show as show_assets
from .next_phase import show as show_next_phase
from .actions import show as show_actions


def show():

    show_header()

    show_kpis()

    show_decision()

    show_metadata()

    show_assets()

    show_next_phase()

    show_actions()
