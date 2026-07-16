/* eslint-disable @typescript-eslint/no-unused-vars */
import { Injectable, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { WebsocketClient } from 'bybit-api';
import { tradeExecuteData, tradeUpdateData } from './input';
import { EventEmitter2 } from '@nestjs/event-emitter';
import * as path from 'path';
import { readFile, writeFile } from 'fs/promises';

type Side = 'Buy' | 'Sell';

interface PositionState {
  symbol: string;
  side: Side;
  qty: number;
  cost: number;
  avgEntry: number;
  entryFees: number;
  realized: number;
  orderId: string;
  orderLinkId: string;
}

@Injectable()
export class ByBitGateway implements OnModuleInit {
  private ws: WebsocketClient | null = null;
  private startupTimer: NodeJS.Timeout;
  private reconnecting = false;
  private positions: Record<string, PositionState> = {};
  private readonly stateFile = path.join(
    process.cwd(),
    'bybit-positions-state.json',
  );
  constructor(
    private readonly configService: ConfigService,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  onModuleInit() {
    // Load persisted state before connecting so closes after restarts still work
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    this.loadState();
    this.createWebSocket();
  }

  private createWebSocket() {
    console.log('🔌 Creating Bybit WS client...');

    try {
      const wsConfig = {
        key: this.configService.getOrThrow('BYBIT_API_KEY'),
        secret: this.configService.getOrThrow('BYBIT_SECRET_KEY'),
        recvWindow: 5000,
        testnet: true,
        pingInterval: 10000,
        pongTimeout: 1000,
        reconnectTimeout: 500,
      };

      this.ws = new WebsocketClient(wsConfig);

      // Subscribe **immediately**
      // eslint-disable-next-line @typescript-eslint/no-floating-promises
      this.ws.subscribeV5(['order', 'execution'], 'spot');

      // --- STARTUP WATCHDOG ----
      this.startupTimer = setTimeout(() => {
        console.log('⛔ WS did not start after 5s. Reinitializing...');
        this.forceReconnect();
      }, 5000);

      // Events
      this.ws.on('open', ({ wsKey }) => {
        clearTimeout(this.startupTimer);
        console.log('✅ WS Connected:', wsKey);
      });

      this.ws.on('update', (data: tradeUpdateData) => {
        console.log('📩 Update received:', data.topic);
        this.handleOrder(data);
      });

      this.ws.on('close', () => {
        console.log('⚠️ WS closed');
        this.forceReconnect();
      });

      this.ws.on('exception', (e) => console.log('❌ WS Exception'));
    } catch (err) {
      console.error('❌ WS Init Error');
      this.forceReconnect();
    }
  }

  private handleOrder(update: tradeUpdateData) {
    switch (update.topic) {
      case 'execution':
        update.data.forEach((exe) => this.handleExecution(exe));
        break;
      case 'order':
        update.data.forEach((order) => this.handleOrderStatus(order));
        break;
      default:
        console.log('Unhandled update topic', update.topic);
    }
  }

  private handleExecution(exe: tradeExecuteData) {
    if (exe.execType !== 'Trade') return;

    const symbol = exe.symbol;
    const price = parseFloat(exe.execPrice);
    const qty = parseFloat(exe.execQty);
    const fee = parseFloat(exe.execFee || '0');
    const side = exe.side as Side;
    const closedSize = parseFloat(exe.closedSize || '0');
    const orderId = exe.orderId;
    const orderLinkId = exe.orderLinkId;

    const hasClosedSize = Number.isFinite(closedSize) && closedSize > 0;
    const reduceOnlyFlag =
      exe.reduceOnly !== undefined ? Boolean(exe.reduceOnly) : false;

    // Determine if this execution is intended to close or reduce a position
    let isClosing = reduceOnlyFlag || hasClosedSize;

    // Check if the current side is opposite to existing positions for this symbol
    if (!isClosing) {
      const existingOpposite = Object.values(this.positions).find(
        (p) => p.symbol === symbol && p.qty > 0 && p.side !== side,
      );
      if (existingOpposite) {
        isClosing = true;
      }
    }

    let positionKey: string | undefined;

    if (isClosing) {
      // 1. Try to find position by matching orderLinkId (if it's a direct closure)
      if (orderLinkId) {
        positionKey = Object.keys(this.positions).find(
          (k) => this.positions[k].orderLinkId === orderLinkId,
        );
      }

      // 2. Try to find by orderId
      if (!positionKey && orderId) {
        positionKey = Object.keys(this.positions).find(
          (k) => this.positions[k].orderId === orderId,
        );
      }

      // 3. Fallback: Find any active position for this symbol with opposite side (FIFO)
      if (!positionKey) {
        positionKey = Object.keys(this.positions).find(
          (k) =>
            this.positions[k].symbol === symbol &&
            this.positions[k].qty > 0 &&
            this.positions[k].side !== side,
        );
      }

      // 4. Legacy fallback: Check if the key is just the symbol
      if (!positionKey && this.positions[symbol]) {
        positionKey = symbol;
      }
    } else {
      // For opening/increasing, use the order identifier as the key
      // If we already have a position with this key, we increase it.
      // Otherwise, we check if we have one for this symbol (legacy/fallback).
      positionKey = orderLinkId || orderId;
    }

    if (isClosing && positionKey) {
      this.closePosition(positionKey, symbol, price, qty, fee);
    } else {
      // If it's not closing, or we couldn't find a position to close, we treat it as opening/increasing
      this.openPosition(
        positionKey || symbol,
        symbol,
        side,
        price,
        qty,
        fee,
        orderId,
        orderLinkId,
      );
    }
  }

  private handleOrderStatus(order: tradeExecuteData) {
    // console.log('Order', { order });
    if (
      order.stopOrderType === 'TakeProfit' &&
      order.orderStatus === 'Untriggered'
    ) {
      console.log({ tp_status: 'waiting', symbol: order.symbol });
    }

    if (
      order.stopOrderType === 'StopLoss' &&
      order.orderStatus === 'Untriggered'
    ) {
      console.log({ sl_status: 'waiting', symbol: order.symbol });
    }

    if (order.orderStatus === 'Filled') {
      console.log({ status: 'Open', symbol: order.symbol });
    }

    if (order.orderStatus === 'Cancelled') {
      console.log({ status: 'cancelled', symbol: order.symbol });
    }

    if (
      order.orderStatus === 'Deactivated' &&
      (order.stopOrderType === 'StopLoss' ||
        order.stopOrderType === 'TakeProfit')
    ) {
      console.log({ status: 'deactivated', symbol: order.symbol });
    }
  }

  private openPosition(
    key: string,
    symbol: string,
    side: Side,
    price: number,
    qty: number,
    fee: number,
    orderId?: string,
    orderLinkId?: string,
  ) {
    const existing = this.positions[key];
    const position: PositionState =
      existing && existing.qty > 0
        ? existing
        : {
            symbol,
            side,
            qty: 0,
            cost: 0,
            avgEntry: 0,
            entryFees: 0,
            realized: 0,
            orderId: orderId ?? '',
            orderLinkId: orderLinkId ?? '',
          };

    position.cost += price * qty;
    position.qty += qty;
    position.avgEntry = position.qty ? position.cost / position.qty : 0;
    position.entryFees += fee;

    this.positions[key] = position;

    console.log({
      event: 'entry_fill',
      symbol,
      key,
      side: position.side,
      qty,
      price,
      fee,
      avg_entry: position.avgEntry,
      position_qty: position.qty,
    });

    void this.persistState();
  }

  private closePosition(
    key: string,
    symbol: string,
    price: number,
    qty: number,
    fee: number,
  ) {
    const position = this.positions[key];

    // console.log(position);

    if (!position || position.qty <= 0) {
      console.log({
        event: 'close_fill_without_position',
        symbol,
        key,
        price,
        qty,
        fee,
      });
      return;
    }

    const qtyToClose = Math.min(qty, position.qty);
    const grossPnl =
      position.side === 'Buy'
        ? (price - position.avgEntry) * qtyToClose
        : (position.avgEntry - price) * qtyToClose;

    const proportionalEntryFee =
      position.qty > 0 ? (position.entryFees * qtyToClose) / position.qty : 0;

    const netPnl = grossPnl - fee - proportionalEntryFee;

    position.entryFees -= proportionalEntryFee;
    position.qty -= qtyToClose;
    position.cost = position.avgEntry * position.qty;
    position.realized += netPnl;

    if (position.qty === 0) {
      this.eventEmitter.emit('trade.pnl.realized', {
        realizedPnL: position.realized,
        orderId: position.orderId,
        orderLinkId: position.orderLinkId,
      });

      console.log({
        event: 'position_closed',
        symbol,
        key,
        side: position.side,
        avg_entry: position.avgEntry,
        realized_pnl: position.realized,
        orderId: position.orderId,
        orderLinkId: position.orderLinkId,
      });

      // Drop flat positions to keep memory tight; realized is emitted elsewhere
      delete this.positions[key];
    }

    void this.persistState();
  }

  private forceReconnect() {
    if (this.reconnecting) return;
    this.reconnecting = true;

    console.log('⏳ Reconnecting WS in 3 seconds...');

    try {
      if (this.ws) {
        this.ws.closeAll();
      }
    } catch (error) {
      console.log('error connecting...');
    }

    setTimeout(() => {
      this.reconnecting = false;
      this.createWebSocket();
    }, 3000);
  }

  private async loadState() {
    try {
      const raw = await readFile(this.stateFile, 'utf8');
      const parsed = JSON.parse(raw) as Record<string, PositionState>;
      if (parsed && typeof parsed === 'object') {
        this.positions = parsed;

        // Migration: add symbol to existing entries if missing (legacy)
        for (const key of Object.keys(this.positions)) {
          if (!this.positions[key].symbol) {
            this.positions[key].symbol = key; // In legacy, the key was the symbol
          }
        }

        console.log(
          `Restored ${Object.keys(this.positions).length} positions from disk`,
        );
      }
    } catch (err) {
      // File likely not present on first run; ignore
    }
  }

  private async persistState() {
    try {
      // Only keep non-flat positions to reduce memory and disk usage
      const active: Record<string, PositionState> = {};
      for (const [sym, pos] of Object.entries(this.positions)) {
        if (pos.qty > 0) active[sym] = pos;
      }
      await writeFile(this.stateFile, JSON.stringify(active), 'utf8');
    } catch (err) {
      console.warn('Failed to persist positions state', err);
    }
  }
}

// TODO notify user with how the trade went
