# dashboard.py
import streamlit as st
from app.ui.components import inject_styles, signal_card, metric_card
from app.ui.tabs import render_tab1, render_tab2, render_tab3, render_tab4, render_tab5, render_tab6
from datetime import datetime

# Konfigurasi
st.set_page_config(
    page_title="💰 InvestIQ - Sistem Analisis Saham & Emas",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS
inject_styles()

# Title dengan HTML
st.markdown("""
<div style="text-align:center; padding:20px; background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); border-radius:20px; margin-bottom:30px;">
    <h1 style="color:white;">💰 InvestIQ Pro</h1>
    <p style="color:#e0e0e0;">Analisis Fundamental | Teknikal | Entry Signal | Scalping Emas</p>
    <p style="color:#c0c0c0; font-size:12px;">Last update: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# Sidebar dengan styling
with st.sidebar:
    st.markdown("""
    <div style="background:#2a2a3a; border-radius:15px; padding:15px; margin-bottom:20px;">
        <h3 style="color:#00b09b;">⚙️ Pengaturan</h3>
        <p style="font-size:13px; color:#a0a0b0;">Sistem real-time entry signal</p>
        <hr style="border-color:#3a3a4a;">
    </div>
    """, unsafe_allow_html=True)
    
    risk_level = st.select_slider(
        "Risk Level",
        options=["Conservative", "Moderate", "Aggressive"],
        value="Moderate"
    )
    
    st.caption("💡 Tips: Conservative = minimal buy signals")
    st.divider()
    st.markdown("**Disclaimer:** Do your own research, cunt.")

# Tabs dengan ikon
tab_titles = ["🏆 Top Saham", "🥇 Emas + Signal", "🔮 Prediksi", "🔍 Search", "📰 Info", "⚡ Scalping"]
tabs = st.tabs(tab_titles)

with tabs[0]:
    render_tab1(risk_level)
with tabs[1]:
    render_tab2()
with tabs[2]:
    render_tab3()
with tabs[3]:
    render_tab4()
with tabs[4]:
    render_tab5()
with tabs[5]:
    render_tab6()