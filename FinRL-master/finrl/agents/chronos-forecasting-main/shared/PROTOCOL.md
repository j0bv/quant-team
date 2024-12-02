# Agent Communication Protocol

This document outlines the communication protocols for agents in the FinRL system.

## Message Format

All messages follow a standardized format:

```python
{
    "message_type": str,  # Type of message (see MessageType enum)
    "sender": str,        # ID of the sending agent
    "timestamp": str,     # ISO format timestamp
    "message_id": str,    # Unique message identifier
    "correlation_id": str,# Optional: ID of related message
    "payload": dict,      # Optional: Message content
    "error": dict        # Optional: Error information
}
```

## Message Types

1. **STRATEGY_REQUEST/RESPONSE**
   - Used for requesting and sharing trading strategies
   - Example payload:
     ```python
     {
         "market": "NASDAQ",
         "symbols": ["AAPL", "GOOGL"],
         "timeframe": "1d",
         "strategy_params": {...}
     }
     ```

2. **DATA_REQUEST/RESPONSE**
   - Used for requesting market data
   - Example payload:
     ```python
     {
         "symbols": ["AAPL"],
         "start_date": "2023-01-01",
         "end_date": "2023-12-31",
         "timeframe": "1d",
         "indicators": ["MA", "RSI"]
     }
     ```

3. **ACTION_REQUEST/RESPONSE**
   - Used for requesting trading actions
   - Example payload:
     ```python
     {
         "symbol": "AAPL",
         "action": "BUY",
         "quantity": 100,
         "price": 150.00,
         "timestamp": "2023-12-31T23:59:59Z"
     }
     ```

4. **ERROR**
   - Used for error reporting
   - Example payload:
     ```python
     {
         "code": "invalid_request",
         "message": "Invalid strategy parameters"
     }
     ```

## Error Handling

Standard error codes:
- `INVALID_MESSAGE`: Malformed message
- `INVALID_REQUEST`: Invalid request parameters
- `DATA_NOT_AVAILABLE`: Requested data not available
- `STRATEGY_ERROR`: Error in strategy execution
- `INTERNAL_ERROR`: Internal agent error

## Usage Guidelines

1. **Message Flow**
   - Always include a `message_id` for tracking
   - Use `correlation_id` to link related messages
   - Handle all responses asynchronously

2. **Best Practices**
   - Validate message format before processing
   - Include appropriate error handling
   - Log all communication for debugging
   - Use appropriate timeouts for requests

3. **Security**
   - Validate message sources
   - Sanitize all input data
   - Handle sensitive data appropriately

## Implementation

1. **Base Agent Class**
   - Inherit from `BaseAgent` class
   - Implement required handler methods:
     - `handle_strategy_request`
     - `handle_data_request`
     - `handle_action_request`

2. **Message Broker**
   - Use the global `broker` instance for communication
   - Subscribe to relevant message types
   - Use async/await for message handling

## Example Usage

```python
from shared.base_agent import BaseAgent
from shared.protocols import MessageType

class MyAgent(BaseAgent):
    async def handle_strategy_request(self, payload):
        # Implement strategy logic
        return {"strategy": "my_strategy", "params": {...}}

    async def handle_data_request(self, payload):
        # Implement data handling
        return {"data": [...]}

    async def handle_action_request(self, payload):
        # Implement action handling
        return {"status": "executed", "details": {...}}

# Usage
agent = MyAgent("agent_id")
await agent.send_message(
    MessageType.STRATEGY_REQUEST,
    payload={"market": "NASDAQ"}
)
```
