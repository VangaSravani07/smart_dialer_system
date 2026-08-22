from models import AgentState, CallState


class SafetyController:

    def __init__(self, max_concurrent_calls=5):
        self.max_concurrent_calls = max_concurrent_calls

    def can_start_call(self, agent, active_calls):

        if agent.state not in [
            AgentState.AVAILABLE,
            AgentState.RESERVED
        ]:
            return False

        active_count = sum(
            1
            for call in active_calls.values()
            if call.state in [
                CallState.INITIATED,
                CallState.RINGING,
                CallState.ANSWERED,
                CallState.CONNECTED
            ]
        )

        if active_count >= self.max_concurrent_calls:
            return False

        return True

    def reserve_agent(self, agent, call_id):

        if agent.state != AgentState.AVAILABLE:
            return False

        agent.state = AgentState.RESERVED
        agent.current_call_id = call_id

        return True

    def release_agent(self, agent):

        agent.state = AgentState.AVAILABLE
        agent.current_call_id = None

    def mark_call_failed(self, agent, call):

        call.state = CallState.FAILED

        self.release_agent(agent)

        print(
            f"Call {call.call_id} failed. "
            f"Agent {agent.agent_id} is available again."
        )

    def mark_call_completed(self, agent, call):

        call.state = CallState.COMPLETED

        self.release_agent(agent)

        print(
            f"Call {call.call_id} completed. "
            f"Agent {agent.agent_id} is available again."
        )

    def validate_call(self, call):

        if call.state in [
            CallState.COMPLETED,
            CallState.FAILED,
            CallState.CANCELLED
        ]:
            return False

        return True