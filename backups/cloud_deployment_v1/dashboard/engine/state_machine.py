from engine.session import session


class AssessmentStateMachine:

    STATES = [

        "INITIALIZING",

        "TARGET",

        "DISCOVERY",

        "INVENTORY",

        "REPORT",

        "COMPLETED",

    ]

    def next(self):

        if session.state not in self.STATES:

            return

        index = self.STATES.index(

            session.state

        )

        if index < len(self.STATES)-1:

            session.transition(

                self.STATES[index+1]

            )

    def current(self):

        return session.state

    def reset(self):

        session.reset()


state_machine = AssessmentStateMachine()

