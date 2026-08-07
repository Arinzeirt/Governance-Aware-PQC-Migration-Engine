from components.assessment.layout import show as assessment_layout

from .form import show as governance_form

from components.assessment.research_brief.briefs import (
    CONFIGURATION,
)


def show():

    return assessment_layout(

        current_step="Governance & Risk",

        form=governance_form,

        research=CONFIGURATION,

    )
