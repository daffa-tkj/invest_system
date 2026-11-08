# app/ui/components.py
import html
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from app.ui.styles import CSS_STYLES
from app.utils.currency import format_price
from app.utils.symbols import display_code

CONF = {"HIGH": "Keyakinan tinggi", "MEDIUM": "Keyakinan sedang", "LOW": "Keyakinan rendah"}


def inject_styles():
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def quote_header(symbol, name, last, prev, stamp=""):
    chg = last - prev
    pct = chg / prev * 100 if prev else 0
    cls = "up" if chg >= 0 else "down"
    arrow = "▲" if chg >= 0 else "▼"
    st.markdown(
        f'<div class="quote"><div><div class="code">{html.escape(display_code(symbol))}</div>'
        f'<div class="name">{html.escape(str(name))}</div></div>'
        f'<div><div class="px">{format_price(last, symbol)}</div>'
        f'<div class="chg {cls}">{arrow} {abs(chg):,.2f} ({pct:+.2f}%)</div>'
        f'<div class="name" style="text-align:right;font-size:.78rem">{stamp}</div></div></div>',
        unsafe_allow_html=True)


def _lv(label, value):
    return f"<div><small>{label}</small><b>{value}</b></div>"


def horizon_card_html(sig, symbol):
    cls = {"BUY": "buy", "SELL": "sell"}.get(sig["action"], "wait")
    fmt = lambda v: format_price(v, symbol) if v else "-"
    levels = ""
    if sig["stop_loss"] and sig["take_profit"]:
        levels = ('<div class="lv">' + _lv("Entri", fmt(sig["entry"])) + _lv("Cut loss", fmt(sig["stop_loss"]))
                  + _lv("Target", fmt(sig["take_profit"])) + (_lv("Risk:Reward", f"1 : {sig['rr']}") if sig["rr"] else "")
                  + "</div>")
    reasons = "".join(f"<li>{html.escape(r)}</li>" for r in sig["reasons"][:8]) or "<li>-</li>"
    return (f'<div class="hz {cls}"><div class="style">{sig["title"]}</div><div class="span">{sig["span"]} · {sig["tf"]}</div>'
            f'<div class="verdict">{html.escape(sig["recommendation"])}</div>'
            f'<div class="meta">Skor {sig["score"]:+d} · {CONF[sig["confidence"]]}</div>{levels}'
            f'<details><summary>Alasan ({len(sig["reasons"])})</summary><ul>{reasons}</ul></details></div>')


def horizon_cards(signals, symbol):
    st.markdown(f'<div class="horizons{" one" if len(signals) == 1 else ""}">' + "".join(horizon_card_html(s, symbol) for s in signals) + "</div>",
                unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="note">{text}</div>', unsafe_allow_html=True)


def footer():
    st.markdown('<div class="foot">Sinyal dihasilkan otomatis dari indikator teknikal dan fundamental dasar, '
                'bukan nasihat keuangan. Data Yahoo Finance bisa tertunda. Selalu pasang cut loss dan putuskan sendiri.</div>',
                unsafe_allow_html=True)


def price_chart(df, symbol, days=180):
    d = df.copy()
    for n in (20, 50, 200):
        d[f"MA{n}"] = d["Close"].rolling(n).mean()
    d = d.tail(days)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.76, 0.24], vertical_spacing=0.03)
    fig.add_trace(go.Candlestick(x=d.index, open=d["Open"], high=d["High"], low=d["Low"], close=d["Close"],
                                 name="Harga", increasing_line_color="#12a36b", decreasing_line_color="#e5484d"), 1, 1)
    for n, c in ((20, "#d99a0b"), (50, "#4c8bf5"), (200, "#9b6bdf")):
        fig.add_trace(go.Scatter(x=d.index, y=d[f"MA{n}"], name=f"MA{n}", line=dict(width=1.4, color=c)), 1, 1)
    colors = ["#12a36b" if c >= o else "#e5484d" for o, c in zip(d["Open"], d["Close"])]
    fig.add_trace(go.Bar(x=d.index, y=d["Volume"], marker_color=colors, name="Volume", opacity=.6), 2, 1)
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=10, b=0), xaxis_rangeslider_visible=False,
                      legend=dict(orientation="h", y=1.04, x=0), hovermode="x unified", bargap=0.1)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(127,127,127,.2)")
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False, "responsive": True})
