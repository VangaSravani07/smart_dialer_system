from models import Agent, Borrower
from dialer import SmartDialer


dialer = SmartDialer()

# Add 2 agents
dialer.add_agent(
    Agent("A001", "Agent 1")
)

dialer.add_agent(
    Agent("A002", "Agent 2")
)

# Add 5 borrowers
for i in range(1, 6):

    dialer.add_borrower(
        Borrower(
            f"B{i:03d}",
            f"Borrower {i}",
            f"98765432{i:02d}"
        )
    )

    dialer.create_call(f"B{i:03d}")


progressive = dialer.calculate_dialing_capacity(
    "PROGRESSIVE"
)

predictive = dialer.calculate_dialing_capacity(
    "PREDICTIVE"
)

print("Progressive capacity:", progressive)
print("Predictive capacity:", predictive)