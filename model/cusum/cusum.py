import pandas as pd
import numpy as np
from datetime import datetime
import os

# 1. 讀取 Excel 數據
file_path = r"C:\NCNU\im\informs\PSVQR\experiment\price\tax_f2\tax_f2.xlsx"
sheet_name = "Dataset"

df = pd.read_excel(file_path, sheet_name=sheet_name)
prices = df['price'].values  # 讀取 price 欄位
dates = pd.to_datetime(df['Date']).values  # 讀取日期欄位

# 2. 定義 CUSUM 函數
def cusum(data, threshold=5, drift=0.0):
    S_pos = np.zeros(len(data))
    S_neg = np.zeros(len(data))
    change_points = []

    for t in range(1, len(data)):
        diff = data[t] - np.mean(data[:t])
        S_pos[t] = max(0, S_pos[t-1] + diff - drift)
        S_neg[t] = min(0, S_neg[t-1] + diff + drift)

        if S_pos[t] > threshold:
            change_points.append(t)
            S_pos[t] = 0
        elif abs(S_neg[t]) > threshold:
            change_points.append(t)
            S_neg[t] = 0

    return change_points

# 3. 設定滑動窗口參數
window_size = 256
n_steps = 63
threshold = 1.5
drift = 0.0

output_rows = []

# 4. 滑動窗口計算 CUSUM，並轉為 0/1 row
for i in range(n_steps):
    start = i
    end = i + window_size
    window_data = prices[start:end]
    cps = cusum(window_data, threshold=threshold, drift=drift)

    # 建立 0/1 row
    row = np.zeros(window_size, dtype=int)
    for cp in cps:
        if cp < window_size:  # 確保不超過 256
            row[cp] = 1

    # window title 為最後一天的下一天
    if end < len(dates):
        title_date = dates[end]  # 下一天的 date
    else:
        title_date = pd.NaT
    output_rows.append(pd.Series(row, name=title_date))

# 5. 整理成 DataFrame（每行一個 window）
df_output = pd.DataFrame(output_rows)

# 6. 輸出到指定資料夾
output_dir = r"C:\NCNU\im\informs\PSVQR\experiment\cusum"
os.makedirs(output_dir, exist_ok=True)
today_str = datetime.today().strftime('%Y%m%d')
output_filename = os.path.join(output_dir, f'cusum_{today_str}.xlsx')

df_output.to_excel(output_filename, index=False)

print(f"CUSUM 結果已輸出到 {output_filename}")
