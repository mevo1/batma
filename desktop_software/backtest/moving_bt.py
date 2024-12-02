import pandas as pd
import numpy as np

def main_moving(df, moving_tp, moving_sl):
    
    # Returnsları grouplara ayırma.
    grouped = df.groupby("Group")["Returns"]

    # Her grubun kümülatif çarpımını yazma.
    for group_name, group_data in grouped:
        df[f"Cumprod {group_name}"] = (group_data+1).cumprod()

    # Cumproad kolonlarını tek sütunda toplama.
    cumprod_columns = [col for col in df.columns if col.startswith("Cumprod ")]
    df["Cumprod"] = df[cumprod_columns].bfill(axis=1).iloc[:, 0]

    # Cumprod alım olmayan yerleri sıfırlama. Group'un sıfır olduğu yerler.  
    df.loc[df["Group"] == 0, "Cumprod"] = float("nan")

    # Boş cumprod sütunlarını silme.
    df.drop(columns=cumprod_columns, inplace=True)

    # Kar al'ı yüzde olarak yapma.
    if "KarAl" in df.columns:
        df["KarAl"] = 1+df["KarAl"]/100

    # Zarar dur'u yüzde olarak yapma.
    if "ZararDur" in df.columns:
        df["ZararDur"] = 1-df["ZararDur"]/100

    # Yüzde değişimleri tutma.
    df["Cumprod"] = df["Cumprod"] - 1
    
    if (moving_tp == True):
        df = cumprod_tp(df)

    if (moving_sl == True):
        df = cumprod_ls(df)

    df["Cumprod"] = df["Cumprod"] + 1

    #cumprodı en yüksek olanı yaz
    if "KarAl" in df.columns:
        df["Position"] = changerKarAl(df)

    if "ZararDur" in df.columns:
        df["Position"] = changerZararDur(df)

    
    #merged = pd.concat([df["Position"],df["Dependency"],df["Returns"],df["KarAl"],df["ZararDur"],df["Group"],df["Close"],df["Cumprod"],df["Cumprod_ls"],df["Cumprod_tp"]], axis=1)
    #print(merged)

    df = df.drop(columns=["Dependency"])

    return df

def cumprod_tp(df):
    temp = 0.0
    cumprod_tp = []
    kar_al = []

    for _, row in df.iterrows():
        if pd.isna(row["Cumprod"]):
            cumprod_tp.append(None)
            temp = 0.0
        else:
            if row["Cumprod"] < temp:
                temp = row["Cumprod"]
            cumprod_tp.append(temp)
        
        # ZararDur hesaplama
        kar_al.append((row["KarAl"] if "KarAl" in row else 0) + (temp if temp else 0))
    
    df["Cumprod_tp"] = cumprod_tp
    df["KarAl"] = kar_al
    
    return df

def cumprod_ls(df):
    temp = 0.0
    cumprod_ls = []
    zarar_dur = []
    
    for _, row in df.iterrows():
        if pd.isna(row["Cumprod"]):
            cumprod_ls.append(None)
            temp = 0.0
        else:
            if row["Cumprod"] > temp:
                temp = row["Cumprod"]
            cumprod_ls.append(temp)
        
        # ZararDur hesaplama
        zarar_dur.append((row["ZararDur"] if "ZararDur" in row else 0) + (temp if temp else 0))
    
    df["Cumprod_ls"] = cumprod_ls
    df["ZararDur"] = zarar_dur
    
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