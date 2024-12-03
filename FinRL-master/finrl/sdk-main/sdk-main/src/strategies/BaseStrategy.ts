import { Strategy, StrategyConfig, StrategyState, TradeSignal } from './types';
import { calculatePnL } from '../trade/pnl';
import { getSpread } from '../trade/spread';
import { isStocksOpen } from '../markets/stocks';

export abstract class BaseStrategy implements Strategy {
  public name: string;
  public config: StrategyConfig;
  public state: StrategyState;

  constructor(name: string, config: StrategyConfig) {
    this.name = name;
    this.config = config;
    this.state = {
      positions: new Map(),
      lastUpdate: new Date(),
      pnl: 0
    };
  }

  public async initialize(): Promise<void> {
    // Override this method to add custom initialization logic
  }

  public abstract predict(timestamp: Date): Promise<TradeSignal[]>;
  
  public abstract train(historicalData: any): Promise<void>;

  protected async validateAndExecuteTrade(signal: TradeSignal): Promise<boolean> {
    if (!isStocksOpen(signal.timestamp)) {
      this.onError?.(new Error('Market is closed'));
      return false;
    }

    const spread = getSpread(signal.symbol, signal.quantity);
    const adjustedPrice = signal.action === 'buy' 
      ? signal.price + spread 
      : signal.price - spread;

    // Check position limits
    const currentPosition = this.state.positions.get(signal.symbol) || 0;
    const newPosition = signal.action === 'buy'
      ? currentPosition + signal.quantity
      : currentPosition - signal.quantity;

    if (this.config.maxPositionSize && Math.abs(newPosition) > this.config.maxPositionSize) {
      this.onError?.(new Error('Position size limit exceeded'));
      return false;
    }

    // Execute trade
    this.state.positions.set(signal.symbol, newPosition);
    
    // Update PnL
    const trade = { ...signal, price: adjustedPrice };
    const tradePnL = calculatePnL([trade]);
    this.state.pnl += tradePnL;

    this.onTrade?.(trade);
    return true;
  }

  protected checkStopLossAndTakeProfit(symbol: string, currentPrice: number): TradeSignal | null {
    const position = this.state.positions.get(symbol);
    if (!position) return null;

    const avgPrice = this.getAveragePrice(symbol);
    if (!avgPrice) return null;

    const pnlPercent = (currentPrice - avgPrice) / avgPrice * 100;

    if (this.config.stopLoss && pnlPercent <= -this.config.stopLoss) {
      return {
        action: 'sell',
        symbol,
        quantity: Math.abs(position),
        price: currentPrice,
        timestamp: new Date()
      };
    }

    if (this.config.takeProfit && pnlPercent >= this.config.takeProfit) {
      return {
        action: 'sell',
        symbol,
        quantity: Math.abs(position),
        price: currentPrice,
        timestamp: new Date()
      };
    }

    return null;
  }

  private getAveragePrice(symbol: string): number | null {
    // This is a simplified version. In a real implementation,
    // you would maintain a history of trades to calculate the average price
    return null;
  }

  public onTrade?(signal: TradeSignal): void {
    console.log(`Trade executed: ${signal.action} ${signal.quantity} ${signal.symbol} @ ${signal.price}`);
  }

  public onError?(error: Error): void {
    console.error(`Strategy error: ${error.message}`);
  }
}
