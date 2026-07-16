"""
Enet Design System (EDS)

Package Entry Point
"""

from design_system.css import load as load_css

VERSION = "1.0.0"

NAME = "Enet Design System"

SHORT_NAME = "EDS"


def load_design():
    """
    Load the Enet Design System.
    """
    load_css()

