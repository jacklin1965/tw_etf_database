import requests
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def fetch_with_retry(url):
    for i in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200 and r.text.strip():
                return r
        except:
            pass
        time.sleep(random.uniform(1, 3))
    return None


# --- TWSE ---
def get_twse(etf):
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={etf}"
    r = fetch_with_retry(url)
    if not r:
        return None
    try:
        data = r.json()
        return float(data['data'][-1][6])
    except:
        return None


# --- Yahoo ---
def get_yahoo(etf):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={etf}.TW"
    r = fetch_with_retry(url)
    if not r:
        return None
    try:
        return r.json()['quoteResponse']['result'][0]['regularMarketPrice']
    except:
        return None


# --- FinMind（高穩定備援） ---
def get_finmind(etf):
    url = f"https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id={etf}"
    r = fetch_with_retry(url)
    if not r:
        return None
    try:
        data = r.json()['data']
        return float(data[-1]['close'])
    except:
        return None


def get_price(etf):
    for source in [get_twse, get_yahoo, get_finmind]:
        price = source(etf)
        if price:
            print(f"✅ {etf} from {source.__name__}: {price}")
            return price
    print(f"❌ ALL FAIL {etf}")
    return None
