import pandas as pd
import numpy as np

def main_stops(df):
    df["Dependency"] = df["Position"].fillna(0) != 0

    df["Group"] = (df["Dependency"] != df["Dependency"].shift()).cumsum() * df["Dependency"]

    grouped = df.groupby("Group")["Returns"]
    for group_name, group_data in grouped:
        df[f"Cumprod {group_name}"] = (group_data+1).cumprod()
        
    cumprod_columns = [col for col in df.columns if col.startswith("Cumprod ")]
    df["Cumprod"] = df[cumprod_columns].bfill(axis=1).iloc[:, 0]

    df.loc[df["Group"] == 0, "Cumprod"] = float("nan")

    df.drop(columns=cumprod_columns, inplace=True)
    
    if "KarAl" in df.columns:
        df["KarAl"] = 1+df["KarAl"]/100
        df["Position"] = changerKarAl(df)

    if "ZararDur" in df.columns:
        df["ZararDur"] = 1-df["ZararDur"]/100
        df["Position"] = changerZararDur(df)

    return df["Position"]

def changerKarAl(df):
    reset = False  # "Cumprod > KarAl" durumunu takip etmek için bir bayrak
    for index, row in df.iterrows():
        if (row["Cumprod"] > row["KarAl"]) & (reset == False):
            reset = True  # Koşul sağlanmaya başlandı
        elif reset:
            df.at[index, "Position"] = 0  # "Position" değerini sıfırla
        if row["Group"] == 0:
            reset = False  # "Group" değeri 0 olduğunda bayrağı sıfırla

    return df["Position"]

def changerZararDur(df):
    reset = False  # "Cumprod > KarAl" durumunu takip etmek için bir bayrak
    for index, row in df.iterrows():
        if (row["Cumprod"] < row["ZararDur"]) & (reset == False):
            reset = True  # Koşul sağlanmaya başlandı
        elif reset:
            df.at[index, "Position"] = 0  # "Position" değerini sıfırla
        if row["Group"] == 0:
            reset = False  # "Group" değeri 0 olduğunda bayrağı sıfırla
    return df["Position"]
    



