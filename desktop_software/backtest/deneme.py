import requests

def get_binance_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        symbols = set()  # Coin isimlerini ve sembollerini tutmak için
        for symbol_info in data['symbols']:
            base_asset = symbol_info['baseAsset']
            quote_asset = symbol_info['quoteAsset']
            symbols.add(base_asset)
            symbols.add(quote_asset)
        return sorted(symbols)
    else:
        print(f"Error: {response.status_code}")
        return None

# Kullanım
coins = get_binance_symbols()
if coins:
    print(f"{len(coins)} coin bulundu:")
    for coin in coins:
        print(coin)
