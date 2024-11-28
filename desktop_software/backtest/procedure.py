import pandas as pd
import numpy as np

def procedure(backtest_dict,position_change_list,i):
    k=i
    position_list01 = []
    position_list02 = []
    ticker_list=[]

    for ticker,df in sorted(backtest_dict.items()):
        ticker_list.append(ticker) 
        position_list01.append(float(backtest_dict[ticker]["Position"].iloc[i-1]))
        position_list02.append(float(backtest_dict[ticker]["Position"].iloc[i]))

    position_list1 = list(position_list01)
    position_list2 = list(position_list02)

    position_diff = 1

    for k in range(len(backtest_dict)): # alım miktarını % 100 ile sınırlama
        if(position_diff != 0):
            if (position_list1[k]==position_list2[k]):
                if(position_diff<position_list2[k]):
                    position_list2[k]=position_diff
                    position_diff = 0.0
                else:
                    position_diff = position_diff - position_list2[k]

            elif(position_list1[k]>position_list2[k]):
                if(position_diff<position_list2[k]):
                    position_list2[k]=position_diff
                    position_diff = 0.0
                else:
                    position_diff = position_diff - position_list2[k]
            elif(position_list1[k]<position_list2[k]):
                if(position_diff<position_list2[k]):
                    position_list2[k]=position_diff
                    position_diff = 0.0
                else:
                    position_diff = position_diff - position_list2[k]
        else:
            position_list2[k] = 0.0

    while(True): # verileri dictionarye yerleştirme.
        print(f"Current index i: {i}, DataFrame size: {backtest_dict[ticker_list[k]].shape[0]}, Poisiton: {position_change_list["Dependency"][i]}")
        for k in range(len(backtest_dict)):
            backtest_dict[ticker_list[k]].loc[backtest_dict[ticker_list[k]].index[i], "Position"] = position_list2[k]
        i+=1
        if(i == (len(position_change_list))):
            print("Break over")
            break
        if(position_change_list["Dependency"][i]==True):
            print("Break true")
            if (i != (len(position_change_list)-1)):
                break
    
    a= i-k

    return backtest_dict, a

