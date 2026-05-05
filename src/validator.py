def validate_nav(new_nav, last_nav):
    if new_nav is None or new_nav <= 0:
        return False

    if last_nav is None:
        return True

    change = abs(new_nav - last_nav) / last_nav

    if change > 0.1:
        print(f"⚠️ 異常波動: {last_nav} -> {new_nav}")
        return False

    return True
