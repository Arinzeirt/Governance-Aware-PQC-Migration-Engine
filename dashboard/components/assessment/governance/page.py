from components.assessment.layout import show as assessment_layout

from .form import show as governance_form


def show():

    return assessment_layout(

        current_step=2,

        form=governance_form,

    )
