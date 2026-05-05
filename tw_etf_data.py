import requests
import pandas as pd
import datetime
import re

def fetch_nav():
    url = "https://www.yuantaetfs.com/product/detail/0050"

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    text = r.text

    # 嘗試抓數字（fallback）
    match = re.search(r"淨值[^0-9]*([0-9]+\.[0-9]+)", text)

    if not match:
        raise Exception("NAV parse failed")

    return float(match.group(1))
