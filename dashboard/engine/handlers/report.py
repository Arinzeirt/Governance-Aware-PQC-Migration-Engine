from report import generate_report

from engine.runtime import runtime


def execute(inventory):

    runtime.emit(

        "Generating Executive Report...",

        progress=92,

        stage="Reporting",

    )

    generate_report(inventory)

    runtime.emit(

        "Executive Report Generated",

        progress=100,

        stage="Completed",

    )

    runtime.finish()

