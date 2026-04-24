# app/data/fetcher.py
import yfinance as yf
import pandas as pd
import sqlite3
from app.utils.config import STOCKS, DB_PATH
import os

def get_fundamental(symbol):
    """Ambil data fundamental dari Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'eps': info.get('trailingEps', 0),
            'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'return_on_equity': info.get('returnOnEquity', 0) * 100,
            'debt_to_equity': info.get('debtToEquity', 0),
            'current_price': info.get('regularMarketPrice', 0),
            'recommendation': info.get('recommendationKey', 'N/A'),
        }
    except Exception as e:
        print(f"[FAIL] {symbol}: {e}")
        return None

def update_fundamental():
    """Update data fundamental semua saham"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    all_data = []
    
    for sym in STOCKS:
        data = get_fundamental(sym)
        if data:
            all_data.append(data)
            print(f"[OK] {sym}")
    
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_sql('fundamental', conn, if_exists='replace', index=False)
        print(f"Data fundamental selesai. Total {len(all_data)} saham")
    
    conn.close()

def update_gold():
    """Update data emas dan DXY"""
    try:
        gold = yf.Ticker("GC=F")
        dxy = yf.Ticker("DX-Y.NYB")
        df_gold = gold.history(period="2y")
        df_dxy = dxy.history(period="2y")
        
        conn = sqlite3.connect(DB_PATH)
        df_gold.to_sql('gold', conn, if_exists='replace')
        df_dxy.to_sql('dxy', conn, if_exists='replace')
        conn.close()
        print("[OK] Data emas & DXY selesai.")
    except Exception as e:
        print(f"[FAIL] Gold data: {e}")

def update_all():
    """Update semua data"""
    print("Updating fundamental data...")
    update_fundamental()
    print("Updating gold data...")
    update_gold()