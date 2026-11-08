# app/core/horizon.py -- sinyal per gaya trading: SWING, SCALPING, LONGTERM
import numpy as np
import pandas as pd
import ta
from app.core.entry_signal import generate_entry_signal
from app.core.scalping import generate_scalping_signal

META = {
    "SWING": {"title": "Swing", "span": "Tahan beberapa hari sampai minggu", "tf": "Harian"},
    "SCALPING": {"title": "Scalping", "span": "Selesai di hari yang sama", "tf": "Per jam"},
    "LONGTERM": {"title": "Longterm", "span": "Tahan bulan sampai tahun", "tf": "Harian + fundamental"},
}


def _empty(horizon, msg):
    return {"horizon": horizon, **META[horizon], "action": "WAIT", "recommendation": "DATA KURANG",
            "confidence": "LOW", "score": 0, "reasons": [msg],
            "entry": None, "stop_loss": None, "take_profit": None, "rr": None}


def _atr(df, n=14):
    v = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"], window=n).average_true_range().iloc[-1]
    return None if pd.isna(v) else float(v)


def _levels(action, price, atr, sl_m, tp_m):
    if action not in ("BUY", "SELL") or not atr:
        return None, None, None
    sign = 1 if action == "BUY" else -1
    return price - sign * atr * sl_m, price + sign * atr * tp_m, round(tp_m / sl_m, 2)


def swing_signal(df, symbol):
    sig = generate_entry_signal(df, symbol)
    if sig["recommendation"] in ("DATA KOSONG", "DATA KURANG"):
        return _empty("SWING", sig["reasons"][0])
    price = float(sig["price"])
    sl, tp, rr = _levels(sig["action"], price, _atr(df), 2.0, 4.0)
    return {"horizon": "SWING", **META["SWING"], "action": "WAIT" if sig["action"] == "HOLD" else sig["action"],
            "recommendation": sig["recommendation"].replace("AGGRESSIVE", "KUAT").replace("MODERATE", "SEDANG"),
            "confidence": sig["confidence"], "score": sig["score"], "reasons": sig["reasons"],
            "entry": price, "stop_loss": sl, "take_profit": tp, "rr": rr}


def scalping_signal(df_intraday):
    if df_intraday is None or len(df_intraday) < 25:
        return _empty("SCALPING", "Data intraday belum cukup (pasar tutup atau likuiditas rendah)")
    s = generate_scalping_signal(df_intraday)
    if not s:
        return _empty("SCALPING", "Data intraday belum cukup")
    rec = {"BUY": "SCALP BELI", "SELL": "SCALP JUAL"}.get(s["action"], "TUNGGU")
    if s["action"] != "WAIT" and s["confidence"] == "MEDIUM":
        rec += " (sedang)"
    live = s["action"] != "WAIT"
    return {"horizon": "SCALPING", **META["SCALPING"], "action": s["action"], "recommendation": rec,
            "confidence": s["confidence"], "score": s["score"], "reasons": s["reasons"],
            "entry": float(s["price"]), "stop_loss": s["stop_loss"] if live else None,
            "take_profit": s["take_profit"] if live else None, "rr": 1.33 if live else None}


def longterm_signal(df, info=None):
    if df is None or len(df) < 120:
        return _empty("LONGTERM", "Butuh minimal sekitar 6 bulan data harian")
    info, close = info or {}, df["Close"]
    price = float(close.iloc[-1])
    ma50 = close.rolling(50).mean().iloc[-1]
    ma200 = close.rolling(200).mean().iloc[-1] if len(df) >= 200 else np.nan
    score, why = 0, []

    if not pd.isna(ma200):
        if price > ma200: score += 2; why.append("Harga di atas MA200 (tren jangka panjang naik)")
        else: score -= 2; why.append("Harga di bawah MA200 (tren jangka panjang turun)")
        if ma50 > ma200: score += 1; why.append("MA50 di atas MA200 (golden cross)")
        else: score -= 1; why.append("MA50 di bawah MA200 (death cross)")
    ret = (price / float(close.iloc[-min(252, len(close))]) - 1) * 100
    if ret > 15: score += 1; why.append(f"Return sekitar 1 tahun {ret:+.0f}%")
    elif ret < -15: score -= 1; why.append(f"Return sekitar 1 tahun {ret:+.0f}%")
    hi, lo = float(df["High"].tail(252).max()), float(df["Low"].tail(252).min())
    pos = (price - lo) / (hi - lo) if hi > lo else 0.5
    if pos < 0.35: score += 1; why.append(f"Harga di zona bawah rentang 52 minggu ({pos:.0%})")
    elif pos > 0.9: score -= 1; why.append(f"Harga dekat puncak 52 minggu ({pos:.0%})")

    roe, pe, der = info.get("returnOnEquity"), info.get("trailingPE"), info.get("debtToEquity")
    rate = info.get("dividendRate")
    dy = (rate / price * 100) if rate and price else 0
    if roe and roe * 100 > 15: score += 1; why.append(f"ROE {roe*100:.1f}% (profitabilitas baik)")
    if pe and 0 < pe < 20: score += 1; why.append(f"PER {pe:.1f}x (valuasi wajar)")
    elif pe and pe > 35: score -= 1; why.append(f"PER {pe:.1f}x (valuasi mahal)")
    if der is not None and der > 200: score -= 1; why.append(f"DER {der:.0f}% (utang tinggi)")
    elif der is not None and 0 <= der < 100: score += 1; why.append(f"DER {der:.0f}% (utang terkendali)")
    if dy >= 3: score += 1; why.append(f"Dividen sekitar {dy:.1f}% per tahun")
    if not info: why.append("Data fundamental tidak tersedia, skor hanya dari teknikal")

    if score >= 4: rec, act, conf = "AKUMULASI KUAT", "BUY", "HIGH"
    elif score >= 2: rec, act, conf = "BELI BERTAHAP", "BUY", "MEDIUM"
    elif score <= -3: rec, act, conf = "HINDARI / JUAL", "SELL", "HIGH"
    elif score <= -1: rec, act, conf = "KURANGI", "SELL", "MEDIUM"
    else: rec, act, conf = "TAHAN", "WAIT", "LOW"

    sl = tp = rr = None
    if act == "BUY":
        sl = float(ma200 * 0.95) if not pd.isna(ma200) and price > ma200 else price * 0.85
        tp = price * 1.30
        rr = round((tp - price) / (price - sl), 2) if price > sl else None
    return {"horizon": "LONGTERM", **META["LONGTERM"], "action": act, "recommendation": rec, "confidence": conf,
            "score": score, "reasons": why, "entry": price, "stop_loss": sl, "take_profit": tp, "rr": rr}


def apply_risk(sig, risk="Moderate"):
    """Conservative: hanya sinyal beli keyakinan tinggi. Aggressive: skor positif ikut jadi beli spekulatif."""
    if risk == "Conservative" and sig["action"] == "BUY" and sig["confidence"] != "HIGH":
        return dict(sig, action="WAIT", recommendation="TUNGGU (konservatif)", stop_loss=None, take_profit=None,
                    rr=None, reasons=sig["reasons"] + ["Mode Conservative: hanya sinyal beli keyakinan tinggi"])
    if risk == "Aggressive" and sig["action"] == "WAIT" and sig["score"] >= 1 and sig["recommendation"] != "DATA KURANG":
        return dict(sig, action="BUY", recommendation="BELI SPEKULATIF", confidence="LOW",
                    reasons=sig["reasons"] + ["Mode Aggressive: skor positif tipis tetap ditandai beli"])
    return sig


def all_signals(symbol, df_daily, intraday, info, risk="Moderate"):
    sigs = [swing_signal(df_daily, symbol), scalping_signal(intraday), longterm_signal(df_daily, info)]
    return [apply_risk(x, risk) for x in sigs]
