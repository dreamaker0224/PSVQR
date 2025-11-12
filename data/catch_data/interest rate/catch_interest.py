import pandas as pd
import requests
from io import StringIO

# 下載資料（新版 FRED 網址）
tb3ms_url = "https://fred.stlouisfed.org/data/TB3MS.csv"
cpi_url   = "https://fred.stlouisfed.org/data/CPIAUCSL.csv"

def read_fred_csv(url):
    r = requests.get(url)
    r.raise_for_status()          # 若 404/500 會直接報錯
    data = StringIO(r.text)
    return pd.read_csv(data, parse_dates=["DATE"], index_col="DATE")

# 讀入資料
tb = read_fred_csv(tb3ms_url).rename(columns={"VALUE": "tb3ms"})
cpi = read_fred_csv(cpi_url).rename(columns={"VALUE": "cpi"})

# 轉季
tb_q  = tb.resample("Q").mean()
cpi_q = cpi.resample("Q").mean()

# 通膨率（季對季 %）
cpi_q["inflation_q_pct"] = cpi_q["cpi"].pct_change() * 100

# 實質利率
df = tb_q.join(cpi_q[["cpi", "inflation_q_pct"]])
df["real_rate_pct"] = df["tb3ms"] - df["inflation_q_pct"]

# 篩選區間
df.index = df.index.to_period("Q")
df = df.loc["1961Q1":"1986Q3"]

# 輸出 CSV
out = df.reset_index().rename(columns={"index": "quarter"})
out["quarter"] = out["quarter"].astype(str)
out.to_csv("us_real_rate_1961Q1_1986Q3.csv", index=False)

print("✅ Saved: us_real_rate_1961Q1_1986Q3.csv")
print(out.head())
