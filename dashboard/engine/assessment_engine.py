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

        #
        # Reset Runtime
        #

        runtime.reset()

        #
        # Create Session
        #

        session.start(

            target_type,

            target_path,

        )

        #
        # INITIALIZING
        #

        state_machine.reset()

        session.transition(

            "INITIALIZING"

        )

        initialize.execute()

        #
        # TARGET
        #

        session.transition(

            "TARGET"

        )

        directory = target.execute(

            target_type,

            target_path,

        )

        #
        # DISCOVERY
        #

        session.transition(

            "DISCOVERY"

        )

        findings = discovery.execute(

            directory,

        )

        #
        # INVENTORY
        #

        session.transition(

            "INVENTORY"

        )

        inventory_data = inventory.execute(

            findings,

        )

        #
        # REPORT
        #

        session.transition(

            "REPORT"

        )

        report.execute(

            inventory_data,

        )

        #
        # COMPLETE
        #

        session.complete()

        runtime.finish()


engine = AssessmentEngine()

