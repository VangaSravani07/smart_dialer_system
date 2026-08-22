from models import Agent, Borrower
from dialer import SmartDialer


dialer = SmartDialer()

# Add 2 agents
dialer.add_agent(Agent("A001", "Agent 1"))
dialer.add_agent(Agent("A002", "Agent 2"))

# Add 5 borrowers
for i in range(1, 6):

    borrower_id = f"B{i:03d}"

    dialer.add_borrower(
        Borrower(
            borrower_id,
            f"Borrower {i}",
            f"98765432{i:02d}"
        )
    )

    dialer.create_call(borrower_id)


print("Running Progressive Dialer...")

started = dialer.run_dialing_cycle("PROGRESSIVE")

print("Calls started:", len(started))

for call in started:
    print(call.call_id, "->", call.state.value)