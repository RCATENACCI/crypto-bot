import pandas as pd

class SimpleMovingAverageStrategy:
    def __init__(self, window=14):
        self.window = window

    def generate_signal(self, prices: pd.Series) -> str:
        sma = prices.rolling(window=self.window).mean()
        if prices.iloc[-1] > sma.iloc[-1]:
            return "buy"
        elif prices.iloc[-1] < sma.iloc[-1]:
            return "sell"
        else:
            return "hold"

class WeightedStrategy:
    def __init__(self, indicators: list, weights: list[float], thresholdhigh=0.65, thresholdlow=0.35):
        assert len(indicators) == len(weights), "Indicators and weights must match."
        self.indicators = indicators
        self.weights = weights
        self.thresholdhigh = thresholdhigh
        self.thresholdlow= thresholdlow

    def generate_signal(self, data: pd.DataFrame) -> str:
        scores = [w * ind.signal(data) for ind, w in zip(self.indicators, self.weights)]
        total = sum(scores)

        if total > self.thresholdhigh:
            return "buy"
        elif total< self.thresholdlow:
            return "sell"
        else: 
            return "notrade"
        
