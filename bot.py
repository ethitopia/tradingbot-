from lumibot.brokers import Alpaca 
from lumibot.backtesting import YahooDataBacktesting 
from lumibot.strategies.strategy import Strategy 
from lumibot.traders import Trader 
from datetime import datetime 

API_KEY = ""
API_SECRET = "" 
BASE_URL = "" 

ALPACA_CREDS = { 
                "API_KEY": API_KEY, 
                "API_SECRET": API_SECRET,
                "PAPER": True
}

class Trader(Strategy):
    def initialize(self, s: str = "SPY"): 
        self.spy = s
        self.sleeptime = "24H" #frequency of trade
        self.last_trade = None 
       
    def onTrade(self): 
        if self.last_trade == None: 
            order = self.create_order(
                self.symbol, 
                10, 
                "buy", 
                type="market"
            )
            self.submit_order(order)
            self.last_trade = "buy"
            
       
   
broker = Alpaca(ALPACA_CREDS)

strategy = Trader(name='Trader1', broker=broker, parameters={})

start_date = datetime(2024, 6, 20)

end_date = datetime(2024, 7, 20)

strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters()
    
) 