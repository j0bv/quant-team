"""Message broker for inter-agent communication."""

import asyncio
from typing import Dict, Set, Callable, Awaitable, Optional
from .protocols import Message, MessageType, ErrorCode, create_error_message
import logging

logger = logging.getLogger(__name__)

class MessageBroker:
    """Central message broker for handling inter-agent communication."""
    
    def __init__(self):
        self._subscribers: Dict[MessageType, Set[Callable[[Message], Awaitable[None]]]] = {
            msg_type: set() for msg_type in MessageType
        }
        self._loop = asyncio.get_event_loop()

    async def publish(self, message: Message) -> None:
        """Publish a message to all subscribers of its type."""
        try:
            subscribers = self._subscribers[message.message_type]
            await asyncio.gather(
                *(subscriber(message) for subscriber in subscribers),
                return_exceptions=True
            )
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            raise

    def subscribe(
        self,
        message_type: MessageType,
        callback: Callable[[Message], Awaitable[None]]
    ) -> None:
        """Subscribe to messages of a specific type."""
        self._subscribers[message_type].add(callback)

    def unsubscribe(
        self,
        message_type: MessageType,
        callback: Callable[[Message], Awaitable[None]]
    ) -> None:
        """Unsubscribe from messages of a specific type."""
        self._subscribers[message_type].discard(callback)

# Global broker instance
broker = MessageBroker()
