# app/core/pattern_detector.py
import pandas as pd
import numpy as np

def detect_candlestick_patterns(df):
    """Deteksi pola candlestick: Doji, Hammer, Engulfing"""
    df = df.copy()
    
    if len(df) < 3:
        df['Doji'] = False
        df['Hammer'] = False
        df['Bullish_Engulfing'] = False
        df['Bearish_Engulfing'] = False
        return df
    
    # Doji (open ≈ close)
    body = abs(df['Close'] - df['Open'])
    range_ = df['High'] - df['Low']
    df['Doji'] = (body / range_ < 0.1) & (range_ > 0)
    
    # Hammer (body kecil, shadow bawah panjang)
    lower_shadow = np.where(
        df['Close'] > df['Open'],
        df['Open'] - df['Low'],
        df['Close'] - df['Low']
    )
    upper_shadow = np.where(
        df['Close'] > df['Open'],
        df['High'] - df['Close'],
        df['High'] - df['Open']
    )
    body_size = abs(df['Close'] - df['Open'])
    df['Hammer'] = (lower_shadow > body_size * 2) & (upper_shadow < body_size * 0.5)
    
    # Bullish Engulfing
    prev_bearish = df['Open'].shift(1) > df['Close'].shift(1)
    curr_bullish = df['Open'] < df['Close']
    open_below_prev_close = df['Open'] < df['Close'].shift(1)
    close_above_prev_open = df['Close'] > df['Open'].shift(1)
    df['Bullish_Engulfing'] = prev_bearish & curr_bullish & open_below_prev_close & close_above_prev_open
    
    # Bearish Engulfing
    prev_bullish = df['Open'].shift(1) < df['Close'].shift(1)
    curr_bearish = df['Open'] > df['Close']
    open_above_prev_close = df['Open'] > df['Close'].shift(1)
    close_below_prev_open = df['Close'] < df['Open'].shift(1)
    df['Bearish_Engulfing'] = prev_bullish & curr_bearish & open_above_prev_close & close_below_prev_open
    
    return df

def get_latest_patterns(df, days=5):
    """Ambil pola terakhir"""
    if df.empty or len(df) < days:
        return []
    
    df = detect_candlestick_patterns(df)
    last_rows = df.tail(days)
    patterns = []
    
    for idx in last_rows.index:
        date = idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else str(idx)[:10]
        row = last_rows.loc[idx]
        
        if row.get('Doji', False):
            patterns.append(f"{date}: Doji (potensi reversal)")
        if row.get('Hammer', False):
            patterns.append(f"{date}: Hammer (bullish reversal)")
        if row.get('Bullish_Engulfing', False):
            patterns.append(f"{date}: Bullish Engulfing (signal beli)")
        if row.get('Bearish_Engulfing', False):
            patterns.append(f"{date}: Bearish Engulfing (signal jual)")
    
    return patterns