from components.assessment.layout import show as assessment_layout

from .form import show as cryptography_form


def show():

    return assessment_layout(

        current_step=4,

        form=cryptography_form,

    )
