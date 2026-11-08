# app/ui/tabs.py
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from app.core.horizon import all_signals, swing_signal, longterm_signal, scalping_signal, apply_risk
from app.core.scalping import generate_scalping_signal
from app.utils.symbols import clean
from app.core.pattern_detector import get_latest_patterns
from app.data.market import get_info, get_intraday, batch_history, get_live_price, resolve_symbol
from app.ui import components as ui
from app.utils import config as cfg
from app.utils.currency import format_price
from app.utils.symbols import display_code


def live_quote(symbol, name, df):
    """Header harga yang menyegarkan dirinya sendiri sesuai interval di sidebar."""
    every = st.session_state.get("refresh_sec", 30) or None

    @st.fragment(run_every=every)
    def _q():
        lp = get_live_price(symbol)
        last, prev = lp if lp else (float(df["Close"].iloc[-1]), float(df["Close"].iloc[-2]))
        now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%H:%M:%S")
        ui.quote_header(symbol, name, last, prev, f"Diperbarui {now} WIB · data tertunda")
    _q()


def render_analysis(symbol, df, risk="Moderate"):
    info = get_info(symbol)
    live_quote(symbol, info.get("longName", symbol), df)
    with st.spinner("Menghitung sinyal..."):
        intraday = get_intraday(symbol, "1h")
        sigs = all_signals(symbol, df, intraday, info, risk)
    c_sum, c_star = st.columns([5, 1])
    c_sum.markdown(f'<div class="note">{summary_line(sigs)}</div>', unsafe_allow_html=True)
    inw = symbol in watchlist()
    c_star.button("★ Di watchlist" if inw else "☆ Simpan", key="star", on_click=toggle_watch, args=(symbol,),
                  width="stretch")
    ui.horizon_cards(sigs, symbol)
    if symbol.endswith(".JK"):
        ui.note("Di bursa Indonesia, sinyal <b>JUAL</b> berarti keluar atau hindari posisi. "
                "Short selling tidak tersedia untuk kebanyakan investor ritel.")

    last = df.tail(252)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tertinggi 52 mgg", format_price(float(last["High"].max()), symbol))
    c2.metric("Terendah 52 mgg", format_price(float(last["Low"].min()), symbol))
    c3.metric("Volume terakhir", f"{int(df['Volume'].iloc[-1]):,}".replace(",", "."))
    c4.metric("Rata-rata vol. 20 hari", f"{int(df['Volume'].tail(20).mean()):,}".replace(",", "."))

    st.subheader("Grafik harga")
    ui.price_chart(df, symbol, days=st.select_slider("Rentang", [60, 120, 180, 365, 500], value=180,
                                                    format_func=lambda d: f"{d} hari"))
    pats = get_latest_patterns(df, 5)
    if pats:
        with st.expander("Pola candlestick 5 hari terakhir"):
            for p in pats:
                st.write("• " + p)
    if info:
        with st.expander("Data fundamental"):
            rows = {"Sektor": info.get("sector", "-"), "Kapitalisasi pasar": info.get("marketCap"),
                    "PER": info.get("trailingPE"), "PBV": info.get("priceToBook"),
                    "ROE": info.get("returnOnEquity"), "DER": info.get("debtToEquity"),
                    "Beta": info.get("beta"), "Konsensus analis": info.get("recommendationKey")}
            st.dataframe(pd.DataFrame({"Metrik": rows.keys(), "Nilai": [str(v) if v is not None else "-" for v in rows.values()]}),
                         hide_index=True, width="stretch")


GROUPS = {"Large cap": cfg.LARGE_CAP_STOCKS, "Mid cap": cfg.MID_CAP_STOCKS, "Small cap": cfg.SMALL_CAP_STOCKS,
          "Perbankan": cfg.BANK_STOCKS, "Energi & tambang": cfg.ENERGY_STOCKS, "Konsumer": cfg.CONSUMER_STOCKS,
          "Properti": cfg.PROPERTY_STOCKS, "Infrastruktur": cfg.INFRA_STOCKS, "Retail": cfg.RETAIL_STOCKS,
          "Otomotif": cfg.AUTOMOTIVE_STOCKS, "Healthcare": cfg.HEALTHCARE_STOCKS, "Teknologi": cfg.TECH_STOCKS,
          "Telekomunikasi": cfg.TELCO_STOCKS, "Dividen (semua)": cfg.DIVIDEN_STOCKS, "Top dividen": cfg.TOP_DIVIDEN,
          "Big cap dividen murah": cfg.CHEAP_BIG_CAPS_DIVIDEN, "Mid cap dividen murah": cfg.CHEAP_MID_CAPS_DIVIDEN,
          "Small cap dividen murah": cfg.CHEAP_SMALL_CAPS_DIVIDEN, "Dividen + bandarmology": cfg.BANDARMOLOGY_DIVIDEN}


def render_screener(risk="Moderate"):
    st.caption(f"Mode risiko: {risk}")
    c1, c2, c3 = st.columns([2, 2, 1])
    group = c1.selectbox("Kelompok saham", list(GROUPS))
    style = c2.selectbox("Gaya trading", ["Swing", "Scalping", "Longterm"])
    only = c3.selectbox("Tampilkan", ["Semua", "Beli", "Jual"])
    if st.button("Pindai sekarang", type="primary", width="stretch"):
        st.session_state["scan_on"] = True
    if not st.session_state.get("scan_on"):
        st.caption("Pemindaian 30–60 saham butuh sekitar 10–40 detik. Hasil disimpan 10 menit.")
        return
    symbols = tuple(dict.fromkeys(GROUPS[group]))
    with st.spinner(f"Mengambil data {len(symbols)} saham..."):
        data = batch_history(symbols, "1mo", "1h") if style == "Scalping" else batch_history(symbols, "2y", "1d")
    rows = []
    for sym, d in data.items():
        try:
            sig = apply_risk({"Swing": lambda: swing_signal(d, sym), "Scalping": lambda: scalping_signal(d),
                              "Longterm": lambda: longterm_signal(d)}[style](), risk)
        except Exception:
            continue
        if sig["recommendation"] == "DATA KURANG":
            continue
        rows.append({"Kode": display_code(sym), "Harga": float(d["Close"].iloc[-1]), "Sinyal": sig["recommendation"],
                     "Aksi": sig["action"], "Skor": sig["score"], "Keyakinan": sig["confidence"],
                     "Cut loss": sig["stop_loss"], "Target": sig["take_profit"]})
    if not rows:
        st.warning("Tidak ada data yang bisa dihitung. Untuk Scalping, coba saat jam bursa buka.")
        return
    out = pd.DataFrame(rows)
    if only != "Semua":
        out = out[out["Aksi"] == {"Beli": "BUY", "Jual": "SELL"}[only]]
    out = out.sort_values("Skor", ascending=(only == "Jual")).drop(columns="Aksi")
    st.caption(f"{len(out)} saham sesuai filter. Longterm di pemindai memakai teknikal saja. Buka saham di tab Search untuk fundamental.")
    st.dataframe(out, hide_index=True, width="stretch", column_config={
        "Harga": st.column_config.NumberColumn(format="%.0f"), "Cut loss": st.column_config.NumberColumn(format="%.0f"),
        "Target": st.column_config.NumberColumn(format="%.0f")})


# ======================= HALAMAN (dipanggil dashboard.py) =======================
DEFAULT_WATCH = ["BBCA", "BBRI", "TLKM", "GOLD"]


def watchlist():
    return st.session_state.setdefault("watch", [("GC=F" if c == "GOLD" else c + ".JK") for c in DEFAULT_WATCH])


def toggle_watch(sym):
    wl = watchlist()
    wl.remove(sym) if sym in wl else wl.append(sym)


def summary_line(sigs):
    buy = [s["title"] for s in sigs if s["action"] == "BUY"]
    sell = [s["title"] for s in sigs if s["action"] == "SELL"]
    if buy and sell:
        return f"<b>Sinyal berbeda tiap gaya:</b> beli di {', '.join(buy)}, jual di {', '.join(sell)}. Pilih sesuai jangka waktu Anda."
    if buy:
        return f"<b>{len(buy)} dari 3 gaya menunjukkan beli:</b> {', '.join(buy)}."
    if sell:
        return f"<b>{len(sell)} dari 3 gaya menunjukkan jual atau hindari:</b> {', '.join(sell)}."
    return "<b>Belum ada sinyal jelas.</b> Tunggu konfirmasi sebelum masuk."


def _big(v):
    if not v:
        return "-"
    for div, suf in ((1e12, "T"), (1e9, "M"), (1e6, "Jt")):
        if v >= div:
            return f"{v / div:,.1f} {suf}"
    return f"{v:,.0f}"


def _wl_add():
    code = st.session_state.get("wl_add", "")
    if clean(code):
        sym, _ = resolve_symbol(code)
        if sym and sym not in watchlist():
            watchlist().append(sym)
        elif not sym:
            st.session_state["wl_msg"] = f"Kode “{clean(code)}” tidak ditemukan."
    st.session_state["wl_add"] = ""


def _open(sym):
    st.session_state["q"] = display_code(sym)
    st.session_state["nav"] = "🔍 Search"


_ICON = {"BUY": "▲ ", "SELL": "▼ ", "WAIT": "• "}


def render_watchlist(risk):
    wl = watchlist()
    st.text_input("Tambah saham", key="wl_add", on_change=_wl_add, placeholder="Ketik kode lalu tekan Enter, mis. ANTM")
    if st.session_state.pop("wl_msg", None):
        st.warning("Kode tidak ditemukan. Periksa ejaan.")
    if not wl:
        st.info("Watchlist kosong. Tambahkan saham di atas atau tekan ☆ Simpan di tab Search.")
        return
    daily = batch_history(tuple(wl), "2y", "1d")
    intra = batch_history(tuple(wl), "1mo", "1h")
    rows = []
    for sym in wl:
        d = daily.get(sym)
        if d is None:
            rows.append({"Kode": display_code(sym), "Harga": None, "Hari ini": None, "Swing": "-", "Scalping": "-", "Longterm": "-"})
            continue
        sg = [apply_risk(swing_signal(d, sym), risk), apply_risk(scalping_signal(intra.get(sym)), risk),
              apply_risk(longterm_signal(d), risk)]
        rows.append({"Kode": display_code(sym), "Harga": float(d["Close"].iloc[-1]),
                     "Hari ini": float(d["Close"].iloc[-1] / d["Close"].iloc[-2] - 1) * 100,
                     **{k: _ICON[x["action"]] + x["recommendation"] for k, x in zip(("Swing", "Scalping", "Longterm"), sg)}})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={
        "Harga": st.column_config.NumberColumn(format="%.2f"), "Hari ini": st.column_config.NumberColumn(format="%+.2f%%")})
    st.caption("▲ beli · ▼ jual atau hindari · • tunggu. Longterm di watchlist memakai teknikal saja.")
    c1, c2, c3 = st.columns([2, 1, 1])
    pick = c1.selectbox("Pilih saham", wl, format_func=display_code, label_visibility="collapsed")
    c2.button("Buka detail", on_click=_open, args=(pick,), width="stretch")
    c3.button("Hapus", on_click=toggle_watch, args=(pick,), width="stretch")
