"""Main module for RLlib agent."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared.utils import load_config, setup_logging

logger = setup_logging('rllib_agent')

def main():
    """Main function for RLlib agent."""
    try:
        config = load_config()
        logger.info("RLlib agent started with config: %s", config)
        # Add your RLlib specific implementation here
        
    except Exception as e:
        logger.error("Error in RLlib agent: %s", str(e))
        raise

if __name__ == "__main__":
    main()
