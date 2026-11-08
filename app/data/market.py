# app/data/market.py -- semua pengambilan data pasar + cache
import pandas as pd
import streamlit as st
import yfinance as yf
from app.utils.symbols import candidates


@st.cache_data(ttl=300, show_spinner=False)
def get_history(symbol, period="2y", interval="1d"):
    try:
        df = yf.Ticker(symbol).history(period=period, interval=interval)
        return df if df is not None and not df.empty else None
    except Exception:
        return None


def resolve_symbol(query):
    """Cari simbol valid dari input bebas (tanpa .JK). Return (symbol, df_harian)."""
    for sym in candidates(query):
        df = get_history(sym, "2y", "1d")
        if df is not None and len(df) > 5:
            return sym, df
    return None, None


@st.cache_data(ttl=3600, show_spinner=False)
def get_info(symbol):
    try:
        return yf.Ticker(symbol).info or {}
    except Exception:
        return {}


def get_intraday(symbol, timeframe="1h"):
    """Data intraday untuk scalping. timeframe: '1h' atau '4h'."""
    df = get_history(symbol, "1mo", "1h")
    if df is None:
        return None
    if timeframe == "4h":
        df = df.resample("4h").agg({"Open": "first", "High": "max", "Low": "min",
                                    "Close": "last", "Volume": "sum"}).dropna()
    return df


@st.cache_data(ttl=600, show_spinner=False)
def batch_history(symbols, period="1y", interval="1d"):
    """Unduh banyak saham sekaligus untuk pemindai."""
    symbols = tuple(symbols)
    out = {}
    try:
        raw = yf.download(list(symbols), period=period, interval=interval,
                          group_by="ticker", threads=True, progress=False, auto_adjust=False)
    except Exception:
        return out
    for s in symbols:
        try:
            d = raw[s] if isinstance(raw.columns, pd.MultiIndex) else raw
            d = d.dropna(subset=["Close"])
            if len(d) > 20:
                out[s] = d
        except Exception:
            continue
    return out


@st.cache_data(ttl=15, show_spinner=False)
def get_live_price(symbol):
    """(harga terakhir, penutupan sebelumnya). Tertunda sesuai kebijakan Yahoo (IDX sekitar 10-15 menit)."""
    try:
        fi = yf.Ticker(symbol).fast_info
        return float(fi["last_price"]), float(fi["previous_close"])
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def fundamentals(symbols):
    """Data fundamental banyak saham sekaligus (paralel)."""
    from concurrent.futures import ThreadPoolExecutor
    from app.data.fetcher import get_fundamental
    with ThreadPoolExecutor(8) as ex:
        rows = [r for r in ex.map(get_fundamental, tuple(symbols)) if r]
    return pd.DataFrame(rows)


@st.cache_data(ttl=600, show_spinner=False)
def get_news(symbol):
    """Berita terbaru: list of (judul, url, sumber). Mendukung format lama dan baru yfinance."""
    out = []
    try:
        for n in (yf.Ticker(symbol).news or [])[:12]:
            c = n.get("content", n)
            url = (c.get("canonicalUrl") or {}).get("url") or c.get("link") or n.get("link")
            src = (c.get("provider") or {}).get("displayName") or c.get("publisher") or ""
            title = c.get("title")
            if title and url:
                out.append((title, url, src))
    except Exception:
        pass
    return out


@st.cache_data(ttl=3600, show_spinner=False)
def get_dividends(symbol):
    try:
        d = yf.Ticker(symbol).dividends
        return d if d is not None and not d.empty else None
    except Exception:
        return None
