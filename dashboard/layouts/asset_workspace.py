import streamlit as st

from views.asset_detail import show as show_asset
from components.enterprise_header import show as show_header


def show():

    # Enterprise branding only.
    # Deliberately omit the top navigation to provide
    # a distraction-free reading experience.

    show_header()

    show_asset()
