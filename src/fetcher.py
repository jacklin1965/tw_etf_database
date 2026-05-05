import requests
from bs4 import BeautifulSoup
from config import HEADERS


def fetch_twse(code):
    try:
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={code}"
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200 or "json" not in r.headers.get("Content-Type", ""):
            return None, None

        data = r.json()
        price = float(data["data"][-1][6])
        return price, "TWSE"
    except:
        return None, None


def fetch_yahoo(code):
    try:
        url = f"https://tw.stock.yahoo.com/quote/{code}"
        r = requests.get(url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.select_one("fin-streamer[data-field='regularMarketPrice']")

        if price:
            return float(price.text), "Yahoo"
    except:
        pass

    return None, None


def fetch_cmoney(code):
    try:
        url = f"https://www.cmoney.tw/etf/e{code}.aspx"
        r = requests.get(url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.select_one(".price")

        if price:
            return float(price.text), "CMoney"
    except:
        pass

    return None, None


def get_price(code):
    for f in [fetch_twse, fetch_yahoo, fetch_cmoney]:
        price, source = f(code)
        if price is not None:
            return price, source

    return None, None
