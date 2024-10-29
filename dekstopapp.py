import sqlite3

# Veritabanı dosyasının yolunu belirtin
db_path = 'D:/InvestProjectSession1/djangoProject/investapp/db.sqlite3'

# Veritabanına bağlanma
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 'backtest_indicator' tablosundaki tüm verileri çekme
cursor.execute("SELECT * FROM backtest_indicator WHERE user_id = 3")
veriler = cursor.fetchall()

# Verileri yazdırma
for veri in veriler:
    print(veri)


# Bağlantıyı kapatma
conn.close()