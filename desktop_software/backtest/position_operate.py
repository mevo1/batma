import pandas as pd
import numpy as np

def sum_position(backtest_dict, row_count): # POZİSYON DEĞERLERİNİ TOPLAMA
    # Boş bir DataFrame oluşturuyoruz
    sum_position = pd.DataFrame(
        np.zeros((row_count, 1)),  # Zero ile doldur
        index=range(row_count),  # Satır sayısı, Position'un uzunluğu kadar
        columns=["sum_position"]  # Tek sütun adı
    )

    for ticker,df in sorted(backtest_dict.items()):
        sum_position["sum_position"] = sum_position["sum_position"] + backtest_dict[ticker]["Position"].reset_index(drop=True)

    return sum_position

def position_filter(sum_position):
    sum_position["sum_position"] = sum_position["sum_position"].where(
    (sum_position["sum_position"] > 1) | (sum_position["sum_position"] < -1), 0)
    return sum_position



