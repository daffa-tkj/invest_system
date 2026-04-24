# app/utils/broker_codes.py

# Daftar kode broker saham Indonesia (update 2026)
# Sumber: BEI, OJK [citation:1][citation:2][citation:4]

BROKER_CODES = {
    # === BROKER BESAR / MAJOR ===
    'AK': {'name': 'UBS Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'MAJOR', 'desc': 'Bank Swiss, dominan asing'},
    'BK': {'name': 'J.P. Morgan Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'MAJOR', 'desc': 'Investment bank US, bandar asing besar'},
    'LG': {'name': 'Trimegah Sekuritas Indonesia Tbk', 'type': 'LOCAL', 'category': 'MAJOR', 'desc': 'Swasta lokal, sering jadi bandar'},
    'HP': {'name': 'Henan Putihrai Sekuritas', 'type': 'LOCAL', 'category': 'MAJOR', 'desc': 'Lokal besar, likuid'},
    'NI': {'name': 'BNI Sekuritas', 'type': 'LOCAL', 'category': 'STATE', 'desc': 'Bank BUMN, sering entry di saham blue chip'},
    'RF': {'name': 'Buana Capital Sekuritas', 'type': 'LOCAL', 'category': 'MAJOR', 'desc': 'Lokal, agresif'},
    
    # === BROKER ASING ===
    'AI': {'name': 'UOB Kay Hian Sekuritas', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Singapura, asing dominan'},
    'AH': {'name': 'Shinhan Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Korea Selatan'},
    'AG': {'name': 'Kiwoom Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Korea Selatan'},
    'BQ': {'name': 'Korea Investment and Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Korea Selatan'},
    'CS': {'name': 'Credit Suisse Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Swiss'},
    'DP': {'name': 'DBS Vickers Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Singapura'},
    'DR': {'name': 'RHB Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Malaysia'},
    'KZ': {'name': 'CLSA Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Hong Kong'},
    'YP': {'name': 'Mirae Asset Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Korea Selatan'},
    'YU': {'name': 'CGS International Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'China-Singapura'},
    'ZP': {'name': 'Maybank Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Malaysia'},
    'TP': {'name': 'OCBC Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Singapura'},
    'RX': {'name': 'Macquarie Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Australia'},
    'GW': {'name': 'HSBC Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Inggris'},
    
    # === BROKER BUMN / STATE ===
    'CC': {'name': 'Mandiri Sekuritas', 'type': 'LOCAL', 'category': 'STATE', 'desc': 'BUMN, bank mandiri'},
    'OD': {'name': 'BRI Danareksa Sekuritas', 'type': 'LOCAL', 'category': 'STATE', 'desc': 'BUMN, bank BRI'},
    'CD': {'name': 'Mega Capital Sekuritas', 'type': 'LOCAL', 'category': 'STATE', 'desc': 'BUMN'},
    'DX': {'name': 'Bahana Sekuritas', 'type': 'LOCAL', 'category': 'STATE', 'desc': 'BUMN, anak usaha BRI'},
    
    # === BROKER LOKAL SWASTA ===
    'IF': {'name': 'Samuel Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta besar'},
    'EP': {'name': 'MNC Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Grup MNC, likuid'},
    'AZ': {'name': 'Sucor Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'KK': {'name': 'Phillip Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'FS': {'name': 'Yuanta Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'BR': {'name': 'Trust Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'AT': {'name': 'Phintraco Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'KI': {'name': 'Ciptadana Sekuritas Asia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'PD': {'name': 'Indo Premier Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'PO': {'name': 'Pilarmas Investindo Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'MG': {'name': 'Semesta Indovest Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'MI': {'name': 'Victoria Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    
    # === BROKER DIGITAL / RETAIL ===
    'XC': {'name': 'Ajaib Sekuritas Asia', 'type': 'LOCAL', 'category': 'RETAIL', 'desc': 'Digital, ritel'},
    'XL': {'name': 'Stockbit Sekuritas Digital', 'type': 'LOCAL', 'category': 'RETAIL', 'desc': 'Digital, komunitas'},
    'OK': {'name': 'NET Sekuritas', 'type': 'LOCAL', 'category': 'RETAIL', 'desc': 'Digital'},
    'XA': {'name': 'NH Korindo Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'RETAIL', 'desc': 'Korea-Indonesia'},
    'GI': {'name': 'Webull Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'RETAIL', 'desc': 'US-based digital'},
    'RO': {'name': 'Pluang Maju Sekuritas', 'type': 'LOCAL', 'category': 'RETAIL', 'desc': 'Digital, micro saving'},
    
    # === BROKER LAINNYA ===
    'AF': {'name': 'Harita Kencana Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'BB': {'name': 'Verdhana Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'CP': {'name': 'KB Valbury Sekuritas', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Korea Selatan'},
    'DH': {'name': 'Sinarmas Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Grup Sinarmas'},
    'GR': {'name': 'Panin Sekuritas Tbk', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Grup Panin'},
    'HD': {'name': 'KGI Sekuritas Indonesia', 'type': 'FOREIGN', 'category': 'FOREIGN', 'desc': 'Taiwan'},
    'LS': {'name': 'Reliance Sekuritas Indonesia Tbk', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'PS': {'name': 'Paramitra Alfa Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'RG': {'name': 'Profindo Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'SS': {'name': 'Supra Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'SQ': {'name': 'BCA Sekuritas', 'type': 'LOCAL', 'category': 'STATE', 'desc': 'Bank BCA'},
    'SH': {'name': 'Artha Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'ZR': {'name': 'Bumiputera Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'AN': {'name': 'Wanteg Sekuritas', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
    'FZ': {'name': 'Waterfront Sekuritas Indonesia', 'type': 'LOCAL', 'category': 'LOCAL_PRIVATE', 'desc': 'Swasta'},
}

def get_broker_info(code):
    """Ambil info broker berdasarkan kode"""
    return BROKER_CODES.get(code.upper(), {
        'name': f'Unknown ({code})',
        'type': 'UNKNOWN',
        'category': 'UNKNOWN',
        'desc': 'Kode broker tidak terdaftar'
    })

def get_top_accumulators(df_rti, limit=10):
    """
    Analisis broker accumulator dari data RTI
    df_rti: dataframe dengan kolom 'BuyVolume', 'SellVolume', 'BrokerCode'
    """
    if df_rti is None or df_rti.empty:
        return None
    
    # Hitung net volume per broker
    broker_summary = []
    for code in df_rti['BrokerCode'].unique():
        broker_data = df_rti[df_rti['BrokerCode'] == code]
        buy_vol = broker_data['BuyVolume'].sum()
        sell_vol = broker_data['SellVolume'].sum()
        net_vol = buy_vol - sell_vol
        net_percent = (net_vol / (buy_vol + sell_vol) * 100) if (buy_vol + sell_vol) > 0 else 0
        
        broker_info = get_broker_info(code)
        broker_summary.append({
            'code': code,
            'name': broker_info['name'],
            'type': broker_info['type'],
            'category': broker_info['category'],
            'buy_vol': buy_vol,
            'sell_vol': sell_vol,
            'net_vol': net_vol,
            'net_percent': net_percent,
            'action': 'ACCUMULATE' if net_vol > 0 else ('DISTRIBUTE' if net_vol < 0 else 'NEUTRAL')
        })
    
    broker_summary.sort(key=lambda x: abs(x['net_vol']), reverse=True)
    return broker_summary[:limit]