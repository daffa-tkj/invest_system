# app/utils/currency.py
def get_currency(symbol):
    """Deteksi mata uang dari kode saham"""
    if symbol == "GOLD" or symbol == "GC=F":
        return 'USD', '$'
    if str(symbol).endswith('.JK'):
        return 'IDR', 'Rp'
    if str(symbol).endswith('.T') or str(symbol).endswith('.KS'):
        return 'JPY', '¥'
    if str(symbol).endswith('.L'):
        return 'GBP', '£'
    return 'USD', '$'

def format_price(price, symbol):
    """Format harga dengan mata uang yang sesuai"""
    if price is None or price == 0:
        return "N/A"
    
    currency, sym = get_currency(symbol)
    
    if currency == 'IDR':
        return f"Rp {price:,.0f}".replace(',', '.')
    elif currency == 'USD':
        return f"${price:.2f}"
    elif currency == 'JPY':
        return f"¥{price:.0f}"
    else:
        return f"{sym}{price:.2f}"