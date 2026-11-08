# app/ui/pages.py -- isi 7 tab: Top Saham, Emas + Signal, Prediksi, Search, Info, Scalping, Bandar
import math
import random
from datetime import date

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.core.analysis import (analyze_gold, compute_fundamental_score, get_foreign_flow_summary,
                               get_institutional_holders, get_realtime_broker_summary)
from app.core.horizon import apply_risk, scalping_signal
from app.core.scalping import generate_scalping_signal
from app.data.market import (batch_history, fundamentals, get_dividends, get_history, get_info, get_intraday,
                             get_news, resolve_symbol)
from app.models.forecast import exponential_smoothing
from app.ui import components as ui
from app.ui.tabs import GROUPS, _big, render_analysis, render_screener
from app.utils import config as cfg
from app.utils.broker_codes import get_broker_info, get_top_accumulators
from app.utils.currency import format_price, get_currency
from app.utils.symbols import display_code

ss = st.session_state


def _line_fig(h=380):
    fig = go.Figure()
    fig.update_layout(height=h, margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", y=1.08), hovermode="x unified")
    return fig


# ============================ 1. TOP SAHAM ============================
def render_tab1(risk):
    mode = st.radio("Peringkat berdasarkan", ["Skor fundamental", "Sinyal teknikal"], horizontal=True)
    if mode == "Sinyal teknikal":
        render_screener(risk)
        return
    c1, c2 = st.columns([3, 1])
    grp = c1.selectbox("Kelompok saham", list(GROUPS), key="fund_grp")
    topn = c2.slider("Tampilkan", 5, 30, 10)
    if st.button("Hitung skor fundamental", type="primary", width="stretch"):
        ss["fund_on"] = True
    if not ss.get("fund_on"):
        st.caption("Skor 0-100: dividen 35%, ROE 20%, konsensus analis 20%, PER 15%, utang 10%. "
                   "Pengambilan data 20-60 saham butuh sekitar 10-30 detik, hasil disimpan 1 jam.")
        return
    with st.spinner("Mengambil data fundamental..."):
        raw = fundamentals(tuple(dict.fromkeys(GROUPS[grp])))
    if raw.empty:
        st.warning("Data fundamental tidak bisa diambil saat ini. Coba lagi beberapa saat.")
        return
    df = compute_fundamental_score(raw).sort_values("total_score", ascending=False).head(topn).reset_index(drop=True)
    cols = st.columns(min(3, len(df)))
    for i, col in enumerate(cols):
        r = df.iloc[i]
        col.metric(f"#{i + 1} {display_code(r['symbol'])}", f"{r['total_score']:.0f} / 100",
                   f"Dividen {r['dividend_yield']:.1f}% · PER {r['pe_ratio']:.1f}x", delta_color="off")
    out = pd.DataFrame({"Kode": df["symbol"].map(display_code), "Nama": df["name"], "Harga": df["current_price"],
                        "Dividen %": df["dividend_yield"], "PER": df["pe_ratio"], "ROE %": df["return_on_equity"],
                        "DER": df["debt_to_equity"], "Konsensus": df["recommendation"], "Skor": df["total_score"]})
    st.dataframe(out, hide_index=True, width="stretch", column_config={
        "Harga": st.column_config.NumberColumn(format="%.0f"),
        "Dividen %": st.column_config.NumberColumn(format="%.2f"), "PER": st.column_config.NumberColumn(format="%.1f"),
        "ROE %": st.column_config.NumberColumn(format="%.1f"), "DER": st.column_config.NumberColumn(format="%.0f"),
        "Skor": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.0f")})
    st.caption("Kolom bernilai 0 berarti Yahoo Finance tidak menyediakan datanya. Buka kode saham di tab Search untuk analisis teknikal.")


# ============================ 2. EMAS + SIGNAL ============================
def _forecast(df, alpha, horizon):
    """Proyeksi + pita dari volatilitas harian. Return (tanggal, nilai, bawah, atas, mape_model, mape_naif)."""
    close = df["Close"].dropna()
    vals = np.array(exponential_smoothing(close, alpha, horizon), dtype=float)
    idx = close.index.tz_localize(None) if close.index.tz is not None else close.index
    dates = pd.bdate_range(idx[-1] + pd.Timedelta(days=1), periods=horizon)
    vol = float(close.pct_change().tail(60).std() or 0)
    band = vals[0] * 0 + float(close.iloc[-1]) * 1.28 * vol * np.sqrt(np.arange(1, horizon + 1))
    mape_m = mape_n = None
    if len(close) > 120:
        train, actual = close.iloc[:-30], close.iloc[-30:].values
        pred = np.array(exponential_smoothing(train, alpha, 30), dtype=float)
        mape_m = float(np.mean(np.abs(pred - actual) / actual) * 100)
        mape_n = float(np.mean(np.abs(float(train.iloc[-1]) - actual) / actual) * 100)
    return dates, vals, vals - band, vals + band, mape_m, mape_n


def _forecast_block(symbol, df, key):
    c1, c2 = st.columns(2)
    horizon = c1.slider("Horizon (hari bursa)", 7, 60, 30, key=f"h_{key}")
    alpha = c2.slider("Kepekaan terhadap harga terbaru", 0.1, 0.9, 0.3, 0.05, key=f"a_{key}",
                      help="Makin besar, proyeksi makin mengikuti pergerakan terakhir.")
    dates, vals, lo, hi, mm, mn = _forecast(df, alpha, horizon)
    close = df["Close"]
    hidx = close.index.tz_localize(None) if close.index.tz is not None else close.index
    fig = _line_fig(400)
    fig.add_trace(go.Scatter(x=hidx[-180:], y=close.iloc[-180:], name="Harga", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=dates, y=hi, line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=dates, y=lo, fill="tonexty", fillcolor="rgba(18,163,107,.15)", line=dict(width=0), name="Pita volatilitas"))
    fig.add_trace(go.Scatter(x=dates, y=vals, name="Proyeksi", line=dict(dash="dash", color="#12a36b", width=2)))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
    a, b, c = st.columns(3)
    a.metric(f"Proyeksi hari ke-{horizon}", format_price(float(vals[-1]), symbol), f"{(vals[-1] / close.iloc[-1] - 1) * 100:+.1f}%")
    b.metric("Kisaran (±1,28σ)", f"{format_price(float(lo[-1]), symbol)} – {format_price(float(hi[-1]), symbol)}")
    if mm is not None:
        c.metric("Uji 30 hari terakhir (MAPE)", f"{mm:.1f}%", f"naif {mn:.1f}%", delta_color="off",
                 help="Rata-rata selisih proyeksi vs harga sebenarnya pada 30 hari terakhir. 'Naif' = menganggap harga tidak berubah.")
        if mm >= mn:
            st.caption("Pada uji 30 hari terakhir, model ini tidak lebih akurat daripada menganggap harga diam. Anggap proyeksi sebagai gambaran arah tren saja.")


def render_tab2(risk):
    sym, df = resolve_symbol("GOLD")
    if sym is None:
        st.error("Data emas tidak tersedia saat ini. Coba lagi beberapa saat.")
        return
    render_analysis(sym, df, risk)

    st.subheader("Emas vs Dolar AS (DXY)")
    dxy = get_history("DX-Y.NYB", "1y", "1d")
    g = df["Close"].tail(252)
    if dxy is not None:
        gi = g.copy(); gi.index = gi.index.tz_localize(None) if gi.index.tz is not None else gi.index
        di = dxy["Close"].copy(); di.index = di.index.tz_localize(None) if di.index.tz is not None else di.index
        both = pd.concat([gi.rename("Emas"), di.rename("DXY")], axis=1).dropna()
        if len(both) > 30:
            fig = _line_fig(320)
            for col, color in (("Emas", "#d99a0b"), ("DXY", "#4c8bf5")):
                fig.add_trace(go.Scatter(x=both.index, y=both[col] / both[col].iloc[0] * 100, name=col, line=dict(color=color, width=2)))
            fig.update_yaxes(title="Indeks (awal = 100)")
            st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
            corr = both.pct_change().tail(60).corr().iloc[0, 1]
            st.metric("Korelasi harian 60 hari (Emas vs DXY)", f"{corr:+.2f}",
                      "Biasanya negatif: dolar menguat, emas cenderung tertekan" if corr < -0.2 else
                      "Hubungan sedang lemah atau searah", delta_color="off")
    else:
        st.caption("Data DXY tidak tersedia.")

    g_an = analyze_gold()
    if g_an:
        with st.expander("Indikator emas (RSI, MACD, MA50)"):
            c1, c2, c3 = st.columns(3)
            c1.metric("RSI 14", f"{g_an['rsi']:.1f}")
            c2.metric("MACD", f"{g_an['macd']:.2f}")
            c3.metric("MA50", format_price(float(g_an["ma50"]), sym))
            for line in g_an["signals"]:
                st.write(line)
    with st.expander("Proyeksi tren emas"):
        _forecast_block(sym, df, "gold")


# ============================ 3. PREDIKSI ============================
def render_tab3(sym, df):
    ui.note("Ini ekstrapolasi tren (exponential smoothing), bukan prediksi pasti. "
            "Pita dihitung dari volatilitas 60 hari terakhir, dan akurasi model diuji pada 30 hari terakhir.")
    _forecast_block(sym, df, "main")
    with st.expander("Proyeksi 30 hari saham pilihan dan emas", expanded=False):
        syms = tuple(cfg.FORECAST_STOCKS) + ("GC=F",)
        data = batch_history(syms, "2y", "1d")
        rows = []
        for s in syms:
            d = data.get(s)
            if d is None:
                continue
            _, v, lo, hi, mm, _ = _forecast(d, 0.3, 30)
            last = float(d["Close"].iloc[-1])
            rows.append({"Kode": display_code(s), "Harga": last, "Proyeksi 30 hari": float(v[-1]),
                         "Perubahan %": (v[-1] / last - 1) * 100, "Galat uji (MAPE %)": mm})
        if rows:
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", column_config={
                "Harga": st.column_config.NumberColumn(format="%.2f"), "Proyeksi 30 hari": st.column_config.NumberColumn(format="%.2f"),
                "Perubahan %": st.column_config.NumberColumn(format="%+.1f%%"), "Galat uji (MAPE %)": st.column_config.NumberColumn(format="%.1f")})


# ============================ 4. SEARCH ============================
def render_tab4(sym, df, risk):
    render_analysis(sym, df, risk)


# ============================ 5. INFO ============================
def render_tab5(sym):
    info = get_info(sym)
    if not info:
        st.warning("Profil perusahaan tidak tersedia untuk kode ini.")
    else:
        st.subheader(info.get("longName", sym))
        st.caption(f"{info.get('sector', '-')} · {info.get('industry', '-')} · {info.get('website', '')}")
        r1 = st.columns(4)
        r1[0].metric("Kapitalisasi", _big(info.get("marketCap")))
        r1[1].metric("PER", f"{info['trailingPE']:.1f}x" if info.get("trailingPE") else "-")
        r1[2].metric("PBV", f"{info['priceToBook']:.2f}x" if info.get("priceToBook") else "-")
        r1[3].metric("ROE", f"{info['returnOnEquity'] * 100:.1f}%" if info.get("returnOnEquity") else "-")
        r2 = st.columns(4)
        r2[0].metric("DER", f"{info['debtToEquity']:.0f}%" if info.get("debtToEquity") is not None else "-")
        r2[1].metric("Beta", f"{info['beta']:.2f}" if info.get("beta") else "-")
        r2[2].metric("Pendapatan", _big(info.get("totalRevenue")))
        r2[3].metric("Laba bersih", _big(info.get("netIncomeToCommon")))
        with st.expander("Tentang perusahaan", expanded=True):
            st.write(info.get("longBusinessSummary", "Deskripsi tidak tersedia"))
        offs = info.get("companyOfficers") or []
        if offs:
            with st.expander("Pengurus"):
                st.dataframe(pd.DataFrame([{"Nama": o.get("name"), "Jabatan": o.get("title")} for o in offs[:8]]),
                             hide_index=True, width="stretch")

    st.subheader("Berita terbaru")
    news = get_news(sym)
    if news:
        for title, url, src in news[:10]:
            st.markdown(f"- [{title}]({url})" + (f"  \n  <small>{src}</small>" if src else ""), unsafe_allow_html=True)
    else:
        st.caption("Tidak ada berita yang tersedia untuk kode ini dari Yahoo Finance.")

    div = get_dividends(sym)
    if div is not None:
        st.subheader("Riwayat dividen")
        yearly = div.groupby(div.index.year).sum().tail(10)
        fig = _line_fig(260)
        fig.add_trace(go.Bar(x=yearly.index.astype(str), y=yearly.values, marker_color="#12a36b", name="Dividen per saham"))
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})

    with st.expander("Pemegang saham institusi"):
        h = get_institutional_holders(sym)
        if h and h["institutional_holders"]:
            st.dataframe(pd.DataFrame(h["institutional_holders"]), hide_index=True, width="stretch")
            ff = h["fund_flow"]
            st.caption(f"Institusi {ff['held_percent_institutions']:.1f}% · Insider {ff['held_percent_insiders']:.1f}%")
        else:
            st.caption("Data pemegang institusi tidak tersedia untuk saham ini.")

    st.subheader("Grup konglomerat")
    own = [g for g in cfg.ALL_KONGLOMERAT_GROUPS if sym in g["stocks"]]
    if own:
        st.success("Saham ini termasuk grup: " + ", ".join(g["name"] for g in own))
    for g in cfg.ALL_KONGLOMERAT_GROUPS:
        with st.expander(g["name"], expanded=g in own):
            st.write(g["desc"])
            st.write("Anggota: " + ", ".join(display_code(x) for x in g["stocks"]))


# ============================ 6. SCALPING ============================
def render_tab6(sym, risk):
    s1 = apply_risk(scalping_signal(get_intraday(sym, "1h")), risk)
    s4 = apply_risk(scalping_signal(get_intraday(sym, "4h")), risk)
    ui.horizon_cards([dict(s1, title="Scalping 1 Jam"), dict(s4, title="Scalping 4 Jam")], sym)
    if "DATA KURANG" not in (s1["recommendation"], s4["recommendation"]):
        if s1["action"] == s4["action"] and s1["action"] != "WAIT":
            ui.note("<b>Searah:</b> timeframe 1 jam dan 4 jam sama-sama menunjukkan " + ("beli." if s1["action"] == "BUY" else "jual."))
        elif {s1["action"], s4["action"]} == {"BUY", "SELL"}:
            ui.note("<b>Berlawanan:</b> 1 jam dan 4 jam saling bertentangan. Sebaiknya tunggu salah satu menyesuaikan.")

    tf = st.radio("Timeframe grafik", ["1h", "4h"], format_func={"1h": "1 Jam", "4h": "4 Jam"}.get, horizontal=True)
    intr = get_intraday(sym, tf)
    if intr is None or len(intr) < 25:
        st.warning("Data intraday belum cukup. Coba saat bursa buka.")
        return
    raw = generate_scalping_signal(intr)
    if raw:
        a, b, c, d = st.columns(4)
        a.metric("ATR", f"{raw['atr']:.2f}")
        b.metric("Pivot", format_price(raw["pivot"], sym))
        c.metric("Resisten R1", format_price(raw["r1"], sym))
        d.metric("Support S1", format_price(raw["s1"], sym))
        e, f = st.columns(2)
        e.metric("Stoch RSI K / D", f"{raw['stoch_rsi_k']:.0f} / {raw['stoch_rsi_d']:.0f}")
        f.metric("EMA 5 / 10 / 20", f"{raw['ema5']:.1f} / {raw['ema10']:.1f} / {raw['ema20']:.1f}")
    ui.price_chart(intr, sym, days=120)

    with st.expander("Kalkulator ukuran posisi"):
        cur = get_currency(sym)[0]
        c1, c2 = st.columns(2)
        modal = c1.number_input(f"Modal ({cur})", min_value=0.0, value=10_000_000.0 if cur == "IDR" else 1000.0, step=1_000_000.0 if cur == "IDR" else 100.0, key=f"modal_{sym}")
        rsk = c2.number_input("Risiko per transaksi (%)", 0.1, 10.0, 1.0, 0.1, key=f"rsk_{sym}")
        entry = c1.number_input("Harga entri", min_value=0.0, value=float(s1["entry"] or 0), key=f"en_{sym}")
        sl = c2.number_input("Cut loss", min_value=0.0, value=float(s1["stop_loss"] or 0), key=f"sl_{sym}")
        tp = c1.number_input("Target", min_value=0.0, value=float(s1["take_profit"] or 0), key=f"tp_{sym}")
        per_unit = abs(entry - sl)
        if entry > 0 and per_unit > 0 and modal > 0:
            units = modal * rsk / 100 / per_unit
            lot = 100 if sym.endswith(".JK") else 1
            qty = math.floor(units / lot) * lot
            value = qty * entry
            m1, m2, m3 = st.columns(3)
            m1.metric("Jumlah lot" if lot == 100 else "Jumlah unit", f"{qty // lot:,}".replace(",", "."))
            m2.metric("Nilai posisi", format_price(value, sym), f"{value / modal * 100:.0f}% dari modal", delta_color="off")
            m3.metric("Rugi jika kena cut loss", format_price(qty * per_unit, sym))
            if value > modal:
                st.warning("Nilai posisi melebihi modal. Kecilkan risiko atau lebarkan jarak cut loss.")
            if tp > 0:
                st.caption(f"Potensi untung di target: {format_price(qty * abs(tp - entry), sym)} · rasio {abs(tp - entry) / per_unit:.2f} : 1")
        else:
            st.caption("Isi harga entri dan cut loss yang berbeda untuk menghitung ukuran posisi.")


# ============================ 7. BANDAR ============================
BANDAR_CATS = {"Foreign flow uptrend": cfg.FOREIGN_FLOW_UPTREN, "Net foreign 1 bulan": cfg.ONE_MONTH_NET_FOREIGN,
               "Akumulasi besar": cfg.BIG_ACCUMULATIONS, "Bandar akumulasi + uptrend": cfg.BANDAR_ACCUM_UPTREN,
               "Lonjakan frekuensi": cfg.FREQUENCY_SPIKES, "Insider net buy": cfg.INSIDER_NET_BUY,
               "Dividen + bandarmology": cfg.BANDARMOLOGY_DIVIDEN}


def render_tab7(sym):
    st.subheader(f"Aliran dana {display_code(sym)}")
    f = get_foreign_flow_summary(sym)
    a, b, c = st.columns(3)
    a.metric("Perubahan harga 1 bulan", f"{f['price_change_1m']:+.1f}%")
    b.metric("Lonjakan volume", f"{f['volume_surge']:.2f}x")
    c.metric("Kepemilikan institusi", f"{f['estimated_foreign_percent']:.1f}%")
    st.info(f["flow_signal"])

    st.subheader("Broker summary")
    ui.note("<b>Data broker di bagian ini simulasi acak</b> (stabil per hari), bukan data bursa asli. Jangan dipakai untuk keputusan. "
            "Sambungkan sumber broker summary resmi untuk data nyata.")
    random.seed(sum(map(ord, sym)) + date.today().toordinal())
    broker_df = get_realtime_broker_summary(sym)
    top = get_top_accumulators(broker_df, limit=10)
    if top:
        t = pd.DataFrame(top)
        fig = _line_fig(320)
        fig.add_trace(go.Bar(x=t["code"], y=t["net_vol"], marker_color=["#12a36b" if v > 0 else "#e5484d" for v in t["net_vol"]],
                             customdata=t["name"], hovertemplate="%{customdata}<br>Net %{y:,.0f}<extra></extra>", name="Net"))
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
        allb = pd.DataFrame(get_top_accumulators(broker_df, limit=99))
        by_type = allb.groupby("type")["net_vol"].sum()
        m = st.columns(3)
        m[0].metric("Net broker asing", f"{int(by_type.get('FOREIGN', 0)):,}".replace(",", "."))
        m[1].metric("Net broker lokal", f"{int(by_type.get('LOCAL', 0)):,}".replace(",", "."))
        m[2].metric("Broker akumulasi", f"{int((allb['net_vol'] > 0).sum())} dari {len(allb)}")
        tbl = t[["code", "name", "category", "buy_vol", "sell_vol", "net_vol", "action"]]
        tbl.columns = ["Kode", "Broker", "Kategori", "Beli", "Jual", "Net", "Aksi"]
        st.dataframe(tbl, hide_index=True, width="stretch")

    st.subheader("Daftar pantauan bandarmology")
    cat = st.selectbox("Kategori", list(BANDAR_CATS))
    if st.button("Pindai kategori", width="stretch"):
        ss["bd_on"] = True
    if not ss.get("bd_on"):
        return
    syms = tuple(dict.fromkeys(BANDAR_CATS[cat]))
    data = batch_history(syms, "3mo", "1d")
    rows = []
    for s, d in data.items():
        pc = (d["Close"].iloc[-1] / d["Close"].iloc[-22] - 1) * 100 if len(d) > 22 else 0
        surge = d["Volume"].tail(5).mean() / d["Volume"].tail(25).mean() if d["Volume"].tail(25).mean() else 1
        sig = ("▲ Akumulasi" if pc > 3 and surge > 1.3 else "▼ Distribusi" if pc < -3 and surge > 1.3 else "• Netral")
        rows.append({"Kode": display_code(s), "Harga": float(d["Close"].iloc[-1]), "1 bulan %": pc, "Lonjakan volume": surge, "Sinyal": sig})
    if rows:
        st.dataframe(pd.DataFrame(rows).sort_values("Lonjakan volume", ascending=False), hide_index=True, width="stretch",
                     column_config={"Harga": st.column_config.NumberColumn(format="%.0f"), "1 bulan %": st.column_config.NumberColumn(format="%+.1f%%"),
                                    "Lonjakan volume": st.column_config.NumberColumn(format="%.2fx")})
        st.caption("Daftar kategori disusun manual di config.py. Kolom sinyal dihitung dari harga dan volume terbaru (volume 5 hari vs 25 hari), bukan dari data broker.")
    else:
        st.warning("Data tidak tersedia untuk kategori ini.")
