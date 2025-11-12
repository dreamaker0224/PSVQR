import pandas as pd
import numpy as np

# === Excel 路徑 ===
file_path = r"C:\NCNU\im\informs\PSVQR\data\interest rate\Interest rate.xlsx"

# === 讀取 Training sheet ===
df = pd.read_excel(file_path, sheet_name="Training")

# 假設目標欄位是 'y'（可改成其他欄位名稱）
C = df['y'].to_numpy()
n = len(C)

# === 計算下三角矩陣 ===
Cm = C.reshape(-1, 1)
Cn = C.reshape(1, -1)
M = np.maximum(Cm - Cn, 0)   # ((Cm - Cn) + abs(Cm - Cn)) / 2 的等價形式
M = np.tril(M, k=-1)         # 保留下三角，對角與上三角皆為 0

# === 轉成 DataFrame ===
M_df = pd.DataFrame(M, columns=[f"C{j+1}" for j in range(n)],
                       index=[f"C{i+1}" for i in range(n)])

# === 輸出到 Preprocess sheet（若已存在會覆蓋） ===
with pd.ExcelWriter(file_path, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
    M_df.to_excel(writer, sheet_name="Preprocess")

print("✅ 下三角矩陣已成功計算並寫入到 'Preprocess' sheet！")
