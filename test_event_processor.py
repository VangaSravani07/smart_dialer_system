from models import Call, CallState
from event_processor import EventProcessor


processor = EventProcessor()

call = Call("C001", "B001")

# First event
processor.process_event(
    "E001",
    CallState.INITIATED,
    call
)

# Duplicate event
processor.process_event(
    "E001",
    CallState.INITIATED,
    call
)

# Out-of-order event
processor.process_event(
    "E002",
    CallState.QUEUED,
    call
)

print("Final call state:", call.state.value)