import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

# === 檔案設定 ===
input_file = r"C:\NCNU\im\informs\PSVQR\experiment\price\tax_f2\tax_f2.xlsx"
sheet_name = "Original data"

# === 取得目前 .py 檔所在路徑 ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# === 讀取資料 ===
df = pd.read_excel(input_file, sheet_name=sheet_name)

# === 取出要標準化的欄位 (除了 'Date' 和 'return') ===
columns_to_scale = [col for col in df.columns if col not in ['Date', 'return']]
data_to_scale = df[columns_to_scale].copy()

# === 標準化 ===
scaler = StandardScaler()
scaled_values = scaler.fit_transform(data_to_scale)

# === 新增標準化欄位，命名為 "欄位名_standard" ===
scaled_df = pd.DataFrame(scaled_values, columns=[f"{col}_standard" for col in columns_to_scale])
df = pd.concat([df, scaled_df], axis=1)

# === 建立輸出路徑 ===
input_basename = os.path.splitext(os.path.basename(input_file))[0]  # 取不含副檔名的檔名
output_file = os.path.join(script_dir, f"{input_basename}_standard.xlsx")

# === 輸出新檔案 ===
df.to_excel(output_file, sheet_name=sheet_name, index=False)

print(f"✅ 標準化完成！輸出檔案：\n{output_file}")
