import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
from config import DB_PATH, DATA_DIR, CHART_DIR


def export_csv():
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM etf_nav", conn)
    conn.close()

    for code in df["code"].unique():
        sub = df[df["code"] == code]
        sub.to_csv(f"{DATA_DIR}/{code}.csv", index=False)


def generate_charts():
    os.makedirs(CHART_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM etf_nav", conn)
    conn.close()

    for code in df["code"].unique():
        sub = df[df["code"] == code]

        plt.figure()
        plt.plot(sub["date"], sub["nav"])
        plt.title(code)
        plt.xticks(rotation=45)

        plt.savefig(f"{CHART_DIR}/{code}.png")
        plt.close()
