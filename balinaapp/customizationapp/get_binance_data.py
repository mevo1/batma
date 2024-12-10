import requests
import pandas as pd
from datetime import datetime, timedelta

def get_binance_data(symbol="BTCUSDT", interval="1h", period="30d"):

    """
    Binance API'den belirtilen sembol, zaman aralığı ve periyoda göre veri çeker.

    Args:
        symbol (str): Kripto para sembolü (örn: "BTCUSDT").
        interval (str): Zaman aralığı (örn: "1h", "1d").
        period (str): Geçmiş veri süresi (örn: "7d" = 7 gün, "30d" = 30 gün).

    Returns:
        pd.DataFrame: Zaman ve kapanış fiyatı içeren DataFrame.
    """

    # Zaman aralığını saniye cinsine çevir
    interval_mapping = {
        "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
        "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "8h": 28800,
        "12h": 43200, "1d": 86400, "3d": 259200, "1w": 604800
    }

    if interval not in interval_mapping:
        raise ValueError("Geçersiz zaman aralığı (interval).")

    # Periyodu gün cinsine çevir
    period_value = int(period[:-1])
    period_unit = period[-1]
    if period_unit == "d":
        days = period_value
    elif period_unit == "w":
        days = period_value * 7
    else:
        raise ValueError("Geçersiz periyot (period) formatı. 'd' (gün) veya 'w' (hafta) kullanılmalı.")

    # Toplam limit hesaplama (Binance API'nin max limit = 1000)
    total_seconds = days * 86400
    interval_seconds = interval_mapping[interval]
    limit = min(total_seconds // interval_seconds, 1000)

    # Binance API isteği
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Verileri DataFrame'e dönüştür
    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    df["time"] = pd.to_datetime(df["time"], unit="ms")
    
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

    df["open"] = df["open"].astype(float)
    df["close"] = df["close"].astype(float)

    df["volume"] = df["volume"].astype(float)

    return df[["time", "high", "low", "open", "close", "volume"]]

