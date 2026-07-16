from collections import deque


class RuntimeEventBus:

    def __init__(self):

        self.reset()

    def reset(self):

        self.events = deque(maxlen=500)

    def publish(

        self,

        event,

        **payload,

    ):

        self.events.append(

            {

                "event": event,

                "payload": payload,

            }

        )

    def consume(self):

        while self.events:

            yield self.events.popleft()


bus = RuntimeEventBus()

