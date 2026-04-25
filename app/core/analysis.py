# app/core/analysis.py
import pandas as pd
import numpy as np
import sqlite3
import ta
import yfinance as yf
import requests
import os
import random
from datetime import datetime, timedelta
from app.utils.config import DB_PATH
from app.utils.currency import format_price, get_currency

# ========== KONFIGURASI API ==========
ITICK_API_KEY = os.getenv("ITICK_API_KEY", "")
ITICK_BASE_URL = "https://api.itick.org/v1"


# ========== FUNGSI DASAR ==========

def load_data(table):
    """Load data dari SQLite"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def save_data(df, table, if_exists='replace'):
    """Save data ke SQLite"""
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table, conn, if_exists=if_exists, index=False)
    conn.close()


def compute_fundamental_score(df):
    """Skor fundamental dengan bobot dividen lebih tinggi"""
    df = df.copy()
    df = df.fillna(0)
    
    df['roe_score'] = np.clip(df['return_on_equity'] / 15, 0, 1) * 20
    df['pe_score'] = np.where(df['pe_ratio'] > 0, np.clip(1 - (df['pe_ratio'] - 8) / 30, 0, 1), 0.5) * 15
    df['div_score'] = np.clip(df['dividend_yield'] / 5, 0, 1) * 35
    df['debt_score'] = np.where(df['debt_to_equity'] > 0, np.clip(1 - df['debt_to_equity'] / 200, 0, 1), 0.8) * 10
    
    rec_map = {'strong_buy': 1.0, 'buy': 0.8, 'hold': 0.5, 'sell': 0.2, 'strong_sell': 0.0}
    df['rec_score'] = df['recommendation'].map(rec_map).fillna(0.4) * 20
    
    df['total_score'] = df['roe_score'] + df['pe_score'] + df['div_score'] + df['debt_score'] + df['rec_score']
    return df


def get_stock_data(symbol, period="6mo"):
    """Ambil data harga historis saham dari Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"Error get_stock_data {symbol}: {e}")
        return None


def get_stock_info(symbol):
    """Ambil info fundamental saham dari Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'country': info.get('country', 'Indonesia'),
            'website': info.get('website', ''),
            'marketCap': info.get('marketCap', 0),
            'trailingPE': info.get('trailingPE', 0),
            'priceToBook': info.get('priceToBook', 0),
            'priceToSalesTrailing12Months': info.get('priceToSalesTrailing12Months', 0),
            'returnOnEquity': info.get('returnOnEquity', 0),
            'debtToEquity': info.get('debtToEquity', 0),
            'dividendYield': info.get('dividendYield', 0),
            'beta': info.get('beta', 0),
            'fullTimeEmployees': info.get('fullTimeEmployees', 0),
            'longBusinessSummary': info.get('longBusinessSummary', 'Deskripsi tidak tersedia'),
            'companyOfficers': info.get('companyOfficers', []),
            'totalRevenue': info.get('totalRevenue', 0),
            'netIncomeToCommon': info.get('netIncomeToCommon', 0),
            'ebitda': info.get('ebitda', 0),
            'currentPrice': info.get('regularMarketPrice', info.get('currentPrice', 0)),
            'recommendationKey': info.get('recommendationKey', 'N/A')
        }
    except Exception as e:
        print(f"Error get_stock_info {symbol}: {e}")
        return {
            'name': symbol, 'sector': 'N/A', 'industry': 'N/A', 'country': 'Indonesia',
            'website': '', 'marketCap': 0, 'trailingPE': 0, 'priceToBook': 0,
            'priceToSalesTrailing12Months': 0, 'returnOnEquity': 0, 'debtToEquity': 0,
            'dividendYield': 0, 'beta': 0, 'fullTimeEmployees': 0,
            'longBusinessSummary': 'Deskripsi tidak tersedia', 'companyOfficers': [],
            'totalRevenue': 0, 'netIncomeToCommon': 0, 'ebitda': 0, 'currentPrice': 0,
            'recommendationKey': 'N/A'
        }


def analyze_gold():
    """Analisis teknikal emas"""
    try:
        gold = yf.Ticker("GC=F")
        df = gold.history(period="6mo")
        
        if df.empty:
            return None
        
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], 14).rsi()
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        
        last = df.iloc[-1]
        signals = []
        score = 0
        
        if last['RSI'] < 30:
            signals.append("🔵 RSI oversold, potensi naik")
            score += 2
        elif last['RSI'] > 70:
            signals.append("🔴 RSI overbought, waspada")
            score -= 2
        
        if last['MACD'] > last['MACD_signal']:
            signals.append("🟢 MACD bullish")
            score += 1
        else:
            signals.append("🔴 MACD bearish")
            score -= 1
        
        if last['Close'] > last['MA50']:
            signals.append("🟢 Harga di atas MA50 (uptrend)")
            score += 1
        else:
            signals.append("🔴 Harga di bawah MA50 (downtrend)")
            score -= 1
        
        if score >= 3:
            rec = "BELI"
        elif score <= -2:
            rec = "JUAL"
        else:
            rec = "NETRAL"
        
        return {
            'price': last['Close'],
            'rsi': last['RSI'],
            'macd': last['MACD'],
            'ma50': last['MA50'],
            'signals': signals,
            'score': score,
            'recommendation': rec
        }
    except Exception as e:
        print(f"Gold analysis error: {e}")
        return None


def get_forecast(symbol):
    """Ambil data prediksi dari database"""
    conn = sqlite3.connect(DB_PATH)
    table = f'forecast_{str(symbol).replace(".", "_")}'
    try:
        df = pd.read_sql(f"SELECT * FROM {table}", conn, parse_dates=['ds'])
        conn.close()
        return df
    except:
        conn.close()
        return None


# ========== FUNGSI UNTUK BANDAR / INSTITUSI ==========

def get_institutional_holders(symbol):
    """Ambil data institusi (bandar) yang megang saham"""
    try:
        ticker = yf.Ticker(symbol)
        inst = ticker.institutional_holders
        inst_list = []
        
        if inst is not None and not inst.empty:
            inst = inst.head(10)
            for _, row in inst.iterrows():
                holder_name = row.get('Holder', 'N/A')
                if holder_name == 'N/A':
                    continue
                inst_list.append({
                    'Holder': holder_name,
                    'Shares': row.get('Shares', 0),
                    'Date': row.get('Date', 'N/A'),
                    '% Out': row.get('% Out', 0)
                })
        
        major = ticker.major_holders
        major_dict = {}
        if major is not None and not major.empty:
            for _, row in major.iterrows():
                if len(row) >= 2:
                    major_dict[row.iloc[0]] = row.iloc[1]
        
        info = ticker.info
        fund_flow = {
            'shares_outstanding': info.get('sharesOutstanding', 0),
            'held_percent_institutions': info.get('heldPercentInstitutions', 0) * 100 if info.get('heldPercentInstitutions') else 0,
            'held_percent_insiders': info.get('heldPercentInsiders', 0) * 100 if info.get('heldPercentInsiders') else 0,
            'institutional_holders_count': len(inst_list)
        }
        
        return {
            'institutional_holders': inst_list,
            'major_holders': major_dict,
            'fund_flow': fund_flow
        }
    except Exception as e:
        print(f"Error get institutional holders for {symbol}: {e}")
        return None


def get_foreign_flow_summary(symbol):
    """Ambil ringkasan aliran dana asing vs domestik"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        inst_percent = info.get('heldPercentInstitutions', 0) * 100 if info.get('heldPercentInstitutions') else 0
        insider_percent = info.get('heldPercentInsiders', 0) * 100 if info.get('heldPercentInsiders') else 0
        
        foreign_estimate = inst_percent
        domestic_estimate = 100 - inst_percent
        
        hist = ticker.history(period="1mo")
        price_change = 0
        volume_surge = 1
        flow_signal = "➡️ Data tidak cukup"
        
        if not hist.empty:
            price_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            avg_volume = hist['Volume'].mean()
            last_volume = hist['Volume'].iloc[-1]
            volume_surge = (last_volume / avg_volume) if avg_volume > 0 else 1
            
            if price_change > 3 and volume_surge > 1.5:
                flow_signal = "🔥 AKUMULASI ASING (harga naik + volume surge)"
            elif price_change > 0 and volume_surge > 1:
                flow_signal = "📈 Akumulasi moderat"
            elif price_change < -3 and volume_surge > 1.5:
                flow_signal = "⚠️ DISTRIBUSI ASING (harga turun + volume surge)"
            else:
                flow_signal = "➡️ Netral / Tidak ada sinyal"
        
        return {
            'estimated_foreign_percent': foreign_estimate,
            'estimated_domestic_percent': domestic_estimate,
            'insider_percent': insider_percent,
            'flow_signal': flow_signal,
            'price_change_1m': price_change,
            'volume_surge': volume_surge
        }
    except Exception as e:
        print(f"Error get foreign flow for {symbol}: {e}")
        return {
            'estimated_foreign_percent': 0,
            'estimated_domestic_percent': 100,
            'insider_percent': 0,
            'flow_signal': "➡️ Error fetching data",
            'price_change_1m': 0,
            'volume_surge': 1
        }


def get_realtime_broker_summary(symbol):
    """Simulasi data broker summary untuk demo"""
    try:
        dummy_brokers = ['AK', 'BK', 'LG', 'HP', 'NI', 'RF', 'CC', 'OD', 'IF', 'EP', 'YP', 'ZP', 'AI', 'DR']
        dummy_data = []
        
        for broker in dummy_brokers:
            buy = random.randint(100000, 10000000)
            sell = random.randint(100000, 10000000)
            dummy_data.append({
                'BrokerCode': broker,
                'BuyVolume': buy,
                'SellVolume': sell
            })
        
        return pd.DataFrame(dummy_data)
    except Exception as e:
        print(f"Error getting realtime broker summary: {e}")
        return None


def get_broker_net_summary(symbol):
    """Ambil ringkasan net per broker untuk saham tertentu"""
    try:
        broker_df = get_realtime_broker_summary(symbol)
        if broker_df is None or broker_df.empty:
            return None
        
        result = []
        for _, row in broker_df.iterrows():
            code = row['BrokerCode']
            buy = row['BuyVolume']
            sell = row['SellVolume']
            net = buy - sell
            
            result.append({
                'broker_code': code,
                'buy_volume': buy,
                'sell_volume': sell,
                'net_volume': net,
                'is_accumulate': net > 0,
                'is_distribute': net < 0
            })
        
        result.sort(key=lambda x: abs(x['net_volume']), reverse=True)
        return result
    except Exception as e:
        print(f"Error get_broker_net_summary: {e}")
        return None


# ========== FUNGSI UNTUK FORECAST ==========

def exponential_smoothing(series, alpha=0.3, forecast_days=30):
    """Simple exponential smoothing untuk prediksi"""
    if len(series) < 50:
        return [series.iloc[-1]] * forecast_days
    
    result = [series.iloc[0]]
    for n in range(1, len(series)):
        result.append(alpha * series.iloc[n] + (1 - alpha) * result[n-1])
    
    trend = series.diff().tail(30).mean() if len(series) > 30 else 0
    last_smooth = result[-1]
    forecast = [last_smooth + (i+1)*trend for i in range(forecast_days)]
    return forecast
