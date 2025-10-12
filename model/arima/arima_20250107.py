import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# 1. 讀取 Excel 文件中的時間序列數據
file_path = "C:\\NCNU\\im\\informs\\PSVQR\\experiment\\template_price.xlsx"  # 修改為你的 Excel 文件路徑
df = pd.read_excel(file_path, sheet_name='Dataset')  # 讀取文件，根據需要更改工作表名稱

# 假設你的時間序列數據在 Excel 文件的第二列 (可以根據需要修改)
time_series_data = df.iloc[:, 2].values  # 把第二列的數據提取為 NumPy 數組

# 設置預測次數（例如進行 62 次預測）
n_predictions = 63

# 保存預測結果的列表
prediction_results = []

# 迴圈：進行 n_predictions 次預測
for i in range(n_predictions):
    # 1. 動態調整訓練數據範圍 (每次取 i 到 256 + i 筆資料)
    train_data = time_series_data[i:256 + i]

    # 打印訓練數據的範圍
    print(f"Iteration {i+1}: Training data from index {i+1} to {256 + i}")

    # 2. 建立並訓練 ARIMA 模型
    model = ARIMA(train_data, order=(1, 0, 1), enforce_stationarity= False)  # 使用 p=1, d=0, q=1
    model_fit = model.fit()

    # 3. 預測下一步，即第 129 + i 筆
    next_prediction = model_fit.forecast(steps=1)[0]

    # 4. 獲取實際的第 129 + i 筆資料
    actual_value = time_series_data[256 + i]

    # 保存預測值和實際值
    prediction_results.append({
        'Iteration': i+1,
        'Predicted Value': next_prediction,
        'Actual Value': actual_value
    })

    # 打印預測結果和實際值
    print(f"Prediction {i+1}: Predicted value = {next_prediction}, Actual value = {actual_value}\n")

# 將預測結果保存到 Excel 文件中
output_df = pd.DataFrame(prediction_results)
output_file = "C:\\NCNU\\im\\informs\\PSVQR\\experiment\\arima_256_62d\\arima_256_62d_price.xlsx"
output_df.to_excel(output_file, index=False)

print(f"預測結果已保存至 {output_file}.")
