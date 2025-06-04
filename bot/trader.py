import time
import pandas as pd
from binance.client import Client
import csv
import os
from datetime import datetime


class Trader:
    def __init__(self, strategy, config):
        self.strategy = strategy
        self.client = Client(config["api_key"], config["api_secret"])
        self.symbol = config["symbol"]
        self.interval = config["interval"]
        self.quantity = config["quantity"]
        self.test_mode = config.get("test_mode", True)

    def fetch_prices(self, limit=100):
        klines = self.client.get_klines(symbol=self.symbol, interval=self.interval, limit=limit)
        closes = [float(kline[4]) for kline in klines]  # Closing prices
        return pd.Series(closes)

    def run(self):
        while True:
            try:
                prices = self.fetch_prices()
                signal = self.strategy.generate_signal(prices)
                print(f"{datetime.now()} - Strategy signal: {signal.upper()}")

                # Log the signal
                self.log_signal(signal, prices.iloc[-1])

                if not self.test_mode:
                    self.execute_trade(signal)

                time.sleep(60)
            except Exception as e:
                self.log_error(e)
                time.sleep(60)


    def execute_trade(self, signal):
        if signal == "buy":
            print("Placing BUY order...")
            # self.client.order_market_buy(symbol=self.symbol, quantity=self.quantity)
        elif signal == "sell":
            print("Placing SELL order...")
            # self.client.order_market_sell(symbol=self.symbol, quantity=self.quantity)

    def log_signal(self, signal, price):
        log_file = "trade_log.csv"
        file_exists = os.path.isfile(log_file)

        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["timestamp", "symbol", "signal", "price"])
            writer.writerow([datetime.now(), self.symbol, signal, price])

    def log_error(self, error):
        with open("error_log.txt", mode='a') as file:
            file.write(f"{datetime.now()} - ERROR: {str(error)}\n")
