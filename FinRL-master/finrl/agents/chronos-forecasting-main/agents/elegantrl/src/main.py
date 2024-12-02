"""ElegantRL agent implementation using the communication protocol."""

import sys
import os
import asyncio
from typing import Dict, Optional, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from shared.base_agent import BaseAgent
from shared.utils import load_config, setup_logging

logger = setup_logging('elegantrl_agent')

class ElegantRLAgent(BaseAgent):
    """ElegantRL agent implementation."""
    
    def __init__(self):
        super().__init__("elegantrl_agent")
        self.config = load_config()
        logger.info("ElegantRL agent initialized with config: %s", self.config)

    async def handle_strategy_request(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle strategy requests."""
        logger.info("Handling strategy request: %s", payload)
        # Implement ElegantRL specific strategy logic
        return {
            "strategy_type": "elegantrl",
            "model_type": "DQN",
            "parameters": {
                "learning_rate": self.config["training"]["learning_rate"],
                "batch_size": self.config["training"]["batch_size"]
            }
        }

    async def handle_data_request(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle data requests."""
        logger.info("Handling data request: %s", payload)
        # Implement ElegantRL specific data handling
        return {
            "data_source": self.config["environment"]["market_data_source"],
            "timeframe": self.config["environment"]["time_interval"]
        }

    async def handle_action_request(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle action requests."""
        logger.info("Handling action request: %s", payload)
        # Implement ElegantRL specific action handling
        return {
            "action_type": "trade",
            "status": "executed",
            "details": payload
        }

async def main():
    """Main function for ElegantRL agent."""
    try:
        agent = ElegantRLAgent()
        # Keep the agent running
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        logger.error("Error in ElegantRL agent: %s", str(e))
        raise

if __name__ == "__main__":
    asyncio.run(main())
