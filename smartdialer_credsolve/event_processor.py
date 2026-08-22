from models import CallState


class EventProcessor:

    EVENT_ORDER = {
        CallState.QUEUED: 0,
        CallState.RESERVED: 1,
        CallState.INITIATED: 2,
        CallState.RINGING: 3,
        CallState.ANSWERED: 4,
        CallState.CONNECTED: 5,
        CallState.COMPLETED: 6,
        CallState.FAILED: 6,
        CallState.CANCELLED: 6
    }

    def __init__(self):
        self.processed_events = set()

    def process_event(self, event_id, new_state, call):

        # Ignore duplicate events
        if event_id in self.processed_events:
            print(f"Duplicate event ignored: {event_id}")
            return False

        # Ignore events that move the call backwards
        current_order = self.EVENT_ORDER[call.state]
        new_order = self.EVENT_ORDER[new_state]

        if new_order < current_order:
            print(
                f"Out-of-order event ignored: "
                f"{event_id}"
            )
            return False

        self.processed_events.add(event_id)

        call.state = new_state

        print(
            f"Event processed: {event_id} "
            f"-> {new_state.value}"
        )

        return True