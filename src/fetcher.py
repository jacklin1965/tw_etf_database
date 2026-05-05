import requests
from bs4 import BeautifulSoup
from config import HEADERS

# =========================
# TWSE
# =========================
def fetch_twse(code):
    try:
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={code}"
        r = requests.get(url, headers=HEADERS, timeout=10)

        data = r.json()

        # 取最新收盤價
        price = float(data["data"][-1][6])
        return price, "TWSE"

    except Exception as e:
        print(f"TWSE FAIL {code}: {e}")
        return None, None


# =========================
# Yahoo
# =========================
def fetch_yahoo(code):
    try:
        url = f"https://tw.stock.yahoo.com/quote/{code}"
        r = requests.get(url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        price = float(price_tag.text.replace(",", ""))

        return price, "Yahoo"

    except Exception as e:
        print(f"Yahoo FAIL {code}: {e}")
        return None, None


# =========================
# CMoney
# =========================
def fetch_cmoney(code):
    try:
        url = f"https://www.cmoney.tw/etf/{code}"
        r = requests.get(url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        price_tag = soup.find("span", {"id": "lastPrice"})
        price = float(price_tag.text.strip())

        return price, "CMoney"

    except Exception as e:
        print(f"CMoney FAIL {code}: {e}")
        return None, None


# =========================
# 主控制（自動切換）
# =========================
def get_price(code):
    for fetch_func in [fetch_twse, fetch_yahoo, fetch_cmoney]:
        price, source = fetch_func(code)

        if price is not None:
            return price, source

    return None, None
