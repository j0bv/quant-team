"""Protocol definitions for inter-agent communication."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any
from enum import Enum
import json
import datetime

class MessageType(Enum):
    """Types of messages that can be exchanged between agents."""
    STRATEGY_REQUEST = "strategy_request"
    STRATEGY_RESPONSE = "strategy_response"
    DATA_REQUEST = "data_request"
    DATA_RESPONSE = "data_response"
    ACTION_REQUEST = "action_request"
    ACTION_RESPONSE = "action_response"
    ERROR = "error"

class ErrorCode(Enum):
    """Standard error codes for agent communication."""
    INVALID_MESSAGE = "invalid_message"
    INVALID_REQUEST = "invalid_request"
    DATA_NOT_AVAILABLE = "data_not_available"
    STRATEGY_ERROR = "strategy_error"
    INTERNAL_ERROR = "internal_error"

@dataclass
class Message:
    """Base message format for all agent communications."""
    message_type: MessageType
    sender: str
    timestamp: datetime.datetime
    message_id: str
    correlation_id: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps({
            "message_type": self.message_type.value,
            "sender": self.sender,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "correlation_id": self.correlation_id,
            "payload": self.payload,
            "error": self.error
        })

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """Create message from JSON string."""
        data = json.loads(json_str)
        return cls(
            message_type=MessageType(data["message_type"]),
            sender=data["sender"],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            message_id=data["message_id"],
            correlation_id=data.get("correlation_id"),
            payload=data.get("payload"),
            error=data.get("error")
        )

def create_error_message(
    error_code: ErrorCode,
    error_message: str,
    sender: str,
    correlation_id: Optional[str] = None
) -> Message:
    """Create a standardized error message."""
    return Message(
        message_type=MessageType.ERROR,
        sender=sender,
        timestamp=datetime.datetime.utcnow(),
        message_id=f"error_{datetime.datetime.utcnow().timestamp()}",
        correlation_id=correlation_id,
        error={
            "code": error_code.value,
            "message": error_message
        }
    )
