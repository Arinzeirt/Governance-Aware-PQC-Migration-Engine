export * from './mail.service';
export enum template {
  broadcast = 'broadcast',
  admin = 'admin',
  reg = 'register',
  reset = 'reset',
  resend = 'resend',
  tradeNote = 'trade-note',
  infoPartner = 'partner',
  infoSupport = 'support',
  customer = 'customer',
  partnership = 'partnership',
  bybit = 'bybit-balance',
  tradeOpen = 'trade-open',
  tradeClose = 'trade-close',
  tradePending = 'trade-pending',
  tradeFail = 'trade-fail',
  notification = 'notification',
}
