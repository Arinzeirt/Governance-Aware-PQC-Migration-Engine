from report import generate_report

from engine.runtime import runtime
from engine.stage import transition


def execute(inventory):

    transition(

        message="Generating Executive Report...",

        progress=95,

        stage="Report",

        delay=0.40,

    )

    generate_report(inventory)

    transition(

        message="Executive Report Generated",

        progress=100,

        stage="Completed",

        delay=0.40,

    )

    runtime.finish()

