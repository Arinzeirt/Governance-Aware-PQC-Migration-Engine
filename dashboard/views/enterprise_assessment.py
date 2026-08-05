from components.assessment.shell import show as assessment_shell

from components.assessment.overview.page import (
    show as overview,
)


def show():

    assessment_shell(

        {
            "step": 1,
            "renderer": overview,
        }

    )
