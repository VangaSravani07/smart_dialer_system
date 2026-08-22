import time

from models import Agent, Borrower
from dialer import SmartDialer


def load_test():

    dialer = SmartDialer()

    # Allow up to 50 concurrent calls
    # for this load test
    dialer.safety_controller.max_concurrent_calls = 50

    # -------------------------
    # Create 50 agents
    # -------------------------

    for i in range(1, 51):

        dialer.add_agent(
            Agent(
                f"A{i:03d}",
                f"Agent {i}"
            )
        )

    # -------------------------
    # Create 500 borrowers
    # and calls
    # -------------------------

    for i in range(1, 501):

        borrower_id = f"B{i:03d}"

        dialer.add_borrower(
            Borrower(
                borrower_id,
                f"Borrower {i}",
                f"900000{i:04d}"
            )
        )

        dialer.create_call(
            borrower_id
        )

    # -------------------------
    # Show load size
    # -------------------------

    print("Agents:", len(dialer.agents))
    print("Calls:", len(dialer.calls))

    # -------------------------
    # Start timer
    # -------------------------

    start_time = time.time()

    # -------------------------
    # Run dialer
    # -------------------------

    started_calls = dialer.run_dialing_cycle(
        "PROGRESSIVE"
    )

    # -------------------------
    # End timer
    # -------------------------

    end_time = time.time()

    # -------------------------
    # Results
    # -------------------------

    print(
        "Calls started:",
        len(started_calls)
    )

    print(
        "Execution time:",
        round(
            end_time - start_time,
            4
        ),
        "seconds"
    )


if __name__ == "__main__":
    load_test()