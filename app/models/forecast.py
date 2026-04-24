# app/models/forecast.py
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
from app.utils.config import DB_PATH, FORECAST_STOCKS, FORECAST_PERIOD, TRAIN_DAYS

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

def train_forecast(symbol, train_days=TRAIN_DAYS):
    """Train forecast untuk satu simbol"""
    try:
        ticker = yf.Ticker(symbol)
        end = datetime.now()
        start = end - timedelta(days=train_days)
        df = ticker.history(start=start, end=end)
        
        if df.empty:
            return None
        
        close = df['Close']
        forecast_values = exponential_smoothing(close, alpha=0.3, forecast_days=FORECAST_PERIOD)
        last_date = df.index[-1]
        forecast_dates = [last_date + timedelta(days=i+1) for i in range(FORECAST_PERIOD)]
        
        forecast_df = pd.DataFrame({
            'ds': forecast_dates,
            'yhat': forecast_values,
            'yhat_lower': [v * 0.97 for v in forecast_values],
            'yhat_upper': [v * 1.03 for v in forecast_values]
        })
        return forecast_df
    except Exception:
        return None

def update_forecasts():
    """Update semua prediksi ke database"""
    import os
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    # Gold forecast
    try:
        gold = yf.Ticker("GC=F")
        end = datetime.now()
        start = end - timedelta(days=TRAIN_DAYS)
        df_gold = gold.history(start=start, end=end)
        
        if not df_gold.empty:
            forecast_values = exponential_smoothing(df_gold['Close'], alpha=0.3, forecast_days=FORECAST_PERIOD)
            last_date = df_gold.index[-1]
            forecast_dates = [last_date + timedelta(days=i+1) for i in range(FORECAST_PERIOD)]
            df_forecast_gold = pd.DataFrame({
                'ds': forecast_dates,
                'yhat': forecast_values,
                'yhat_lower': [v * 0.97 for v in forecast_values],
                'yhat_upper': [v * 1.03 for v in forecast_values]
            })
            df_forecast_gold.to_sql('gold_forecast', conn, if_exists='replace', index=False)
            print(f"[OK] Gold forecast: {len(forecast_values)} days")
    except Exception as e:
        print(f"[FAIL] Gold forecast: {e}")
    
    # Stock forecasts
    for sym in FORECAST_STOCKS:
        df = train_forecast(sym)
        if df is not None:
            table_name = f'forecast_{sym.replace(".", "_")}'
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"[OK] {sym} forecast")
    
    conn.close()
    print("Semua prediksi selesai.")