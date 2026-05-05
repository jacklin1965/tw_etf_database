import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "data/etf.db"
CHART_DIR = "charts"


def generate_chart(code):
    os.makedirs(CHART_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(f"""
        SELECT date, nav
        FROM etf_data
        WHERE code = '{code}' AND valid = 1
        ORDER BY date
    """, conn)

    conn.close()

    if df.empty:
        print(f"⚠️ No data for {code}")
        return

    df["date"] = pd.to_datetime(df["date"])

    plt.figure()
    plt.plot(df["date"], df["nav"])
    plt.title(f"{code} NAV Trend")
    plt.xlabel("Date")
    plt.ylabel("NAV")
    plt.xticks(rotation=45)

    filepath = f"{CHART_DIR}/{code}.png"
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()

    print(f"📈 Chart saved: {filepath}")
