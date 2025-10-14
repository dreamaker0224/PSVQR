import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

# === 檔案設定 ===
input_file = r"D:\NCNU\im\informs\PSVQR\experiment\template_price.xlsx"
sheet_name = "Training"

# === 取得目前 .py 檔所在路徑 ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# === 讀取資料 ===
df = pd.read_excel(input_file, sheet_name=sheet_name)

# 檢查欄位是否存在
if not {'x', 'y'}.issubset(df.columns):
    raise ValueError("❌ Excel 檔案中找不到 'x' 或 'y' 欄位，請確認標題是否正確。")

# === 取出要標準化的欄位 ===
data = df[['x', 'y']].copy()

# === 標準化 ===
scaler = StandardScaler()
scaled_values = scaler.fit_transform(data)

# === 新增標準化欄位 ===
df[['x_standard', 'y_standard']] = scaled_values

# === 建立輸出路徑 ===
input_basename = os.path.splitext(os.path.basename(input_file))[0]  # 取不含副檔名的檔名
output_file = os.path.join(script_dir, f"{input_basename}_standard.xlsx")

# === 輸出新檔案 ===
df.to_excel(output_file, sheet_name=sheet_name, index=False)

print(f"✅ 標準化完成！輸出檔案：\n{output_file}")
