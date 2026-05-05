import requests
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TIMEOUT = 10
RETRY = 3


# =========================
# 主入口
# =========================
def get_price(code):
    """
    多來源抓取（TWSE → Yahoo）
    """

    # 1️⃣ TWSE
    price = safe_fetch(fetch_twse, code, "TWSE")
    if price:
        return price

    # 2️⃣ Yahoo fallback
    price = safe_fetch(fetch_yahoo, code, "YAHOO")
    if price:
        return price

    print(f"[ERROR] {code} all sources failed")
    return None


# =========================
# Retry 包裝器
# =========================
def safe_fetch(func, code, source):
    for i in range(RETRY):
        try:
            price = func(code)
            if price:
                print(f"[SUCCESS] {code} {source} -> {price}")
                return price
        except Exception as e:
            print(f"[{source} FAIL] {code} attempt {i+1}: {e}")

        sleep_random()

    return None


# =========================
# TWSE（容易被擋）
# =========================
def fetch_twse(code):
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{code}.tw"

    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

    # 防止被擋（回 HTML）
    if "html" in res.text.lower():
        raise Exception("Blocked by TWSE")

    data = res.json()

    if not data.get("msgArray"):
        raise Exception("Empty data")

    price = data["msgArray"][0].get("z")

    return float(price) if price not in ["-", None] else None


# =========================
# Yahoo（穩定來源）
# =========================
def fetch_yahoo(code):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={code}.TW"

    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    data = res.json()

    result = data["quoteResponse"]["result"]

    if not result:
        raise Exception("No result")

    return float(result[0]["regularMarketPrice"])


# =========================
# 小工具
# =========================
def sleep_random():
    time.sleep(random.uniform(1, 2))
