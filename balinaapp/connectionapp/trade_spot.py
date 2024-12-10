from binance.client import Client
from decimal import Decimal

def trade_crypto(api_key, api_secret, dolar_miktari, parite, islem_turu):
    """
    Binance API kullanarak belirtilen miktarda bir pariteyi satın almak veya satmak için bir piyasa emri oluşturur.

    Args:
        api_key (str): Binance API anahtarı.
        api_secret (str): Binance API gizli anahtarı.
        dolar_miktari (float): İşlem miktarı (USDT).
        parite (str): İşlem yapılacak paritenin sembolü (örn: "SNXUSDT").
        islem_turu (str): "buy" (satın alma) veya "sell" (satış).

    Returns:
        dict: Emir oluşturma sonucunu döndürür veya hata mesajını içeren bir sözlük döner.
    """
    try:
        # Binance Client oluştur
        client = Client(api_key, api_secret)

        # Güncel fiyatı al
        fiyat = float(client.get_symbol_ticker(symbol=parite)['price'])
        print(f"Güncel fiyat: {fiyat}")

        # İşlem miktarını hesapla
        if islem_turu == "buy":
            miktar = dolar_miktari / fiyat
        elif islem_turu == "sell":
            miktar = dolar_miktari  # Satışta miktar direkt olarak girilir
        else:
            raise ValueError("Geçersiz işlem türü. 'buy' veya 'sell' olmalıdır.")

        # Sembol bilgilerini al
        symbol_info = client.get_symbol_info(parite)

        for filtre in symbol_info['filters']:
            if filtre['filterType'] == 'LOT_SIZE':
                step_size = float(filtre['stepSize'])
                min_qty = float(filtre['minQty'])
                max_qty = float(filtre['maxQty'])
                break

        # Miktarı step_size'a göre yuvarla
        def round_step_size(quantity, step_size):
            step_size = Decimal(str(step_size))
            quantity = Decimal(str(quantity))
            return float((quantity // step_size) * step_size)

        miktar_fixed = round_step_size(miktar, step_size)

        # Sınır kontrolü
        if miktar_fixed < min_qty:
            miktar_fixed = min_qty
        elif miktar_fixed > max_qty:
            miktar_fixed = max_qty

        # İşlem emri gönder
        if islem_turu == "buy":
            order = client.order_market_buy(
                symbol=parite, 
                quantity=miktar_fixed
            )
        elif islem_turu == "sell":
            order = client.order_market_sell(
                symbol=parite,
                quantity=miktar_fixed
            )

        print(f"{islem_turu.capitalize()} emri başarıyla oluşturuldu: {order}")
        return order

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return {"error": str(e)}