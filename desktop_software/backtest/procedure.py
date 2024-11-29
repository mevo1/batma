import pandas as pd
import numpy as np

def procedure(backtest_dict,position_change_list,i):
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
                if(position_diff<abs(position_list2[k])):
                    if(position_list2[k]<0):
                        position_list2[k]= (-1) * position_diff
                    else:
                        position_list2[k]=position_diff
                    position_diff = 0.0
                else:
                    position_diff = position_diff - abs(position_list2[k])
            elif(position_list1[k]>position_list2[k]):
                if(position_diff<abs(position_list2[k])):
                    if(position_list2[k]<0):
                        position_list2[k]= (-1) * position_diff
                    else:
                        position_list2[k]=position_diff
                    position_diff = 0.0
                else:
                    position_diff = position_diff - abs(position_list2[k])
            elif(position_list1[k]<position_list2[k]):
                if(position_diff<abs(position_list2[k])):
                    if(position_list2[k]<0):
                        position_list2[k]= (-1) * position_diff
                    else:
                        position_list2[k]=position_diff
                    position_diff = 0.0
                else:
                    position_diff = position_diff - abs(position_list2[k])
        else:
            position_list2[k] = 0.0

    while(True): # verileri dictionarye yerleştirme.
        for k in range(len(backtest_dict)):
            date_label = backtest_dict[ticker_list[k]].index[i]
            try:
                backtest_dict[ticker_list[k]].loc[date_label, "Position"] = position_list2[k]
            except KeyError as e:
                print(f"KeyError: {e} - Possible issue with the ticker {ticker_list[k]} or date {date_label}.")
            except IndexError as e:
                print(f"IndexError: {e} - Index out of range for ticker list or position list.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        i+=1
        if(i == (len(position_change_list))):
            break
        if(position_change_list["Dependency"][i]==True):
            if (i != (len(position_change_list)-1)):
                break
    return backtest_dict, i

