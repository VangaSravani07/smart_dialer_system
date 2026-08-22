import unittest

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
from event_processor import EventProcessor


class TestPacingEngine(unittest.TestCase):

    def test_progressive(self):

        engine = PacingEngine()

        result = engine.calculate_progressive_calls(
            3,
            10
        )

        self.assertEqual(result, 3)

    def test_predictive(self):

        engine = PacingEngine()

        result = engine.calculate_predictive_calls(
            3,
            10
        )

        self.assertEqual(result, 6)


class TestSafetyController(unittest.TestCase):

    def test_reserve_and_release(self):

        controller = SafetyController()

        agent = Agent(
            "A001",
            "Agent 1"
        )

        result = controller.reserve_agent(
            agent,
            "C001"
        )

        self.assertTrue(result)
        self.assertEqual(
            agent.state,
            AgentState.RESERVED
        )

        controller.release_agent(agent)

        self.assertEqual(
            agent.state,
            AgentState.AVAILABLE
        )


class TestCallAllocator(unittest.TestCase):

    def test_allocation(self):

        agents = {
            "A001": Agent("A001", "Agent 1")
        }

        calls = {
            "C001": Call("C001", "B001")
        }

        allocator = CallAllocator()

        result = allocator.allocate(
            agents,
            calls
        )

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            calls["C001"].state,
            CallState.RESERVED
        )


class TestEventProcessor(unittest.TestCase):

    def test_duplicate_event(self):

        processor = EventProcessor()

        call = Call(
            "C001",
            "B001"
        )

        first = processor.process_event(
            "E001",
            CallState.INITIATED,
            call
        )

        second = processor.process_event(
            "E001",
            CallState.INITIATED,
            call
        )

        self.assertTrue(first)
        self.assertFalse(second)

    def test_out_of_order_event(self):

        processor = EventProcessor()

        call = Call(
            "C001",
            "B001"
        )

        processor.process_event(
            "E001",
            CallState.INITIATED,
            call
        )

        result = processor.process_event(
            "E002",
            CallState.QUEUED,
            call
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()