# dashboard.py  ->  jalankan: streamlit run dashboard.py
import streamlit as st

st.set_page_config(page_title="Ridho Capital", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

from app.data.market import resolve_symbol
from app.ui import views
from app.ui.components import footer, inject_styles
from app.utils.symbols import clean

inject_styles()
ss = st.session_state
ss.setdefault("q", st.query_params.get("s", "BBCA"))
ss.setdefault("risk", "Moderate")
ss.setdefault("refresh_sec", 30)

ANALYSIS, SCANNER = "🔎 Analisis", "🧭 Pemindai"


def _goto_analysis():
    """Mengetik kode atau memilih pilihan cepat selalu membuka halaman Analisis."""
    v = ss.get("quick")
    if v:
        ss["q"], ss["quick"] = v, None
    ss["nav"], ss["sec"] = ANALYSIS, "Ringkasan"


top, cfg = st.columns([6, 1])
top.markdown('<div class="brand"><h1>Ridho Capital</h1><span>Analisis dan pemindai saham & emas: Swing, Scalping, Longterm</span></div>',
             unsafe_allow_html=True)
with cfg.popover("Pengaturan", width="stretch"):
    st.select_slider("Tingkat risiko", ["Conservative", "Moderate", "Aggressive"], key="risk")
    st.caption("Conservative: hanya sinyal beli keyakinan tinggi. Aggressive: skor positif tipis ikut ditandai beli.")
    st.select_slider("Segarkan harga tiap", [0, 15, 30, 60], key="refresh_sec",
                     format_func=lambda s: "Mati" if s == 0 else f"{s} detik",
                     help="Data Yahoo Finance tertunda, bukan realtime bursa.")

st.text_input("Cari saham atau emas", key="q", on_change=_goto_analysis, label_visibility="collapsed",
              help="Tanpa .JK. Tekan Enter untuk membuka analisisnya.", placeholder="Ketik kode lalu Enter, mis. BBCA, TLKM, GOTO, GOLD")
st.pills("Pilihan cepat", ["BBCA", "BBRI", "TLKM", "ANTM", "GOTO", "GOLD", "IHSG"], key="quick",
         on_change=_goto_analysis, label_visibility="collapsed")
page = st.pills("Halaman", [ANALYSIS, SCANNER], key="nav", default=ANALYSIS, label_visibility="collapsed") or ANALYSIS
st.divider()

risk = ss["risk"]
if page == SCANNER:
    views.render_scanner(risk)
else:
    if not clean(ss["q"]):
        st.info("Ketik kode saham di kolom pencarian untuk mulai.")
        st.stop()
    with st.spinner("Mencari data..."):
        symbol, df = resolve_symbol(ss["q"])
    if symbol is None:
        st.error(f"Kode “{clean(ss['q'])}” tidak ditemukan. Periksa ejaan atau coba kode lain.")
        st.stop()
    st.query_params["s"] = clean(ss["q"])
    views.render_analysis_page(symbol, df, risk)

footer()
