# app/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ========== DATABASE ==========
DB_PATH = os.getenv("DB_PATH", "data/invest.db")

# ========== SAHAM ==========
STOCKS = [
    # BANK
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'BRIS.JK',
    'BNGA.JK', 'BNLI.JK', 'AGRO.JK', 'ARTO.JK', 'BBTN.JK',
    'BDMN.JK', 'BJBR.JK', 'BJTM.JK', 'BMAS.JK', 'BTPN.JK',
    'MAYA.JK', 'MEGA.JK', 'NISP.JK', 'NOBU.JK', 'PNBN.JK',
    
    # TELEKOMUNIKASI
    'TLKM.JK', 'ISAT.JK', 'EXCL.JK', 'FREN.JK', 'TOWR.JK', 'TBIG.JK', 'MTEL.JK',
    
    # ENERGI
    'ADRO.JK', 'ITMG.JK', 'PTBA.JK', 'MEDC.JK', 'PGAS.JK', 'BUMI.JK', 'BYAN.JK',
    'DOID.JK', 'INDY.JK', 'HRUM.JK', 'ADMR.JK', 'ENRG.JK', 'AKRA.JK', 'ESSA.JK',
    
    # CONSUMER GOODS
    'UNVR.JK', 'ICBP.JK', 'INDF.JK', 'MYOR.JK', 'GGRM.JK', 'HMSP.JK', 'WIIM.JK',
    'DLTA.JK', 'MLBI.JK', 'ULTJ.JK', 'ROTI.JK', 'KEJU.JK', 'CAMP.JK', 'SKBM.JK', 'ADES.JK',
    
    # PROPERTY
    'BSDE.JK', 'CTRA.JK', 'PWON.JK', 'SMRA.JK', 'LPKR.JK', 'DMAS.JK', 'DILD.JK',
    'MDLN.JK', 'KIJA.JK', 'RISE.JK', 'TARA.JK',
    
    # INFRASTRUKTUR
    'JSMR.JK', 'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK', 'INTP.JK', 'SMCB.JK', 'SMGR.JK',
    
    # RETAIL
    'AMRT.JK', 'ACES.JK', 'RALS.JK', 'MAPI.JK', 'ERAA.JK', 'LPPF.JK', 'JPFA.JK', 'CPIN.JK', 'MAIN.JK',
    
    # OTOMOTIF
    'ASII.JK', 'AUTO.JK', 'GDYR.JK', 'GJTL.JK', 'LPIN.JK', 'SMSM.JK',
    
    # FARMASI
    'KAEF.JK', 'SIDO.JK', 'KLBF.JK', 'MERK.JK', 'PYFA.JK', 'TSPC.JK', 'HEAL.JK', 'SILO.JK', 'MIKA.JK',
    
    # TAMBANG
    'ANTM.JK', 'INCO.JK', 'TINS.JK', 'MDKA.JK', 'BRMS.JK', 'CITA.JK', 'NCKL.JK', 'PBID.JK',
    
    # TEKNOLOGI
    'DIVA.JK', 'BELI.JK', 'BUKA.JK', 'GOTO.JK',
    'BRPT.JK', 'BREN.JK', 'TPIA.JK', 'CUAN.JK', 'PTRO.JK', 'CDIA.JK',
]

# ========== PREDIKSI ==========
FORECAST_STOCKS = ['BBCA.JK', 'BBRI.JK', 'TLKM.JK', 'ASII.JK', 'ADRO.JK']
FORECAST_PERIOD = 30
TRAIN_DAYS = 730

# ========== TELEGRAM ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

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
BANDARMOLOGY_DIVIDEN = ['ADRO.JK', 'PTBA.JK', 'TLKM.JK', 'BRIS.JK', 'ACES.JK', 'DMAS.JK', 'CARS.JK', 'SUNI.JK', 'ESSA.JK', 'ADMR.JK']

# ========== GRUP KONGLOMERAT ==========
DJARUM_GROUP = {
    'name': 'Grup Djarum (Robert Budi Hartono)',
    'stocks': ['BBCA.JK', 'TOWR.JK', 'MTEL.JK', 'SSIA.JK', 'HEAL.JK'],
    'desc': 'Konglomerat rokok terbesar, pemilik BCA'
}
SALIM_GROUP = {
    'name': 'Grup Salim (Anthony Salim)',
    'stocks': ['INDF.JK', 'ICBP.JK', 'AMMN.JK', 'PANI.JK', 'DNET.JK', 'FAPA.JK', 'SIMP.JK', 'LSIP.JK', 'AGRO.JK'],
    'desc': 'Konglomerat makanan terbesar (Indomie)'
}
SINARMAS_GROUP = {
    'name': 'Grup Sinar Mas (Keluarga Widjaja)',
    'stocks': ['SMMA.JK', 'BSIM.JK', 'BSDE.JK', 'DMAS.JK', 'DSSA.JK', 'GEMS.JK', 'INKP.JK', 'TKIM.JK', 'SMAR.JK', 'DSNG.JK'],
    'desc': 'Konglomerat properti, energi, pulp & kertas'
}
PRAJOGO_GROUP = {
    'name': 'Grup Barito (Prajogo Pangestu)',
    'stocks': ['BRPT.JK', 'BREN.JK', 'TPIA.JK', 'CUAN.JK', 'PTRO.JK', 'CDIA.JK'],
    'desc': 'Konglomerat energi & petrokimia'
}
ASTRA_GROUP = {
    'name': 'Grup Astra (Keluarga Soeryadjaya)',
    'stocks': ['ASII.JK', 'UNTR.JK', 'AALI.JK', 'AUTO.JK', 'ASSA.JK'],
    'desc': 'Konglomerat otomotif & alat berat'
}
BAKRIE_GROUP = {
    'name': 'Grup Bakrie (Keluarga Bakrie)',
    'stocks': ['BUMI.JK', 'BRMS.JK', 'DEWA.JK', 'ENRG.JK', 'BNBR.JK', 'VKTR.JK', 'ALII.JK'],
    'desc': 'Konglomerat energi & tambang'
}
LIPPO_GROUP = {
    'name': 'Grup Lippo (James Riady)',
    'stocks': ['LPKR.JK', 'LPCK.JK', 'SILO.JK', 'MPPA.JK', 'LPPF.JK', 'MLPT.JK', 'BUKA.JK'],
    'desc': 'Konglomerat properti, kesehatan, ritel'
}

ALL_KONGLOMERAT_GROUPS = [DJARUM_GROUP, SALIM_GROUP, SINARMAS_GROUP, PRAJOGO_GROUP, ASTRA_GROUP, BAKRIE_GROUP, LIPPO_GROUP]