# SmartDialer – Predictive & Progressive Calling System

## Overview

SmartDialer is a Python-based functional prototype designed to improve collection-agent utilization while maintaining safe outbound calling.

The system supports both Progressive and Predictive dialing. Predictive pacing can recommend how many calls to start, but every call must pass through the Safety Controller before reaching a telecom provider.

The prototype demonstrates:

- Agent allocation
- Call lifecycle management
- Progressive dialing
- Predictive pacing
- Safety controls
- Provider failures
- Duplicate events
- Out-of-order events
- Failure recovery
- Automated testing
- Load testing

---

## Architecture

The system follows this flow:

```text
Campaign / Borrower Queue
        ↓
Pacing Engine
(Progressive / Predictive)
        ↓
Safety Controller
        ↓
Call Allocator
        ↓
Telecom Provider
(Provider A / Provider B)
        ↓
Provider Events
        ↓
Event Processor
        ↓
Agent & Call State

The Pacing Engine cannot directly place a call.

The Safety Controller acts as an independent safety boundary and can approve, reduce, or reject dialing requests.

Architecture diagrams are available in the diagrams/ directory.

Main Components
models.py

Defines the core models:

Agent
Borrower
Call
Agent states
Call states
pacing_engine.py

Calculates dialing capacity for Progressive and Predictive modes.

safety_controller.py

Controls whether a call is safe to start based on agent availability and concurrent-call limits.

call_allocator.py

Assigns available agents to queued calls.

providers.py

Contains two mock telecom providers with different behavior and supports successful and failed call outcomes.

event_processor.py

Processes provider events and protects call state from duplicate and out-of-order events.

dialer.py

Integrates the pacing engine, safety controller, call allocator, providers, and event processor.

main.py

Runs the complete SmartDialer simulation.

simulation.py

Runs different dialing scenarios with different answer rates and reports safety and utilization results.

load_test.py

Runs a basic load test using multiple agents and calls.

Progressive Dialing

Progressive dialing follows a conservative approach:

One available agent → one outbound call

The system does not start more agent-bound calls than the available safe capacity.

This provides predictable behavior and reduces the risk of a borrower answering without an available agent.

Predictive Dialing

Predictive dialing attempts to improve agent utilization by estimating how many calls can safely be started.

The pacing logic can consider factors such as:

Available agents
Current calls
Calls already ringing
Historical answer rate
Call duration
Provider health

The predictive engine only produces a recommendation.

For example:
Predictive Engine
        ↓
Request: 15 calls
        ↓
Safety Controller
        ↓
Approve: 5 calls
        ↓
Call Allocator
        ↓
5 calls started
The Safety Controller ensures that predictive recommendations cannot bypass safety limits.

Safety and Failure Handling

The prototype is designed to handle unreliable external systems.

It considers:

Provider failures
Duplicate provider events
Out-of-order events
Failed call setup
Agent availability changes
Safe call limits
Call state consistency

The Safety Controller remains independent from the predictive pacing logic.

Mock Telecom Providers

Two mock providers are included:

Provider A
Fast
Reliable
Low failure rate
Provider B
Slower
Can simulate failures
Can simulate unreliable provider behavior

The dialer interacts through a provider interface so that provider-specific implementation details remain separate from the dialer.

Testing

The project contains unit and system tests covering:

Models
Call allocation
Dialer behavior
Dialing modes
Event processing
Failure handling
Pacing engine
Predictive dialing
Provider failures
Safety controller
End-to-end system behavior
Simulation

The scenario simulation tests different answer-rate conditions.

Example scenarios include:

Low answer rate: 20%
Medium answer rate: 50%
High answer rate: 70%

The simulation reports:

Calls initiated
Calls connected
Calls not connected
Agent utilization
Safety Controller decisions
Load Test

The load test simulates a larger workload with multiple agents and calls.

Example:
Agents: 50
Calls: 500
The purpose is to verify that the system respects safe dialing limits under higher load.

How to Run
Requirements
Python 3.10 or higher
No external packages required
Run the main simulation
python main.py
Run the scenario simulation
python simulation.py
Run the load test
python load_test.py
Run all tests
python -m unittest discover
Project Structure
smart_dialer_system/
│
├── models.py
├── dialer.py
├── pacing_engine.py
├── safety_controller.py
├── call_allocator.py
├── providers.py
├── event_processor.py
├── main.py
├── simulation.py
├── load_test.py
│
├── test_models.py
├── test_dialer.py
├── test_dialer_events.py
├── test_dialer_failure.py
├── test_dialing_mode.py
├── test_event_processor.py
├── test_failure_handling.py
├── test_pacing_engine.py
├── test_predictive_dialer.py
├── test_provider_failure.py
├── test_providers.py
├── test_run_dialing.py
├── test_safety_controller.py
├── test_call_allocator.py
├── test_system.py
│
├── diagrams/
│   ├── architecture.png
│   ├── agent_state_machine.png
│   └── call_state_machine.png
│
└── ARCHITECTURE.md
Design Principle

The main design principle is:

Predictive pacing can recommend more aggressive dialing, but deterministic safety controls always have the final decision.

This allows the system to obtain some of the utilization benefits of predictive dialing while retaining the safety characteristics of progressive dialing.

Future Improvements

For a production system, the prototype could be extended with:

Database-backed state management
Atomic agent reservation
Distributed locking
Provider health monitoring
Retry and backoff policies
Persistent event storage
Metrics and monitoring
Real telecom provider integration
Horizontal scaling for large agent volumes
Conclusion

SmartDialer demonstrates a practical approach to safe progressive and predictive dialing.

The design prioritizes correctness and safety before dialing aggressiveness, while keeping the system modular, testable, and easy to extend.
