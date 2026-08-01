from pathlib import Path

import streamlit as st

from engine.runtime import runtime
from engine.session import session
from engine.runner import runner

from components.discovered_asset_card import show as show_asset
from components.next_phase import show as show_next_phase

from design_system.components import (
    hero,
    panel,
    metric,
    section,
)


def calculate_risk():

    if runtime.critical > 0:
        return "HIGH", "Immediate"

    if runtime.medium > 0:
        return "MEDIUM", "Planned"

    return "LOW", "Monitor"


def readiness_score():

    score = 100

    score -= runtime.critical * 20
    score -= runtime.medium * 8
    score -= runtime.low * 2

    return max(score, 0)


def readiness_label(score):

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 60:
        return "Moderate"

    return "Immediate Action Required"


def executive_decision(risk):

    if risk == "HIGH":

        return (
            "Immediate Migration Required",
            "Critical cryptographic assets require executive oversight and governance-led migration."
        )

    if risk == "MEDIUM":

        return (
            "Migration Planning Required",
            "Prioritise business-critical services."
        )

    return (
        "Continue Monitoring",
        "Continue governance and periodic assessments."
    )


def show():

    risk, priority = calculate_risk()

    score = readiness_score()

    decision, explanation = executive_decision(risk)

    #
    # Enterprise Hero
    #

    hero(

        title="Enterprise Discovery Complete",

        subtitle=(
            "Enterprise cryptographic discovery has completed successfully. "
            "Review the executive assessment outcome before continuing "
            "to Business Configuration."
        ),

        eyebrow="Executive Summary",

        status=runtime.status,

    )

    #
    # STOP HERE
    #
    # Leave the remainder of your existing show()
    # function exactly as it is for now.
    #
