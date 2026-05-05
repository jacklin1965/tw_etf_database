import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"

def save(etf, price):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = f"{DATA_DIR}/{etf}.csv"

    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["date", "nav"])

    if today in df['date'].values:
        old = df.loc[df['date'] == today, 'nav'].values[0]

        if abs(old - price) > 0.01:
            print(f"🔄 UPDATE {etf}: {old} -> {price}")
            df.loc[df['date'] == today, 'nav'] = price
            return df, True
        else:
            return df, False

    df = pd.concat([
        df,
        pd.DataFrame([[today, price]], columns=["date", "nav"])
    ])
    return df, True
