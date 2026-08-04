from components.assessment.header import show as header
from components.assessment.progress import show as progress
from components.assessment.navigation import show as navigation


def show(content):

    step = content["step"]

    header()

    progress(step)

    result = content["renderer"]()

    navigation(
        step,
        can_continue=result.get("can_continue", True),
        on_continue=result.get("on_continue"),
    )
