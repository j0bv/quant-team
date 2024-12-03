"""Market interface bridge between SDK and Python strategies."""
from datetime import datetime
from typing import Dict, List, Optional, Union
import json
import subprocess
import os

class MarketInterface:
    def __init__(self, sdk_path: str):
        """Initialize the market interface.
        
        Args:
            sdk_path: Path to the SDK directory
        """
        self.sdk_path = sdk_path
        self._validate_sdk_path()
    
    def _validate_sdk_path(self):
        """Validate that the SDK path exists and contains necessary files."""
        if not os.path.exists(self.sdk_path):
            raise ValueError(f"SDK path does not exist: {self.sdk_path}")
        
        required_dirs = ['markets', 'trade']
        for dir_name in required_dirs:
            if not os.path.exists(os.path.join(self.sdk_path, 'src', dir_name)):
                raise ValueError(f"Required directory {dir_name} not found in SDK")

    def is_market_open(self, market_type: str, date: Optional[datetime] = None) -> bool:
        """Check if a specific market is open.
        
        Args:
            market_type: Type of market ('stocks', 'indices', etc.)
            date: Date to check. Defaults to current date.
        
        Returns:
            bool: Whether the market is open
        """
        date_str = date.isoformat() if date else datetime.now().isoformat()
        
        # Call the corresponding TypeScript function through Node.js
        cmd = [
            'node', '-e',
            f'const {{ is{market_type.capitalize()}Open }} = require("{os.path.join(self.sdk_path, "src/markets")}");'
            f'console.log(is{market_type.capitalize()}Open(new Date("{date_str}")))'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip().lower() == 'true'
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to check market status: {e}")

    def calculate_pnl(self, trades: List[Dict]) -> float:
        """Calculate PnL for a list of trades using SDK's PnL calculation.
        
        Args:
            trades: List of trade dictionaries with required fields
        
        Returns:
            float: Calculated PnL
        """
        # Convert trades to JSON format expected by TypeScript
        trades_json = json.dumps(trades)
        
        cmd = [
            'node', '-e',
            f'const {{ calculatePnL }} = require("{os.path.join(self.sdk_path, "src/trade")}");'
            f'console.log(calculatePnL({trades_json}))'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to calculate PnL: {e}")

    def get_spread(self, symbol: str, quantity: float) -> float:
        """Get the spread for a given symbol and quantity.
        
        Args:
            symbol: Trading symbol
            quantity: Trade quantity
        
        Returns:
            float: Calculated spread
        """
        cmd = [
            'node', '-e',
            f'const {{ getSpread }} = require("{os.path.join(self.sdk_path, "src/trade")}");'
            f'console.log(getSpread("{symbol}", {quantity}))'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get spread: {e}")
