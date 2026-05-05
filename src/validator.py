def validate_nav(new_nav, last_nav=None):
    """
    機構級 NAV 驗證：
    1. 型別 / 數值檢查
    2. 第一筆資料允許
    3. 異常波動過濾（>10%）
    """

    # ===== 1️⃣ 基本檢查 =====
    if new_nav is None:
        return False

    try:
        new_nav = float(new_nav)
    except:
        return False

    if new_nav <= 0:
        return False

    # ===== 2️⃣ 第一筆資料直接通過 =====
    if last_nav is None:
        return True

    try:
        last_nav = float(last_nav)
    except:
        return False

    if last_nav <= 0:
        return False

    # ===== 3️⃣ 波動檢查 =====
    change = abs(new_nav - last_nav) / last_nav

    # ETF 單日波動 >10% 幾乎不可能
    if change > 0.1:
        print(f"[ANOMALY] NAV jump too large: {last_nav} -> {new_nav}")
        return False

    return True
