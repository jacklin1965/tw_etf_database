import requests
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TIMEOUT = 10
RETRY = 3


# =========================
# 主入口（智能來源選擇）
# =========================
def get_price(code):
    """
    Source Priority:
    1. TWSE (官方)
    2. Yahoo (穩定)
    3. CMoney (備援)
    """

    sources = [
        ("TWSE", fetch_twse),
        ("YAHOO", fetch_yahoo),
        ("CMONEY", fetch_cmoney)
    ]

    for name, func in sources:
        price = safe_fetch(func, code, name)
        if price:
            return price

    print(f"[ERROR] {code} all sources failed")
    return None


# =========================
# Retry + 防擋
# =========================
def safe_fetch(func, code, source):
    for i in range(RETRY):
        try:
            price = func(code)

            if price and price > 0:
                print(f"[SUCCESS] {code} {source} -> {price}")
                return price

        except Exception as e:
            print(f"[{source} FAIL] {code} attempt {i+1}: {e}")

        sleep_random()

    return None


# =========================
# TWSE（最快但會擋）
# =========================
def fetch_twse(code):
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{code}.tw"

    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

    if "html" in res.text.lower():
        raise Exception("Blocked")

    data = res.json()

    if not data.get("msgArray"):
        raise Exception("Empty")

    price = data["msgArray"][0].get("z")

    if price in ["-", None]:
        raise Exception("No price")

    return float(price)


# =========================
# Yahoo（最穩）
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
# CMoney（備援）
# =========================
def fetch_cmoney(code):
    url = f"https://www.cmoney.tw/finance/etf/{code}"

    res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

    if res.status_code != 200:
        raise Exception("HTTP error")

    html = res.text

    # 簡單解析（避免 heavy parser）
    import re
    match = re.search(r'"closePrice":([0-9\.]+)', html)

    if not match:
        raise Exception("Parse fail")

    return float(match.group(1))


# =========================
# 防封鎖
# =========================
def sleep_random():
    time.sleep(random.uniform(1, 2))
