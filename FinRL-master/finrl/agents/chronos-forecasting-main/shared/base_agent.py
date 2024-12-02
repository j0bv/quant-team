"""Base agent class for all FinRL agents."""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import uuid
import datetime
import logging

from .protocols import Message, MessageType, ErrorCode, create_error_message
from .broker import broker

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._setup_message_handlers()

    def _setup_message_handlers(self):
        """Setup message handlers for different message types."""
        broker.subscribe(MessageType.STRATEGY_REQUEST, self._handle_strategy_request)
        broker.subscribe(MessageType.DATA_REQUEST, self._handle_data_request)
        broker.subscribe(MessageType.ACTION_REQUEST, self._handle_action_request)

    async def send_message(
        self,
        message_type: MessageType,
        payload: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ) -> None:
        """Send a message through the broker."""
        message = Message(
            message_type=message_type,
            sender=self.agent_id,
            timestamp=datetime.datetime.utcnow(),
            message_id=str(uuid.uuid4()),
            correlation_id=correlation_id,
            payload=payload
        )
        await broker.publish(message)

    async def _handle_strategy_request(self, message: Message) -> None:
        """Handle incoming strategy requests."""
        try:
            if message.sender == self.agent_id:
                return
            response = await self.handle_strategy_request(message.payload)
            await self.send_message(
                MessageType.STRATEGY_RESPONSE,
                payload=response,
                correlation_id=message.message_id
            )
        except Exception as e:
            logger.error(f"Error handling strategy request: {str(e)}")
            await self.send_message(
                MessageType.ERROR,
                payload=create_error_message(
                    ErrorCode.STRATEGY_ERROR,
                    str(e),
                    self.agent_id,
                    message.message_id
                ).to_json()
            )

    async def _handle_data_request(self, message: Message) -> None:
        """Handle incoming data requests."""
        try:
            if message.sender == self.agent_id:
                return
            response = await self.handle_data_request(message.payload)
            await self.send_message(
                MessageType.DATA_RESPONSE,
                payload=response,
                correlation_id=message.message_id
            )
        except Exception as e:
            logger.error(f"Error handling data request: {str(e)}")
            await self.send_message(
                MessageType.ERROR,
                payload=create_error_message(
                    ErrorCode.DATA_NOT_AVAILABLE,
                    str(e),
                    self.agent_id,
                    message.message_id
                ).to_json()
            )

    async def _handle_action_request(self, message: Message) -> None:
        """Handle incoming action requests."""
        try:
            if message.sender == self.agent_id:
                return
            response = await self.handle_action_request(message.payload)
            await self.send_message(
                MessageType.ACTION_RESPONSE,
                payload=response,
                correlation_id=message.message_id
            )
        except Exception as e:
            logger.error(f"Error handling action request: {str(e)}")
            await self.send_message(
                MessageType.ERROR,
                payload=create_error_message(
                    ErrorCode.INVALID_REQUEST,
                    str(e),
                    self.agent_id,
                    message.message_id
                ).to_json()
            )

    @abstractmethod
    async def handle_strategy_request(
        self,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle strategy requests specific to the agent."""
        pass

    @abstractmethod
    async def handle_data_request(
        self,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle data requests specific to the agent."""
        pass

    @abstractmethod
    async def handle_action_request(
        self,
        payload: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Handle action requests specific to the agent."""
        pass
