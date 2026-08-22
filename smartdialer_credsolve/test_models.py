from models import Agent, Borrower, Call


agent = Agent("A001", "Agent 1")
borrower = Borrower("B001", "John", "9876543210")
call = Call("C001", "B001")


print(agent)
print(borrower)
print(call)