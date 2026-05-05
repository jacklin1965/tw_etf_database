import requests
import pandas as pd
import datetime
import os

def fetch_nav():
    # 你的 fallback 或 API
    return 100.0

def save_csv(nav):
    os.makedirs("data", exist_ok=True)

    file_path = "data/data_0050.csv"

    df = pd.DataFrame([{
        "date": datetime.date.today(),
        "nav": nav
    }])

    df.to_csv(file_path, index=False)

    print("CSV CREATED:", file_path)
    print("FILES IN DIR:", os.listdir("data"))

def main():
    nav = fetch_nav()
    save_csv(nav)

if __name__ == "__main__":
    main()
