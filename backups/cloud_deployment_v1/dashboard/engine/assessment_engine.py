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

        runtime.log("ENGINE START")

        session.start(

            target_type,

            target_path,

        )

        #
        # INITIALIZING
        #

        runtime.log("ENTER INITIALIZE")

        state_machine.reset()

        session.transition(

            "INITIALIZING"

        )

        initialize.execute()

        runtime.log("EXIT INITIALIZE")

        #
        # TARGET
        #

        runtime.log("ENTER TARGET")

        session.transition(

            "TARGET"

        )

        directory = target.execute(

            target_type,

            target_path,

        )

        runtime.log("EXIT TARGET")

        #
        # DISCOVERY
        #

        runtime.log("ENTER DISCOVERY")

        session.transition(

            "DISCOVERY"

        )

        findings = discovery.execute(

            directory,

        )

        runtime.log("EXIT DISCOVERY")

        #
        # INVENTORY
        #

        runtime.log("ENTER INVENTORY")

        session.transition(

            "INVENTORY"

        )

        inventory_data = inventory.execute(

            findings,

        )

        runtime.log("EXIT INVENTORY")

        #
        # REPORT
        #

        runtime.log("ENTER REPORT")

        session.transition(

            "REPORT"

        )

        report.execute(

            inventory_data,

        )

        runtime.log("EXIT REPORT")

        #
        # COMPLETE
        #

        runtime.log("ENGINE COMPLETE")

        session.complete()

        runtime.finish()


engine = AssessmentEngine()
