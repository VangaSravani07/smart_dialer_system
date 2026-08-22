from models import Agent, Borrower
from dialer import SmartDialer


dialer = SmartDialer()

# Add agents
dialer.add_agent(
    Agent("A001", "Agent 1")
)

dialer.add_agent(
    Agent("A002", "Agent 2")
)

# Add borrowers
dialer.add_borrower(
    Borrower(
        "B001",
        "John",
        "9876543210"
    )
)

dialer.add_borrower(
    Borrower(
        "B002",
        "Sarah",
        "9876543211"
    )
)

# Create calls
call1 = dialer.create_call("B001")
call2 = dialer.create_call("B002")

print("Calls created:")
print(call1)
print(call2)

# Allocate calls
allocations = dialer.allocate_calls()

print("\nAllocations:")

for agent, call in allocations:

    print(
        f"{agent.name} -> {call.call_id}"
    )

    dialer.initiate_call(
        agent,
        call
    )

print("\nFinal call states:")

for call in dialer.calls.values():

    print(
        call.call_id,
        "->",
        call.state.value
    )