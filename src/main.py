from datetime import datetime

from config import ETF_LIST
from fetcher import get_price
from validator import validate_nav
from storage import init_db, insert_etf_info, get_last_nav, insert_nav
from exporter import export_csv, generate_charts


def run():
    init_db()

    for etf in ETF_LIST:
        code = etf["code"]
        name = etf["name"]

        insert_etf_info(code, name)

        last_nav = get_last_nav(code)

        new_nav, source = get_price(code)

        print(f"{code} -> {new_nav} ({source})")

        if new_nav is None:
            continue

        valid = validate_nav(new_nav, last_nav)

        if last_nav is None:
            change_pct = 0
        else:
            change_pct = (new_nav - last_nav) / last_nav

        today = datetime.now().strftime("%Y-%m-%d")

        insert_nav(today, code, new_nav, source, change_pct, valid)

    export_csv()
    generate_charts()


if __name__ == "__main__":
    run()
