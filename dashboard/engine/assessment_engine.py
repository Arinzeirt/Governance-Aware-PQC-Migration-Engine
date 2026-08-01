#
# Bootstrap Python Path
#
import engine.bootstrap

from engine.handlers import initialize
from engine.handlers import target
from engine.handlers import discovery
from engine.handlers import inventory
from engine.handlers import report

from engine.runtime import runtime

from engine.session import session
from engine.state_machine import state_machine


class AssessmentEngine:

    def run(

        self,

        target_type,

        target_path,

    ):

        runtime.reset()

        runtime.log("Enterprise Discovery Assessment Started")

        session.start(

            target_type,

            target_path,

        )

        #
        # INITIALIZING
        #

        runtime.log("Loading Assessment Configuration")

        state_machine.reset()

        session.transition(

            "INITIALIZING"

        )

        initialize.execute()

        runtime.log("Assessment Configuration Loaded")

        #
        # TARGET
        #

        runtime.log("Connecting Assessment Target")

        session.transition(

            "TARGET"

        )

        directory = target.execute(

            target_type,

            target_path,

        )

        runtime.log("Repository Connected Successfully")

        #
        # DISCOVERY
        #

        runtime.log("Beginning Cryptographic Discovery")

        session.transition(

            "DISCOVERY"

        )

        findings = discovery.execute(

            directory,

        )

        runtime.log("Cryptographic Discovery Completed")

        #
        # INVENTORY
        #

        runtime.log("Building Enterprise Inventory")

        session.transition(

            "INVENTORY"

        )

        inventory_data = inventory.execute(

            findings,

        )
        runtime.log("Enterprise Inventory Completed")
        #
        # REPORT
        #

        runtime.log("Generating Executive Migration Report")

        session.transition(

            "REPORT"

        )

        report.execute(

            inventory_data,

        )

        runtime.log("Executive Report Generated")

        #
        # COMPLETE
        #

        runtime.log("Enterprise Discovery Completed Successfully")

        session.complete()

        runtime.finish()

engine = AssessmentEngine()
