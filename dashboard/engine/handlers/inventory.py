from inventory import save_inventory

from engine.runtime import runtime


def execute(findings):

    runtime.emit(

        "Building Cryptographic Inventory...",

        progress=70,

        stage="Inventory",

    )

    inventory = save_inventory(findings)

    runtime.update_statistics(

        inventory=len(inventory),

    )

    runtime.emit(

        f"Inventory Created ({len(inventory)} records)",

        progress=82,

    )

    return inventory

