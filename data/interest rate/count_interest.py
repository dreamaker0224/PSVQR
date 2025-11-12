import pandas as pd

file_path = r"C:\NCNU\im\informs\PSVQR\data\interest rate\Interest rate.xlsx"

# 讀取 DTB3 資料（90d Treasure Bill）
dtb3 = pd.read_excel(file_path, sheet_name="Treasure Bill", 
                     parse_dates=["observation_date"], index_col="observation_date")

# 轉成季度平均
dtb3_q = dtb3.resample("Q").mean()

# 讀取 CPI 資料
cpi = pd.read_excel(file_path, sheet_name="CPI", 
                    parse_dates=["observation_date"], index_col="observation_date")

# 將 CPI index 轉成季度末以對齊 DTB3
cpi.index = cpi.index.to_period("Q").to_timestamp("Q")

# 合併資料
df = dtb3_q.join(cpi, how="inner")

# 計算實質利率
# 假設 CPI 的欄位名是 CPALTT01USQ657N
df['real_rate'] = df['DTB3'] - df['CPALTT01USQ657N']

# 篩選 1961Q1–1986Q3
df = df.loc['1961-03-31':'1986-09-30']

# 只保留 date 和實質利率欄位
df_output = df[['real_rate']].reset_index()
df_output.columns = ['date', 'real interest rate']

# 儲存到同一個 Excel 的 "real" sheet
with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
    df_output.to_excel(writer, sheet_name='real', index=False)

print(df_output.head())
