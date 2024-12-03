import { BaseStrategy } from './BaseStrategy';
import { TradeSignal, StrategyConfig } from './types';

interface SMAConfig extends StrategyConfig {
  shortPeriod: number;
  longPeriod: number;
}

export class SimpleMovingAverageStrategy extends BaseStrategy {
  private prices: Map<string, number[]>;
  private config: SMAConfig;

  constructor(config: SMAConfig) {
    super('SimpleMovingAverage', config);
    this.prices = new Map();
    this.config = config;
  }

  public async initialize(): Promise<void> {
    // Initialize price history for each symbol
    this.config.symbols.forEach(symbol => {
      this.prices.set(symbol, []);
    });
  }

  public async predict(timestamp: Date): Promise<TradeSignal[]> {
    const signals: TradeSignal[] = [];

    for (const symbol of this.config.symbols) {
      const prices = this.prices.get(symbol);
      if (!prices || prices.length < this.config.longPeriod) continue;

      const shortSMA = this.calculateSMA(prices, this.config.shortPeriod);
      const longSMA = this.calculateSMA(prices, this.config.longPeriod);
      const currentPrice = prices[prices.length - 1];

      // Check for crossover signals
      if (shortSMA > longSMA) {
        // Golden cross - buy signal
        signals.push({
          action: 'buy',
          symbol,
          quantity: 100, // Example fixed quantity
          price: currentPrice,
          timestamp
        });
      } else if (shortSMA < longSMA) {
        // Death cross - sell signal
        signals.push({
          action: 'sell',
          symbol,
          quantity: 100,
          price: currentPrice,
          timestamp
        });
      }

      // Check stop loss and take profit
      const sltp = this.checkStopLossAndTakeProfit(symbol, currentPrice);
      if (sltp) signals.push(sltp);
    }

    return signals;
  }

  public async train(historicalData: any): Promise<void> {
    // In this simple strategy, we just need to initialize the price history
    // More complex strategies might need actual training
    if (Array.isArray(historicalData)) {
      historicalData.forEach(data => {
        const prices = this.prices.get(data.symbol) || [];
        prices.push(data.price);
        this.prices.set(data.symbol, prices);
      });
    }
  }

  private calculateSMA(prices: number[], period: number): number {
    if (prices.length < period) return 0;
    
    const sum = prices.slice(-period).reduce((a, b) => a + b, 0);
    return sum / period;
  }
}
