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

# 'backtest_strategy' tablosunda 'code' sütunundaki verileri çekme
cursor.execute("SELECT code FROM backtest_strategy WHERE user_id = 3")
codes = cursor.fetchall()

# 'codes' listesi içinde tek sütun olduğundan veri[0] olarak yazdırabiliriz
for code in codes:
    user_code = code[0]
    #print(code[0])

print(user_code)

# Bağlantıyı kapatma
conn.close()


def execute_user_code(user_code, data):
    # user_code: Kullanıcının yazdığı strateji kodu (string formatında)
    local_vars = {"data": data}
    exec(user_code, {}, local_vars)
    strategy_instance = local_vars["UserStrategy"](data)  # Kullanıcı strateji sınıfı örneği
    return strategy_instance.generate_signals()
