import { google } from '@app/utils';
import { z } from 'genkit';

export const AiTradeInputSchema = z.object({
  id: z.string().describe('The unique identifier of the trade'),
  asset: z.string().describe('The asset of the trade'),
  action: z.enum(['Buy', 'Sell']).describe('The action of the trade'),
  symbol: z.string().describe('The symbol of the trade'),
  entryPrice: z.number().nullable().describe('The entry price of the trade'),
  category: z
    .enum(['spot', 'linear', 'inverse', 'option'])
    .describe('The category of the trade'),
  stopLoss: z.number().describe('The stop loss of the trade'),
  takeProfit: z.number().describe('The take profit of the trade'),
  leverage: z.number().describe('The leverage of the trade'),
  isDraft: z.boolean().describe('The draft status of the trade'),
  outcome: z
    .enum(['Win', 'Loss', 'Liquidated'])
    .nullable()
    .optional()
    .describe('The outcome of the trade'),
  tradeRoi: z.number().describe('The trade ROI of the trade'),
  userId: z.string().describe('The user ID of the trade'),
  creatorId: z.string().describe('The creator ID of the trade'),
  currentPrice: z.number().describe('The current price of the trade'),
  positionSize: z
    .object({
      amount: z.number().describe('The amount of the trade'),
      currency: z.enum(['USDT', 'BTC']).describe('The currency of the trade'),
    })
    .describe('The position size of the trade'),
  realizedPnl: z.number().describe('The realized PnL of the trade'),
  noOfCopiers: z.number().describe('The number of copiers of the trade'),
  duration: z
    .enum(['Scalp', 'Intraday', 'Swing', 'Position', 'custom'])
    .describe('The duration of the trade'),
  scheduleStartId: z
    .number()
    .optional()
    .describe('The schedule start ID of the trade'),
  scheduleEndId: z
    .number()
    .optional()
    .describe('The schedule end ID of the trade'),
  image: z.string().optional().nullable().describe('The image of the trade'),
  startDate: z.string().describe('The start date of the trade'),
  orderType: z
    .enum(['Market Order', 'Limit Order'])
    .describe('The order type of the trade'),
  expiresAt: z.string().describe('The expires at of the trade'),
  riskLevel: z
    .enum(['Low', 'Medium', 'High'])
    .describe('The risk level of the trade'),
  fundId: z.string().optional().nullable().describe('The fund ID of the trade'),
  comment: z.string().optional().describe('The comment of the trade'),
  exitPrice: z
    .number()
    .optional()
    .nullable()
    .describe('The exit price of the trade'),
  status: z.string().describe('The status of the trade'),
  tradeType: z
    .enum(['original', 'copy'])
    .describe('The trade type of the trade'),
  orderLinkId: z
    .string()
    .optional()
    .nullable()
    .describe('The order link ID of the trade'),
  orderId: z
    .string()
    .optional()
    .nullable()
    .describe('The order ID of the trade'),
  errorMsg: z
    .string()
    .optional()
    .nullable()
    .describe('The error message of the trade'),
  margin: z.number().describe('The margin of the trade'),
  identifier: z.string().describe('The identifier of the trade'),
  createdAt: z.string().describe('The created at of the trade'),
  updatedAt: z.string().describe('The updated at of the trade'),
});

export type AITradeInput = z.infer<typeof AiTradeInputSchema>;

export const AiTradeOutputSchema = z.object({
  risk_reward_score: z.number().describe('The risk reward score of the trade'),
  trend_alignment_score: z
    .number()
    .describe('The trend alignment score of the trade'),
  liquidity_score: z.number().describe('The liquidity score of the trade'),
  volatility_risk_score: z
    .number()
    .describe('The volatility risk score of the trade'),
  entry_quality_score: z
    .number()
    .describe('The entry quality score of the trade'),
  timing_score: z.number().describe('The timing score of the trade'),
  leverage_risk_score: z
    .number()
    .describe('The leverage risk score of the trade'),
  overall_score: z.number().describe('The overall score of the trade'),
  reasoning: z.string().describe('The reasoning of the trade'),
  suggestions: z.string().describe('The suggestions of the trade'),
});

export type AITradeOutput = z.infer<typeof AiTradeOutputSchema>;

export const PromptTemplate = google.definePrompt({
  name: 'ai-trade-prompt',
  input: { schema: z.object({ tradeData: AiTradeInputSchema }) },
  output: { schema: AiTradeOutputSchema },
  prompt: `
You are an expert quantitative analyst and trading strategist. Your task is to analyze the provided trade data and generate a comprehensive trading analysis report.
I will provide you with a JSON object containing the trade details.

**Trade Data JSON:**
{tradeData}

**Analysis Requirements:**
1. **Risk-Reward Ratio**: Calculate the risk-reward ratio based on the entry price, stop loss, and take profit.
2. **Trend Alignment**: Analyze the trade direction against the prevailing market trend (if available in the data).
3. **Liquidity Assessment**: Evaluate the liquidity of the asset based on its trading volume and volatility.
4. **Volatility Risk**: Assess the risk associated with the asset's volatility.
5. **Entry Quality**: Determine the quality of the entry price based on the current market price.
6. **Timing**: Evaluate the timing of the trade entry.
7. **Leverage Risk**: Assess the risk associated with the chosen leverage level.
8. **Overall Score**: Calculate an overall score (0-100) that reflects the quality of the trade.
9. **Reasoning**: Provide a detailed explanation for your analysis and scoring.
10. **Suggestions**: Offer actionable suggestions to improve the trade or for future trades.

**Output Format:**
Return the analysis in JSON format with the following structure:
{
  "risk_reward_score": number,
  "trend_alignment_score": number,
  "liquidity_score": number,
  "volatility_risk_score": number,
  "entry_quality_score": number,
  "timing_score": number,
  "leverage_risk_score": number,
  "overall_score": number,
  "reasoning": string,
  "suggestions": string
}
`,
});
