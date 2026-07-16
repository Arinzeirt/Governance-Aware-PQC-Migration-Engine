import streamlit as st

from design_system import section_title


class ExecutivePanel:

    def __init__(self, title, subtitle):

        self.title = title

        self.subtitle = subtitle

    def __enter__(self):

        self.container = st.container(border=True)

        self.container.__enter__()

        section_title(
            self.title,
            self.subtitle
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.container.__exit__(
            exc_type,
            exc_val,
            exc_tb
        )


def executive_panel(title, subtitle):

    return ExecutivePanel(
        title,
        subtitle
    )

