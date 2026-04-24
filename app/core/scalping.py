# app/core/scalping.py
import yfinance as yf
import pandas as pd
import numpy as np
import ta

def get_gold_data(timeframe="1h", days=7):
    """Ambil data emas dengan timeframe tertentu"""
    ticker = yf.Ticker("GC=F")
    
    if timeframe == "1h":
        period = "7d"
        interval = "1h"
    elif timeframe == "4h":
        period = "30d"
        interval = "1h"
    else:
        period = "30d"
        interval = "1d"
    
    df = ticker.history(period=period, interval=interval)
    
    if timeframe == "4h" and not df.empty:
        df = df.resample('4H').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
    
    return df

def calculate_scalping_indicators(df):
    """Hitung indikator untuk scalping"""
    if df.empty or len(df) < 20:
        return df
    
    df = df.copy()
    
    df['EMA5'] = ta.trend.EMAIndicator(df['Close'], window=5).ema_indicator()
    df['EMA10'] = ta.trend.EMAIndicator(df['Close'], window=10).ema_indicator()
    df['EMA20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
    
    stoch_rsi = ta.momentum.StochRSIIndicator(df['Close'], window=14, smooth1=3, smooth2=3)
    df['StochRSI_K'] = stoch_rsi.stochrsi_k()
    df['StochRSI_D'] = stoch_rsi.stochrsi_d()
    
    df['Volume_MA'] = df['Volume'].rolling(20).mean()
    df['Volume_Surge'] = df['Volume'] > df['Volume_MA'] * 1.5
    df['Support_Intra'] = df['Low'].rolling(20).min()
    df['Resistance_Intra'] = df['High'].rolling(20).max()
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['R1'] = 2 * df['Pivot'] - df['Low']
    df['S1'] = 2 * df['Pivot'] - df['High']
    
    return df

def generate_scalping_signal(df):
    """Generate sinyal scalping berdasarkan indikator"""
    if df.empty or len(df) < 20:
        return None
    
    df = calculate_scalping_indicators(df)
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    score = 0
    reasons = []
    
    # EMA Alignment
    if last['EMA5'] > last['EMA10'] > last['EMA20']:
        score += 2
        reasons.append("EMA 5 > 10 > 20 (Strong Uptrend)")
    elif last['EMA5'] > last['EMA10']:
        score += 1
        reasons.append("EMA 5 > 10 (Uptrend)")
    elif last['EMA5'] < last['EMA10'] < last['EMA20']:
        score -= 2
        reasons.append("EMA 5 < 10 < 20 (Strong Downtrend)")
    elif last['EMA5'] < last['EMA10']:
        score -= 1
        reasons.append("EMA 5 < 10 (Downtrend)")
    
    # Stochastic RSI
    if last['StochRSI_K'] < 20 and prev['StochRSI_K'] <= prev['StochRSI_D'] and last['StochRSI_K'] > last['StochRSI_D']:
        score += 2
        reasons.append(f"StochRSI Oversold Crossover (K={last['StochRSI_K']:.1f})")
    elif last['StochRSI_K'] < 20:
        score += 1
        reasons.append(f"StochRSI Oversold ({last['StochRSI_K']:.1f})")
    elif last['StochRSI_K'] > 80 and prev['StochRSI_K'] >= prev['StochRSI_D'] and last['StochRSI_K'] < last['StochRSI_D']:
        score -= 2
        reasons.append(f"StochRSI Overbought Crossover (K={last['StochRSI_K']:.1f})")
    elif last['StochRSI_K'] > 80:
        score -= 1
        reasons.append(f"StochRSI Overbought ({last['StochRSI_K']:.1f})")
    
    # Price vs EMA
    if last['Close'] > last['EMA10'] and prev['Close'] <= prev['EMA10']:
        score += 1
        reasons.append("Breakout above EMA10")
    elif last['Close'] < last['EMA10'] and prev['Close'] >= prev['EMA10']:
        score -= 1
        reasons.append("Breakdown below EMA10")
    
    # Volume Surge
    if last['Volume_Surge']:
        if last['Close'] > last['Open']:
            score += 1
            reasons.append("Volume surge + bullish candle")
        else:
            score -= 1
            reasons.append("Volume surge + bearish candle")
    
    # Support/Resistance
    if last['Close'] <= last['Support_Intra'] * 1.005:
        score += 1
        reasons.append(f"Mendekati support intraday ({last['Support_Intra']:.2f})")
    if last['Close'] >= last['Resistance_Intra'] * 0.995:
        score -= 1
        reasons.append(f"Mendekati resistance intraday ({last['Resistance_Intra']:.2f})")
    
    # Decision
    if score >= 3:
        recommendation = "SCALP BUY"
        action = "BUY"
        confidence = "HIGH"
    elif score >= 1:
        recommendation = "SCALP BUY (Moderate)"
        action = "BUY"
        confidence = "MEDIUM"
    elif score <= -3:
        recommendation = "SCALP SELL"
        action = "SELL"
        confidence = "HIGH"
    elif score <= -1:
        recommendation = "SCALP SELL (Moderate)"
        action = "SELL"
        confidence = "MEDIUM"
    else:
        recommendation = "NO SCALP SIGNAL"
        action = "WAIT"
        confidence = "LOW"
    
    atr = last['ATR']
    if action == "BUY":
        stop_loss = last['Close'] - (atr * 1.5)
        take_profit = last['Close'] + (atr * 2)
    elif action == "SELL":
        stop_loss = last['Close'] + (atr * 1.5)
        take_profit = last['Close'] - (atr * 2)
    else:
        stop_loss = last['Close']
        take_profit = last['Close']
    
    return {
        'price': last['Close'],
        'score': score,
        'recommendation': recommendation,
        'action': action,
        'confidence': confidence,
        'reasons': reasons,
        'ema5': last['EMA5'],
        'ema10': last['EMA10'],
        'ema20': last['EMA20'],
        'stoch_rsi_k': last['StochRSI_K'],
        'stoch_rsi_d': last['StochRSI_D'],
        'atr': atr,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'support': last['Support_Intra'],
        'resistance': last['Resistance_Intra'],
        'pivot': last['Pivot'],
        'r1': last['R1'],
        's1': last['S1']
    }