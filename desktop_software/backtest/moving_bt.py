import pandas as pd
import numpy as np

def main_moving(df):
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

    if "ZararDur" in df.columns:
        df["ZararDur"] = 1-df["ZararDur"]/100

    df = cumprod_tp(df)

    df = cumprod_ls(df)

    #cumprodı en yüksek olanı yaz

    if "KarAl" in df.columns:
        df["Position"] = changerKarAl(df)

    if "ZararDur" in df.columns:
        df["Position"] = changerZararDur(df)

    # merged = pd.concat([df["KarAl"],df["ZararDur"],df["Close"],df["Cumprod"],df["Cumprod_tp_cumsum"],df["Cumprod_ls_cumsum"]], axis=1)

    # print(merged)

    df = df.drop(columns=["Dependency","Group","Cumprod","Cumprod_tp_cumsum","Cumprod_ls_cumsum"])

    return df

def cumprod_tp(df):
    df["Cumprod_tp_cumsum"] = df["Cumprod"] - 1
    for index, row in df.iterrows():
        if(row["Cumprod_tp_cumsum"]<0):
            df.at[index, "KarAl"] = row["KarAl"] - row["Cumprod_tp_cumsum"]
    return df

def cumprod_ls(df):
    df["Cumprod_ls_cumsum"] = df["Cumprod"] - 1
    for index, row in df.iterrows():
        if(row["Cumprod_ls_cumsum"]>0):
            df.at[index, "ZararDur"] = row["ZararDur"] + row["Cumprod_ls_cumsum"]
    return df

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