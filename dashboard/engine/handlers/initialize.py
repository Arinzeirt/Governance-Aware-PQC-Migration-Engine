from engine.runtime import runtime
from engine.stage import transition


def execute():

    #
    # Assessment runtime begins.
    #

    runtime.start()

    transition(
        message="Assessment session created",
        progress=2,
        stage="Initializing",
        delay=0.15,
    )

    transition(
        message="Loading enterprise configuration",
        progress=4,
        stage="Initializing",
        delay=0.15,
    )

    transition(
        message="Loading migration policies",
        progress=6,
        stage="Initializing",
        delay=0.15,
    )

    transition(
        message="Initializing runtime services",
        progress=8,
        stage="Initializing",
        delay=0.15,
    )

    transition(
        message="Preparing discovery engine",
        progress=9,
        stage="Initializing",
        delay=0.15,
    )

    transition(
        message="Assessment engine ready",
        progress=10,
        stage="Initializing",
        delay=0.15,
    )
