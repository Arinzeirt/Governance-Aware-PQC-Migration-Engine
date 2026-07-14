import os

from target_manager import manager

from engine.runtime import runtime


def execute(

    target_type,

    target,

):

    runtime.emit(

        "Resolving Assessment Target...",

        progress=15,

        stage="Target",

    )

    #
    # Resolve Target
    #

    if target_type == "Local Directory":

        directory = manager.prepare_local(target)

    elif target_type == "GitHub Repository":

        directory = manager.prepare_github(target)

    else:

        raise ValueError(

            "Unsupported assessment target."

        )

    #
    # Update Runtime Repository Information
    #

    runtime.set_repository(

        name=os.path.basename(directory),

        repo_type=target_type,

    )

    runtime.emit(

        f"Repository Loaded: {os.path.basename(directory)}",

        progress=20,

    )

    return directory

