import os

from target_manager import manager

from engine.runtime import runtime
from engine.stage import transition


def execute(

    target_type,

    target,

):

    transition(

        message="Resolving Assessment Target...",

        progress=15,

        stage="Target",

        delay=0.30,

    )

    if target_type == "Local Directory":

        directory = manager.prepare_local(target)

    elif target_type == "GitHub Repository":

        directory = manager.prepare_github(target)

    else:

        raise ValueError(

            "Unsupported assessment target."

        )

    runtime.set_repository(

        name=os.path.basename(directory),

        repo_type=target_type,

    )

    transition(

        message="Repository Loaded",

        progress=25,

        stage="Target",

        delay=0.30,

    )

    return directory

