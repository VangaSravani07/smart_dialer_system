import random

from dialer import SmartDialer
from models import Agent, Borrower


def run_scenario(name, answer_rate):
    print("\n" + "=" * 60)
    print(f"SCENARIO: {name}")
    print(f"Answer Rate: {answer_rate * 100:.0f}%")
    print("=" * 60)

    # Create a fresh dialer for every scenario
    dialer = SmartDialer()

    # 10 agents
    for i in range(1, 11):
        dialer.add_agent(
            Agent(
                agent_id=f"A{i:03d}",
                name=f"Agent {i}"
            )
        )

    # 20 borrowers
    for i in range(1, 21):
        borrower = Borrower(
            borrower_id=f"B{i:03d}",
            name=f"Borrower {i}",
            phone_number=f"90000000{i:02d}",
            priority=1
        )

        dialer.add_borrower(borrower)
        dialer.create_call(borrower.borrower_id)

    # Run predictive dialing
    started_calls = dialer.run_dialing_cycle("PREDICTIVE")

    initiated = len(started_calls)

    # Simulate borrower answers using the selected answer rate
    random.seed(42)

    connected = 0

    for call in started_calls:

        random_value = random.random()

        if random_value < answer_rate:
            connected += 1

    not_connected = initiated - connected

    utilization = (
        connected / len(dialer.agents)
    ) * 100 if dialer.agents else 0

    print("\nRESULTS")
    print("-" * 60)

    print(f"Agents available initially: {len(dialer.agents)}")
    print(f"Calls initiated: {initiated}")
    print(f"Calls connected: {connected}")
    print(f"Calls not connected: {not_connected}")
    print(f"Estimated agent utilization: {utilization:.1f}%")

    print("\nSafety Controller")
    print("-" * 60)
    print(
        f"Maximum safe calls allowed: {len(dialer.agents)}"
    )
    print(
        f"Calls actually initiated: {initiated}"
    )

    if initiated <= len(dialer.agents):
        print("Safety result: PASS")
    else:
        print("Safety result: FAIL")


if __name__ == "__main__":

    run_scenario(
        "A - Low Answer Rate",
        0.20
    )

    run_scenario(
        "B - Medium Answer Rate",
        0.50
    )

    run_scenario(
        "C - High Answer Rate",
        0.70
    )