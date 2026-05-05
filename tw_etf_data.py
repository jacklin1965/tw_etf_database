import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"

def fetch_etf_nav(etf_code: str):
    """
    TODO: 你原本的 requests + parsing 保留
    回傳格式：
    [
        {"date": "2026-05-05", "nav": 100.0}
    ]
    """
    # === 這裡用假資料示範 ===
    today = datetime.today().strftime("%Y-%m-%d")
    return [{"date": today, "nav": 100.0}]


def update_etf_file(etf_code: str):
    os.makedirs(DATA_DIR, exist_ok=True)

    path = f"{DATA_DIR}/{etf_code}.csv"

    new_data = pd.DataFrame(fetch_etf_nav(etf_code))

    if os.path.exists(path):
        old = pd.read_csv(path)
        df = pd.concat([old, new_data])
        df = df.drop_duplicates(subset=["date"], keep="last")
        df = df.sort_values("date")
    else:
        df = new_data

    df.to_csv(path, index=False)
    print(f"UPDATED: {path}")


if __name__ == "__main__":
    etfs = ["0050", "0056", "00878"]

    for etf in etfs:
        update_etf_file(etf)
