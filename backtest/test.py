from lumibot.brokers import Alpaca 
from lumibot.backtesting import YahooDataBacktesting 
from datetime import datetime, timedelta
from lumibot.backtesting import Backtester
from lumibot.strategies.strategy import Strategy
from bot import TraderStrat, ALPACA_CREDS


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

def run_backtest():
    backtester = Backtester(
        strategy=strategy, 
        symbols=["AAPL"],  #backtest selection example 
        start=datetime(2023, 1, 1), 
        end=datetime.now(),  
        cash=100000  
    )
    backtester.run()


