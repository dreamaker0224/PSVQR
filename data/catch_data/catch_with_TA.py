import yfinance as yf
import pandas as pd
import numpy as np
import re
import os

# === 設定代號與下載參數 (S&P 500) ===
symbol = "PLTR"
start_date = "2023-09-01"
end_date = "2025-08-29"

# === 下載日線資料 ===
data = yf.download(symbol, start=start_date, end=end_date, interval="1d", auto_adjust=False)

# === 計算技術指標 ===
# 1. SMA (Simple Moving Average)
data['SMA_20'] = data['Close'].rolling(window=20).mean()

# 2. WMA (Weighted Moving Average)
def WMA(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)

data['WMA_20'] = WMA(data['Close'], 20)

# 3. RSI (Relative Strength Index)
def RSI(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI_14'] = RSI(data['Close'], 14)

# 4. ATR (Average True Range)
high_low = data['High'] - data['Low']
high_close = (data['High'] - data['Close'].shift()).abs()
low_close = (data['Low'] - data['Close'].shift()).abs()
tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
data['ATR_14'] = tr.rolling(14).mean()

# === 取得當前 .py 檔所在資料夾 ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# 去除代號中的特殊符號，作為檔名
filename = re.sub(r'[^A-Za-z0-9]+', '', symbol) + "_daily_indicators.csv"
output_path = os.path.join(script_dir, filename)

# === 輸出為 CSV ===
data.to_csv(output_path)

print(f"✅ 資料已儲存為：{output_path}")
print(data.tail())
