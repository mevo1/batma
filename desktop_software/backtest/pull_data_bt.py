# database'den veriler
symbols = {"BTC-USD","ETC-USD","DOGE-USD"}
start_date = "2024-09-28"   
end_date = "2024-10-28"
interval = "1d"
moving_tp = True
moving_sl = True
commission = 0.001

# Kullanının kodunu al.
user_code = """
def strategy(data):
    data['30_MA'] = data['Close'].rolling(window=5).mean()
    
    data['KarAl'] = 5
    data['ZararDur'] = 5

    data['Signal'] = 0
    data['Signal'] = data['Signal'].astype("float64")
    data.loc[data['Close'] > data['30_MA'], 'Signal'] = 0.25 
    return data
"""