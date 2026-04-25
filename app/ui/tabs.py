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
    """Tab Prediksi - Dengan semua saham + Analisis Bandar (AK, BK, LG, HP, NI, RF)"""
    from app.utils.config import ALL_STOCKS, FORECAST_STOCKS, ALL_KONGLOMERAT_GROUPS
    
    st.subheader("🔮 Prediksi Harga 30 Hari + Analisis Bandar (Kode Broker)")
    
    # Build dropdown options
    dropdown_options = []
    
    # Emas
    dropdown_options.append(("🥇 GOLD", "GOLD"))
    
    # Kategori konglomerat
    if ALL_KONGLOMERAT_GROUPS:
        dropdown_options.append(("━━━ KONGLOMERAT ━━━", "SEPARATOR"))
        for group in ALL_KONGLOMERAT_GROUPS:
            dropdown_options.append((f"🏢 {group['name']}", f"GROUP_{group['name']}"))
    
    dropdown_options.append(("━━━ SAHAM INDIVIDUAL ━━━", "SEPARATOR"))
    # Filter saham yang valid (yang ada titik JK)
    valid_stocks = [s for s in ALL_STOCKS if '.JK' in s]
    for sym in valid_stocks[:100]:  # Tampilkan 100 saham pertama
        dropdown_options.append((f"📊 {sym}", sym))
    
    selected_label, selected_value = st.selectbox(
        "Pilih Aset / Grup Konglomerat",
        options=dropdown_options,
        format_func=lambda x: x[0]
    )
    
    # Proses berdasarkan pilihan
    if selected_value == "SEPARATOR":
        st.info("Pilih aset dari menu di atas")
        return
    
    # Tentukan list saham yang akan diproses
    stock_list = []
    if selected_value == "GOLD":
        stock_list = ["GOLD"]
        display_name = "Emas (XAU/USD)"
    elif selected_value.startswith("GROUP_"):
        group_name = selected_value.replace("GROUP_", "")
        for group in ALL_KONGLOMERAT_GROUPS:
            if group['name'] == group_name:
                stock_list = group['stocks']
                display_name = f"{group['name']} ({len(stock_list)} saham)"
                break
    else:
        stock_list = [selected_value]
        display_name = selected_value
    
    st.info(f"📊 Menampilkan: **{display_name}** - {len(stock_list)} aset")
    
    # ========== UNTUK SAHAM TUNGGAL (BUKAN GOLD) ==========
    if len(stock_list) == 1 and stock_list[0] != "GOLD":
        symbol = stock_list[0]
        
        with st.spinner(f"Mengambil data {symbol} dan analisis bandar..."):
            df_hist = get_stock_data(symbol, period="3mo")
            currency, _ = get_currency(symbol)
            price_label = "Rp" if currency == "IDR" else "$"
            
            if df_hist is None or df_hist.empty:
                st.error("Gagal mengambil data")
                return
            
            # Ambil data institusi/bandar
            inst_data = get_institutional_holders(symbol)
            foreign_data = get_foreign_flow_summary(symbol)
            broker_df = get_realtime_broker_summary(symbol)
            
            hist_price = df_hist['Close']
            pred_values = exponential_smoothing(hist_price, forecast_days=30)
            
            current_price = hist_price.iloc[-1]
            last_pred = pred_values[-1]
            pct_change = ((last_pred - current_price) / current_price) * 100
            
            col1, col2 = st.columns(2)
            col1.metric("Harga Saat Ini", f"{price_label}{current_price:.2f}")
            col2.metric("Prediksi 30 Hari", f"{price_label}{last_pred:.2f}", delta=f"{pct_change:+.1f}%")
            
            future_dates = [datetime.now() + timedelta(days=i+1) for i in range(30)]
            
            # Chart Candlestick
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
            fig.update_layout(title=f"{symbol} - 30 Day Forecast", height=450, template="plotly_dark", paper_bgcolor="#0a0a0a", plot_bgcolor="#1a1a2e")
            st.plotly_chart(fig, use_container_width=True)
            
            # ========== BAGIAN BANDAR ==========
            st.divider()
            st.subheader("🏦 Analisis Bandar (Institusi Asing vs Domestik)")
            
            if foreign_data:
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    st.metric("Estimasi Kepemilikan Asing", f"{foreign_data['estimated_foreign_percent']:.1f}%")
                with col_f2:
                    st.metric("Estimasi Kepemilikan Domestik", f"{foreign_data['estimated_domestic_percent']:.1f}%")
                with col_f3:
                    st.metric("Insider Ownership", f"{foreign_data['insider_percent']:.1f}%")
                
                st.markdown(f"""
                <div style="background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #00ffcc;">
                    <strong>📊 Sinyal Aliran Dana:</strong><br>
                    {foreign_data['flow_signal']}
                </div>
                """, unsafe_allow_html=True)
            
            # ========== KODE BROKER ==========
            st.divider()
            st.subheader("🦈 Analisis Bandar Berdasarkan Kode Broker")
            st.caption("Kode broker: AK (UBS), BK (JP Morgan), LG (Trimegah), HP (Henan), NI (BNI), RF (Buana), CC (Mandiri), OD (BRI), IF (Samuel)")
            
            if broker_df is not None and not broker_df.empty:
                broker_activity = []
                for _, row in broker_df.iterrows():
                    code = row['BrokerCode']
                    buy = row['BuyVolume']
                    sell = row['SellVolume']
                    net = buy - sell
                    
                    broker_info = get_broker_info(code)
                    
                    broker_activity.append({
                        'Kode': code,
                        'Nama Broker': broker_info['name'],
                        'Tipe': '🌍 ASING' if broker_info['type'] == 'FOREIGN' else '🇮🇩 LOKAL',
                        'Kategori': broker_info['category'],
                        'Beli (Lot)': f"{buy//100:,.0f}",
                        'Jual (Lot)': f"{sell//100:,.0f}",
                        'Net (Lot)': f"{net//100:+,.0f}",
                        'Aksi': '🔥 AKUMULASI' if net > 0 else ('⚠️ DISTRIBUSI' if net < 0 else '➡️ NETRAL')
                    })
                
                if broker_activity:
                    broker_activity.sort(key=lambda x: int(x['Net (Lot)'].replace('+', '').replace(',', '')), reverse=True)
                    
                    st.markdown("### Top 10 Broker Paling Aktif")
                    st.dataframe(pd.DataFrame(broker_activity[:10]), use_container_width=True, hide_index=True)
                    
                    total_accum = 0
                    total_dist = 0
                    for a in broker_activity:
                        net_str = a['Net (Lot)'].replace(',', '').strip()
                        if '+' in net_str:
                            try:
                                total_accum += int(net_str.replace('+', ''))
                            except:
                                pass
                        elif '-' in net_str:
                            try:
                                total_dist += int(net_str.replace('-', ''))
                            except:
                                pass
                    
                    net_flow = total_accum - total_dist
                    if net_flow > 0:
                        st.success(f"📈 Net Flow: +{net_flow:,} lot (Bandar akumulasi)")
                    elif net_flow < 0:
                        st.error(f"📉 Net Flow: {net_flow:,} lot (Bandar distribusi)")
                    else:
                        st.info(f"➡️ Net Flow: {net_flow:,} lot (Netral)")
                    
                    st.markdown("#### 🎯 Fokus Broker Besar:")
                    important_brokers = ['AK', 'BK', 'LG', 'HP', 'NI', 'RF', 'CC', 'OD', 'IF']
                    for broker in broker_activity:
                        if broker['Kode'] in important_brokers:
                            if 'AKUMULASI' in broker['Aksi']:
                                st.success(f"**{broker['Kode']} ({broker['Nama Broker']})**: {broker['Aksi']} - Net {broker['Net (Lot)']}")
                            elif 'DISTRIBUSI' in broker['Aksi']:
                                st.error(f"**{broker['Kode']} ({broker['Nama Broker']})**: {broker['Aksi']} - Net {broker['Net (Lot)']}")
                            else:
                                st.info(f"**{broker['Kode']} ({broker['Nama Broker']})**: {broker['Aksi']}")
                else:
                    st.info("Tidak ada data aktivitas broker")
            else:
                st.warning("Data broker tidak tersedia")
            
            with st.expander("📊 Detail Prediksi 30 Hari"):
                pred_df = pd.DataFrame({
                    'Hari ke-': list(range(1, 31)),
                    'Tanggal': [(datetime.now() + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(1, 31)],
                    'Prediksi': [f"{price_label}{p:.2f}" for p in pred_values],
                    'Perubahan': [f"{((p - current_price)/current_price*100):+.2f}%" for p in pred_values]
                })
                st.dataframe(pred_df, use_container_width=True, hide_index=True)
    
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
                fig.add_trace(go.Scatter(x=future_dates, y=pred_values, name='Prediksi', line=dict(color='red', dash='dot')))
                fig.update_layout(title="Gold - 30 Day Forecast", height=450, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                st.info("🥇 Untuk emas, analisis bandar (kode broker) tidak tersedia karena hanya untuk saham.")
    
    else:
        # Multiple stocks (konglomerat)
        st.subheader(f"📊 {display_name}")
        
        forecast_data = []
        for sym in stock_list:
            df_hist = get_stock_data(sym, period="3mo")
            if df_hist is not None and not df_hist.empty:
                hist_price = df_hist['Close']
                pred_values = exponential_smoothing(hist_price, forecast_days=30)
                current_price = hist_price.iloc[-1]
                last_pred = pred_values[-1]
                pct_change = ((last_pred - current_price) / current_price) * 100
                forecast_data.append({
                    'Kode': sym,
                    'Harga': format_price(current_price, sym),
                    'Prediksi 30H': format_price(last_pred, sym),
                    'Perubahan': f"{pct_change:+.1f}%",
                    'Trend': '📈' if pct_change > 2 else ('📉' if pct_change < -2 else '➡️')
                })
        
        if forecast_data:
            df_ringkasan = pd.DataFrame(forecast_data)
            st.dataframe(df_ringkasan, use_container_width=True, hide_index=True)
            
            st.divider()
            st.subheader("🔍 Cari Manual - Detail + Analisis Bandar")
            st.caption("Pilih saham dari daftar di atas untuk melihat detail prediksi dan analisis bandar")
            
            stock_codes = [d['Kode'] for d in forecast_data]
            selected_symbol = st.selectbox("Pilih Kode Saham untuk Detail", options=stock_codes, key="manual_search_konglo")
            
            if selected_symbol:
                with st.spinner(f"Mengambil detail {selected_symbol}..."):
                    df_hist_detail = get_stock_data(selected_symbol, period="3mo")
                    currency, _ = get_currency(selected_symbol)
                    price_label = "Rp" if currency == "IDR" else "$"
                    
                    if df_hist_detail is not None and not df_hist_detail.empty:
                        inst_data = get_institutional_holders(selected_symbol)
                        foreign_data = get_foreign_flow_summary(selected_symbol)
                        broker_df = get_realtime_broker_summary(selected_symbol)
                        
                        hist_price = df_hist_detail['Close']
                        pred_values = exponential_smoothing(hist_price, forecast_days=30)
                        current_price = hist_price.iloc[-1]
                        last_pred = pred_values[-1]
                        pct_change = ((last_pred - current_price) / current_price) * 100
                        
                        col1, col2 = st.columns(2)
                        col1.metric("Harga Saat Ini", f"{price_label}{current_price:.2f}")
                        col2.metric("Prediksi 30 Hari", f"{price_label}{last_pred:.2f}", delta=f"{pct_change:+.1f}%")
                        
                        future_dates = [datetime.now() + timedelta(days=i+1) for i in range(30)]
                        
                        fig = go.Figure()
                        fig.add_trace(go.Candlestick(
                            x=df_hist_detail.index[-60:],
                            open=df_hist_detail['Open'][-60:],
                            high=df_hist_detail['High'][-60:],
                            low=df_hist_detail['Low'][-60:],
                            close=df_hist_detail['Close'][-60:],
                            name=selected_symbol,
                            increasing_line_color='#00ffcc',
                            decreasing_line_color='#ff3366'
                        ))
                        fig.add_trace(go.Scatter(x=future_dates, y=pred_values, name='Prediksi', line=dict(color='#ffaa00', width=2, dash='dot')))
                        fig.update_layout(title=f"{selected_symbol} - 30 Day Forecast", height=450, template="plotly_dark")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.divider()
                        st.subheader(f"🏦 Analisis Bandar - {selected_symbol}")
                        
                        if foreign_data:
                            col_f1, col_f2, col_f3 = st.columns(3)
                            with col_f1:
                                st.metric("Estimasi Kepemilikan Asing", f"{foreign_data['estimated_foreign_percent']:.1f}%")
                            with col_f2:
                                st.metric("Estimasi Kepemilikan Domestik", f"{foreign_data['estimated_domestic_percent']:.1f}%")
                            with col_f3:
                                st.metric("Insider Ownership", f"{foreign_data['insider_percent']:.1f}%")
                        
                        st.subheader("🦈 Aktivitas Broker")
                        if broker_df is not None and not broker_df.empty:
                            broker_activity = []
                            for _, row in broker_df.iterrows():
                                code = row['BrokerCode']
                                buy = row['BuyVolume']
                                sell = row['SellVolume']
                                net = buy - sell
                                broker_info = get_broker_info(code)
                                broker_activity.append({
                                    'Kode': code,
                                    'Nama Broker': broker_info['name'],
                                    'Beli (Lot)': f"{buy//100:,.0f}",
                                    'Jual (Lot)': f"{sell//100:,.0f}",
                                    'Net (Lot)': f"{net//100:+,.0f}",
                                    'Aksi': '🔥 AKUMULASI' if net > 0 else ('⚠️ DISTRIBUSI' if net < 0 else '➡️ NETRAL')
                                })
                            
                            if broker_activity:
                                broker_activity.sort(key=lambda x: int(x['Net (Lot)'].replace('+', '').replace(',', '')), reverse=True)
                                st.dataframe(pd.DataFrame(broker_activity[:10]), use_container_width=True, hide_index=True)


def render_tab4():
    """Tab Search Saham + Profil Perusahaan + Pemegang Saham (FULL API)"""
    from app.utils.config import ALL_STOCKS, ALL_KONGLOMERAT_GROUPS
    from app.core.analysis import get_stock_info, get_stock_data, load_data
    from app.core.entry_signal import generate_entry_signal
    from app.ui.components import signal_card, divider
    from app.utils.currency import format_price
    import plotly.graph_objects as go
    import yfinance as yf
    import pandas as pd
    import streamlit as st
    import requests
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    STOCKTV_API_KEY = os.getenv("STOCKTV_API_KEY", "")
    
    st.subheader("🔍 Cari Saham & Lihat Profil Perusahaan")
    st.caption("Cari kode saham (contoh: BBCA.JK, ADRO.JK, ANTM.JK)")
    
    # ========== SEARCH MANUAL ==========
    if 'search_symbol' not in st.session_state:
        st.session_state.search_symbol = ""
    if 'search_triggered' not in st.session_state:
        st.session_state.search_triggered = False
    
    col_search1, col_search2 = st.columns([4, 1])
    with col_search1:
        manual_search = st.text_input(
            "Ketik kode saham:", 
            placeholder="BBCA.JK, ADRO.JK, TLKM.JK",
            key="manual_search_input"
        ).upper().strip()
    
    with col_search2:
        search_clicked = st.button("🔍 CARI", type="primary", use_container_width=True)
    
    symbol = None
    
    if search_clicked and manual_search:
        if manual_search in ALL_STOCKS or manual_search.endswith('.JK'):
            symbol = manual_search
            st.session_state.search_symbol = symbol
            st.session_state.search_triggered = True
        else:
            st.error(f"❌ Kode saham '{manual_search}' tidak ditemukan.")
    
    if st.session_state.search_triggered and st.session_state.search_symbol:
        symbol = st.session_state.search_symbol
    
    if not symbol:
        if not manual_search:
            st.info("💡 Masukkan kode saham (contoh: BBCA.JK)")
        return
    
    if not STOCKTV_API_KEY:
        st.error("❌ STOCKTV_API_KEY tidak ditemukan di .env file")
        st.stop()
    
    # ========== FUNGSI API STOCKTV ==========
    def call_stocktv_api(endpoint, symbol):
        """Panggil StockTV API dengan endpoint tertentu"""
        clean_sym = symbol.replace('.JK', '')
        url = f"https://api.stocktv.top/stock/{endpoint}"
        params = {
            "countryId": 48,
            "symbol": clean_sym,
            "key": STOCKTV_API_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    return data.get('data', {})
            return None
        except Exception as e:
            print(f"API Error {endpoint}: {e}")
            return None
    
    # ========== TAMPILKAN DATA ==========
    with st.spinner(f"📊 Mengambil data {symbol} dari API..."):
        
        # Ambil semua data dari API dalam satu go
        company_data = call_stocktv_api("company", symbol)
        quote_data = call_stocktv_api("quote", symbol)
        shareholders_data = call_stocktv_api("shareholders", symbol)
        fundamental_data = call_stocktv_api("fundamental", symbol)
        
        # Cek apakah API berhasil
        if not company_data and not quote_data:
            st.error(f"❌ Gagal mengambil data {symbol} dari StockTV API. Cek API key atau kode saham.")
            st.session_state.search_triggered = False
            return
        
        # ========== HEADER ==========
        company_name = company_data.get('name', 'N/A') if company_data else 'N/A'
        sector = company_data.get('sector', 'N/A') if company_data else 'N/A'
        industry = company_data.get('industry', 'N/A') if company_data else 'N/A'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 16px; margin-bottom: 20px; border-left: 4px solid #00ffcc;">
            <h1 style="color: #00ffcc; margin: 0;">{symbol}</h1>
            <h3 style="color: #ffffff; margin-top: 8px;">{company_name}</h3>
            <p style="color: #aaaaaa; margin-top: 8px;">
                📍 {sector} | 🏭 {industry}
            </p>
            <p style="color: #888888; font-size: 12px;">
                🌐 <a href="{company_data.get('website', '#')}" style="color: #00ffcc;" target="_blank">{company_data.get('website', 'N/A')}</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== METRIK DARI QUOTE ==========
        current_price = quote_data.get('price', quote_data.get('last', 0)) if quote_data else 0
        price_change = quote_data.get('change', quote_data.get('changePercent', 0)) if quote_data else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Harga", format_price(current_price, symbol), delta=f"{price_change:+.2f}%")
        with col2:
            pe = fundamental_data.get('pe', fundamental_data.get('peRatio', 0)) if fundamental_data else 0
            st.metric("📊 P/E Ratio", f"{pe:.2f}" if pe > 0 else "N/A")
        with col3:
            pb = fundamental_data.get('pb', fundamental_data.get('priceToBook', 0)) if fundamental_data else 0
            st.metric("📈 P/B Ratio", f"{pb:.2f}" if pb > 0 else "N/A")
        with col4:
            roe = fundamental_data.get('roe', fundamental_data.get('returnOnEquity', 0)) if fundamental_data else 0
            st.metric("⭐ ROE", f"{roe:.2f}%" if roe else "N/A")
        
        # ========== PROFIL PERUSAHAAN ==========
        st.markdown("### 🏢 Profil Perusahaan")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("**📋 Informasi Dasar**")
            st.write(f"• **Nama**: {company_name}")
            st.write(f"• **Sektor**: {sector}")
            st.write(f"• **Industri**: {industry}")
            st.write(f"• **Kode**: {symbol}")
        
        with col_p2:
            st.markdown("**📊 Info Tambahan**")
            market_cap = fundamental_data.get('marketCap', 0) if fundamental_data else 0
            if market_cap >= 1e12:
                cap_text = f"{market_cap/1e12:.2f} T"
            elif market_cap >= 1e9:
                cap_text = f"{market_cap/1e9:.2f} M"
            else:
                cap_text = "N/A"
            st.write(f"• **Market Cap**: {cap_text}")
            
            div_yield = fundamental_data.get('dividendYield', 0) if fundamental_data else 0
            st.write(f"• **Dividen Yield**: {div_yield:.2f}%" if div_yield else "• **Dividen Yield**: N/A")
        
        # ========== DESKRIPSI BISNIS ==========
        st.markdown("### 📝 Deskripsi Bisnis")
        description = company_data.get('description', '') if company_data else ''
        if description:
            st.write(description)
        else:
            st.info("Deskripsi tidak tersedia dari API")
        
        # ========== PEMEGANG SAHAM (WAJIB DARI API) ==========
        st.markdown("### 👥 Pemegang Saham (>1% - Data Resmi BEI/KSEI)")
        st.caption("Sumber: StockTV API - Data real-time dari Bursa Efek Indonesia")
        
        if shareholders_data and shareholders_data.get('shareholders'):
            sh_list = shareholders_data.get('shareholders', [])
            if sh_list:
                df_sh = pd.DataFrame(sh_list)
                st.dataframe(df_sh, use_container_width=True, hide_index=True)
                st.success(f"✅ Data pemegang saham berhasil diambil dari API")
            else:
                st.warning("Data pemegang saham kosong dari API")
        else:
            st.error("❌ Gagal mengambil data pemegang saham dari StockTV API")
            st.info("Pastikan API key valid dan saham ini memiliki data kepemilikan publik")
        
        # ========== KEPEMILIKAN INSTITUSI ==========
        st.markdown("### 🏦 Kepemilikan Institusi")
        
        if fundamental_data and fundamental_data.get('institutionalHolders'):
            inst_data = fundamental_data.get('institutionalHolders', [])
            if inst_data:
                df_inst = pd.DataFrame(inst_data)
                st.dataframe(df_inst, use_container_width=True, hide_index=True)
            else:
                st.info("Data kepemilikan institusi tidak tersedia")
        else:
            st.info("Data kepemilikan institusi tidak tersedia dari API")
        
        # ========== CHART CANDLESTICK ==========
        st.markdown("### 📈 Candlestick Chart (90 hari terakhir)")
        
        # Ambil data historis untuk chart
        df = get_stock_data(symbol, period="6mo")
        
        if df is not None and not df.empty:
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
            
            df['MA20'] = df['Close'].rolling(20).mean()
            fig.add_trace(go.Scatter(
                x=df.index[-90:], 
                y=df['MA20'][-90:], 
                name='MA20', 
                line=dict(color='#ffaa00', width=1.5)
            ))
            
            fig.update_layout(
                title=f"{symbol} - Candlestick Chart",
                height=450,
                template="plotly_dark",
                paper_bgcolor="#0a0a0a",
                plot_bgcolor="#1a1a2e",
                xaxis=dict(rangeslider=dict(visible=False))
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Data historis tidak tersedia untuk chart")
        
        # ========== SUPPORT & RESISTANCE (SIMULASI DARI QUOTE) ==========
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            support = current_price * 0.95 if current_price > 0 else 0
            st.metric("🛡️ Support (Estimasi)", format_price(support, symbol))
        with col_s2:
            resistance = current_price * 1.05 if current_price > 0 else 0
            st.metric("🚀 Resistance (Estimasi)", format_price(resistance, symbol))
        
        # ========== TOMBOL RESET ==========
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
