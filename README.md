# Sentiment Trading Bot: 

Vanilla Implementation of a Algorithmic Trading Bot leveraging pretrained sentiment analysis of financial news to inform trading decisions.

### Strategy Workflow:

Data Fetching: Daily fetches the latest market news and financial data for the designated symbol.
Sentiment Calculation: Analyzes the sentiment of news headlines from the last five days, calculating a net sentiment score.
Trading Logic: If the sentiment score is positive and there are no open trades, the strategy submits a buy order using a bracket order format to manage the trade actively.
Position Sizing: Determines the quantity of shares to buy based on the available cash and a predefined risk parameter (cash at risk).

### Frameworks: 

Pytorch, Lumibot, AlpacaTrade API, Transformers

### Testing: 

Currently backtesting w/ real time market data 
