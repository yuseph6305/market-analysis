import pandas as pd
import numpy as np


def load_data(path: str) -> pd.DataFrame:
    """
    Load CSV or Parquet into a DataFrame with proper dtypes.
    Does not add features — just loads and ensures timestamp parsing.
    """
    if path.lower().endswith(".parquet"):
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path, parse_dates=["timestamp"])

    # Ensure timestamp column is datetime
    if "timestamp" in df and not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute engineered features:
    - mid price
    - spread and spread in basis points
    - return by symbol
    """
    df = df.sort_values(["symbol", "timestamp"]).copy()
    df["mid"] = (df["bid"] + df["ask"]) / 2.0
    df["spread"] = df["ask"] - df["bid"]
    df["spread_bps"] = (df["spread"] / df["mid"]) * 10000
    df["ret"] = df.groupby("symbol")["mid"].pct_change().fillna(0.0)
    return df


def resample_agg(df: pd.DataFrame, freq: str = "1min") -> pd.DataFrame:
    """
    Resample to frequency by symbol with common KPIs.
    """
    g = (
        df.set_index("timestamp")
        .groupby("symbol")
        .resample(freq)
    )
    out = g.agg(
        mid_mean=("mid", "mean"),
        mid_last=("mid", "last"),
        spread_mean=("spread", "mean"),
        spread_bps_mean=("spread_bps", "mean"),
        ticks=("mid", "count"),
        size_sum=("size", "sum"),
        vol=("ret", lambda s: (s.std(ddof=0) * np.sqrt(60 * 6)) if len(s) > 1 else 0.0),
    ).reset_index()
    return out


def rolling_metrics(df: pd.DataFrame, window: int = 60) -> pd.DataFrame:
    """
    Rolling metrics over seconds (or base cadence):
    - rolling mean spread (bps)
    - rolling volatility of returns
    """
    df = df.copy()
    df["roll_spread_bps"] = (
        df.groupby("symbol")["spread_bps"]
        .transform(lambda s: s.rolling(window, min_periods=1).mean())
    )
    df["roll_vol"] = (
        df.groupby("symbol")["ret"]
        .transform(lambda s: s.rolling(window, min_periods=2).std(ddof=0))
    )
    return df


def distribution_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Distribution stats per symbol for spread (bps) and size.
    """
    stats = (
        df.groupby("symbol")
        .agg(
            spread_bps_mean=("spread_bps", "mean"),
            spread_bps_p95=("spread_bps", lambda s: s.quantile(0.95)),
            spread_bps_p99=("spread_bps", lambda s: s.quantile(0.99)),
            size_mean=("size", "mean"),
            size_p95=("size", lambda s: s.quantile(0.95)),
            ticks=("mid", "count"),
        )
        .reset_index()
    )
    return stats


def detect_outliers(df: pd.DataFrame, z: float = 4.0) -> pd.DataFrame:
    """
    Flag spread outliers by simple z-score per symbol.
    """
    df = df.copy()

    def z_flag(s):
        mu, sd = s.mean(), s.std(ddof=0)
        if sd == 0:
            return pd.Series([False] * len(s), index=s.index)
        return (abs((s - mu) / sd) > z)

    df["spread_outlier"] = df.groupby("symbol")["spread_bps"].transform(z_flag)
    return df


def minute_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Produce a pivot table: minute of day x symbol -> mean spread_bps.
    """
    df = df.copy()
    df["minute_of_day"] = df["timestamp"].dt.hour * 60 + df["timestamp"].dt.minute
    piv = df.pivot_table(
        index="minute_of_day",
        columns="symbol",
        values="spread_bps",
        aggfunc="mean"
    )
    return piv
