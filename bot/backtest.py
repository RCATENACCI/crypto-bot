import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

def run_directional_backtest(df: pd.DataFrame, strategy, start: str, end: str, buffer: int = 200) -> pd.DataFrame:
    """
    Run a binary directional backtest (1 = buy, 0 = short), with Sharpe Ratio.

    Returns:
        results (pd.DataFrame): All signals and returns
        sharpe (float): Sharpe ratio of the strategy (risk-free = 0)
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Subset with buffer
    start_idx = df.index[df["timestamp"] >= pd.to_datetime(start)][0]
    df = df.iloc[start_idx - buffer:]

    signals, dates, closes = [], [], []

    for i in range(buffer, len(df)):
        window = df.iloc[i - buffer : i + 1].copy()
        signal = strategy.generate_signal(window)
        signals.append(signal)
        dates.append(df.iloc[i]["timestamp"])
        closes.append(df.iloc[i]["close"])

    results = pd.DataFrame({
        "timestamp": dates,
        "signal": signals,
        "close": closes
    })

    # Strategy logic: 1 = long, 0 = short
    results["position"] = results["signal"].map({"buy": 1, "sell": -1, "notrade": 0})
    results["return"] = results["close"].pct_change().shift(-1)
    results["strategy_return"] = results["position"] * results["return"]

    results["cumulative_strategy"] = (1 + results["strategy_return"]).cumprod()
    results["cumulative_market"] = (1 + results["return"]).cumprod()

    # Compute Sharpe ratio (risk-free = 0)
    mean_return = results["strategy_return"].mean()
    std_return = results["strategy_return"].std()
    periods_per_year = 96 * 252  # 15min candles
    sharpe_ratio = (mean_return / std_return) * np.sqrt(periods_per_year)

    print(f"🔍 Sharpe Ratio (risk-free=0): {sharpe_ratio:.4f}")

    return results, sharpe_ratio
