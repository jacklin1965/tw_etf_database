import os
import pandas as pd
from datetime import datetime

from config import ETF_LIST, DATA_DIR
from fetcher import get_price
from validator import validate_nav


def run():
    os.makedirs(DATA_DIR, exist_ok=True)

    changed = False

    for code in ETF_LIST:
        file_path = f"{DATA_DIR}/{code}.csv"

        # =========================
        # 讀取舊資料
        # =========================
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            last_nav = df.iloc[-1]["nav"]
        else:
            df = pd.DataFrame(columns=["date", "nav"])
            last_nav = None

        # =========================
        # 抓新價格
        # =========================
        new_nav, source = get_price(code)

        if new_nav is None:
            print(f"❌ ALL FAIL {code}")
            continue

        print(f"{code} -> {new_nav} ({source})")

        # =========================
        # 驗證
        # =========================
        if not validate_nav(new_nav, last_nav):
            print(f"⛔ SKIP {code} (invalid)")
            continue

        today = datetime.now().strftime("%Y-%m-%d")

        # =========================
        # 避免同一天重複寫入
        # =========================
        if len(df) > 0 and df.iloc[-1]["date"] == today:
            print(f"⏩ SKIP {code} (already updated)")
            continue

        # =========================
        # 寫入
        # =========================
        new_row = pd.DataFrame([[today, new_nav]], columns=["date", "nav"])
        df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(file_path, index=False)
        changed = True

    # =========================
    # 給 GitHub Actions 用
    # =========================
    with open("changed.flag", "w") as f:
        f.write("true" if changed else "false")


if __name__ == "__main__":
    run()
