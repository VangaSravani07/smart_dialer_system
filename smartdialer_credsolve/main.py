from models import (
    Agent,
    Borrower,
    CallState
)

from dialer import SmartDialer


def main():

    print("=" * 50)
    print("SMART DIALER SIMULATION")
    print("=" * 50)

    # --------------------------------
    # Create Smart Dialer
    # --------------------------------

    dialer = SmartDialer()

    # --------------------------------
    # Add Agents
    # --------------------------------

    dialer.add_agent(
        Agent("A001", "Agent 1")
    )

    dialer.add_agent(
        Agent("A002", "Agent 2")
    )

    dialer.add_agent(
        Agent("A003", "Agent 3")
    )

    # --------------------------------
    # Add Borrowers
    # --------------------------------

    borrowers = [
        ("B001", "John", "9876543210"),
        ("B002", "Sarah", "9876543211"),
        ("B003", "Mike", "9876543212"),
        ("B004", "Emma", "9876543213"),
        ("B005", "David", "9876543214")
    ]

    for borrower_id, name, phone in borrowers:

        dialer.add_borrower(
            Borrower(
                borrower_id,
                name,
                phone
            )
        )

        dialer.create_call(
            borrower_id
        )

    # --------------------------------
    # Show initial state
    # --------------------------------

    print("\nInitial Calls:")

    for call in dialer.calls.values():

        print(
            call.call_id,
            "->",
            call.state.value
        )

    # --------------------------------
    # Run Progressive Dialer
    # --------------------------------

    print("\nRunning Progressive Dialer...")

    started_calls = dialer.run_dialing_cycle(
        "PROGRESSIVE"
    )

    print(
        "\nCalls started:",
        len(started_calls)
    )

    # --------------------------------
    # Process call events
    # --------------------------------

    print("\nProcessing call events...")

    event_number = 1

    for call in started_calls:

        dialer.process_call_event(
            f"E{event_number:03d}",
            call.call_id,
            CallState.CONNECTED
        )

        event_number += 1

    # --------------------------------
    # Complete calls
    # --------------------------------

    print("\nCompleting calls...")

    for call in started_calls:

        agent = dialer.agents[
            call.agent_id
        ]

        dialer.safety_controller.mark_call_completed(
            agent,
            call
        )

    # --------------------------------
    # Final state
    # --------------------------------

    print("\nFinal Call States:")

    for call in dialer.calls.values():

        print(
            call.call_id,
            "->",
            call.state.value
        )

    print("\nFinal Agent States:")

    for agent in dialer.agents.values():

        print(
            agent.agent_id,
            "->",
            agent.state.value
        )

    print("\n" + "=" * 50)
    print("SIMULATION COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()