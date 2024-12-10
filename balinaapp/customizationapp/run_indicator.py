
code = """def balina_indicator():
    global close
    global 
    # Fiyat değişimlerini hesapla
    delta = close.diff()
    
    # Kazanç ve kayıp serilerini ayır
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    # Ortalama kazanç ve kayıp (EWMA kullanarak)
    avg_gain = pd.Series(gain).rolling(window=period, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=period, min_periods=1).mean()
    
    # RS ve RSI hesapla
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    RSI = pd.DataFrame({"RSI": rsi.values},index=close.index)
    
    return RSI"""

def run_indicator(data,code):
