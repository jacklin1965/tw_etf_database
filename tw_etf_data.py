import pandas as pd
import datetime
import os

ETF_ID = "0050"
OUTPUT_FILE = "data_0050.csv"

def main():
    today = datetime.date.today()

    # 先用測試資料（確保流程成功）
    df = pd.DataFrame({
        "date": [today],
        "etf_id": [ETF_ID],
        "nav": [100]  # 測試用數值
    })

    # 若檔案存在就合併
    if os.path.exists(OUTPUT_FILE):
        old = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([old, df], ignore_index=True)
        df = df.drop_duplicates(subset=["date", "etf_id"])

    df.to_csv(OUTPUT_FILE, index=False)

    print("SUCCESS")

if __name__ == "__main__":
    main()
