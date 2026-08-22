from models import Agent, Call
from safety_controller import SafetyController


controller = SafetyController(max_concurrent_calls=2)

agent = Agent("A001", "Agent 1")
call = Call("C001", "B001")

print("Can start call:",
      controller.can_start_call(agent, {}))
      
        

print("Reserve agent:",
      controller.reserve_agent(agent, call.call_id))

print("Agent after reservation:",
      agent)

controller.release_agent(agent)

print("Agent after release:",
      agent)