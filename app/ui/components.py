# app/ui/components.py
import streamlit as st
import pandas as pd
from app.ui.styles import CSS_STYLES
from app.utils.currency import format_price

def inject_styles():
    st.markdown(CSS_STYLES, unsafe_allow_html=True)

def signal_card(signal):
    rec = signal['recommendation']
    
    if "BELI" in rec:
        badge_class = "buy-signal"
        icon = "🔥"
    elif "JUAL" in rec:
        badge_class = "sell-signal"
        icon = "⚠️"
    else:
        badge_class = "neutral-signal"
        icon = "⚪"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <div class="{badge_class}">
            {icon} {rec} | Score: {signal['score']:.1f} | Confidence: {signal['confidence']} {icon}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if signal.get('reasons'):
        with st.expander("📝 Detail Alasan", expanded=True):
            for reason in signal['reasons'][:5]:
                st.markdown(f"✅ {reason}")

def metric_card(label, value, delta=None, delta_color="normal"):
    if delta:
        st.metric(label, value, delta)
    else:
        st.metric(label, value)

def stock_table(df, title="Data Saham"):
    if df.empty:
        st.warning("Tidak ada data")
        return
    
    st.markdown(f"### {title}")
    
    display_df = df.copy()
    if 'current_price' in display_df.columns:
        display_df['current_price'] = display_df.apply(
            lambda x: format_price(x['current_price'], x['symbol']), axis=1
        )
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "dividend_yield": st.column_config.NumberColumn("Dividen %", format="%.2f%%"),
            "total_score": st.column_config.NumberColumn("Score", format="%.1f"),
        }
    )

def divider():
    st.markdown("<hr>", unsafe_allow_html=True)

def info_box(message, box_type="info"):
    type_class = {
        "info": "info-box-info",
        "warning": "info-box-warning", 
        "error": "info-box-error"
    }.get(box_type, "info-box-info")
    
    st.markdown(f"""
    <div class="info-box {type_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)