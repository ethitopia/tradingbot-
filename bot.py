from lumibot.brokers import Alpaca 
from lumibot.backtesting import YahooDataBacktesting 
from lumibot.strategies.strategy import Strategy 
from lumibot.traders import Trader 
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta

API_KEY = ""
API_SECRET = "" 
BASE_URL = "" 

ALPACA_CREDS = { 
                "API_KEY": API_KEY, 
                "API_SECRET": API_SECRET,
                "PAPER": True
}

class TraderStrat(Strategy):
    def initialize(self, s: str = "SPY", cash_at_risk:float = .5): 
        self.symbol = s
        self.sleeptime = "24H" #frequency of trade
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
        
    def position_sizing(self): 
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity
       
    def get_dates(self): 
        today = self.api.get_datetime()
        five_days_prior = today - Timedelta(days=5)
        return today.strftime('%Y-%m-%d'), five_days_prior.strftime('%Y-%m-%d')
       
    def get_news_sentiment(self): 
        today, start = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=start, end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        return news 
        
    def onTrade(self): 
        cash, last_price, quantity = self.position_sizing
        news = self.get_news()
        
        if cash > last_price: 
            if self.last_trade == None: 
                order = self.create_order(
                    self.symbol, 
                    quantity,
                    10, 
                    "buy", 
                    type="bracket", 
                    take_profit_price = last_price*1.3, 
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade = "buy"
       
   
broker = Alpaca(ALPACA_CREDS)

strategy = TraderStrat(name='Trader1', broker=broker, parameters={"symbol": "SPY", 
                                                             "cash_at_risk": .5})

start_date = datetime(2024, 6, 20)

end_date = datetime(2024, 7, 20)

strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters = {"symbol": "SPY", "cash_at_risk": .5}) 