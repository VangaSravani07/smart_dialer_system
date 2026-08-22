from models import Call, CallState
from dialer import SmartDialer


dialer = SmartDialer()

# Add a call directly
call = Call(
    call_id="C001",
    borrower_id="B001"
)

dialer.calls["C001"] = call


print("Processing first event:")

dialer.process_call_event(
    "E001",
    "C001",
    CallState.INITIATED
)

print("\nProcessing duplicate event:")

dialer.process_call_event(
    "E001",
    "C001",
    CallState.INITIATED
)

print("\nProcessing out-of-order event:")

dialer.process_call_event(
    "E002",
    "C001",
    CallState.QUEUED
)

print("\nFinal call state:",
      call.state.value)