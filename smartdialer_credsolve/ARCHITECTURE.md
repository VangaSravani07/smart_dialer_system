# SmartDialer Architecture Decision Document

## 1. Objective

The objective of SmartDialer is to improve agent utilization while maintaining safe outbound calling.

The system supports both Progressive and Predictive dialing.

The Predictive Pacing Engine can recommend how many calls should be started, but it cannot directly place calls. Every call must pass through the Safety Controller.

---

## 2. High-Level Architecture

```text
Campaign / Borrower Queue
          |
          v
   Pacing Engine
 Progressive / Predictive
          |
          v
  Safety Controller
          |
          v
   Call Allocator
          |
          v
 Telecom Provider
 Provider A / Provider B
          |
          v
   Event Processor
          |
          v
 Agent / Call State

The Safety Controller is the mandatory safety boundary between the pacing logic and telecom providers.

3. Progressive Dialing

Progressive dialing follows a simple rule:

One available agent → One outbound call

This provides predictable and safe behavior.

The system does not start more agent-bound calls than the available safe capacity.

4. Predictive Dialing

Predictive dialing attempts to improve agent utilization by estimating how many calls can safely be started.

The pacing calculation can consider:

Available agents
Current calls
Calls already ringing
Historical answer rate
Average call duration
Provider health

The Predictive Pacing Engine only makes a recommendation.

Example:

Predictive Engine
      |
      | Request: 15 calls
      v
Safety Controller
      |
      | Approve: 5 calls
      v
Call Allocator
      |
      v
Telecom Provider

This prevents the predictive logic from bypassing the safety mechanism.

5. Safety Controller

The Safety Controller is the main safety boundary.

It checks whether calls can actually be started based on current system conditions.

It can:

Approve calls
Reject calls
Limit the number of calls
Reserve agents
Release agents after failures

Even if the predictive engine requests a large number of calls, the Safety Controller has final authority.

The main design principle is:

Predictive logic can recommend. The Safety Controller decides.

6. Agent Allocation

Agents have explicit states such as:

OFFLINE
AVAILABLE
RESERVED
DIALING
CONNECTED
WRAP_UP
PAUSED

Before a call is started, an available agent is reserved.

In a production multi-worker system, agent reservation should be atomic.

For example:

UPDATE agents
SET state = 'RESERVED'
WHERE agent_id = ?
AND state = 'AVAILABLE';

Only the worker that successfully changes the state should own the reservation.

This prevents two workers from reserving the same agent.

7. Call State Management

Calls have explicit lifecycle states:

QUEUED
   ↓
RESERVED
   ↓
INITIATED
   ↓
RINGING
   ↓
ANSWERED
   ↓
CONNECTED
   ↓
COMPLETED

Failure and cancellation states are also supported.

Explicit states make it easier to handle provider events and failures safely.

8. Duplicate Events

Telecom providers may send the same event more than once.

The Event Processor keeps track of processed events.

For example:

E001 → INITIATED
E001 → INITIATED

The second event is treated as a duplicate and ignored.

This prevents duplicate events from causing repeated state transitions.

9. Out-of-Order Events

External systems may send events in an unexpected order.

For example:

COMPLETED
ANSWERED
RINGING

The Event Processor does not blindly apply these events.

Invalid backward transitions are rejected or ignored so that the call remains in a consistent state.

10. Provider Failure

The prototype contains two mock telecom providers.

If a provider fails during call setup:

The call is marked as FAILED.
The assigned agent is released.
The agent becomes AVAILABLE.
The system can continue processing other calls.

In a production system, provider health should also influence the pacing decision.

If provider failures increase, the dialer should reduce new call attempts.

11. Worker Crash Recovery

A production implementation should use reservation leases or timeouts.

Example:

Agent RESERVED
      ↓
Worker crashes
      ↓
Reservation becomes stale
      ↓
Recovery detects timeout
      ↓
Agent released

This prevents agents from remaining permanently stuck in the RESERVED state.

12. Provider Interface

The dialer communicates with telecom providers through a common provider interface.

This keeps provider-specific implementation details separate from the dialer.

It also makes it easier to:

Add another provider
Test failures
Switch providers
Simulate different provider behavior
13. Technology Choice

Python was selected because this assignment focuses on system design, correctness, and functional prototyping.

The prototype uses in-memory state to keep the implementation simple and easy to run locally.

A production implementation would require persistent storage and stronger concurrency controls.

14. Scalability

The current implementation is a small in-memory prototype.

At larger scale, likely bottlenecks include:

Concurrent agent reservations
Shared state
Event processing
Provider API throughput
Worker coordination

For a production system with thousands of agents, possible improvements include:

Transactional database
Distributed workers
Partitioned event processing
Provider-specific worker pools
Idempotent event consumers

Infrastructure should be introduced based on actual bottlenecks rather than added unnecessarily.

15. Key Trade-offs
Simplicity vs Production Complexity

The prototype avoids unnecessary infrastructure.

Benefit: Easy to understand, run, and test.

Trade-off: It does not provide all the durability and distributed concurrency guarantees of a production system.

Predictive Utilization vs Safety

Predictive dialing can improve agent utilization.

However, predictions can be wrong.

The Safety Controller therefore has final authority over call execution.

In-Memory State vs Persistent State

In-memory state keeps the prototype simple.

A production implementation would use durable storage so state can survive worker crashes and process restarts.

16. Future Improvements

If the system were taken toward production, the next improvements would be:

Persistent database-backed state
Atomic multi-worker agent reservation
Reservation leases and recovery
Provider circuit breakers
Retry and backoff policies
Persistent event storage
More advanced pacing metrics
Monitoring and alerting
Larger-scale load testing
Real telecom provider integration
17. Conclusion

SmartDialer combines the utilization benefits of predictive dialing with the deterministic safety characteristics of progressive dialing.

The key architectural principle is:

The pacing engine can suggest how aggressively to dial, but the Safety Controller always has final authority over whether calls can be started.