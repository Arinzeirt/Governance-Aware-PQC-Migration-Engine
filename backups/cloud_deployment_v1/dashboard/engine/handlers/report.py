from report import generate_report
from pdf_report import build_pdf_report
from package_report import build_package

from engine.runtime import runtime
from engine.stage import transition


def execute(inventory):

    transition(
        message="Generating Executive Report...",
        progress=95,
        stage="Report",
        delay=0.40,
    )

    # Generate TXT report
    generate_report(inventory)

    # Generate Executive PDF
    build_pdf_report()

    # Build downloadable package
    build_package()

    transition(
        message="Assessment Package Generated",
        progress=100,
        stage="Completed",
        delay=0.40,
    )

    runtime.finish()
