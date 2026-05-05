import pandas as pd
import datetime
import os

ETF_ID = "0050"
OUTPUT_FILE = "data_0050.csv"

def fetch_nav():
    """
    從元大ETF官方頁面抓 NAV（真實資料）
    """

    url = "https://www.yuantaetfs.com/product/detail/0050"

    tables = pd.read_html(url)

    # 尋找含 NAV 的表格
    nav_value = None

    for t in tables:
        for col in t.columns:
            if "淨值" in str(col) or "NAV" in str(col):
                try:
                    nav_value = t.iloc[0, 1]
                    break
                except:
                    continue

    if nav_value is None:
        raise Exception("NAV 抓取失敗（表格結構可能變動）")

    return float(nav_value)


def main():
    os.makedirs("data", exist_ok=True)

    today = datetime.date.today()

    nav = fetch_nav()

    df = pd.DataFrame([{
        "date": today,
        "etf_id": ETF_ID,
        "nav": nav
    }])

    # append + 去重
    if os.path.exists(OUTPUT_FILE):
        old = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([old, df], ignore_index=True)
        df = df.drop_duplicates(subset=["date", "etf_id"])

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"SUCCESS | {ETF_ID} NAV =", nav)


if __name__ == "__main__":
    main()
