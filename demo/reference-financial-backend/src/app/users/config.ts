import { AiTradeInputSchema } from '@app/trades/config';
import { google } from '@app/utils';
import { z } from 'genkit';

export const userSchema = z.object({
  fullName: z.string().describe('The full name of the user'),
  email: z.string().describe('The email address of the user'),
  bio: z.string().optional().nullable().describe('The bio of the user'),
  username: z
    .string()
    .optional()
    .nullable()
    .describe('The username of the user'),
  gender: z
    .enum(['MALE', 'FEMALE', 'OTHERS'])
    .optional()
    .nullable()
    .describe('The gender of the user'),
});

export type UserInterface = z.infer<typeof userSchema>;

export const outputSchema = z.object({
  result: z
    .string()
    .describe('The result of the analysis in rich text (HTML) format.'),
});

export type OutputInterface = z.infer<typeof outputSchema>;

export const tradeSchema = z.array(AiTradeInputSchema);

export const inputScheme = z.object({
  tradeData: tradeSchema,
  userData: userSchema,
});

export type TradeInterface = z.infer<typeof tradeSchema>;

export const PromptTemplate = google.definePrompt({
  name: 'user-prompt',
  input: { schema: inputScheme },
  output: { schema: outputSchema },
  prompt: `
        You are an expert quantitative analyst, trading strategist, and behavioral finance specialist. Your task is to analyze the provided user profile alongside their complete trading history to generate a comprehensive, personalized trading performance and behavioral analysis report.

        **User Profile:**
        {userData}

        **Trade History (Array):**
        {tradeData}

        **Analysis Requirements:**

        Perform a deep, multi-dimensional analysis covering the following areas:

        ## 1. TRADER PROFILE ANALYSIS
        - Analyze the user's demographic information (name, username, bio, gender) to understand their trading identity
        - Assess their self-described trading style and goals (if mentioned in bio)
        - Identify any patterns or characteristics that might influence their trading behavior

        ## 2. TRADING PERFORMANCE METRICS
        - **Overall Performance**: Calculate total win rate, loss rate, and liquidation rate across all trades
        - **Profitability Analysis**: Compute total realized PnL, average profit per winning trade, average loss per losing trade
        - **ROI Analysis**: Calculate average ROI, best performing trades, worst performing trades
        - **Consistency Score**: Evaluate the consistency of returns over time
        - **Risk-Adjusted Returns**: Assess performance relative to risk taken (Sharpe-like ratio)

        ## 3. RISK MANAGEMENT ASSESSMENT
        - **Position Sizing**: Analyze position size patterns and consistency
        - **Leverage Usage**: Evaluate leverage patterns (average, maximum, minimum) and appropriateness
        - **Stop Loss Discipline**: Assess how consistently stop losses are set and honored
        - **Risk Level Distribution**: Analyze the distribution of Low/Medium/High risk trades
        - **Margin Management**: Evaluate margin usage and efficiency
        - **Risk-Reward Ratios**: Calculate average risk-reward ratios across all trades

        ## 4. TRADING STRATEGY ANALYSIS
        - **Asset Preference**: Identify most traded assets and diversification level
        - **Market Category**: Analyze preference for spot, linear, inverse, or options trading
        - **Trade Duration**: Assess preference for scalping, intraday, swing, or position trading
        - **Action Bias**: Determine if there's a bias toward buying or selling
        - **Order Type Preference**: Analyze usage of market orders vs limit orders
        - **Trade Timing**: Identify patterns in trade entry timing and duration

        ## 5. BEHAVIORAL PATTERNS
        - **Trading Frequency**: Analyze trading activity patterns over time
        - **Emotional Trading Indicators**: Identify potential revenge trading, overtrading, or fear-based decisions
        - **Draft Usage**: Assess how often trades are drafted vs executed immediately
        - **Copy Trading Behavior**: Analyze original vs copied trades ratio
        - **Social Influence**: Evaluate the number of copiers and social trading impact
        - **Learning Curve**: Identify improvement or deterioration in trading performance over time

        ## 6. STRENGTHS IDENTIFICATION
        - Highlight the trader's top 3-5 strengths based on the data
        - Identify what they're doing well (e.g., risk management, asset selection, timing)
        - Recognize any exceptional skills or consistent positive patterns

        ## 7. WEAKNESSES & AREAS FOR IMPROVEMENT
        - Identify the top 3-5 areas that need improvement
        - Highlight risky behaviors or patterns that could lead to losses
        - Point out inconsistencies or concerning trends

        ## 8. COMPARATIVE ANALYSIS
        - Compare the trader's performance against typical retail trader benchmarks
        - Assess their skill level (Beginner, Intermediate, Advanced, Expert)
        - Identify if they're trending toward becoming a professional trader

        ## 9. PERSONALIZED RECOMMENDATIONS
        Provide specific, actionable recommendations including:
        - **Immediate Actions**: 3-5 things to do right now to improve performance
        - **Risk Management Improvements**: Specific adjustments to leverage, position sizing, or stop losses
        - **Strategy Refinements**: Suggestions for optimizing their trading approach
        - **Educational Focus**: Areas where additional learning would be most beneficial
        - **Psychological Considerations**: Mental game improvements and emotional discipline tips
        - **Portfolio Diversification**: Suggestions for better asset allocation

        ## 10. PREDICTIVE INSIGHTS
        - Forecast potential future performance based on current trajectory
        - Identify warning signs of potential account blow-up or significant losses
        - Highlight positive trends that could lead to consistent profitability

        **Output Format:**

        Generate a comprehensive, well-structured HTML report that is:
        - **Professional**: Use clear headings, sections, and formatting
        - **Visual**: Include emphasis on key metrics using bold, colors, and highlights
        - **Data-Driven**: Support all claims with specific numbers and percentages from the trade data
        - **Actionable**: Provide concrete, specific recommendations
        - **Personalized**: Address the user by name and reference their specific trading patterns
        - **Encouraging yet Honest**: Be supportive while being truthful about areas needing improvement

        Use HTML formatting with:
        - Proper heading hierarchy (h1, h2, h3)
        - Tables for metrics comparison
        - Color coding (green for positive, red for negative, yellow for warnings)
        - Lists for recommendations and key points
        - Emphasis tags (strong, em) for important insights
        - Sections with clear visual separation

        The report should be comprehensive (detailed enough to be valuable) yet concise (focused on the most important insights). Aim for a report that would take 5-10 minutes to read thoroughly.
    `,
});
