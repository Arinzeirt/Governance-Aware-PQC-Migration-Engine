from components.assessment.layout import show as assessment_layout

from .form import show as review_form


def show():

    return assessment_layout(
        current_step=5,
        form=review_form,
    )
