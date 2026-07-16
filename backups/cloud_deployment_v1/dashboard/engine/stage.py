from engine.runtime import runtime


#
# Stage Transition
#

def transition(

    message,

    progress,

    stage,

    delay=0,

):

    runtime.emit(

        message,

        progress=progress,

        stage=stage,

    )

