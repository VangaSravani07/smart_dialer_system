from models import Agent, Borrower
from dialer import SmartDialer
from providers import MockProviderA


dialer = SmartDialer()

# Add agent
agent = Agent(
    "A001",
    "Agent 1"
)

dialer.add_agent(agent)

# Add borrower
borrower = Borrower(
    "B001",
    "John",
    "9876543210"
)

dialer.add_borrower(borrower)

# Create call
call = dialer.create_call("B001")

# Force Provider A to fail
dialer.providers[0] = MockProviderA(
    should_fail=True
)

print("Starting failed call...\n")

result = dialer.run_dialing_cycle(
    "PROGRESSIVE"
)

print("\nCalls successfully started:",
      len(result))

print(
    "Final call state:",
    call.state.value
)

print(
    "Final agent state:",
    agent.state.value
)