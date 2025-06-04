import pandas as pd
import ta

# --- 1. Indicateurs techniques ---
def add_all_indicators(df):
    df = df.copy()

    # Trend indicators
    df["sma_14"] = ta.trend.SMAIndicator(close=df["close"], window=14).sma_indicator()
    df["ema_14"] = ta.trend.EMAIndicator(close=df["close"], window=14).ema_indicator()
    macd = ta.trend.MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()

    # Momentum indicators
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
    df["stoch_k"] = ta.momentum.StochasticOscillator(high=df["high"], low=df["low"], close=df["close"]).stoch()
    df["stoch_d"] = ta.momentum.StochasticOscillator(high=df["high"], low=df["low"], close=df["close"]).stoch_signal()
    df["roc"] = ta.momentum.ROCIndicator(close=df["close"], window=12).roc()

    # Volatility indicators
    atr = ta.volatility.AverageTrueRange(high=df["high"], low=df["low"], close=df["close"])
    df["atr"] = atr.average_true_range()
    boll = ta.volatility.BollingerBands(close=df["close"])
    df["bollinger_mavg"] = boll.bollinger_mavg()
    df["bollinger_hband"] = boll.bollinger_hband()
    df["bollinger_lband"] = boll.bollinger_lband()
    df["bollinger_width"] = boll.bollinger_wband()

    # Volume indicators
    df["obv"] = ta.volume.OnBalanceVolumeIndicator(close=df["close"], volume=df["volume"]).on_balance_volume()
    df["mfi"] = ta.volume.MFIIndicator(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"]).money_flow_index()

    # Statistical rolling features
    df["rolling_mean"] = df["close"].rolling(window=14).mean()
    df["rolling_std"] = df["close"].rolling(window=14).std()
    df["rolling_skew"] = df["close"].rolling(window=14).skew()
    df["rolling_kurt"] = df["close"].rolling(window=14).kurt()

    return df

# --- 2. Lag features sur le close ---
def add_lag_features(df, column="close", n_lags=4):
    for lag in range(1, n_lags + 1):
        df[f"{column}_lag{lag}"] = df[column].shift(lag)
    return df

# --- 3. Target multi-classe (-1, 0, 1) avec seuils de 0.1% ---
def add_classification_target(df, column="close", threshold=0.001):
    df["return_future"] = (df[column].shift(-1) - df[column]) / df[column]
    df["target"] = df["return_future"].apply(lambda x: 1 if x > 0 else 0 )
    return df

# --- 4. Enchaînement ---
def prepare_features(df):
    df = df.copy()
    cols_to_float = ["open", "high", "low", "close", "volume"]
    df[cols_to_float] = df[cols_to_float].astype(float)
    df = add_all_indicators(df)
    df = add_lag_features(df, column="close", n_lags=4)
    df = add_classification_target(df, column="close", threshold=0.001)
    df = df.dropna().reset_index(drop=True)
    return df


