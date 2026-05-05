import os
from datetime import datetime

from fetcher import get_price
from validator import validate_nav
from storage import get_last_nav, append_csv

# ===== ETF清單 =====
ETF_LIST = [
    "0050",
    "0056",
    "006208",
    "00713",
    "00878",
    "00919",
    "00929",
    "00940"
]

DATA_DIR = "data"


def main():
    today = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(DATA_DIR, exist_ok=True)

    changed = False

    for code in ETF_LIST:
        print(f"\n=== {code} ===")

        # ===== 1️⃣ 抓資料 =====
        nav = get_price(code)

        if nav is None:
            print(f"[SKIP] {code} no data")
            continue

        # ===== 2️⃣ 讀取舊資料 =====
        last_nav = get_last_nav(code)

        print(f"{code} -> {nav} (last: {last_nav})")

        # ===== 3️⃣ 驗證 =====
        if not validate_nav(nav, last_nav):
            print(f"[SKIP] {code} invalid NAV")
            continue

        # ===== 4️⃣ 避免重複寫入 =====
        if last_nav is not None and abs(nav - last_nav) < 1e-6:
            print(f"[SKIP] {code} no change")
            continue

        # ===== 5️⃣ 寫入CSV =====
        append_csv(code, today, nav)
        print(f"[UPDATE] {code} saved")

        changed = True

    # ===== GitHub Actions用 =====
    with open("changed.flag", "w") as f:
        f.write("true" if changed else "false")


if __name__ == "__main__":
    main()
