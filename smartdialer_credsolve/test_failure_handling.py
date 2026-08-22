from models import Agent, Call
from models import AgentState, CallState
from safety_controller import SafetyController


controller = SafetyController()

agent = Agent("A001", "Agent 1")
call = Call("C001", "B001")

# Reserve agent
controller.reserve_agent(
    agent,
    call.call_id
)

print("Before failure:")
print("Agent:", agent.state.value)
print("Call:", call.state.value)

# Simulate failure
controller.mark_call_failed(
    agent,
    call
)

print("\nAfter failure:")
print("Agent:", agent.state.value)
print("Call:", call.state.value)