import yfinance as yf
import pandas as pd
import re

# 設定代號與下載參數
symbol = "^IXIC"
start_date = "2025-04-01"
end_date = "2025-04-30"

# 下載 30 分鐘 NASDAQ 資料
data = yf.download(symbol, start=start_date, end=end_date, interval="30m", auto_adjust=False)

# 去除代號中的特殊符號，作為檔名
filename = re.sub(r'[^A-Za-z0-9]+', '', symbol) + ".csv"

# 輸出為 CSV
data.to_csv(filename)

print(f"資料已儲存為：{filename}")
print(data.tail())
