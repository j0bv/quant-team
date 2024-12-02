"""Main module for ElegantRL agent."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared.utils import load_config, setup_logging

logger = setup_logging('elegantrl_agent')

def main():
    """Main function for ElegantRL agent."""
    try:
        config = load_config()
        logger.info("ElegantRL agent started with config: %s", config)
        # Add your ElegantRL specific implementation here
        
    except Exception as e:
        logger.error("Error in ElegantRL agent: %s", str(e))
        raise

if __name__ == "__main__":
    main()
