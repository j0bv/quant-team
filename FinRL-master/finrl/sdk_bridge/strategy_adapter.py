"""Strategy adapter to connect FinRL strategies with SDK functionality."""
from typing import Any, Dict, List, Optional
from datetime import datetime
from .market_interface import MarketInterface

class StrategyAdapter:
    def __init__(self, sdk_path: str):
        """Initialize the strategy adapter.
        
        Args:
            sdk_path: Path to the SDK directory
        """
        self.market_interface = MarketInterface(sdk_path)
        
    def execute_trade(self, strategy_output: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a trade based on strategy output using SDK functionality.
        
        Args:
            strategy_output: Dictionary containing strategy decisions
                Expected format:
                {
                    'action': 'buy'|'sell',
                    'symbol': str,
                    'quantity': float,
                    'price': float,
                    'timestamp': datetime
                }
        
        Returns:
            Dict containing trade execution results
        """
        # Validate market is open
        if not self.market_interface.is_market_open('stocks', strategy_output.get('timestamp')):
            return {'status': 'failed', 'reason': 'Market closed'}
            
        # Get spread costs
        spread = self.market_interface.get_spread(
            strategy_output['symbol'],
            strategy_output['quantity']
        )
        
        # Adjust price for spread
        adjusted_price = (
            strategy_output['price'] + spread if strategy_output['action'] == 'buy'
            else strategy_output['price'] - spread
        )
        
        # Create trade record
        trade = {
            'symbol': strategy_output['symbol'],
            'quantity': strategy_output['quantity'],
            'price': adjusted_price,
            'timestamp': strategy_output['timestamp'].isoformat(),
            'action': strategy_output['action'],
            'spread': spread
        }
        
        return {
            'status': 'success',
            'trade': trade,
            'estimated_pnl': self.market_interface.calculate_pnl([trade])
        }
    
    def validate_strategy(self, strategy_class: Any) -> bool:
        """Validate that a strategy class implements required methods and interfaces.
        
        Args:
            strategy_class: The strategy class to validate
        
        Returns:
            bool: Whether the strategy is valid
        """
        required_methods = ['predict', 'train']
        
        for method in required_methods:
            if not hasattr(strategy_class, method):
                return False
        
        return True
