import pandas as pd
import joblib
import ta

class MLIndicator:
    def __init__(self, model_path: str, feature_names: list[str]):
        self.model = joblib.load(model_path)
        self.feature_names = feature_names

    def signal(self, data: pd.DataFrame) -> float:
        # Make sure features are present
        X = data[self.feature_names].copy()
        X = X.iloc[[-1]]  # Latest row only
        pred = self.model.predict(X)[0]
        return float(pred)  # 0 or 1



class RSIIndicator:
    def __init__(self, window=14, upper=70, lower=30):
        self.window = window
        self.upper = upper
        self.lower = lower

    def signal(self, data: pd.DataFrame) -> float:
        rsi = ta.momentum.RSIIndicator(close=data["close"], window=self.window).rsi().iloc[-1]
        if rsi > self.upper:
            return 0  # overbought → hold
        elif rsi < self.lower:
            return 1  # oversold → buy
        else:
            return 0.5  # neutral

class MACDIndicator:
    def __init__(self):
        self.macd = ta.trend.MACD

    def signal(self, data):
        macd = self.macd(close=data["close"])
        hist = macd.macd_diff().iloc[-1]
        return 1 if hist > 0 else 0

class BollingerIndicator:
    def __init__(self):
        self.boll = ta.volatility.BollingerBands

    def signal(self, data):
        bb = self.boll(close=data["close"])
        close = data["close"].iloc[-1]
        lower = bb.bollinger_lband().iloc[-1]
        return 1 if close < lower else 0.5

class ATRVolatilityIndicator:
    def __init__(self):
        self.atr = ta.volatility.AverageTrueRange

    def signal(self, data):
        atr = self.atr(high=data["high"], low=data["low"], close=data["close"]).average_true_range().iloc[-1]
        return 1 if atr > data["close"].rolling(14).std().iloc[-1] else 0

class StochasticKIndicator:
    def __init__(self):
        self.stoch = ta.momentum.StochasticOscillator

    def signal(self, data):
        stoch_k = self.stoch(data["high"], data["low"], data["close"]).stoch().iloc[-1]
        return 1 if stoch_k < 20 else 0 if stoch_k > 80 else 0.5

class ROCIndicator:
    def __init__(self):
        self.roc = ta.momentum.ROCIndicator

    def signal(self, data):
        value = self.roc(close=data["close"]).roc().iloc[-1]
        return 1 if value > 0 else 0

class OBVIndicator:
    def __init__(self):
        self.obv = ta.volume.OnBalanceVolumeIndicator

    def signal(self, data):
        obv = self.obv(data["close"], data["volume"]).on_balance_volume()
        return 1 if obv.iloc[-1] > obv.iloc[-2] else 0
class MFIIndicator:
    def __init__(self):
        self.mfi = ta.volume.MFIIndicator

    def signal(self, data):
        value = self.mfi(data["high"], data["low"], data["close"], data["volume"]).money_flow_index().iloc[-1]
        return 1 if value < 20 else 0 if value > 80 else 0.5
class RollingVolatilityIndicator:
    def signal(self, data):
        vol = data["close"].rolling(window=14).std().iloc[-1]
        return 1 if vol > data["close"].rolling(28).std().iloc[-1] else 0
class PriceMomentumIndicator:
    def signal(self, data):
        diff = data["close"].diff().rolling(5).sum().iloc[-1]
        return 1 if diff > 0 else 0
