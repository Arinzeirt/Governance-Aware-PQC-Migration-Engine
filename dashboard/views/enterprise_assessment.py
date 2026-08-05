from components.landing.navigation import show as navigation

from components.assessment.shell import show as assessment_shell

from components.assessment.overview.page import (
    show as overview,
)


def show():

    #
    # Global Navigation
    #

    navigation()

    #
    # Enterprise Assessment
    #

    assessment_shell(

        {
            "step": 1,
            "renderer": overview,
        }

    )

