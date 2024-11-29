import yfinance as yf
import pandas as pd
from datetime import datetime
from position_operate import *
from position_change_list import *
from procedure import *
from stops_bt import *
from moving_bt import *
pd.set_option('display.max_rows', None)

from pull_data_bt import symbols, start_date, end_date, interval, moving_tp, moving_sl, commission, user_code

# Verileri saklamak için dictionary
data_dict = {}
backtest_dict = {}
ticker_list = list(symbols)

def fetch_data(symbol, start_date, end_date,interval):
    # Yahoo Finance API'den veri çekme
    data = yf.download(symbol, start=start_date,end=end_date, interval=interval)
    return data

exec(user_code)  # Kullanıcı kodunu çalıştır.

for symbol in symbols: # indirme ve kodu çalıştırma işlemleri
    # Veri indirme
    data_dict[symbol] = fetch_data(symbol, start_date, end_date, interval)
    
    # Strateji uygulama
    backtest_dict[symbol] = strategy(data_dict[symbol])
    
    # Backtest hesaplamaları
    backtest_dict[symbol]['Position'] = backtest_dict[symbol]['Signal'].shift()

row_count = len(next(iter(backtest_dict.values())))

sum_position = sum_position(backtest_dict,row_count) # position_operate

filted_sum_position = position_filter(sum_position) # position_operate

position_change_list = position_change_list(backtest_dict,row_count)

merged_df1 = pd.concat(
    [backtest_dict[ticker]["Position"].rename(ticker) for ticker in ticker_list], 
    axis=1,
    sort=False
)

#print(merged_df1)

i = 0
while i < len(filted_sum_position["sum_position"]) - 1:
    if filted_sum_position["sum_position"].iloc[i] == 0:
        i += 1
        continue
    else:
        try:
            backtest_dict, i = procedure(backtest_dict, position_change_list, i)
        except KeyError as e:
            print(f"KeyError: {e} - Possible issue with the ticker or date.")
            break
        except IndexError as e:
            print(f"IndexError: {e} - Index out of range for ticker list or position list.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
        

merged_df2 = pd.concat(
    [backtest_dict[ticker]["Position"].rename(ticker) for ticker in ticker_list], 
    axis=1,
    sort=False
)

merged_df = pd.concat([merged_df1, merged_df2], axis=1)

totals = 0

for symbol in symbols:
    backtest_dict[symbol]['Returns'] = backtest_dict[symbol]['Open'].pct_change()
    backtest_dict[symbol]['Strategy_Returns'] = (backtest_dict[symbol]['Position'] * backtest_dict[symbol]['Returns']) - (commission * abs(backtest_dict[symbol]['Position'].diff()))
    
    if moving_tp == True or moving_sl == True:
        if moving_tp == True and "KarAl" not in backtest_dict[symbol].columns:
            print("Kar Al Kolonunuz Yok")
        if moving_sl == True and "ZararDur" not in backtest_dict[symbol].columns:
            print("Zarar Durdur Kolonunuz Yok")

        backtest_dict[symbol] = main_moving(backtest_dict[symbol])

    # Ts/Sl
    elif "KarAl" in backtest_dict[symbol].columns or "ZararDur" in backtest_dict[symbol].columns:
        backtest_dict[symbol]['Position'] = main_stops(backtest_dict[symbol])
        backtest_dict[symbol]['Position'] = backtest_dict[symbol]['Position'].fillna(0)
        backtest_dict[symbol]['Strategy_Returns'] = (backtest_dict[symbol]['Position'] * backtest_dict[symbol]['Returns']) - (commission * abs(backtest_dict[symbol]['Position'].diff()))

    total_return = (1+ backtest_dict[symbol]['Strategy_Returns']).cumprod().iloc[-1]
    totals += (total_return-1)

    print(symbol, "Getiri:", total_return)

print("Toplam Getiri:", totals+1)



