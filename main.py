from bot.trader import Trader
from bot.strategy import SimpleMovingAverageStrategy
from bot.utils import load_config

def main():
    config = load_config("config/config.yaml")
    strategy = SimpleMovingAverageStrategy(window=14)
    trader = Trader(strategy=strategy, config=config)
    trader.run()

if __name__ == "__main__":
    main()
