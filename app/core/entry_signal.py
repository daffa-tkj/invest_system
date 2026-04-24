# app/core/entry_signal.py
import pandas as pd
import numpy as np
import ta
from app.core.pattern_detector import detect_candlestick_patterns
from app.utils.currency import format_price, get_currency

def generate_entry_signal(df, symbol="GOLD"):
    """
    Generate signal beli/jual dengan skor dan confidence
    FIXED: Added empty df check and proper error handling
    """
    # FIX #1: Empty dataframe check
    if df is None or df.empty:
        return {
            'symbol': symbol,
            'price': 0,
            'score': 0,
            'recommendation': "DATA KOSONG",
            'action': "HOLD",
            'confidence': "LOW",
            'reasons': ["Tidak ada data harga"],
            'rsi': 50,
            'macd': 0,
            'ma20': 0,
            'ma50': 0,
            'support': 0,
            'resistance': 0
        }
    
    df = df.copy()
    df = detect_candlestick_patterns(df)
    
    # FIX #2: Minimum data check
    if len(df) < 50:
        last_price = df['Close'].iloc[-1] if 'Close' in df.columns else 0
        return {
            'symbol': symbol,
            'price': last_price,
            'score': 0,
            'recommendation': "DATA KURANG",
            'action': "HOLD",
            'confidence': "LOW",
            'reasons': [f"Data historis hanya {len(df)} hari (minimal 50)"],
            'rsi': 50,
            'macd': 0,
            'ma20': last_price,
            'ma50': last_price,
            'support': last_price * 0.95,
            'resistance': last_price * 1.05
        }
    
    # Indikator teknikal
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    macd_ind = ta.trend.MACD(df['Close'])
    df['MACD'] = macd_ind.macd()
    df['MACD_signal'] = macd_ind.macd_signal()
    df['MACD_hist'] = macd_ind.macd_diff()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['Support'] = df['Low'].rolling(window=20).min()
    df['Resistance'] = df['High'].rolling(window=20).max()
    
    avg_volume = df['Volume'].rolling(window=20).mean()
    df['Volume_Surge'] = df['Volume'] > avg_volume * 1.5
    
    # FIX #3: Safe last row access
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    
    score = 0
    reasons = []
    
    # 1. RSI
    if last['RSI'] < 30:
        score += 2
        reasons.append(f"RSI oversold ({last['RSI']:.1f})")
    elif last['RSI'] < 40:
        score += 1
        reasons.append(f"RSI mendekati oversold ({last['RSI']:.1f})")
    elif last['RSI'] > 70:
        score -= 2
        reasons.append(f"RSI overbought ({last['RSI']:.1f})")
    elif last['RSI'] > 60:
        score -= 1
        reasons.append(f"RSI mendekati overbought ({last['RSI']:.1f})")
    
    # 2. MACD Crossover
    if not pd.isna(last['MACD']) and not pd.isna(last['MACD_signal']):
        if last['MACD'] > last['MACD_signal'] and prev['MACD'] <= prev['MACD_signal']:
            score += 3
            reasons.append("MACD bullish crossover")
        elif last['MACD'] < last['MACD_signal'] and prev['MACD'] >= prev['MACD_signal']:
            score -= 3
            reasons.append("MACD bearish crossover")
    
    # 3. Moving Averages
    if last['Close'] > last['MA20'] and prev['Close'] <= prev['MA20']:
        score += 2
        reasons.append("Breakout di atas MA20")
    elif last['Close'] < last['MA20'] and prev['Close'] >= prev['MA20']:
        score -= 2
        reasons.append("Breakdown di bawah MA20")
    
    if last['Close'] > last['MA50']:
        score += 1
        reasons.append("Harga di atas MA50 (uptrend)")
    else:
        score -= 1
        reasons.append("Harga di bawah MA50 (downtrend)")
    
    # 4. Support/Resistance
    if last['Close'] <= last['Support'] * 1.02:
        score += 2
        reasons.append(f"Mendekati support di {last['Support']:.2f}")
    if last['Close'] >= last['Resistance'] * 0.98:
        score -= 2
        reasons.append(f"Mendekati resistance di {last['Resistance']:.2f}")
    
    # 5. Volume
    if last['Volume_Surge']:
        if last['Close'] > last['Open']:
            score += 1
            reasons.append("Volume surge + harga naik (konfirmasi beli)")
        else:
            score -= 1
            reasons.append("Volume surge + harga turun (konfirmasi jual)")
    
    # 6. Candlestick Patterns
    if last.get('Bullish_Engulfing', False):
        score += 3
        reasons.append("Bullish Engulfing pattern (strong buy signal)")
    elif last.get('Hammer', False):
        score += 2
        reasons.append("Hammer pattern (potential reversal up)")
    elif last.get('Bearish_Engulfing', False):
        score -= 3
        reasons.append("Bearish Engulfing pattern (strong sell signal)")
    
    # Decision
    if score >= 5:
        recommendation = "BELI AGGRESSIVE"
        action = "BUY"
        confidence = "HIGH"
    elif score >= 2:
        recommendation = "BELI MODERATE"
        action = "BUY"
        confidence = "MEDIUM"
    elif score <= -5:
        recommendation = "JUAL AGGRESSIVE"
        action = "SELL"
        confidence = "HIGH"
    elif score <= -2:
        recommendation = "JUAL MODERATE"
        action = "SELL"
        confidence = "MEDIUM"
    else:
        recommendation = "NETRAL / HOLD"
        action = "HOLD"
        confidence = "LOW"
    
    return {
        'symbol': symbol,
        'price': last['Close'],
        'score': score,
        'recommendation': recommendation,
        'action': action,
        'confidence': confidence,
        'reasons': reasons,
        'rsi': last['RSI'] if not pd.isna(last['RSI']) else 50,
        'macd': last['MACD'] if not pd.isna(last['MACD']) else 0,
        'ma20': last['MA20'],
        'ma50': last['MA50'],
        'support': last['Support'],
        'resistance': last['Resistance']
    }