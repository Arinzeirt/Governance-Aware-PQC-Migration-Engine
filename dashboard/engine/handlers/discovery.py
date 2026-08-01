from pathlib import Path

from scanner import scan_directory

from engine.runtime import runtime


DISCOVERY_START = 35
DISCOVERY_END = 65


def scanner_callback(**event):

    #
    # Discovery Started
    #

    if event["event"] == "scan_started":

        runtime.log(

            f"{event['total']} supported source files identified"

        )

        runtime.log(

            "Beginning enterprise cryptographic analysis"

        )

        return

    #
    # File Progress
    #

    if event["event"] == "file":

        runtime.update_scan(

            file=event["file"],

            current=event["current"],

            total=event["total"],

        )

        #
        # Milestone updates
        #

        if event["current"] == 1:

            runtime.log(

                "Scanning source code"

            )

        elif event["current"] % 50 == 0:

            runtime.log(

                f"{event['current']} files analysed"

            )

        #
        # Entering a new directory
        #

        parent = Path(event["file"]).parent.name

        if parent:

            runtime.emit(

                f"Scanning {parent}/",

                progress=None,

                stage="Discovery",

                log=False,

            )

        progress = DISCOVERY_START + (

            (event["current"] / event["total"])

            * (DISCOVERY_END - DISCOVERY_START)

        )

        runtime.emit(

            "",

            progress=int(progress),

            stage="Discovery",

            log=False,

        )

        return

    #
    # Keyword Discovery
    #

    if event["event"] == "keyword":

        runtime.add_discovery(

            title=event["keyword"],

            file=event["file"],

            severity="High",

        )

        runtime.log(

            f"{event['keyword']} detected"

        )

        return

    #
    # Classification
    #

    if event["event"] == "classification":

        runtime.add_discovery(

            title=event["classification"],

            file=event["file"],

            severity="Medium",

        )

        runtime.log(

            f"{event['classification']} classified"

        )

        return


def execute(directory):

    runtime.emit(

        "Preparing cryptographic discovery",

        progress=30,

        stage="Discovery",

    )

    runtime.log(

        "Enumerating repository structure"

    )

    runtime.log(

        "Identifying supported source files"

    )

    runtime.log(

        "Building discovery workspace"

    )

    runtime.emit(

        "Cryptographic discovery started",

        progress=35,

        stage="Discovery",

    )

    findings = scan_directory(

        directory,

        callback=scanner_callback,

    )

    runtime.log(

        "Building enterprise inventory"

    )

    runtime.emit(

        f"Discovery completed ({len(findings)} assets)",

        progress=65,

        stage="Discovery",

    )

    return findings
