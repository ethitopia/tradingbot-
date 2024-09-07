from lumibot.brokers import Alpaca 
from lumibot.backtesting import YahooDataBacktesting 
from lumibot.strategies.strategy import Strategy 
from lumibot.traders import Trader 
from datetime import datetime, timedelta
from utils.sentiment_util import estimate_sentiment
from alpaca_trade_api import REST 

API_KEY = ""
API_SECRET = "" 
BASE_URL = "" 

ALPACA_CREDS = { 
    "API_KEY": API_KEY, 
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class TraderStrat(Strategy):
    def initialize(self, s: str = "SPY", cash_at_risk: float = 0.5): 
        super().initialize()
        self.symbol = s
        self.sleeptime = timedelta(hours=24) #frequency of trade
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(API_KEY, API_SECRET, BASE_URL)
        
    def position_sizing(self): 
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity
       
    def get_dates(self): 
        today = self.api.get_clock().timestamp
        five_days_prior = today - timedelta(days=5)
        return today.strftime('%Y-%m-%d'), five_days_prior.strftime('%Y-%m-%d')
       
    def get_news(self): 
        today, start = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=start, end=today)
        news_list = [ev.__dict__["_raw"]["headline"] for ev in news]
        return news_list
        
    def onTrade(self): 
        cash, last_price, quantity = self.position_sizing()
        news_list = self.get_news()
        
        if news_list:  # Ensure there's news to analyze
            sentiments = [estimate_sentiment(news) for news in news_list]
            sentiment_score = sentiments.count('positive') - sentiments.count('negative')
            
            if cash > last_price and sentiment_score > 0: 
                if self.last_trade is None:  # only buys if no previous trade
                    order = self.create_order(
                        self.symbol, 
                        quantity,
                        10, 
                        "buy", 
                        type="bracket", 
                        take_profit_price=last_price*1.3, 
                        stop_loss_price=last_price*0.95
                    )
                    self.submit_order(order)
                    self.last_trade = "buy"
        else:
            print("No news available for sentiment analysis.")

   
broker = Alpaca(ALPACA_CREDS)

strategy = TraderStrat(name='Trader1', broker=broker, parameters={"symbol": "SPY", "cash_at_risk": 0.5})

start_date = datetime(2024, 6, 20)
end_date = datetime(2024, 7, 20)

strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"symbol": "SPY", "cash_at_risk": 0.5}
)
