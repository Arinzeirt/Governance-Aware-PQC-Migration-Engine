from engine.runtime import runtime
from engine.stage import transition


def execute():

    #
    # Assessment officially starts here.
    #

    runtime.start()

    transition(

        message="Initializing Assessment Engine...",

        progress=10,

        stage="Initializing",

        delay=0.35,

    )

