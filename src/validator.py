def validate_price(new, old):
    if new is None:
        return False

    if old is None:
        return True

    # 避免異常跳動（>10%）
    if abs(new - old) / old > 0.1:
        print(f"⚠️ 異常價格: {old} -> {new}")
        return False

    return True
