from components.assessment.layout import show as assessment_layout

from .form import show as technology_form


def show():

    return assessment_layout(

        current_step=3,

        form=technology_form,

    )
