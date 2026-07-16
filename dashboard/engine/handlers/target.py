import os

from target_manager import manager

from engine.runtime import runtime
from engine.stage import transition


def execute(target_type, target):

    runtime.log(f"Target Type: {target_type}")
    runtime.log(f"Target: {target}")

    transition(
        message="Resolving Assessment Target...",
        progress=15,
        stage="Target",
        delay=0.30,
    )

    if target_type in ("Local Directory", "Demo Repository"):

        directory = manager.prepare_local(target)

    elif target_type == "GitHub Repository":

        directory = manager.prepare_github(target)

    else:

        raise ValueError(
            f"Unsupported assessment target: {target_type}"
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
