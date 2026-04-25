# app/core/analysis.py
import pandas as pd
import numpy as np
import sqlite3
import ta
import yfinance as yf
import requests
import os
from datetime import datetime, timedelta
from app.utils.config import DB_PATH
from app.utils.currency import format_price, get_currency

# ========== KONFIGURASI API ==========
# Daftar gratis di https://itick.org
# Free tier: 1000 request/hari
ITICK_API_KEY = os.getenv("ITICK_API_KEY", "")
ITICK_BASE_URL = "https://api.itick.org/v1"


# ========== FUNGSI iTICK API - FULL OTOMATIS ==========

def call_itick_api(endpoint, params=None):
    """
    Fungsi generic buat panggil iTICK API
    """
    if not ITICK_API_KEY:
        print("[iTICK] API Key not set. Get free API key from https://itick.org")
        return None
    
    if params is None:
        params = {}
    
    url = f"{ITICK_BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {ITICK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data and data.get('status') in ['success', 'ok', 200]:
                return data.get('data', data)
            else:
                print(f"[iTICK] API error for {endpoint}: {data.get('message', 'Unknown error')}")
                return None
        else:
            print(f"[iTICK] HTTP {response.status_code} for {endpoint}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"[iTICK] Timeout for {endpoint}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[iTICK] Connection error for {endpoint}")
        return None
    except Exception as e:
        print(f"[iTICK] Error for {endpoint}: {e}")
        return None


def get_stock_info_from_itick(symbol):
    """
    Ambil data fundamental LENGKAP dari iTICK API
    Returns data profil perusahaan (name, sector, industry, market cap, pe, roe, description, website, dll)
    """
    clean_symbol = symbol.replace('.JK', '').upper()
    
    # Coba beberapa endpoint yang mungkin tersedia
    endpoints = [
        f"stock/profile",           # Profile perusahaan
        f"stock/info",              # Info umum
        f"stock/fundamental",       # Data fundamental
        f"stock/detail",            # Detail lengkap
        f"stock/company",           # Company profile
        f"stock/quote"              # Quote + info dasar
    ]
    
    for endpoint in endpoints:
        params = {"symbol": clean_symbol, "region": "ID"}
        data = call_itick_api(endpoint, params)
        
        if data:
            # Extract data dari response
            if isinstance(data, dict):
                # Cek apakah ada data yang valid
                if data.get('name') or data.get('longName') or data.get('companyName'):
                    return {
                        'name': data.get('name') or data.get('longName') or data.get('companyName') or symbol,
                        'sector': data.get('sector') or data.get('industrySector') or 'N/A',
                        'industry': data.get('industry') or data.get('industryGroup') or 'N/A',
                        'market_cap': data.get('marketCap') or data.get('market_cap') or 0,
                        'pe_ratio': data.get('pe') or data.get('peRatio') or data.get('trailingPE') or 0,
                        'pb_ratio': data.get('pb') or data.get('priceToBook') or 0,
                        'roe': data.get('roe') or data.get('returnOnEquity') or 0,
                        'roa': data.get('roa') or data.get('returnOnAssets') or 0,
                        'dividend_yield': data.get('dividendYield') or data.get('dividend_yield') or 0,
                        'eps': data.get('eps') or data.get('earningPerShare') or 0,
                        'beta': data.get('beta') or 0,
                        'description': data.get('description') or data.get('longBusinessSummary') or data.get('businessSummary') or 'Deskripsi tidak tersedia',
                        'website': data.get('website') or data.get('weburl') or '',
                        'country': data.get('country') or 'Indonesia',
                        'employees': data.get('employees') or data.get('fullTimeEmployees') or 0
                    }
    
    # Jika iTICK gagal, coba Yahoo
    return get_stock_info_from_yahoo(symbol)


def get_stock_info_from_yahoo(symbol):
    """
    Fallback ke Yahoo Finance jika iTICK gagal
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
            'roa': info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0,
            'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'eps': info.get('trailingEps', 0),
            'beta': info.get('beta', 0),
            'description': info.get('longBusinessSummary', 'Deskripsi tidak tersedia'),
            'website': info.get('website', ''),
            'country': info.get('country', 'Indonesia'),
            'employees': info.get('fullTimeEmployees', 0)
        }
    except Exception as e:
        print(f"Yahoo Finance error for {symbol}: {e}")
        return {
            'name': symbol,
            'sector': 'N/A',
            'industry': 'N/A',
            'market_cap': 0,
            'pe_ratio': 0,
            'pb_ratio': 0,
            'roe': 0,
            'roa': 0,
            'dividend_yield': 0,
            'eps': 0,
            'beta': 0,
            'description': 'Deskripsi tidak tersedia',
            'website': '',
            'country': 'Indonesia',
            'employees': 0
        }


def get_stock_data_from_itick(symbol, period="6mo"):
    """
    Ambil data historis harga dari iTICK API
    """
    clean_symbol = symbol.replace('.JK', '').upper()
    
    # Konversi period ke days
    days_map = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730}
    days = days_map.get(period, 180)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Coba endpoint historis
    endpoints = [
        f"stock/historical",
        f"stock/klines",
        f"stock/bars"
    ]
    
    for endpoint in endpoints:
        params = {
            "symbol": clean_symbol,
            "region": "ID",
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "interval": "1d"
        }
        data = call_itick_api(endpoint, params)
        
        if data:
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                
                # Standardize column names
                column_mapping = {
                    'date': 'Date',
                    'time': 'Date',
                    'timestamp': 'Date',
                    'open': 'Open',
                    'Open': 'Open',
                    'high': 'High',
                    'High': 'High',
                    'low': 'Low',
                    'Low': 'Low',
                    'close': 'Close',
                    'Close': 'Close',
                    'volume': 'Volume',
                    'Volume': 'Volume',
                    'price': 'Close'
                }
                
                df.rename(columns=column_mapping, inplace=True)
                
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                    df.set_index('Date', inplace=True)
                
                # Pastikan semua kolom ada
                required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                for col in required_cols:
                    if col not in df.columns and col == 'Close' and 'price' in df.columns:
                        df['Close'] = df['price']
                    elif col not in df.columns:
                        df[col] = 0
                
                return df
    
    # Fallback ke Yahoo
    return get_stock_data_from_yahoo(symbol, period)


def get_stock_data_from_yahoo(symbol, period="6mo"):
    """
    Fallback ke Yahoo Finance untuk data historis
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        return df if not df.empty else None
    except Exception as e:
        print(f"Yahoo Finance historical error for {symbol}: {e}")
        return None


def get_realtime_price_from_itick(symbol):
    """
    Ambil harga real-time dari iTICK API
    """
    clean_symbol = symbol.replace('.JK', '').upper()
    
    data = call_itick_api(f"stock/quote", {"symbol": clean_symbol, "region": "ID"})
    
    if data:
        # Coba extract harga dari berbagai kemungkinan key
        return data.get('price') or data.get('last') or data.get('lastPrice') or data.get('close') or 0
    
    # Fallback ke Yahoo
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info.get('regularMarketPrice', info.get('currentPrice', 0))
    except:
        return 0


# ========== MAIN FUNCTIONS (UNIFIED API) ==========

def get_stock_info(symbol):
    """
    Get comprehensive stock information from iTICK API
    Auto - tanpa fallback manual
    """
    return get_stock_info_from_itick(symbol)


def get_stock_data(symbol, period="6mo"):
    """
    Get historical price data from iTICK API
    Auto - tanpa fallback manual
    """
    return get_stock_data_from_itick(symbol, period)


def get_realtime_price(symbol):
    """
    Get real-time price from iTICK API
    Auto - tanpa fallback manual
    """
    return get_realtime_price_from_itick(symbol)


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


def analyze_gold():
    """Analisis teknikal emas dari Yahoo Finance"""
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
    except:
        df = None
    conn.close()
    return df


def get_institutional_holders(symbol):
    """Ambil data institusi dari Yahoo (iTICK mungkin gak punya data ini)"""
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
        
        return {'institutional_holders': inst_list} if inst_list else None
    except Exception as e:
        print(f"Error get institutional holders for {symbol}: {e}")
        return None


# ========== BROKER FUNCTIONS (Simulation) ==========

def get_realtime_broker_summary(symbol):
    """
    Simulasi data broker summary - untuk data real perlu API RTI Business
    """
    import random
    
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
