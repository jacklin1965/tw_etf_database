import os
import pandas as pd

DATA_DIR = "data"


def get_last_nav(code):
    path = f"{DATA_DIR}/{code}.csv"

    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)

    if df.empty:
        return None

    return float(df.iloc[-1]["nav"])


def append_csv(code, date, nav):
    path = f"{DATA_DIR}/{code}.csv"

    new_row = {"date": date, "nav": nav}

    if os.path.exists(path):
        df = pd.read_csv(path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(path, index=False)
