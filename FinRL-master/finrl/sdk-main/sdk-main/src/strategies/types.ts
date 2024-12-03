import { Market } from '../markets/types';

export interface TradeSignal {
  action: 'buy' | 'sell';
  symbol: string;
  quantity: number;
  price: number;
  timestamp: Date;
}

export interface StrategyConfig {
  market: Market;
  symbols: string[];
  interval: number;  // Trading interval in milliseconds
  maxPositionSize?: number;
  stopLoss?: number;
  takeProfit?: number;
}

export interface StrategyState {
  positions: Map<string, number>;
  lastUpdate: Date;
  pnl: number;
}

export interface Strategy {
  name: string;
  config: StrategyConfig;
  state: StrategyState;
  
  initialize(): Promise<void>;
  predict(timestamp: Date): Promise<TradeSignal[]>;
  train(historicalData: any): Promise<void>;
  onTrade?(signal: TradeSignal): void;
  onError?(error: Error): void;
}
