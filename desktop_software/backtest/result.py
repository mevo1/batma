import pandas as pd
import numpy as np

def result(df,symbols,first_margin):
    last_margin = last_margin_fonks(df,symbols,first_margin)
    total_return = total_return_fonks(last_margin,first_margin)
    
    process_count = process_count_fonks(df,symbols)
    profit_process_count = profit_process_count_fonks(df,symbols)
    
    #print(df["BTC-USD"]["Position"])
    #print(df["BTC-USD"]["Cumprod"])
    #print(df["DOGE-USD"]["deger"])
    #loss_process_count = 

    printer(last_margin,total_return,process_count,profit_process_count)


def last_margin_fonks(df,symbols,first_margin):
    totals = 0
    for symbol in symbols:
        total_return = df[symbol]['Total_Returns'].iloc[-1]
        totals = totals + total_return
    totals = totals/len(symbols)
    return first_margin * totals

def total_return_fonks(last_margin,first_margin):
    return last_margin - first_margin

def process_count_fonks(df,symbols):
    count = 0
    for symbol in symbols:
        count = count + (df[symbol]["Group"].max())/2
    return count

def profit_process_count_fonks(df,symbols):
    count = 0
    for symbol in symbols:
        df[symbol]["Last_Deger"] = ((df[symbol]["Position"] == 0) & (df[symbol]["Position"].shift(1) !=0)).shift(-1)
        df[symbol].loc[df[symbol].index[-1],"Last_Deger"] = df[symbol]["Position"].iloc[-1] != 0

        count += df[symbol][(df[symbol]['Last_Deger'] == True) & (df[symbol]['Cumprod'] > 0)].shape[0]

    return count





def printer(last_margin,total_return,process_count,profit_process_count):
    print(f"Portföy Son Büyüklüğü: {last_margin:.0f} USD")
    print(f"Toplam Kar/Zarar:      {total_return:.0f} USD")
    print(f"Total İşlem Sayısı:    {process_count:.0f} ADET")
    print(f"Karlı İşlem Sayısı:    {profit_process_count:.0f} ADET")

