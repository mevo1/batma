import yfinance as yf
import pandas as pd
from datetime import datetime
from position_operate import *
from position_change_list import *
from procedure import *
pd.set_option('display.max_rows', None)

# Seçili (indirilmesi gereken) verileri indirme.
symbols = {"BTC-USD","ETC-USD","DOGE-USD","ETH-USD","XRP-USD","SHIB-USD"}
start_date = "2024-10-01"   
end_date = "2024-11-01"

# Verileri saklamak için dictionary
data_dict = {}
backtest_dict = {}
ticker_list = list(symbols)

def fetch_data(symbol, start_date, end_date):
    # Yahoo Finance API'den veri çekme
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Kullanının kodunu al.
user_code = """
def strategy(data):
    data['14_RSI'] = basic_rsi(data['Close'], period = 14)
    data['14_RSI_10_MA'] = data['14_RSI'].rolling(window=10).mean()
    data['FARK_14_RSI_10_MA'] = data['14_RSI_10_MA'].diff()

    data['Signal'] = 0
    data['Signal'] = data['Signal'].astype("float64")

    current_signal = 0.0

    for i in range(len(data)):
        fark_value = data.loc[data.index[i], 'FARK_14_RSI_10_MA']
        if fark_value > 3:
            current_signal = 0.25
        elif fark_value < -4:
            current_signal = 0
        data.loc[data.index[i], 'Signal'] = current_signal

    return data

def basic_rsi(close, period=14):
    # Fiyat değişimlerini hesapla
    delta = close.diff()
    
    # Kazanç ve kayıp serilerini ayır
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    # Ortalama kazanç ve kayıp (EWMA kullanarak)
    avg_gain = pd.Series(gain).rolling(window=period, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=period, min_periods=1).mean()
    
    # RS ve RSI hesapla
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    RSI = pd.DataFrame({"RSI": rsi.values},index=close.index)
    
    return RSI
"""

exec(user_code)  # Kullanıcı kodunu çalıştır.

for symbol in symbols: # indirme ve kodu çalıştırma işlemleri
    # Veri indirme
    data_dict[symbol] = fetch_data(symbol, start_date, end_date)
    
    # Strateji uygulama
    backtest_dict[symbol] = strategy(data_dict[symbol])
    
    # Backtest hesaplamaları
    backtest_dict[symbol]['Position'] = backtest_dict[symbol]['Signal'].shift()

row_count = len(next(iter(backtest_dict.values())))

sum_position = sum_position(backtest_dict,row_count)

filted_sum_position = position_filter(sum_position)

position_change_list = position_change_list(backtest_dict,row_count)

merged_df1 = pd.concat(
    [backtest_dict[ticker]["Position"].rename(ticker) for ticker in ticker_list], 
    axis=1,
    sort=False
)

for i in range(len(filted_sum_position["sum_position"])-1): # 1'den büyük olanları 
    print(f"for i: {i}")
    if(filted_sum_position["sum_position"].iloc[i] == 0):
        pass
    else:
        backtest_dict,a = procedure(backtest_dict,position_change_list,i)
        i+=a
        

merged_df2 = pd.concat(
    [backtest_dict[ticker]["Position"].rename(ticker) for ticker in ticker_list], 
    axis=1,
    sort=False
)

merged_df = pd.concat([merged_df1, merged_df2], axis=1)

print(merged_df)

totals = 0

for symbol in symbols:
    backtest_dict[symbol]['Returns'] = backtest_dict[symbol]['Close'].pct_change()
    backtest_dict[symbol]['Strategy_Returns'] = (backtest_dict[symbol]['Position'] * backtest_dict[symbol]['Returns'])

    total_return = (1+ backtest_dict[symbol]['Strategy_Returns']).cumprod().iloc[-1]
    totals += (total_return-1)
    print(symbol, "Getiri:", total_return)

print("Toplam Getiri:", totals+1)



