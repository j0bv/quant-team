"""Main module for Portfolio Optimization agent."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared.utils import load_config, setup_logging

logger = setup_logging('portfolio_optimization_agent')

def main():
    """Main function for Portfolio Optimization agent."""
    try:
        config = load_config()
        logger.info("Portfolio Optimization agent started with config: %s", config)
        # Add your Portfolio Optimization specific implementation here
        
    except Exception as e:
        logger.error("Error in Portfolio Optimization agent: %s", str(e))
        raise

if __name__ == "__main__":
    main()
