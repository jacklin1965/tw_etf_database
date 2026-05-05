def validate_nav(new_nav, last_nav):
    # 基本檢查
    if new_nav is None or new_nav <= 0:
        return False

    # 第一筆資料直接通過
    if last_nav is None:
        return True

    # 漲跌幅
    change = abs(new_nav - last_nav) / last_nav

    # ETF 不可能一天 >10%
    if change > 0.1:
        print(f"⚠️ 異常波動: {last_nav} -> {new_nav}")
        return False

    return True
