from engine.runtime import runtime


def execute():

    runtime.emit(

        "Initializing Assessment Engine...",

        progress=5,

        stage="Initialization",

    )

    runtime.start()

