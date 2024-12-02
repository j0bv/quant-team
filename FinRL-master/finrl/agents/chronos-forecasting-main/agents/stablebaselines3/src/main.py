"""Main module for Stable-Baselines3 agent."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared.utils import load_config, setup_logging

logger = setup_logging('sb3_agent')

def main():
    """Main function for Stable-Baselines3 agent."""
    try:
        config = load_config()
        logger.info("Stable-Baselines3 agent started with config: %s", config)
        # Add your Stable-Baselines3 specific implementation here
        
    except Exception as e:
        logger.error("Error in Stable-Baselines3 agent: %s", str(e))
        raise

if __name__ == "__main__":
    main()
