from config import ETF_LIST
from fetcher import get_price
from storage import save
from validator import validate_nav
import pandas as pd
import os

changed = False

for etf in ETF_LIST:
    code = etf["code"]

    price = get_price(code)
    if price is None:
        continue

    file_path = f"data/{code}.csv"
    last_nav = None

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if not df.empty:
            old_price = df.iloc[-1]['nav']

    if not validate_nav(new_nav, last_nav):
        continue

    df, updated = save(code, price)
    df.to_csv(file_path, index=False)

    if updated:
        changed = True

# GitHub Actions flag
with open("changed.flag", "w") as f:
    f.write("true" if changed else "false")
