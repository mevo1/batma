import pandas as pd
import numpy as np

def position_change_list(backtest_dict, row_count):
    positions = pd.DataFrame(
        index=range(row_count),  # Satır sayısı, Position'un uzunluğu kadar
    )

    for ticker,df in sorted(backtest_dict.items()):
        positions[ticker] = backtest_dict[ticker]["Position"].reset_index(drop=True)
        positions[f'{ticker} Dependency'] = positions[ticker].diff().fillna(0) != 0    

    positions["Dependency"] = positions[f"{next(iter(backtest_dict))} Dependency"]
    positions["Dependency"] = False

    for ticker,df in sorted(backtest_dict.items()):
        positions["Dependency"] = positions["Dependency"] | positions[f"{ticker} Dependency"]
        positions = positions.drop(columns=ticker)
        positions = positions.drop(columns=[f"{ticker} Dependency"])

    return positions



