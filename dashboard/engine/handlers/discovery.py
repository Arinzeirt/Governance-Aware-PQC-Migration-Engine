from scanner import scan_directory

from engine.runtime import runtime


DISCOVERY_START = 35
DISCOVERY_END = 65


def scanner_callback(**event):

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

        runtime.progress = int(progress)

    elif event["event"] == "keyword":

        runtime.add_discovery(

            title=event["keyword"],

            file=event["file"],

            severity="High",

        )

        runtime.log(

            f"{event['keyword']} detected"

        )

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

    runtime.stage = "Discovery"

    runtime.log(

        "Cryptographic discovery started"

    )

    findings = scan_directory(

        directory,

        callback=scanner_callback,

    )

    runtime.log(

        f"Discovery completed ({len(findings)} assets)"

    )

    return findings

