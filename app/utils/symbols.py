# app/utils/symbols.py
ALIAS = {"GOLD": "GC=F", "EMAS": "GC=F", "XAU": "GC=F", "IHSG": "^JKSE", "DXY": "DX-Y.NYB"}


def clean(query):
    return (query or "").strip().upper().replace(" ", "")


def candidates(query):
    """BBCA -> ['BBCA.JK', 'BBCA'] ; GOLD -> ['GC=F'] ; BBCA.JK -> ['BBCA.JK']"""
    s = clean(query)
    if not s:
        return []
    if s in ALIAS:
        return [ALIAS[s]]
    if s.startswith("^") or any(ch in s for ch in "=.-"):
        return [s]
    return [s + ".JK", s]  # saham IDX dulu, lalu ticker global (mis. AAPL)


def display_code(symbol):
    return symbol[:-3] if str(symbol).endswith(".JK") else symbol
