from models import AgentState, CallState


class CallAllocator:

    def allocate(self, agents, calls):

        available_agents = [
            agent for agent in agents.values()
            if agent.state == AgentState.AVAILABLE
        ]

        queued_calls = [
            call for call in calls.values()
            if call.state == CallState.QUEUED
        ]

        allocations = []

        for agent, call in zip(available_agents, queued_calls):

            agent.state = AgentState.RESERVED
            agent.current_call_id = call.call_id

            call.agent_id = agent.agent_id
            call.state = CallState.RESERVED

            allocations.append((agent, call))

        return allocations