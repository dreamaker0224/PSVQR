import yfinance as yf
import pandas_ta as ta

# 下載歷史資料
data = yf.download("^GSPC", start="2023-08-01", end="2023-09-01", auto_adjust=False)

# 計算 RSI
data['RSI'] = ta.rsi(data['Close'], length=14)

# 計算 MACD（DataFrame 方法，不會回傳 None）
macd_df = data.ta.macd(fast=12, slow=26, signal=9)
data = pd.concat([data, macd_df], axis=1)

print(data.tail())
