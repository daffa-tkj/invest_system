# app/ui/tabs.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import sqlite3
from app.core.analysis import load_data, compute_fundamental_score, get_stock_data, get_institutional_holders, get_foreign_flow_summary, get_realtime_broker_summary
from app.core.entry_signal import generate_entry_signal
from app.core.scalping import get_gold_data, generate_scalping_signal
from app.core.pattern_detector import get_latest_patterns
from app.models.forecast import exponential_smoothing
from app.ui.components import signal_card, divider, info_box
from app.utils.currency import format_price, get_currency
from app.utils.broker_codes import get_broker_info
from app.utils.config import STOCKS, FORECAST_STOCKS, DB_PATH, ALL_KONGLOMERAT_GROUPS


def render_tab1(risk_level):
    """Tab Top Saham"""
    st.subheader("🏆 Rekomendasi Saham + Entry Signal")
    
    df_fund = load_data('fundamental')
    if df_fund.empty:
        st.warning("⚠️ Data fundamental kosong. Jalankan fetcher dulu.")
        return
    
    df_scored = compute_fundamental_score(df_fund)
    local_stocks = df_scored[df_scored['symbol'].str.endswith('.JK')].copy()
    
    col1, col2 = st.columns(2)
    with col1:
        min_yield = st.slider("Minimal Dividen Yield (%)", 0, 12, 3)
    with col2:
        min_score = st.slider("Minimal Fundamental Score", 0, 100, 40)
    
    filtered = local_stocks[(local_stocks['dividend_yield'] >= min_yield) &
                            (local_stocks['total_score'] >= min_score)]
    
    if filtered.empty:
        st.warning(f"Tidak ada saham dengan kriteria tersebut")
        return
    
    with st.spinner("Menghitung entry signal..."):
        stock_signals = []
        for _, row in filtered.iterrows():
            sym = row['symbol']
            df_price = get_stock_data(sym, period="3mo")
            if df_price is not None and not df_price.empty:
                signal = generate_entry_signal(df_price, sym)
                signal['dividend_yield'] = row['dividend_yield']
                signal['total_score'] = row['total_score']
                signal['name'] = row.get('name', sym)
                stock_signals.append(signal)
    
    if not stock_signals:
        st.info("Tidak ada sinyal yang dihasilkan")
        return
    
    stock_signals.sort(key=lambda x: x['score'], reverse=True)
    
    buy_count = len([s for s in stock_signals if "BELI" in s['recommendation']])
    sell_count = len([s for s in stock_signals if "JUAL" in s['recommendation']])
    
    col_stats = st.columns(4)
    col_stats[0].metric("Total Saham", len(stock_signals))
    col_stats[1].metric("BUY Signal", buy_count, delta=f"{buy_count/len(stock_signals)*100:.0f}%")
    col_stats[2].metric("SELL Signal", sell_count)
    col_stats[3].metric("Avg Score", f"{sum(s['score'] for s in stock_signals)/len(stock_signals):.1f}")
    
    divider()
    
    for sig in stock_signals[:10]:
        with st.container():
            cols = st.columns([2, 1, 1])
            cols[0].markdown(f"### {sig['symbol']}")
            cols[0].caption(sig.get('name', '')[:50])
            
            rec = sig['recommendation']
            if "BELI" in rec:
                cols[1].markdown(f"<div class='buy-signal' style='font-size:0.9rem; padding:8px 16px;'>{rec}</div>", unsafe_allow_html=True)
            elif "JUAL" in rec:
                cols[1].markdown(f"<div class='sell-signal' style='font-size:0.9rem; padding:8px 16px;'>{rec}</div>", unsafe_allow_html=True)
            else:
                cols[1].markdown(f"<div class='neutral-signal' style='font-size:0.9rem; padding:8px 16px;'>{rec}</div>", unsafe_allow_html=True)
            
            cols[2].write(f"**Score:** {sig['score']:.1f}")
            cols[2].write(f"**Confidence:** {sig['confidence']}")
            
            m_cols = st.columns(4)
            m_cols[0].metric("Harga", format_price(sig['price'], sig['symbol']))
            m_cols[1].metric("RSI", f"{sig['rsi']:.1f}")
            m_cols[2].metric("Dividen", f"{sig['dividend_yield']:.2f}%")
            m_cols[3].metric("Fund Score", f"{sig['total_score']:.1f}")
            
            with st.expander("📝 Lihat Alasan"):
                for reason in sig['reasons'][:5]:
                    st.write(f"✅ {reason}")
            
            divider()


def render_tab2():
    """Tab Emas"""
    st.subheader("🥇 Analisis Emas (XAU/USD)")
    
    conn = sqlite3.connect(DB_PATH)
    try:
        gold = pd.read_sql("SELECT * FROM gold", conn, index_col='Date', parse_dates=True)
    except:
        gold = pd.DataFrame()
    conn.close()
    
    if gold.empty:
        st.warning("⚠️ Data emas kosong. Jalankan fetcher dulu.")
        return
    
    signal = generate_entry_signal(gold, "GOLD")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Harga", f"${signal['price']:.2f}")
    col2.metric("📊 RSI", f"{signal['rsi']:.1f}",
                delta="Oversold" if signal['rsi'] < 30 else ("Overbought" if signal['rsi'] > 70 else None))
    col3.metric("📈 MACD", f"{signal['macd']:.2f}")
    col4.metric("MA50", f"${signal['ma50']:.2f}")
    
    divider()
    signal_card(signal)
    
    st.subheader("📈 Candlestick Chart - 90 Hari Terakhir")
    gold_ta = gold.copy()
    gold_ta['MA20'] = gold_ta['Close'].rolling(20).mean()
    gold_ta['MA50'] = gold_ta['Close'].rolling(50).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=gold_ta.index[-90:],
        open=gold_ta['Open'][-90:],
        high=gold_ta['High'][-90:],
        low=gold_ta['Low'][-90:],
        close=gold_ta['Close'][-90:],
        name='Emas',
        increasing_line_color='#00ffcc',
        decreasing_line_color='#ff3366'
    ))
    fig.add_trace(go.Scatter(x=gold_ta.index[-90:], y=gold_ta['MA20'][-90:], name='MA20', line=dict(color='#ffaa00', width=1.5)))
    fig.add_trace(go.Scatter(x=gold_ta.index[-90:], y=gold_ta['MA50'][-90:], name='MA50', line=dict(color='#00ccff', width=1.5)))
    
    fig.update_layout(
        title="Gold Price - 90 Days (Candlestick)",
        height=500,
        xaxis_title="Date",
        yaxis_title="USD/oz",
        template="plotly_dark",
        paper_bgcolor="#0a0a0a",
        plot_bgcolor="#1a1a2e",
        font={"color": "#e0e0e0"},
        xaxis=dict(rangeslider=dict(visible=False))
    )
    st.plotly_chart(fig, use_container_width=True)
    
    patterns = get_latest_patterns(gold, days=30)
    if patterns:
        with st.expander("🕯️ Candlestick Patterns Detected"):
            for p in patterns:
                st.write(f"🔍 {p}")


def render_tab3():
    """Tab Prediksi - Dengan semua saham + Analisis Bandar (Semua Broker Asing + Lokal) + DOM"""
    from app.utils.config import ALL_STOCKS, FORECAST_STOCKS, ALL_KONGLOMERAT_GROUPS
    from app.core.analysis import get_institutional_holders, get_foreign_flow_summary, get_realtime_broker_summary, get_broker_net_summary
    from app.utils.broker_codes import get_broker_info, BROKER_CODES
    import plotly.graph_objects as go
    from datetime import datetime, timedelta
    import random
    
    st.subheader("🔮 Prediksi Harga 30 Hari + Analisis Bandar (Semua Broker)")
    
    # ========== DROPDOWN PILIHAN ==========
    options = []
    options.append("🥇 GOLD")
    
    if ALL_KONGLOMERAT_GROUPS:
        options.append("━━━ KONGLOMERAT ━━━")
        for group in ALL_KONGLOMERAT_GROUPS:
            options.append(f"🏢 {group['name']}")
    
    options.append("━━━ SAHAM TOP ━━━")
    top_stocks = ['BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK', 
                  'ADRO.JK', 'BRPT.JK', 'TPIA.JK', 'UNVR.JK', 'ICBP.JK',
                  'CPIN.JK', 'JPFA.JK', 'PGAS.JK', 'SMGR.JK', 'TOWR.JK',
                  'BSDE.JK', 'PWON.JK', 'JSMR.JK', 'ANTM.JK', 'MDKA.JK']
    for sym in top_stocks:
        options.append(f"📈 {sym}")
    
    options.append("━━━ SEMUA SAHAM ━━━")
    all_stocks_sorted = sorted([s for s in ALL_STOCKS if '.JK' in s])
    for sym in all_stocks_sorted[:150]:
        options.append(f"📊 {sym}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected = st.selectbox("Pilih Aset / Grup / Saham", options=options, key="tab3_select")
    with col2:
        st.write("")
        st.write("")
        manual_input = st.text_input("Atau ketik kode", placeholder="BBCA.JK", key="tab3_manual").upper().strip()
        if manual_input and manual_input in ALL_STOCKS:
            selected = f"📊 {manual_input}"
    
    if selected.startswith("━━━"):
        st.info("Silakan pilih aset dari menu di atas")
        return
    
    # Tentukan list saham
    stock_list = []
    display_name = ""
    
    if selected == "🥇 GOLD":
        stock_list = ["GOLD"]
        display_name = "Emas (XAU/USD)"
    elif selected.startswith("🏢 "):
        group_name = selected.replace("🏢 ", "")
        for group in ALL_KONGLOMERAT_GROUPS:
            if group['name'] == group_name:
                stock_list = group['stocks']
                display_name = f"{group['name']} ({len(stock_list)} saham)"
                break
    elif selected.startswith("📈 ") or selected.startswith("📊 "):
        symbol = selected.split(" ")[1]
        stock_list = [symbol]
        display_name = symbol
    
    if not stock_list:
        st.warning("Tidak ada saham yang dipilih")
        return
    
    st.info(f"📊 Menampilkan: **{display_name}**")
    
    # ========== SAHAM TUNGGAL ==========
    if len(stock_list) == 1 and stock_list[0] != "GOLD":
        symbol = stock_list[0]
        
        with st.spinner(f"Mengambil data {symbol}..."):
            df_hist = get_stock_data(symbol, period="3mo")
            currency, _ = get_currency(symbol)
            price_label = "Rp" if currency == "IDR" else "$"
            
            if df_hist is None or df_hist.empty:
                st.error("Gagal mengambil data")
                return
            
            inst_data = get_institutional_holders(symbol)
            foreign_data = get_foreign_flow_summary(symbol)
            broker_df = get_realtime_broker_summary(symbol)
            
            hist_price = df_hist['Close']
            pred_values = exponential_smoothing(hist_price, forecast_days=30)
            
            current_price = hist_price.iloc[-1]
            last_pred = pred_values[-1]
            pct_change = ((last_pred - current_price) / current_price) * 100
            
            # ========== 1. METRIK ==========
            col1, col2 = st.columns(2)
            col1.metric("Harga Saat Ini", f"{price_label}{current_price:,.2f}".replace(',', '.'))
            col2.metric("Prediksi 30 Hari", f"{price_label}{last_pred:,.2f}".replace(',', '.'), delta=f"{pct_change:+.1f}%")
            
            # ========== 2. CHART ==========
            future_dates = [datetime.now() + timedelta(days=i+1) for i in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df_hist.index[-60:],
                open=df_hist['Open'][-60:],
                high=df_hist['High'][-60:],
                low=df_hist['Low'][-60:],
                close=df_hist['Close'][-60:],
                name='Historis',
                increasing_line_color='#00ffcc',
                decreasing_line_color='#ff3366'
            ))
            fig.add_trace(go.Scatter(x=future_dates, y=pred_values, name='Prediksi 30 Hari', line=dict(color='#ffaa00', width=2.5, dash='dot')))
            
            support = df_hist['Low'].rolling(20).min().iloc[-1]
            resistance = df_hist['High'].rolling(20).max().iloc[-1]
            fig.add_hline(y=support, line_dash="dash", line_color="green", annotation_text=f"Support {support:.2f}")
            fig.add_hline(y=resistance, line_dash="dash", line_color="red", annotation_text=f"Resistance {resistance:.2f}")
            
            fig.update_layout(
                title=f"{symbol} - 30 Day Forecast",
                height=450,
                template="plotly_dark",
                paper_bgcolor="#0a0a0a",
                plot_bgcolor="#1a1a2e"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # ========== 3. TRADE FLOW ==========
            st.divider()
            st.subheader("🌊 Trade Flow - Aliran Dana Asing vs Domestik")
            
            if foreign_data:
                foreign_pct = foreign_data.get('estimated_foreign_percent', 50)
                domestic_pct = foreign_data.get('estimated_domestic_percent', 50)
                insider_pct = foreign_data.get('insider_percent', 0)
                
                total = foreign_pct + domestic_pct + insider_pct
                if total > 0:
                    foreign_pct = (foreign_pct / total) * 100
                    domestic_pct = (domestic_pct / total) * 100
                    insider_pct = (insider_pct / total) * 100
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_flow = go.Figure(data=[go.Pie(
                        labels=['🌍 Asing', '🇮🇩 Domestik', '👔 Insider'],
                        values=[foreign_pct, domestic_pct, insider_pct],
                        hole=.5,
                        marker_colors=['#00ffcc', '#ff3366', '#ffaa00'],
                        textinfo='label+percent',
                        textposition='inside'
                    )])
                    fig_flow.update_layout(
                        title="Komposisi Kepemilikan",
                        height=350,
                        template="plotly_dark",
                        paper_bgcolor="#0a0a0a",
                        plot_bgcolor="#1a1a2e"
                    )
                    st.plotly_chart(fig_flow, use_container_width=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #1a1a2e; padding: 20px; border-radius: 12px; border: 1px solid #00ffcc;">
                        <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                            <span style="color: #00ffcc;">🌍 Asing</span>
                            <span style="color: #00ffcc; font-weight: bold; font-size: 18px;">{foreign_pct:.1f}%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-top: 1px solid #333;">
                            <span style="color: #ff3366;">🇮🇩 Domestik</span>
                            <span style="color: #ff3366; font-weight: bold; font-size: 18px;">{domestic_pct:.1f}%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-top: 1px solid #333;">
                            <span style="color: #ffaa00;">👔 Insider</span>
                            <span style="color: #ffaa00; font-weight: bold; font-size: 18px;">{insider_pct:.1f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    flow_signal = foreign_data.get('flow_signal', 'N/A')
                    price_change_1m = foreign_data.get('price_change_1m', 0)
                    volume_surge = foreign_data.get('volume_surge', 1)
                    
                    st.markdown(f"""
                    <div style="background: #1a1a2e; padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 4px solid #00ffcc;">
                        <strong>📊 Sinyal Aliran Dana:</strong><br>
                        {flow_signal}
                        <br><br>
                        <div style="display: flex; justify-content: space-between;">
                            <span>📈 1 Bulan: <strong style="color: {'#00ffcc' if price_change_1m > 0 else '#ff3366'}">{price_change_1m:+.1f}%</strong></span>
                            <span>📊 Volume Surge: <strong style="color: #ffaa00">{volume_surge:.1f}x</strong></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Data Trade Flow tidak tersedia")
            
            # ========== 4. BROKER FLOW ==========
            st.divider()
            st.subheader("🏦 Broker Flow - Aktivitas Semua Broker")
            
            if broker_df is not None and not broker_df.empty:
                broker_data = []
                for _, row in broker_df.iterrows():
                    code = row['BrokerCode']
                    buy = row['BuyVolume']
                    sell = row['SellVolume']
                    net = buy - sell
                    info = get_broker_info(code)
                    
                    broker_data.append({
                        'Kode': code,
                        'Nama Broker': info['name'],
                        'Tipe': '🌍 ASING' if info['type'] == 'FOREIGN' else '🇮🇩 LOKAL',
                        'Kategori': info['category'],
                        'Buy (Lot)': buy // 100,
                        'Sell (Lot)': sell // 100,
                        'Net (Lot)': net // 100,
                        'Net %': (net / (buy + sell) * 100) if (buy + sell) > 0 else 0,
                        'Aksi': '🔥 AKUMULASI' if net > 0 else ('⚠️ DISTRIBUSI' if net < 0 else '➡️ NETRAL')
                    })
                
                broker_data.sort(key=lambda x: abs(x['Net (Lot)']), reverse=True)
                st.dataframe(pd.DataFrame(broker_data), use_container_width=True, hide_index=True)
                
                # ========== 5. BROKER SUMMARY ==========
                st.divider()
                st.subheader("📊 Broker Summary - Ringkasan Akumulasi/Distribusi")
                
                total_accum = sum([d['Net (Lot)'] for d in broker_data if d['Net (Lot)'] > 0])
                total_dist = sum([abs(d['Net (Lot)']) for d in broker_data if d['Net (Lot)'] < 0])
                total_volume = sum([d['Buy (Lot)'] + d['Sell (Lot)'] for d in broker_data])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🔥 Akumulasi", f"{total_accum:+,} lot")
                with col2:
                    st.metric("⚠️ Distribusi", f"{total_dist:+,} lot")
                with col3:
                    net_flow = total_accum - total_dist
                    st.metric("Net Flow", f"{net_flow:+,} lot", 
                             delta="Bullish" if net_flow > 0 else ("Bearish" if net_flow < 0 else "Neutral"))
                with col4:
                    st.metric("Total Volume", f"{total_volume:+,} lot")
                
                # ========== BAR CHART BROKER FLOW ==========
                fig_bar = go.Figure()
                sorted_data = sorted(broker_data[:20], key=lambda x: x['Net (Lot)'], reverse=True)
                
                fig_bar.add_trace(go.Bar(
                    x=[d['Kode'] for d in sorted_data],
                    y=[d['Net (Lot)'] for d in sorted_data],
                    marker_color=['#00ffcc' if d['Net (Lot)'] > 0 else '#ff3366' for d in sorted_data],
                    text=[d['Nama Broker'][:15] for d in sorted_data],
                    textposition='outside',
                    name='Net Flow'
                ))
                
                fig_bar.update_layout(
                    title="Net Flow per Broker (Top 20)",
                    height=400,
                    template="plotly_dark",
                    paper_bgcolor="#0a0a0a",
                    plot_bgcolor="#1a1a2e",
                    xaxis_title="Kode Broker",
                    yaxis_title="Net Volume (Lot)",
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # ========== 6. RUNNING TRADE ==========
                st.divider()
                st.subheader("💼 Running Trade Realtime - Semua Broker (Asing + Lokal)")
                st.caption("⚠️ Menampilkan semua broker yang terdaftar. Harga bid/offer disimulasikan dengan spread realistis.")
                
                col_refresh1, col_refresh2, col_refresh3 = st.columns([1, 2, 1])
                with col_refresh2:
                    refresh_btn = st.button("🔄 Refresh Data Realtime", use_container_width=True, type="primary")
                
                atr = df_hist['High'].rolling(14).max() - df_hist['Low'].rolling(14).min()
                atr_value = atr.iloc[-1] if not atr.empty else current_price * 0.02
                
                spread_pct = random.uniform(0.001, 0.003)
                spread = current_price * spread_pct
                bid_price = current_price - spread/2
                offer_price = current_price + spread/2
                
                running = []
                trade_no = 0
                
                # Proses semua broker
                all_broker_codes = list(BROKER_CODES.keys())
                broker_dict = {b['Kode']: b for b in broker_data}
                
                for code in all_broker_codes:
                    if code not in broker_dict:
                        continue
                    
                    b = broker_dict[code]
                    net_lot = b['Net (Lot)']
                    info = BROKER_CODES.get(code, {})
                    
                    if net_lot > 50:
                        action = '🟢 BUY'
                        price_fluctuation = random.uniform(-0.002, 0.005) * current_price
                        current_pos = current_price + price_fluctuation
                        pnl = ((current_pos - current_price) / current_price) * 100
                        sl = current_price - atr_value * 0.5
                        tp = current_price + atr_value * 1.0
                        status = '✅ AKTIF' if pnl > -3 else '⚠️ NEAR SL'
                    elif net_lot < -50:
                        action = '🔴 SELL'
                        price_fluctuation = random.uniform(-0.005, 0.002) * current_price
                        current_pos = current_price + price_fluctuation
                        pnl = ((current_price - current_pos) / current_price) * 100
                        sl = current_price + atr_value * 0.5
                        tp = current_price - atr_value * 1.0
                        status = '✅ AKTIF' if pnl > -3 else '⚠️ NEAR SL'
                    else:
                        action = '🟡 NETRAL'
                        current_pos = current_price
                        pnl = 0
                        sl = current_price
                        tp = current_price
                        status = '⏸️ HOLD'
                    
                    type_icon = '🌍' if info.get('type') == 'FOREIGN' else '🇮🇩'
                    
                    trade_no += 1
                    running.append({
                        'No': trade_no,
                        'Kode': code,
                        'Nama Broker': info.get('name', 'Unknown')[:18],
                        'Tipe': f"{type_icon} {info.get('type', 'UNKNOWN')}",
                        'Aksi': action,
                        'Entry': f"{price_label}{current_price:,.2f}".replace(',', '.'),
                        'Bid': f"{price_label}{bid_price:,.2f}".replace(',', '.'),
                        'Offer': f"{price_label}{offer_price:,.2f}".replace(',', '.'),
                        'Current': f"{price_label}{current_pos:,.2f}".replace(',', '.'),
                        'Net (Lot)': f"{net_lot:+,}",
                        'SL': f"{price_label}{sl:,.2f}".replace(',', '.'),
                        'TP': f"{price_label}{tp:,.2f}".replace(',', '.'),
                        'P&L': f"{pnl:+.2f}%",
                        'Status': status,
                        'Spread': f"{spread_pct*100:.3f}%"
                    })
                
                if running:
                    st.dataframe(pd.DataFrame(running), use_container_width=True, hide_index=True)
                    
                    # ====== METRIK REALTIME ======
                    st.markdown("#### 📊 Realtime Market Data")
                    col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
                    with col_r1:
                        st.metric("💰 Harga", f"{price_label}{current_price:,.2f}".replace(',', '.'))
                    with col_r2:
                        st.metric("📈 Bid", f"{price_label}{bid_price:,.2f}".replace(',', '.'), delta="Beli")
                    with col_r3:
                        st.metric("📉 Offer", f"{price_label}{offer_price:,.2f}".replace(',', '.'), delta="Jual")
                    with col_r4:
                        st.metric("📊 Spread", f"{(spread/current_price*100):.3f}%")
                    with col_r5:
                        total_pnl = 0
                        for t in running:
                            try:
                                pnl_val = float(t['P&L'].replace('%', '').replace('+', ''))
                                total_pnl += pnl_val
                            except:
                                pass
                        st.metric("💵 Total P&L", f"{total_pnl:+.2f}%", 
                                 delta="Profit" if total_pnl > 0 else ("Loss" if total_pnl < 0 else "BEP"))
                    
                    # ====== STATISTIK POSISI ======
                    buy_trades = [t for t in running if 'BUY' in t['Aksi']]
                    sell_trades = [t for t in running if 'SELL' in t['Aksi']]
                    netral_trades = [t for t in running if 'NETRAL' in t['Aksi']]
                    active_trades = [t for t in running if 'AKTIF' in t['Status']]
                    near_sl = [t for t in running if 'NEAR SL' in t['Status']]
                    
                    col_stat1, col_stat2, col_stat3, col_stat4, col_stat5 = st.columns(5)
                    with col_stat1:
                        st.metric("🟢 BUY", len(buy_trades))
                    with col_stat2:
                        st.metric("🔴 SELL", len(sell_trades))
                    with col_stat3:
                        st.metric("🟡 NETRAL", len(netral_trades))
                    with col_stat4:
                        st.metric("✅ Aktif", len(active_trades))
                    with col_stat5:
                        st.metric("⚠️ Near SL", len(near_sl), delta="⚠️" if near_sl else "✅")
                    
                    # ====== BROKER DOMINAN ======
                    st.markdown("#### 🏆 Broker Teratas")
                    
                    foreign_brokers = [t for t in running if 'FOREIGN' in t['Tipe'] and ('BUY' in t['Aksi'] or 'SELL' in t['Aksi'])]
                    local_brokers = [t for t in running if 'LOKAL' in t['Tipe'] and ('BUY' in t['Aksi'] or 'SELL' in t['Aksi'])]
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if foreign_brokers:
                            st.markdown("##### 🌍 Top 5 Broker Asing")
                            for b in foreign_brokers[:5]:
                                st.write(f"{b['Kode']} - {b['Nama Broker']}: {b['Aksi']} (Net: {b['Net (Lot)']})")
                        else:
                            st.info("Tidak ada broker asing aktif")
                    
                    with col_b2:
                        if local_brokers:
                            st.markdown("##### 🇮🇩 Top 5 Broker Lokal")
                            for b in local_brokers[:5]:
                                st.write(f"{b['Kode']} - {b['Nama Broker']}: {b['Aksi']} (Net: {b['Net (Lot)']})")
                        else:
                            st.info("Tidak ada broker lokal aktif")
                    
                    # ====== SINYAL TRADING ======
                    if len(buy_trades) > len(sell_trades):
                        st.success("📈 **Sinyal Bullish** - Lebih banyak posisi BUY dari broker. Pertimbangkan entry di area support.")
                    elif len(sell_trades) > len(buy_trades):
                        st.warning("📉 **Sinyal Bearish** - Lebih banyak posisi SELL dari broker. Pertimbangkan exit di area resistance.")
                    else:
                        st.info("➡️ **Netral** - Posisi BUY dan SELL seimbang. Tunggu konfirmasi arah.")
                    
                    if near_sl:
                        st.error(f"⚠️ **{len(near_sl)} posisi mendekati Stop Loss!** Pertimbangkan cut loss atau trailing stop.")
                    
                    st.caption("⚠️ **Disclaimer:** Running Trade adalah simulasi berdasarkan data broker. Bukan rekomendasi investasi.")
                    
                    # ====== AUTO-REFRESH ======
                    st.markdown(f"""
                    <div style="background: #1a1a2e; padding: 8px 16px; border-radius: 8px; margin-top: 10px; border: 1px solid #00ffcc;">
                        <span style="color: #00ffcc;">🔄</span> 
                        <span style="color: #aaaaaa;">Data diupdate secara realtime. Klik tombol Refresh untuk update terbaru.</span>
                        <span style="color: #00ffcc; float: right;">⏱️ Last update: {datetime.now().strftime('%H:%M:%S')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ========== 7. DOM (Depth of Market) ==========
                st.divider()
                st.subheader("📊 DOM (Depth of Market) - Level 2 Data")
                st.caption("Menampilkan volume bid (beli) dan offer (jual) di setiap level harga")
                
                def gen_dom(price, label, n=11):
                    step = price * 0.001 / 2
                    
                    bid_p = [price - (i+1)*step for i in range(n)]
                    bid_v = [int(random.uniform(15000, 120000) * (1 + (n-i)/n)) for i in range(n)]
                    bid_f = [int(random.uniform(100, 2000)) for i in range(n)]
                    
                    offer_p = [price + (i+1)*step for i in range(n)]
                    offer_v = [int(random.uniform(15000, 120000) * (1 + (n-i)/n)) for i in range(n)]
                    offer_f = [int(random.uniform(100, 2000)) for i in range(n)]
                    
                    return bid_p, offer_p, bid_v, offer_v, bid_f, offer_f
                
                bid_p, offer_p, bid_v, offer_v, bid_f, offer_f = gen_dom(current_price, price_label)
                
                dom_rows = []
                for i in range(len(bid_p)):
                    dom_rows.append({
                        'Freq': f"{bid_f[i]:,}",
                        'Lot': f"{bid_v[i]:,}",
                        'Bid': f"{price_label}{bid_p[i]:,.0f}".replace(',', '.'),
                        'Offer': '',
                        'Lot_Offer': '',
                        'Freq_Offer': ''
                    })
                
                dom_rows.append({
                    'Freq': '-',
                    'Lot': '-',
                    'Bid': f"{price_label}{current_price:,.0f}".replace(',', '.'),
                    'Offer': f"{price_label}{current_price:,.0f}".replace(',', '.'),
                    'Lot_Offer': '-',
                    'Freq_Offer': '-'
                })
                
                for i in range(len(offer_p)):
                    dom_rows.append({
                        'Freq': '',
                        'Lot': '',
                        'Bid': '',
                        'Offer': f"{price_label}{offer_p[i]:,.0f}".replace(',', '.'),
                        'Lot_Offer': f"{offer_v[i]:,}",
                        'Freq_Offer': f"{offer_f[i]:,}"
                    })
                
                st.dataframe(pd.DataFrame(dom_rows), use_container_width=True, hide_index=True)
                
                # ====== VISUALISASI DOM ======
                fig_dom = go.Figure()
                fig_dom.add_trace(go.Bar(
                    x=bid_p,
                    y=[-v for v in bid_v],
                    name='Bid (Beli)',
                    marker_color='#00ffcc',
                    orientation='v'
                ))
                fig_dom.add_trace(go.Bar(
                    x=offer_p,
                    y=offer_v,
                    name='Offer (Jual)',
                    marker_color='#ff3366',
                    orientation='v'
                ))
                fig_dom.add_vline(x=current_price, line_dash="dash", line_color="#ffaa00")
                fig_dom.update_layout(
                    title="Depth of Market - Bid vs Offer",
                    height=350,
                    template="plotly_dark",
                    paper_bgcolor="#0a0a0a",
                    plot_bgcolor="#1a1a2e",
                    barmode='relative'
                )
                st.plotly_chart(fig_dom, use_container_width=True)
                
                # ====== DOM SUMMARY ======
                total_bid = sum(bid_v)
                total_offer = sum(offer_v)
                
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    st.metric("📥 Total Bid Volume", f"{total_bid:,} lot")
                with col_d2:
                    st.metric("📤 Total Offer Volume", f"{total_offer:,} lot")
                with col_d3:
                    imbalance = total_bid - total_offer
                    st.metric("⚖️ Volume Imbalance", f"{imbalance:+,} lot", 
                             delta="Bid Dominant" if imbalance > 0 else ("Offer Dominant" if imbalance < 0 else "Balanced"))
                
                # ========== INSTITUTIONAL HOLDERS ==========
                if inst_data:
                    with st.expander("🏛️ Institutional Holders (Data Institusi)"):
                        if inst_data.get('institutional_holders'):
                            df_inst = pd.DataFrame(inst_data['institutional_holders'])
                            st.dataframe(df_inst, use_container_width=True, hide_index=True)
                        else:
                            st.info("Tidak ada data institutional holders")
                
            else:
                st.warning("Data Broker tidak tersedia untuk saham ini")
            
            # ========== DETAIL PREDIKSI ==========
            with st.expander("📊 Detail Prediksi 30 Hari"):
                pred_df = pd.DataFrame({
                    'Hari': list(range(1, 31)),
                    'Tanggal': [(datetime.now() + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(1, 31)],
                    'Prediksi': [f"{price_label}{p:,.2f}".replace(',', '.') for p in pred_values],
                    'Perubahan': [f"{((p - current_price)/current_price*100):+.2f}%" for p in pred_values]
                })
                st.dataframe(pred_df, use_container_width=True, hide_index=True)
                
                fig_pred = go.Figure()
                fig_pred.add_trace(go.Scatter(
                    x=list(range(1, 31)),
                    y=pred_values,
                    mode='lines+markers',
                    name='Prediksi',
                    line=dict(color='#00ffcc', width=2),
                    marker=dict(size=6)
                ))
                fig_pred.add_hline(y=current_price, line_dash="dash", line_color="gray", annotation_text="Harga Saat Ini")
                fig_pred.update_layout(
                    title="Trend Prediksi 30 Hari",
                    height=300,
                    template="plotly_dark",
                    paper_bgcolor="#0a0a0a",
                    plot_bgcolor="#1a1a2e",
                    xaxis_title="Hari ke-",
                    yaxis_title="Harga"
                )
                st.plotly_chart(fig_pred, use_container_width=True)
            
            # ========== CANDLESTICK PATTERNS ==========
            from app.core.pattern_detector import get_latest_patterns
            patterns = get_latest_patterns(df_hist, days=30)
            if patterns:
                with st.expander("🕯️ Candlestick Patterns Detected"):
                    for p in patterns:
                        st.write(f"🔍 {p}")
    
    # ========== GOLD ==========
    elif len(stock_list) == 1 and stock_list[0] == "GOLD":
        with st.spinner("Menghitung prediksi emas..."):
            ticker = yf.Ticker("GC=F")
            df_hist = ticker.history(period="3mo")
            if df_hist is not None and not df_hist.empty:
                hist_price = df_hist['Close']
                pred_values = exponential_smoothing(hist_price, forecast_days=30)
                current_price = hist_price.iloc[-1]
                last_pred = pred_values[-1]
                pct_change = ((last_pred - current_price) / current_price) * 100
                
                col1, col2 = st.columns(2)
                col1.metric("Harga Saat Ini", f"${current_price:.2f}")
                col2.metric("Prediksi 30 Hari", f"${last_pred:.2f}", delta=f"{pct_change:+.1f}%")
                
                future_dates = [datetime.now() + timedelta(days=i+1) for i in range(30)]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_hist.index[-60:], y=hist_price[-60:], name='Historis', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=future_dates, y=pred_values, name='Prediksi', line=dict(color='#ffaa00', dash='dot')))
                fig.update_layout(title="Gold - 30 Day Forecast", height=450, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
                # Running Trade Gold
                st.divider()
                st.subheader("💼 Running Trade - Emas")
                
                spread_pct = random.uniform(0.0005, 0.0015)
                spread = current_price * spread_pct
                bid_price = current_price - spread/2
                offer_price = current_price + spread/2
                
                atr = df_hist['High'].rolling(14).max() - df_hist['Low'].rolling(14).min()
                atr_value = atr.iloc[-1] if not atr.empty else current_price * 0.02
                
                if pct_change > 1:
                    action = '🟢 BUY'
                    sl = current_price - atr_value * 0.5
                    tp = current_price + atr_value * 1.5
                    pnl = random.uniform(-0.3, 1.5)
                elif pct_change < -1:
                    action = '🔴 SELL'
                    sl = current_price + atr_value * 0.5
                    tp = current_price - atr_value * 1.5
                    pnl = random.uniform(-1.5, 0.3)
                else:
                    action = '🟡 HOLD'
                    sl = current_price
                    tp = current_price
                    pnl = 0
                
                trade_data = [{
                    'No': 1,
                    'Broker': 'Sistem - Prediksi',
                    'Aksi': action,
                    'Entry': f"${current_price:.2f}",
                    'Bid': f"${bid_price:.2f}",
                    'Offer': f"${offer_price:.2f}",
                    'SL': f"${sl:.2f}",
                    'TP': f"${tp:.2f}",
                    'P&L': f"{pnl:+.2f}%",
                    'Spread': f"{spread_pct*100:.3f}%"
                }]
                st.dataframe(pd.DataFrame(trade_data), use_container_width=True, hide_index=True)
                
                # DOM Gold
                st.divider()
                st.subheader("📊 DOM (Depth of Market)")
                
                def gen_dom_gold(price, n=11):
                    step = price * 0.0005 / 2
                    bid_p = [price - (i+1)*step for i in range(n)]
                    bid_v = [int(random.uniform(1500, 12000) * (1 + (n-i)/n)) for i in range(n)]
                    bid_f = [int(random.uniform(50, 500)) for i in range(n)]
                    offer_p = [price + (i+1)*step for i in range(n)]
                    offer_v = [int(random.uniform(1500, 12000) * (1 + (n-i)/n)) for i in range(n)]
                    offer_f = [int(random.uniform(50, 500)) for i in range(n)]
                    return bid_p, offer_p, bid_v, offer_v, bid_f, offer_f
                
                bid_p, offer_p, bid_v, offer_v, bid_f, offer_f = gen_dom_gold(current_price)
                
                dom_rows = []
                for i in range(len(bid_p)):
                    dom_rows.append({
                        'Freq': f"{bid_f[i]:,}",
                        'Lot': f"{bid_v[i]:,}",
                        'Bid': f"${bid_p[i]:.2f}",
                        'Offer': '',
                        'Lot_Offer': '',
                        'Freq_Offer': ''
                    })
                
                dom_rows.append({
                    'Freq': '-',
                    'Lot': '-',
                    'Bid': f"${current_price:.2f}",
                    'Offer': f"${current_price:.2f}",
                    'Lot_Offer': '-',
                    'Freq_Offer': '-'
                })
                
                for i in range(len(offer_p)):
                    dom_rows.append({
                        'Freq': '',
                        'Lot': '',
                        'Bid': '',
                        'Offer': f"${offer_p[i]:.2f}",
                        'Lot_Offer': f"{offer_v[i]:,}",
                        'Freq_Offer': f"{offer_f[i]:,}"
                    })
                
                st.dataframe(pd.DataFrame(dom_rows), use_container_width=True, hide_index=True)
                
                fig_dom = go.Figure()
                fig_dom.add_trace(go.Bar(
                    x=bid_p,
                    y=[-v for v in bid_v],
                    name='Bid',
                    marker_color='#00ffcc',
                    orientation='v'
                ))
                fig_dom.add_trace(go.Bar(
                    x=offer_p,
                    y=offer_v,
                    name='Offer',
                    marker_color='#ff3366',
                    orientation='v'
                ))
                fig_dom.add_vline(x=current_price, line_dash="dash", line_color="#ffaa00")
                fig_dom.update_layout(
                    title="Depth of Market - Gold",
                    height=350,
                    template="plotly_dark",
                    paper_bgcolor="#0a0a0a",
                    plot_bgcolor="#1a1a2e",
                    barmode='relative'
                )
                st.plotly_chart(fig_dom, use_container_width=True)
                
                st.info("🥇 Untuk emas, analisis bandar tidak tersedia karena hanya untuk saham.")
    
    # ========== MULTIPLE STOCKS ==========
    else:
        st.subheader(f"📊 {display_name}")
        
        data = []
        for sym in stock_list:
            df = get_stock_data(sym, period="3mo")
            if df is not None and not df.empty:
                hist = df['Close']
                pred = exponential_smoothing(hist, forecast_days=30)
                current = hist.iloc[-1]
                last = pred[-1]
                pct = ((last - current) / current) * 100
                
                broker_net = get_broker_net_summary(sym)
                if broker_net:
                    top = broker_net[0] if broker_net else None
                    signal = "🔥 AKUMULASI" if top and top['is_accumulate'] else ("⚠️ DISTRIBUSI" if top and top['is_distribute'] else "➡️ NETRAL")
                    name = get_broker_info(top['broker_code'])['name'] if top else "N/A"
                else:
                    signal = "N/A"
                    name = "N/A"
                
                data.append({
                    'Kode': sym,
                    'Harga': format_price(current, sym),
                    'Prediksi 30H': format_price(last, sym),
                    'Perubahan': f"{pct:+.1f}%",
                    'Trend': '📈' if pct > 2 else ('📉' if pct < -2 else '➡️'),
                    'Broker Signal': signal,
                    'Top Broker': name
                })
        
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

def render_tab4():
    """Tab Search Saham + Profil Perusahaan Lengkap"""
    from app.utils.config import ALL_STOCKS, ALL_KONGLOMERAT_GROUPS
    from app.core.analysis import get_stock_info, get_stock_data, load_data
    from app.core.entry_signal import generate_entry_signal
    from app.ui.components import signal_card, divider
    from app.utils.currency import format_price
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import streamlit as st
    
    st.subheader("🔍 Cari Saham & Lihat Profil Perusahaan")
    st.caption("Cari kode saham (contoh: BBCA.JK, ADRO.JK, ANTM.JK) atau pilih dari daftar")
    
    # ========== SEARCH MANUAL - TAMPILAN SIMETRIS ==========
    st.markdown("### 🔍 Cari Manual")
    
    # Initial session state
    if 'search_symbol' not in st.session_state:
        st.session_state.search_symbol = ""
    if 'search_triggered' not in st.session_state:
        st.session_state.search_triggered = False
    
    # Pake 3 kolom biar simetris
    col_left, col_mid, col_right = st.columns([1, 6, 1])
    
    with col_mid:
        with st.form(key="search_form", clear_on_submit=False):
            col_input, col_button = st.columns([4, 1])
            with col_input:
                search_input = st.text_input(
                    "Ketik kode saham (contoh: BBCA.JK, ADRO.JK, ANTM.JK)", 
                    placeholder="Masukkan kode saham...",
                    key="form_search_input",
                    label_visibility="collapsed"
                ).upper().strip()
            
            with col_button:
                submitted = st.form_submit_button("🔍 CARI", type="primary", use_container_width=True)
    
    # Proses search dari form
    if submitted and search_input:
        if search_input in ALL_STOCKS or search_input.endswith('.JK'):
            st.session_state.search_symbol = search_input
            st.session_state.search_triggered = True
            st.rerun()
        else:
            st.error(f"❌ Kode saham '{search_input}' tidak ditemukan. Gunakan format seperti BBCA.JK, ADRO.JK, ANTM.JK")
    
    # Reset jika tidak ada input
    if not search_input and not st.session_state.search_triggered:
        st.session_state.search_symbol = ""
    
    # Gunakan dari session state
    symbol = st.session_state.search_symbol if st.session_state.search_triggered else None
    
    # ========== ATAU PILIH DARI DAFTAR (ALTERNATIF) ==========
    if not symbol:
        st.markdown("---")
        st.markdown("### 📋 Atau Pilih dari Daftar")
        
        col_opt_left, col_opt_mid, col_opt_right = st.columns([1, 4, 1])
        with col_opt_mid:
            search_options = []
            
            # Grup konglomerat
            if ALL_KONGLOMERAT_GROUPS:
                for group in ALL_KONGLOMERAT_GROUPS:
                    search_options.append((f"🏛️ {group['name']}", f"GROUP_{group['name']}", group['desc']))
            
            if search_options:
                search_options.append(("━━━━━━━━━━━━━━━━━━━━", "SEPARATOR", ""))
            
            # Saham top
            top_stocks = ['BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK', 
                          'ADRO.JK', 'BRPT.JK', 'TPIA.JK', 'UNVR.JK', 'ICBP.JK',
                          'CPIN.JK', 'JPFA.JK', 'PGAS.JK', 'SMGR.JK', 'TOWR.JK',
                          'BSDE.JK', 'PWON.JK', 'JSMR.JK', 'ANTM.JK', 'MDKA.JK']
            for sym in top_stocks:
                search_options.append((f"📈 {sym}", sym, ""))
            
            if top_stocks:
                search_options.append(("━━━━━━━━━━━━━━━━━━━━", "SEPARATOR", ""))
                search_options.append(("✏️ Atau ketik manual di atas", "MANUAL", ""))
            
            selected_item = st.selectbox(
                "Pilih Grup Konglomerat / Saham Top", 
                options=search_options, 
                format_func=lambda x: x[0],
                key="dropdown_select",
                label_visibility="collapsed"
            )
            
            selected_value = selected_item[1]
            
            if selected_value == "SEPARATOR":
                st.info("Pilih grup konglomerat atau saham dari menu di atas")
                return
            elif selected_value == "MANUAL":
                st.info("Silakan ketik kode saham di kotak pencarian manual di atas")
                return
            elif selected_value.startswith("GROUP_"):
                # Proses grup konglomerat
                group_name = selected_value.replace("GROUP_", "")
                for group in ALL_KONGLOMERAT_GROUPS:
                    if group['name'] == group_name:
                        st.markdown(f"## 🏛️ {group['name']}")
                        st.caption(group['desc'])
                        stocks_in_group = group['stocks']
                        st.markdown(f"**Jumlah Saham:** {len(stocks_in_group)}")
                        
                        with st.spinner(f"Mengambil data untuk {len(stocks_in_group)} saham..."):
                            group_data = []
                            for sym in stocks_in_group:
                                df_price = get_stock_data(sym, period="3mo")
                                if df_price is not None and not df_price.empty:
                                    sig = generate_entry_signal(df_price, sym)
                                    df_fund = load_data('fundamental')
                                    fund_row = df_fund[df_fund['symbol'] == sym]
                                    div_yield = fund_row['dividend_yield'].values[0] if not fund_row.empty else 0
                                    group_data.append({
                                        'Kode': sym,
                                        'Harga': format_price(sig['price'], sym),
                                        'RSI': f"{sig['rsi']:.1f}",
                                        'Sinyal': sig['recommendation'],
                                        'Score': sig['score'],
                                        'Dividen %': f"{div_yield:.2f}%"
                                    })
                            
                            if group_data:
                                df_group = pd.DataFrame(group_data)
                                st.dataframe(df_group, use_container_width=True, hide_index=True)
                                buy_count = len([d for d in group_data if "BELI" in d['Sinyal']])
                                sell_count = len([d for d in group_data if "JUAL" in d['Sinyal']])
                                c1, c2, c3 = st.columns(3)
                                c1.metric("Total Saham", len(group_data))
                                c2.metric("BUY Signal", buy_count)
                                c3.metric("SELL Signal", sell_count)
                        return
            else:
                symbol = selected_value
                st.session_state.search_symbol = symbol
                st.session_state.search_triggered = True
                st.rerun()
    
    # Jika belum ada symbol
    if not symbol:
        if not search_input and not st.session_state.search_triggered:
            st.info("💡 Silakan ketik kode saham di kotak pencarian atau pilih dari daftar di atas")
        return
    
    # ========== TAMPILKAN PROFIL PERUSAHAAN LENGKAP ==========
    with st.spinner(f"📊 Mengambil data {symbol}..."):
        # Ambil data harga
        df = get_stock_data(symbol, period="6mo")
        
        if df is None or df.empty:
            st.error(f"❌ Data {symbol} tidak ditemukan. Periksa kode saham.")
            st.session_state.search_triggered = False
            st.session_state.search_symbol = ""
            return
        
        # Ambil info perusahaan
        info = get_stock_info(symbol)
        
        # Generate entry signal
        signal = generate_entry_signal(df, symbol)
        
        # ========== HEADER PROFIL ==========
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 16px; margin-bottom: 20px; border-left: 4px solid #00ffcc;">
            <h1 style="color: #00ffcc; margin: 0;">{symbol}</h1>
            <h3 style="color: #ffffff; margin-top: 8px;">{info.get('name', 'N/A') if info else 'N/A'}</h3>
            <p style="color: #aaaaaa; margin-top: 8px;">
                📍 {info.get('sector', 'N/A') if info else 'N/A'} | 🏭 {info.get('industry', 'N/A') if info else 'N/A'}
            </p>
            <p style="color: #888888; font-size: 12px;">
                🌐 <a href="{info.get('website', '#')}" style="color: #00ffcc;" target="_blank">{info.get('website', 'N/A')}</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== METRIK UTAMA ==========
        st.markdown("### 📊 Ringkasan")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            price_change = 0
            if len(df) > 1:
                price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            st.metric("💰 Harga", format_price(signal['price'], symbol), delta=f"{price_change:+.2f}%")
        with col2:
            st.metric("📊 RSI (14)", f"{signal['rsi']:.1f}")
        with col3:
            signal_color = "🟢" if "BELI" in signal['recommendation'] else ("🔴" if "JUAL" in signal['recommendation'] else "🟡")
            st.metric("🎯 Sinyal", f"{signal_color} {signal['recommendation']}")
        with col4:
            st.metric("⭐ Skor Teknikal", f"{signal['score']:.1f}")
        
        divider()
        signal_card(signal)
        
        # ========== PROFIL PERUSAHAAN ==========
        st.markdown("### 🏢 Profil Perusahaan")
        
        if info:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("**📋 Informasi Dasar**")
                st.write(f"• **Nama Lengkap**: {info.get('name', 'N/A')}")
                st.write(f"• **Sektor**: {info.get('sector', 'N/A')}")
                st.write(f"• **Industri**: {info.get('industry', 'N/A')}")
                st.write(f"• **Kantor Pusat**: {info.get('country', 'Indonesia')}")
                if info.get('website'):
                    st.write(f"• **Website**: [{info.get('website')}]({info.get('website')})")
            
            with col_p2:
                st.markdown("**👥 Manajemen & Karyawan**")
                officers = info.get('companyOfficers', [])
                if officers and len(officers) > 0:
                    st.write(f"• **CEO/President**: {officers[0].get('name', 'N/A')}")
                else:
                    st.write(f"• **CEO/President**: N/A")
                if info.get('fullTimeEmployees'):
                    st.write(f"• **Jumlah Karyawan**: {info.get('fullTimeEmployees'):,}")
                else:
                    st.write(f"• **Jumlah Karyawan**: N/A")
        else:
            st.warning("Data fundamental tidak tersedia untuk saham ini")
        
        # ========== DESKRIPSI BISNIS ==========
        st.markdown("### 📝 Deskripsi Bisnis")
        if info and info.get('longBusinessSummary'):
            summary = info.get('longBusinessSummary')
            if len(summary) > 500:
                with st.expander("Lihat deskripsi lengkap"):
                    st.write(summary)
            else:
                st.write(summary)
        else:
            st.info("Deskripsi bisnis tidak tersedia untuk saham ini")
        
        # ========== KEUANGAN & VALUASI ==========
        st.markdown("### 💰 Keuangan & Valuasi")
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            market_cap = info.get('marketCap', 0) if info else 0
            if market_cap >= 1e12:
                cap_text = f"{market_cap/1e12:.2f} T"
            elif market_cap >= 1e9:
                cap_text = f"{market_cap/1e9:.2f} M"
            elif market_cap >= 1e6:
                cap_text = f"{market_cap/1e6:.2f} B"
            else:
                cap_text = "N/A"
            st.metric("Market Cap", cap_text)
        with col_f2:
            pe = info.get('trailingPE', 0) if info else 0
            st.metric("P/E Ratio", f"{pe:.2f}" if pe > 0 else "N/A")
        with col_f3:
            pb = info.get('priceToBook', 0) if info else 0
            st.metric("P/B Ratio", f"{pb:.2f}" if pb > 0 else "N/A")
        with col_f4:
            ps = info.get('priceToSalesTrailing12Months', 0) if info else 0
            st.metric("P/S Ratio", f"{ps:.2f}" if ps > 0 else "N/A")
        
        col_f5, col_f6, col_f7, col_f8 = st.columns(4)
        with col_f5:
            roe = info.get('returnOnEquity', 0) * 100 if info and info.get('returnOnEquity') else 0
            st.metric("ROE", f"{roe:.2f}%" if roe != 0 else "N/A")
        with col_f6:
            debt = info.get('debtToEquity', 0) if info else 0
            st.metric("Debt to Equity", f"{debt:.2f}%" if debt > 0 else "N/A")
        with col_f7:
            div_yield = info.get('dividendYield', 0) * 100 if info and info.get('dividendYield') else 0
            st.metric("Dividen Yield", f"{div_yield:.2f}%" if div_yield > 0 else "N/A")
        with col_f8:
            beta = info.get('beta', 0) if info else 0
            st.metric("Beta", f"{beta:.2f}" if beta > 0 else "N/A")
        
        # ========== KINERJA KEUANGAN TTM ==========
        if info and (info.get('totalRevenue', 0) > 0 or info.get('netIncomeToCommon', 0) > 0):
            st.markdown("### 📈 Kinerja Keuangan (Trailing Twelve Months)")
            
            col_k1, col_k2, col_k3 = st.columns(3)
            with col_k1:
                revenue = info.get('totalRevenue', 0)
                if revenue >= 1e12:
                    rev_text = f"Rp {revenue/1e12:.2f} Triliun"
                elif revenue >= 1e9:
                    rev_text = f"Rp {revenue/1e9:.2f} Miliar"
                else:
                    rev_text = f"Rp {revenue/1e6:.2f} Juta" if revenue > 0 else "N/A"
                st.metric("Total Pendapatan", rev_text)
            with col_k2:
                net_income = info.get('netIncomeToCommon', 0)
                if net_income >= 1e12:
                    inc_text = f"Rp {net_income/1e12:.2f} Triliun"
                elif net_income >= 1e9:
                    inc_text = f"Rp {net_income/1e9:.2f} Miliar"
                else:
                    inc_text = f"Rp {net_income/1e6:.2f} Juta" if net_income > 0 else "N/A"
                st.metric("Laba Bersih", inc_text)
            with col_k3:
                ebitda = info.get('ebitda', 0)
                if ebitda >= 1e12:
                    ebitda_text = f"Rp {ebitda/1e12:.2f} Triliun"
                elif ebitda >= 1e9:
                    ebitda_text = f"Rp {ebitda/1e9:.2f} Miliar"
                else:
                    ebitda_text = f"Rp {ebitda/1e6:.2f} Juta" if ebitda > 0 else "N/A"
                st.metric("EBITDA", ebitda_text)
        
        # ========== CHART CANDLESTICK ==========
        st.markdown("### 📈 Candlestick Chart (90 hari terakhir)")
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index[-90:],
            open=df['Open'][-90:],
            high=df['High'][-90:],
            low=df['Low'][-90:],
            close=df['Close'][-90:],
            name=symbol,
            increasing_line_color='#00ffcc',
            decreasing_line_color='#ff3366'
        ))
        
        # Moving Averages
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        fig.add_trace(go.Scatter(x=df.index[-90:], y=df['MA20'][-90:], name='MA20', line=dict(color='#ffaa00', width=1.5)))
        fig.add_trace(go.Scatter(x=df.index[-90:], y=df['MA50'][-90:], name='MA50', line=dict(color='#00ccff', width=1.5)))
        
        fig.update_layout(
            title=f"{symbol} - Candlestick Chart",
            height=450,
            template="plotly_dark",
            paper_bgcolor="#0a0a0a",
            plot_bgcolor="#1a1a2e",
            xaxis=dict(rangeslider=dict(visible=False)),
            yaxis_title="Harga",
            xaxis_title="Tanggal"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ========== SUPPORT & RESISTANCE ==========
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("🛡️ Support (20 hari)", format_price(signal['support'], symbol))
        with col_s2:
            st.metric("🚀 Resistance (20 hari)", format_price(signal['resistance'], symbol))
        
        # ========== DIVIDEN HISTORY ==========
        try:
            ticker_obj = yf.Ticker(symbol)
            dividends = ticker_obj.dividends
            if not dividends.empty:
                with st.expander("📅 Riwayat Dividen (5 tahun terakhir)"):
                    div_df = pd.DataFrame(dividends.tail(5))
                    div_df.columns = ['Dividen']
                    div_df['Tanggal'] = div_df.index.strftime('%Y-%m-%d')
                    div_df['Dividen'] = div_df['Dividen'].apply(lambda x: format_price(x, symbol))
                    st.dataframe(div_df[['Tanggal', 'Dividen']], use_container_width=True, hide_index=True)
            else:
                with st.expander("📅 Riwayat Dividen"):
                    st.info("Belum ada riwayat dividen untuk saham ini")
        except:
            pass
        
        # ========== ALASAN SINYAL ==========
        with st.expander("📝 Detail Alasan Sinyal Entry"):
            if signal.get('reasons'):
                for reason in signal['reasons'][:5]:
                    st.write(f"✅ {reason}")
            else:
                st.write("Tidak ada alasan spesifik")
        
        # ========== TOMBOL RESET SEARCH ==========
        st.markdown("---")
        if st.button("🔄 Cari Saham Lain", use_container_width=True):
            st.session_state.search_triggered = False
            st.session_state.search_symbol = ""
            st.rerun()

def render_tab5():
    """Tab Info Saham"""
    st.subheader("📰 Info Saham")
    symbol = st.text_input("Kode Saham", placeholder="BBCA.JK").upper().strip()
    if symbol:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📊 Info Perusahaan")
                st.write(f"**Nama:** {info.get('longName', 'N/A')}")
                st.write(f"**Sektor:** {info.get('sector', 'N/A')}")
                st.write(f"**Industri:** {info.get('industry', 'N/A')}")
            with col2:
                st.markdown("### 💰 Keuangan")
                market_cap = info.get('marketCap', 0)
                market_cap_str = f"{market_cap/1e12:.2f}T" if market_cap >= 1e12 else f"{market_cap/1e9:.2f}B"
                st.write(f"**Market Cap:** {market_cap_str}")
                st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                div_yield = info.get('dividendYield', 0) * 100
                st.write(f"**Dividen Yield:** {div_yield:.2f}%")
            dividends = ticker.dividends
            if not dividends.empty:
                st.markdown("### 💸 Riwayat Dividen")
                st.dataframe(dividends.tail(5), use_container_width=True)
        except Exception as e:
            st.error(f"Gagal mengambil info: {e}")


def render_tab6():
    """Tab Scalping Emas"""
    st.subheader("⚡ Scalping Signal - Emas")
    timeframe = st.selectbox("Timeframe", ["1 Jam", "4 Jam", "Daily"], index=0)
    tf_map = {"1 Jam": "1h", "4 Jam": "4h", "Daily": "1d"}
    with st.spinner(f"Mengambil data {timeframe}..."):
        df = get_gold_data(timeframe=tf_map[timeframe])
        if df.empty:
            st.error("Data tidak tersedia")
            return
        signal = generate_scalping_signal(df)
        if signal is None:
            st.warning("Data tidak cukup untuk scalping")
            return
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Harga", f"${signal['price']:.2f}")
        col2.metric("Score", f"{signal['score']:.1f}")
        col3.metric("ATR", f"${signal['atr']:.2f}")
        divider()
        if signal['action'] == "BUY":
            st.success(f"🔥 {signal['recommendation']} 🔥")
        elif signal['action'] == "SELL":
            st.error(f"⚠️ {signal['recommendation']} ⚠️")
        else:
            st.warning(f"⚪ {signal['recommendation']} ⚪")
        col_sl, col_tp = st.columns(2)
        col_sl.metric("Stop Loss", f"${signal['stop_loss']:.2f}")
        col_tp.metric("Take Profit", f"${signal['take_profit']:.2f}")
        with st.expander("📝 Alasan Signal"):
            for reason in signal['reasons']:
                st.write(f"✅ {reason}")

def render_tab7():
    """Tab khusus liat bandar - Pilih kode broker, lihat saham mana yang mereka akumulasi/distribusi"""
    from app.utils.config import ALL_STOCKS
    
    st.subheader("🦈 TRACKING BANDAR - CARI SAHAM YANG DIKONTROL BROKER")
    st.caption("""
    Pilih kode broker, sistem akan menampilkan saham-saham yang sedang diakumulasi (net buy) atau didistribusi (net sell) oleh broker tersebut.
    
    **Kode Broker:**  
    AK (UBS), BK (JP Morgan), LG (Trimegah), HP (Henan Putihrai), NI (BNI Sekuritas), RF (Buana Capital),  
    CC (Mandiri Sekuritas), OD (BRI Danareksa), IF (Samuel), YP (Mirae Asset), ZP (Maybank), AI (UOB), DR (RHB)
    """)
    
    # Daftar broker yang tersedia
    from app.utils.broker_codes import BROKER_CODES
    
    broker_options = []
    for code, info in BROKER_CODES.items():
        broker_options.append({
            'code': code,
            'name': info['name'],
            'type': info['type'],
            'display': f"{code} - {info['name']} ({'ASING' if info['type'] == 'FOREIGN' else 'LOKAL'})"
        })
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_broker = st.selectbox(
            "Pilih Kode Broker",
            options=broker_options,
            format_func=lambda x: x['display'],
            key="bandar_broker_select"
        )
    
    with col2:
        filter_type = st.selectbox(
            "Filter Transaksi",
            options=["SEMUA", "AKUMULASI (Net Buy)", "DISTRIBUSI (Net Sell)"],
            index=0,
            key="bandar_filter_type"
        )
    
    if not selected_broker:
        st.info("Silakan pilih kode broker terlebih dahulu")
        return
    
    broker_code = selected_broker['code']
    broker_name = selected_broker['name']
    
    st.markdown(f"### 🔍 Tracking: **{broker_code} - {broker_name}**")
    
    with st.spinner(f"Mencari saham yang diakumulasi/distribusi oleh {broker_code}..."):
        from app.core.analysis import get_realtime_broker_summary, get_stock_data
        from app.utils.config import STOCKS
        
        # Ambil sample saham (batasi 50 dulu biar cepet)
        sample_stocks = STOCKS[:50]
        
        stock_activity = []
        progress_bar = st.progress(0)
        
        for idx, sym in enumerate(sample_stocks):
            progress_bar.progress((idx + 1) / len(sample_stocks))
            
            broker_df = get_realtime_broker_summary(sym)
            if broker_df is not None and not broker_df.empty:
                # Cari data untuk broker yang dipilih
                broker_row = broker_df[broker_df['BrokerCode'] == broker_code]
                if not broker_row.empty:
                    row = broker_row.iloc[0]
                    buy = row['BuyVolume']
                    sell = row['SellVolume']
                    net = buy - sell
                    
                    if net != 0:
                        # Ambil harga saham untuk konteks
                        df_price = get_stock_data(sym, period="1mo")
                        current_price = df_price['Close'].iloc[-1] if df_price is not None and not df_price.empty else 0
                        currency, _ = get_currency(sym)
                        price_label = "Rp" if currency == "IDR" else "$"
                        
                        net_lot = net // 100
                        buy_lot = buy // 100
                        sell_lot = sell // 100
                        
                        if net > 0:
                            aksi = "AKUMULASI"
                            aksi_icon = "🔥"
                        else:
                            aksi = "DISTRIBUSI"
                            aksi_icon = "⚠️"
                        
                        stock_activity.append({
                            'Kode Saham': sym,
                            'Harga': f"{price_label}{current_price:,.0f}".replace(',', '.'),
                            'Beli (Lot)': f"{buy_lot:,.0f}",
                            'Jual (Lot)': f"{sell_lot:,.0f}",
                            'Net (Lot)': f"{'+' if net_lot > 0 else ''}{net_lot:,.0f}",
                            'Aksi': f"{aksi_icon} {aksi}",
                            'Net Volume': net_lot
                        })
        
        progress_bar.empty()
        
        if not stock_activity:
            st.warning(f"Tidak ditemukan saham yang diakumulasi/distribusi oleh {broker_code} dalam 50 saham teratas")
            return
        
        # Filter berdasarkan aksi
        if filter_type == "AKUMULASI (Net Buy)":
            stock_activity = [s for s in stock_activity if 'AKUMULASI' in s['Aksi']]
        elif filter_type == "DISTRIBUSI (Net Sell)":
            stock_activity = [s for s in stock_activity if 'DISTRIBUSI' in s['Aksi']]
        
        # Urutkan berdasarkan volume net terbesar
        stock_activity.sort(key=lambda x: abs(x['Net Volume']), reverse=True)
        
        # Statistik
        total_accum = sum([s['Net Volume'] for s in stock_activity if s['Net Volume'] > 0])
        total_dist = sum([abs(s['Net Volume']) for s in stock_activity if s['Net Volume'] < 0])
        
        st.markdown("### 📊 Ringkasan Aktivitas")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Total Saham", len(stock_activity))
        with col_s2:
            st.metric("🔥 Total Akumulasi", f"{total_accum:+,} lot")
        with col_s3:
            st.metric("⚠️ Total Distribusi", f"{total_dist:+,} lot")
        
        if total_accum > total_dist:
            st.success(f"📈 **{broker_code} sedang NET AKUMULASI** sebesar {total_accum - total_dist:+,} lot - Bullish signal!")
        elif total_dist > total_accum:
            st.error(f"📉 **{broker_code} sedang NET DISTRIBUSI** sebesar {total_dist - total_accum:+,} lot - Bearish signal!")
        else:
            st.info(f"➡️ **{broker_code} netral** - Tidak ada akumulasi/distribusi signifikan")
        
        st.divider()
        st.markdown(f"### 📋 Daftar Saham yang Diakumulasi/Distribusi oleh **{broker_code}**")
        
        # Tampilkan tabel
        df_display = pd.DataFrame(stock_activity)
        df_display = df_display.drop(columns=['Net Volume'])
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Kode Saham': st.column_config.TextColumn('Kode Saham', width='small'),
                'Harga': st.column_config.TextColumn('Harga', width='small'),
                'Beli (Lot)': st.column_config.TextColumn('Beli (Lot)', width='small'),
                'Jual (Lot)': st.column_config.TextColumn('Jual (Lot)', width='small'),
                'Net (Lot)': st.column_config.TextColumn('Net (Lot)', width='small'),
                'Aksi': st.column_config.TextColumn('Sinyal', width='small'),
            }
        )
        
        # Highlight saham dengan net volume terbesar
        st.divider()
        st.markdown("### 🎯 Top 5 Saham dengan Volume Terbesar")
        
        top_5 = stock_activity[:5]
        for s in top_5:
            if 'AKUMULASI' in s['Aksi']:
                st.success(f"**{s['Kode Saham']}** - {s['Aksi']} - Net {s['Net (Lot)']} lot @ {s['Harga']}")
            else:
                st.error(f"**{s['Kode Saham']}** - {s['Aksi']} - Net {s['Net (Lot)']} lot @ {s['Harga']}")
        
        st.caption("⚠️ **Catatan:** Data ini simulasi berdasarkan 50 saham teratas. Untuk data real-time akurat, perlu integrasi API RTI Business. Harga saham adalah harga terkini dari Yahoo Finance.")
