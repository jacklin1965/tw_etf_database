from config import ETF_LIST
from fetcher import get_best_price
from validator import validate_nav
from storage import init_db, get_last_nav, save_to_db, export_csv
from chart import generate_chart


def run():
    init_db()

    updated = False

    for etf in ETF_LIST:
        code = etf["code"]
        name = etf["name"]

        new_nav, source = get_best_price(code)

        print(f"{code} -> {new_nav} ({source})")

        if new_nav is None:
            continue

        last_nav = get_last_nav(code)

        valid = validate_nav(new_nav, last_nav)

        save_to_db(code, name, new_nav, source, valid)

        if valid:
            export_csv(code)
            generate_chart(code)
            updated = True

    with open("changed.flag", "w") as f:
        f.write("true" if updated else "false")


if __name__ == "__main__":
    run()
