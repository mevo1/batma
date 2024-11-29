import yfinance as yf

print(yf.download("BTC-USD",period="1mo",interval="1d"))
