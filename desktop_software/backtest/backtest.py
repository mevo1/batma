import sqlite3
import sys
from pathlib import Path
import yfinance as yf

# Üst dizine erişim sağlama
sys.path.append(str(Path(__file__).resolve().parent.parent))

# variables.py dosyasından db_path'i içeri aktarma
from variables import db_path

# Veritabanına bağlanma
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 'backtest_strategy' tablosunda 'code' sütunundaki verileri çekme
cursor.execute("SELECT code FROM backtest_strategy WHERE user_id = 3")
codes = cursor.fetchall()

# 'codes' listesi içinde tek sütun olduğundan veri[0] olarak yazdırabiliriz
for code in codes:
    user_code = code[0]
    #print(code[0])

#print(user_code)

# Bağlantıyı kapatma
conn.close()

def fetch_data(symbol, start_date, end_date):
    # Yahoo Finance API'den veri çekme
    data = yf.download(symbol, start=start_date, end=end_date)
    return data


# Kullanıcı fonksiyonlarını çağırma
symbol = "BTC-USD"
start_date = "2023-01-01"
end_date = "2024-11-01"

# Kullanıcıdan veri çek
data = fetch_data(symbol, start_date, end_date)
exec(user_code)
backtest_data = strategy(data)

# Basit bir backtest analizi: kar/zarar hesaplama
backtest_data['Position'] = backtest_data['Signal'].shift()
backtest_data['Returns'] = backtest_data['Close'].pct_change()
backtest_data['Strategy_Returns'] = backtest_data['Position'] * backtest_data['Returns']

# Toplam kar/zarar
total_return = (1 + backtest_data['Strategy_Returns']).cumprod().iloc[-1]

print(backtest_data['Position'])
print(backtest_data['Strategy_Returns'])


print("Toplam Getiri:", total_return)

