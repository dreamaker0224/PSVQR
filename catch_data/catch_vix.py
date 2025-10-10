import yfinance as yf

Ticker = "^GSPC"

# 下載歷史資料
vix_data = yf.download( Ticker , start="2023-08-01", end="2023-09-30")  # end 不包含當天，所以設 8/30

# 匯出到 CSV
vix_data.to_csv(f"{Ticker[1:]}.csv")

print(f"已匯出到 {Ticker[1:]}.csv")
