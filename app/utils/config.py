# app/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ========== DATABASE ==========
DB_PATH = os.getenv("DB_PATH", "data/invest.db")

# ========== SAHAM BERDASARKAN KAPITALISASI ==========

# === LARGE CAP (Market Cap > Rp50 Triliun) ===
LARGE_CAP_STOCKS = [
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'TLKM.JK', 'ASII.JK', 
    'ADRO.JK', 'UNVR.JK', 'ICBP.JK', 'INDF.JK', 'CPIN.JK', 'JPFA.JK',
    'PGAS.JK', 'SMGR.JK', 'JSMR.JK', 'KLBF.JK', 'MYOR.JK', 'GGRM.JK',
    'HMSP.JK', 'TOWR.JK', 'BRPT.JK', 'TPIA.JK', 'BREN.JK', 'MDKA.JK',
    'AMMN.JK', 'ARTO.JK', 'AGRO.JK', 'BUKA.JK', 'GOTO.JK'
]

# === MID CAP (Rp10 Triliun - Rp50 Triliun) ===
MID_CAP_STOCKS = [
    'BRIS.JK', 'BNGA.JK', 'BTPS.JK', 'MAPI.JK', 'ERAA.JK', 'ACES.JK',
    'AMRT.JK', 'LSIP.JK', 'AALI.JK', 'SIMP.JK', 'PTBA.JK', 'ITMG.JK',
    'BYAN.JK', 'MEDC.JK', 'ENRG.JK', 'ESSA.JK', 'AKRA.JK', 'CUAN.JK',
    'PTRO.JK', 'CDIA.JK', 'TBIG.JK', 'MTEL.JK', 'EXCL.JK', 'ISAT.JK',
    'FREN.JK', 'BSDE.JK', 'CTRA.JK', 'PWON.JK', 'LPKR.JK', 'DMAS.JK',
    'DILD.JK', 'KIJA.JK', 'SILO.JK', 'MIKA.JK', 'HEAL.JK', 'SIDO.JK',
    'KAEF.JK', 'MERK.JK', 'PYFA.JK', 'TSPC.JK', 'ASSA.JK', 'UNTR.JK',
    'AUTO.JK', 'GDYR.JK', 'SMSM.JK', 'ANTM.JK', 'INCO.JK', 'TINS.JK',
    'BRMS.JK', 'NCKL.JK', 'PBID.JK', 'RALS.JK', 'LPPF.JK'
]

# === SMALL CAP (Rp1 Triliun - Rp10 Triliun) ===
SMALL_CAP_STOCKS = [
    'BNLI.JK', 'MAYA.JK', 'MEGA.JK', 'NISP.JK', 'NOBU.JK', 'PNBN.JK',
    'BJBR.JK', 'BJTM.JK', 'BMAS.JK', 'BTPN.JK', 'BBTN.JK', 'AGRO.JK',
    'BNLI.JK', 'INPC.JK', 'ERAL.JK', 'WIIM.JK', 'DLTA.JK', 'MLBI.JK',
    'ULTJ.JK', 'ROTI.JK', 'KEJU.JK', 'CAMP.JK', 'SKBM.JK', 'ADES.JK',
    'DOID.JK', 'INDY.JK', 'HRUM.JK', 'ADMR.JK', 'BUMI.JK', 'DEWA.JK',
    'BNBR.JK', 'VKTR.JK', 'ALII.JK', 'SMRA.JK', 'TARA.JK', 'MDLN.JK',
    'RISE.JK', 'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK', 'INTP.JK',
    'SMCB.JK', 'LPIN.JK', 'MAIN.JK', 'DIVA.JK', 'BELI.JK', 'SSIA.JK',
    'SMMA.JK', 'BSIM.JK', 'DSNG.JK', 'INKP.JK', 'TKIM.JK', 'SMAR.JK',
    'DSSA.JK', 'GEMS.JK', 'MORA.JK', 'ASDM.JK', 'TECH.JK'
]

# === MICRO CAP (Market Cap < Rp1 Triliun) ===
MICRO_CAP_STOCKS = [
    'FAPA.JK', 'PANI.JK', 'DNET.JK', 'BTPN.JK', 'MORA.JK', 'ASDM.JK',
    'INPC.JK', 'ERAL.JK', 'LPIN.JK', 'MAIN.JK', 'BELI.JK', 'DIVA.JK',
    'SSIA.JK', 'SMMA.JK', 'BSIM.JK', 'DSNG.JK', 'INKP.JK', 'TKIM.JK',
    'SMAR.JK', 'DSSA.JK', 'GEMS.JK', 'TECH.JK', 'VKTR.JK', 'ALII.JK',
    'BNBR.JK', 'DEWA.JK', 'BUMI.JK', 'ADMR.JK', 'HRUM.JK', 'INDY.JK',
    'DOID.JK', 'CAMP.JK', 'KEJU.JK', 'ROTI.JK', 'ULTJ.JK', 'DLTA.JK',
    'WIIM.JK', 'PNBN.JK', 'NOBU.JK', 'MEGA.JK', 'MAYA.JK', 'BNLI.JK'
]

# === GABUNGAN SEMUA SAHAM ===
ALL_STOCKS = LARGE_CAP_STOCKS + MID_CAP_STOCKS + SMALL_CAP_STOCKS + MICRO_CAP_STOCKS

# ========== BACKWARD COMPATIBLE ==========
STOCKS = ALL_STOCKS  # Untuk file lama yang masih panggil STOCKS

# ========== SAHAM BERDASARKAN SEKTOR ==========

# Perbankan
BANK_STOCKS = [
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'BRIS.JK', 'BNGA.JK',
    'BTPS.JK', 'BNLI.JK', 'MAYA.JK', 'MEGA.JK', 'NISP.JK', 'NOBU.JK',
    'PNBN.JK', 'BJBR.JK', 'BJTM.JK', 'BMAS.JK', 'BTPN.JK', 'BBTN.JK',
    'AGRO.JK', 'ARTO.JK', 'INPC.JK'
]

# Telekomunikasi & Media
TELCO_STOCKS = [
    'TLKM.JK', 'ISAT.JK', 'EXCL.JK', 'FREN.JK', 'TOWR.JK', 'TBIG.JK',
    'MTEL.JK', 'MORA.JK', 'EMTK.JK', 'SCMA.JK'
]

# Energi & Tambang
ENERGY_STOCKS = [
    'ADRO.JK', 'PTBA.JK', 'ITMG.JK', 'BYAN.JK', 'DOID.JK', 'INDY.JK',
    'HRUM.JK', 'ADMR.JK', 'BUMI.JK', 'DEWA.JK', 'ENRG.JK', 'ESSA.JK',
    'AKRA.JK', 'MEDC.JK', 'PGAS.JK', 'MDKA.JK', 'ANTM.JK', 'INCO.JK',
    'TINS.JK', 'BRMS.JK', 'NCKL.JK', 'PBID.JK', 'CITA.JK', 'PTRO.JK'
]

# Consumer Goods
CONSUMER_STOCKS = [
    'UNVR.JK', 'ICBP.JK', 'INDF.JK', 'MYOR.JK', 'GGRM.JK', 'HMSP.JK',
    'WIIM.JK', 'DLTA.JK', 'MLBI.JK', 'ULTJ.JK', 'ROTI.JK', 'KEJU.JK',
    'CAMP.JK', 'SKBM.JK', 'ADES.JK', 'CPIN.JK', 'JPFA.JK', 'MAIN.JK',
    'SIDO.JK', 'KAEF.JK', 'KLBF.JK', 'MERK.JK', 'PYFA.JK', 'TSPC.JK'
]

# Property & Real Estate
PROPERTY_STOCKS = [
    'BSDE.JK', 'CTRA.JK', 'PWON.JK', 'SMRA.JK', 'LPKR.JK', 'DMAS.JK',
    'DILD.JK', 'MDLN.JK', 'KIJA.JK', 'RISE.JK', 'TARA.JK', 'SMMA.JK',
    'BSIM.JK', 'DSSA.JK', 'GEMS.JK'
]

# Infrastruktur & Konstruksi
INFRA_STOCKS = [
    'JSMR.JK', 'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK', 'INTP.JK',
    'SMCB.JK', 'SMGR.JK', 'SSIA.JK', 'TPIA.JK', 'BREN.JK', 'CUAN.JK'
]

# Retail & Distribusi
RETAIL_STOCKS = [
    'AMRT.JK', 'ACES.JK', 'RALS.JK', 'MAPI.JK', 'ERAA.JK', 'LPPF.JK',
    'LPIN.JK', 'MAIN.JK', 'ASSA.JK', 'FAPA.JK'
]

# Otomotif
AUTOMOTIVE_STOCKS = [
    'ASII.JK', 'AUTO.JK', 'GDYR.JK', 'LPIN.JK', 'SMSM.JK', 'GJTL.JK'
]

# Healthcare
HEALTHCARE_STOCKS = [
    'SILO.JK', 'MIKA.JK', 'HEAL.JK', 'KAEF.JK', 'KLBF.JK', 'MERK.JK',
    'PYFA.JK', 'TSPC.JK', 'SIDO.JK'
]

# Teknologi & Digital
TECH_STOCKS = [
    'DIVA.JK', 'BELI.JK', 'BUKA.JK', 'GOTO.JK', 'DNET.JK', 'PANI.JK'
]

# ========== SAHAM KONGLOMERAT ==========

DJARUM_GROUP = {
    'name': 'Grup Djarum (Robert Budi Hartono)',
    'stocks': ['BBCA.JK', 'TOWR.JK', 'MTEL.JK', 'SSIA.JK', 'HEAL.JK'],
    'desc': 'Konglomerat rokok terbesar, pemilik BCA, tower telekomunikasi, dan properti'
}

SALIM_GROUP = {
    'name': 'Grup Salim (Anthony Salim)',
    'stocks': ['INDF.JK', 'ICBP.JK', 'AGRO.JK', 'SIMP.JK', 'LSIP.JK', 'FAPA.JK'],
    'desc': 'Konglomerat makanan terbesar (Indomie), perkebunan'
}

SINARMAS_GROUP = {
    'name': 'Grup Sinar Mas (Keluarga Widjaja)',
    'stocks': ['SMMA.JK', 'BSIM.JK', 'BSDE.JK', 'DMAS.JK', 'DSSA.JK', 'GEMS.JK', 'INKP.JK', 'TKIM.JK', 'SMAR.JK', 'DSNG.JK'],
    'desc': 'Konglomerat properti, energi, pulp & kertas, dan perkebunan'
}

ASTRA_GROUP = {
    'name': 'Grup Astra (Keluarga Soeryadjaya)',
    'stocks': ['ASII.JK', 'UNTR.JK', 'AALI.JK', 'AUTO.JK', 'ASSA.JK'],
    'desc': 'Konglomerat otomotif & alat berat terbesar di Indonesia'
}

# ========== SAHAM PREDIKSI ==========
FORECAST_STOCKS = ['BBCA.JK', 'BBRI.JK', 'TLKM.JK', 'ASII.JK', 'ADRO.JK']

# ========== TELEGRAM ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ========== PREDIKSI ==========
FORECAST_PERIOD = 30
TRAIN_DAYS = 730

# ========== KATEGORI BANDARMOLOGY ==========
FOREIGN_FLOW_UPTREN = ['BBCA.JK', 'BMRI.JK', 'TLKM.JK', 'ASII.JK', 'ADRO.JK', 'MDKA.JK', 'ISAT.JK', 'TOWR.JK']
ONE_MONTH_NET_FOREIGN = ['CARS.JK', 'SUNI.JK', 'ADMR.JK', 'ESSA.JK', 'BRIS.JK', 'ACES.JK', 'AMRT.JK']
BIG_ACCUMULATIONS = ['CARS.JK', 'SUNI.JK', 'DMAS.JK', 'ADMR.JK', 'MDKA.JK', 'PTBA.JK', 'WIKA.JK', 'PTPP.JK']
BANDAR_ACCUM_UPTREN = ['CARS.JK', 'SUNI.JK', 'ADMR.JK', 'MDKA.JK', 'BRIS.JK', 'ESSA.JK', 'TLKM.JK']
FREQUENCY_SPIKES = ['CARS.JK', 'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK', 'DMAS.JK']
INSIDER_NET_BUY = ['DMAS.JK', 'ADMR.JK', 'ESSA.JK', 'MDKA.JK', 'BRIS.JK', 'ACES.JK']

# ========== KATEGORI DIVIDEN ==========
DIVIDEN_STOCKS = [
    'ADRO.JK', 'PTBA.JK', 'ITMG.JK', 'TLKM.JK', 'BBCA.JK', 'BBRI.JK', 'BMRI.JK',
    'ASII.JK', 'INDF.JK', 'ICBP.JK', 'UNVR.JK', 'MYOR.JK', 'ACES.JK', 'AMRT.JK',
    'JSMR.JK', 'PGAS.JK', 'SMGR.JK', 'KLBF.JK', 'SIDO.JK'
]

CHEAP_BIG_CAPS_DIVIDEN = ['TLKM.JK', 'BBRI.JK', 'BMRI.JK', 'ASII.JK', 'ADRO.JK', 'PTBA.JK', 'PGAS.JK', 'JSMR.JK']
CHEAP_MID_CAPS_DIVIDEN = ['ACES.JK', 'AMRT.JK', 'BRIS.JK', 'INDF.JK', 'ICBP.JK', 'MYOR.JK', 'TOWR.JK', 'TBIG.JK']
CHEAP_SMALL_CAPS_DIVIDEN = ['DMAS.JK', 'SUNI.JK', 'CARS.JK', 'ESSA.JK', 'ADMR.JK', 'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK']
TOP_DIVIDEN = ['ADRO.JK', 'PTBA.JK', 'ITMG.JK', 'BYAN.JK', 'DOID.JK', 'HRUM.JK', 'INDY.JK']
BANDARMOLOGY_DIVIDEN = [
    'ADRO.JK', 'PTBA.JK', 'TLKM.JK', 'BRIS.JK', 'ACES.JK', 'DMAS.JK', 'CARS.JK', 'SUNI.JK', 'ESSA.JK', 'ADMR.JK'
]

# ========== SEMUA GRUP KONGLOMERAT ==========
ALL_KONGLOMERAT_GROUPS = [
    DJARUM_GROUP, SALIM_GROUP, SINARMAS_GROUP, ASTRA_GROUP
]

# ========== TIMEFRAME SCALPING ==========
TIMEFRAMES = {
    "1 Jam": "60m",
    "4 Jam": "240m",
    "Daily": "1d"
}

# ========== PARAMETER SCALPING ==========
SCALPING_ATR_PERIOD = 14
SCALPING_STOCH_RSI_PERIOD = 14
SCALPING_EMA_SHORT = 5
SCALPING_EMA_MEDIUM = 10
SCALPING_EMA_LONG = 20
