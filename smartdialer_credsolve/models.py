from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class AgentState(Enum):
    OFFLINE = "OFFLINE"
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    DIALING = "DIALING"
    CONNECTED = "CONNECTED"
    WRAP_UP = "WRAP_UP"
    PAUSED = "PAUSED"


class CallState(Enum):
    QUEUED = "QUEUED"
    RESERVED = "RESERVED"
    INITIATED = "INITIATED"
    RINGING = "RINGING"
    ANSWERED = "ANSWERED"
    CONNECTED = "CONNECTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class Borrower:
    borrower_id: str
    name: str
    phone_number: str
    priority: int = 1


@dataclass
class Agent:
    agent_id: str
    name: str
    state: AgentState = AgentState.AVAILABLE
    current_call_id: Optional[str] = None


@dataclass
class Call:
    call_id: str
    borrower_id: str
    agent_id: Optional[str] = None
    state: CallState = CallState.QUEUED
    provider: Optional[str] = None
    created_at: Optional[datetime] = None