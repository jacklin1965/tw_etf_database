import requests
import pandas as pd
import os
from datetime import datetime

ETF_LIST = ["0050", "0056", "00878"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# =========================
# 來源1：TWSE（主）
# =========================
def get_nav_twse(etf_id):
    url = f"https://www.twse.com.tw/rwd/zh/ETF/etfNav?response=json&stockNo={etf_id}"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        data = res.json()

        if "data" in data and len(data["data"]) > 0:
            latest = data["data"][0]

            nav = float(latest[1])

            if 5 < nav < 500:
                return nav

    except Exception as e:
        print(f"TWSE FAIL {etf_id}: {e}")

    return None


# =========================
# 來源2：Yahoo（備援）
# =========================
def get_nav_yahoo(etf_id):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{etf_id}.TW"
        res = requests.get(url, headers=HEADERS, timeout=10)
        data = res.json()

        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

        if 5 < price < 500:
            return float(price)

    except Exception as e:
        print(f"YAHOO FAIL {etf_id}: {e}")

    return None


# =========================
# 多來源容錯
# =========================
def get_nav(etf_id):
    nav = get_nav_twse(etf_id)

    if nav is None:
        nav = get_nav_yahoo(etf_id)

    if nav is None:
        print(f"❌ ALL FAIL {etf_id}")

    return nav


# =========================
# CSV 更新（防重複）
# =========================
def update_csv(etf_id, nav):
    if nav is None:
        return False

    os.makedirs("data", exist_ok=True)

    file_path = f"data/{etf_id}.csv"
    today = datetime.now().strftime("%Y-%m-%d")

    new_row = pd.DataFrame([[today, nav]], columns=["date", "nav"])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        # 若今日已存在 → 不更新
        if today in df["date"].values:
            print(f"⏩ SKIP {etf_id} (already updated)")
            return False

        df = pd.concat([df, new_row])
    else:
        df = new_row

    df.to_csv(file_path, index=False)

    print(f"✅ UPDATE {etf_id} NAV={nav}")
    return True


# =========================
# 主程式
# =========================
def main():
    changed = False

    for etf in ETF_LIST:
        nav = get_nav(etf)
        print(f"{etf} -> {nav}")

        if update_csv(etf, nav):
            changed = True

    return changed


if __name__ == "__main__":
    changed = main()

    # 寫入 flag 給 GitHub Actions 判斷
    with open("changed.flag", "w") as f:
        f.write("true" if changed else "false")
