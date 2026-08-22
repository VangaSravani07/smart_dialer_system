from datetime import datetime

from models import (
    Agent,
    Borrower,
    Call,
    AgentState,
    CallState
)

from pacing_engine import PacingEngine
from safety_controller import SafetyController
from call_allocator import CallAllocator
from providers import (
    MockProviderA,
    MockProviderB,
    ProviderResult
)
from event_processor import EventProcessor


class SmartDialer:

    def __init__(self):

        self.agents = {}
        self.borrowers = {}
        self.calls = {}

        self.pacing_engine = PacingEngine()
        self.safety_controller = SafetyController()
        self.call_allocator = CallAllocator()

        self.providers = [
            MockProviderA(),
            MockProviderB()
        ]

        self.event_processor = EventProcessor()

    # -------------------------
    # Add agent
    # -------------------------

    def add_agent(self, agent):

        self.agents[agent.agent_id] = agent

    # -------------------------
    # Add borrower
    # -------------------------

    def add_borrower(self, borrower):

        self.borrowers[borrower.borrower_id] = borrower

    # -------------------------
    # Create call
    # -------------------------

    def create_call(self, borrower_id):

        call_id = f"C{len(self.calls) + 1:03d}"

        call = Call(
            call_id=call_id,
            borrower_id=borrower_id,
            state=CallState.QUEUED,
            created_at=datetime.now()
        )

        self.calls[call_id] = call

        return call

    # -------------------------
    # Allocate calls
    # -------------------------

    def allocate_calls(self):

        return self.call_allocator.allocate(
            self.agents,
            self.calls
        )

    # -------------------------
    # Calculate dialing capacity
    # -------------------------

    def calculate_dialing_capacity(self, mode):

        available_agents = sum(
            1
            for agent in self.agents.values()
            if agent.state == AgentState.AVAILABLE
        )

        queued_borrowers = sum(
            1
            for call in self.calls.values()
            if call.state == CallState.QUEUED
        )

        if mode.upper() == "PROGRESSIVE":

            return self.pacing_engine.calculate_progressive_calls(
                available_agents,
                queued_borrowers
            )

        elif mode.upper() == "PREDICTIVE":

            return self.pacing_engine.calculate_predictive_calls(
                available_agents,
                queued_borrowers
            )

        else:

            raise ValueError(
                "Mode must be PROGRESSIVE or PREDICTIVE"
            )

    # -------------------------
    # Run dialing cycle
    # -------------------------

    def run_dialing_cycle(self, mode):

        capacity = self.calculate_dialing_capacity(mode)

        queued_calls = [
            call
            for call in self.calls.values()
            if call.state == CallState.QUEUED
        ]

        available_agents = [
            agent
            for agent in self.agents.values()
            if agent.state == AgentState.AVAILABLE
        ]

        started_calls = []

        for agent, call in zip(
            available_agents,
            queued_calls[:capacity]
        ):

            agent.state = AgentState.RESERVED
            agent.current_call_id = call.call_id

            call.agent_id = agent.agent_id
            call.state = CallState.RESERVED

            if self.initiate_call(agent, call):

                started_calls.append(call)

        return started_calls

    # -------------------------
    # Initiate call
    # -------------------------

    def initiate_call(self, agent, call):

        if not self.safety_controller.can_start_call(
            agent,
            self.calls
        ):

            print(
                f"Safety check failed for {call.call_id}"
            )

            return False

        borrower = self.borrowers[
            call.borrower_id
        ]

        agent.state = AgentState.DIALING
        call.state = CallState.INITIATED

        provider = self.providers[0]

        result = provider.initiate_call(
            borrower.phone_number
        )

        # Successful call
        if result == ProviderResult.SUCCESS:

            call.provider = "ProviderA"
            call.state = CallState.RINGING

            print(
                f"{call.call_id} is now RINGING"
            )

            return True

        # Failed call
        self.safety_controller.mark_call_failed(
            agent,
            call
        )

        return False

    # -------------------------
    # Process call event
    # -------------------------

    def process_call_event(
        self,
        event_id,
        call_id,
        new_state
    ):

        if call_id not in self.calls:

            print(
                f"Call not found: {call_id}"
            )

            return False

        call = self.calls[call_id]

        return self.event_processor.process_event(
            event_id,
            new_state,
            call
        )