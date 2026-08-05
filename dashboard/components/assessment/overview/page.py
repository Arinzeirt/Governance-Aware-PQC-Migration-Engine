from components.assessment.layout import show as assessment_layout

from .form import show as organisation_form

from components.assessment.research_brief.briefs import (
    OVERVIEW,
)


def show():

    return assessment_layout(

        current_step="Enterprise Profile",

        form=organisation_form,

        research=OVERVIEW,

    )
