from scanner import scan_directory

from engine.runtime import runtime


DISCOVERY_START = 35
DISCOVERY_END = 65


def scanner_callback(**event):

    #
    # File Progress
    #

    if event["event"] == "file":

        runtime.update_scan(

            file=event["file"],

            current=event["current"],

            total=event["total"],

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

    #
    # Keyword Discovery
    #

    elif event["event"] == "keyword":

        runtime.add_discovery(

            title=event["keyword"],

            file=event["file"],

            severity="High",

        )

        runtime.log(

            f"{event['keyword']} detected"

        )

    #
    # Classification
    #

    elif event["event"] == "classification":

        runtime.add_discovery(

            title=event["classification"],

            file=event["file"],

            severity="Medium",

        )

        runtime.log(

            f"{event['classification']} classified"

        )


def execute(directory):

    runtime.emit(

        "Cryptographic discovery started",

        progress=35,

        stage="Discovery",

    )

    findings = scan_directory(

        directory,

        callback=scanner_callback,

    )

    runtime.emit(

        f"Discovery completed ({len(findings)} assets)",

        progress=65,

        stage="Discovery",

    )

    return findings

