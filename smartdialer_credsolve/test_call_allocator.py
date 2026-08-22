from models import Agent, Borrower, Call
from call_allocator import CallAllocator


agents = {
    "A001": Agent("A001", "Agent 1"),
    "A002": Agent("A002", "Agent 2")
}

calls = {
    "C001": Call("C001", "B001"),
    "C002": Call("C002", "B002")
}

allocator = CallAllocator()

allocations = allocator.allocate(agents, calls)

print("Number of allocations:", len(allocations))

for agent, call in allocations:
    print(
        f"{agent.name} -> {call.call_id} "
        f"-> {call.state.value}"
    )