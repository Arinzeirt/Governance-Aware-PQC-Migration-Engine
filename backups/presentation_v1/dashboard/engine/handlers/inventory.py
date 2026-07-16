from inventory import save_inventory

from engine.runtime import runtime
from engine.stage import transition


def execute(findings):

    transition(

        message="Building Cryptographic Inventory...",

        progress=80,

        stage="Inventory",

        delay=0.35,

    )

    inventory = save_inventory(findings)

    runtime.update_statistics(

        inventory=len(inventory),

    )

    transition(

        message=f"Inventory Created ({len(inventory)} records)",

        progress=88,

        stage="Inventory",

        delay=0.35,

    )

    return inventory

