import sqlite3
import sys
from pathlib import Path

# Üst dizine erişim sağlama
sys.path.append(str(Path(__file__).resolve().parent.parent))

# variables.py dosyasından db_path'i içeri aktarma
from variables import db_path

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