from components.assessment.layout import show as assessment_layout

from .form import show as cryptography_form

from components.assessment.research_brief.briefs import (
    CRYPTOGRAPHY,
)


def show():

    return assessment_layout(

        current_step="Cryptographic Posture",

        form=cryptography_form,

        research=CRYPTOGRAPHY,

    )
