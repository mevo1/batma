# Kullanıcının kodunu yazabileceği bir şablon yapı
user_code = """
import yfinance as yf

def fetch_data(symbol, start_date, end_date):
    # Yahoo Finance API'den veri çekme
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def strategy(data):
    # Basit bir strateji: Fiyat 50 günlük ortalamanın üstünde ise satın al
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['Signal'] = 0
    data.loc[data['Close'] > data['50_MA'], 'Signal'] = 1
    return data
"""

exec(user_code)  # Güvenlik kontrolünden sonra kodu çalıştırın


import pandas as pd
from datetime import datetime

# Kullanıcı fonksiyonlarını çağırma
symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2023-01-01"

# Kullanıcıdan veri çek
data = fetch_data(symbol, start_date, end_date)

# Kullanıcının stratejisini uygula
backtest_data = strategy(data)

# Basit bir backtest analizi: kar/zarar hesaplama
backtest_data['Position'] = backtest_data['Signal'].shift()
backtest_data['Returns'] = backtest_data['Close'].pct_change()
backtest_data['Strategy_Returns'] = backtest_data['Position'] * backtest_data['Returns']

# Toplam kar/zarar
total_return = (1 + backtest_data['Strategy_Returns']).cumprod().iloc[-1]
print("Toplam Getiri:", total_return)
