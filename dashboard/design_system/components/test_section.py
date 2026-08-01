import streamlit as st

from design_system.components.section import show


def demo():
    show(
        title="Enterprise Discovery",
        subtitle="Discover cryptographic assets across enterprise systems.",
        eyebrow="EDS-001",
    )
