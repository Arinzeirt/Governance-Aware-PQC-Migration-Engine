from components.assessment.layout import show as assessment_layout

from .form import show as technology_form

from components.assessment.research_brief.briefs import (
    TECHNOLOGY,
)


def show():

    return assessment_layout(

        current_step="Technology Landscape",

        form=technology_form,

        research=TECHNOLOGY,

    )
