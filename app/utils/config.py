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

# ========== BACKWARD COMPATIBLE ==========

# ========== SAHAM BERDASARKAN SEKTOR ==========

# Perbankan
BANK_STOCKS = [
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'BRIS.JK', 'BNGA.JK',
    'BTPS.JK', 'BNLI.JK', 'MAYA.JK', 'MEGA.JK', 'NISP.JK', 'NOBU.JK',
    'PNBN.JK', 'BJBR.JK', 'BJTM.JK', 'BMAS.JK', 'BTPN.JK', 'BBTN.JK',
    'AGRO.JK', 'ARTO.JK', 'INPC.JK',
    # --- tambahan saham IDX lainnya ---
    'BDMN.JK', 'BINA.JK', 'BSWD.JK', 'BSIM.JK', 'SUPA.JK', 'BBHI.JK',
    'BNII.JK', 'BBSI.JK', 'BBMD.JK', 'BBKP.JK', 'MASB.JK', 'AMAR.JK',
    'BANK.JK', 'SDRA.JK', 'AGRS.JK', 'MCOR.JK', 'BBYB.JK', 'BGTG.JK',
    'BNBA.JK', 'BCIC.JK', 'BACA.JK', 'BEKS.JK', 'BKSW.JK', 'DNAR.JK',
    'PNBS.JK', 'BVIC.JK', 'BABP.JK',
]

# Telekomunikasi & Media
TELCO_STOCKS = [
    'TLKM.JK', 'ISAT.JK', 'EXCL.JK', 'FREN.JK', 'TOWR.JK', 'TBIG.JK',
    'MTEL.JK', 'MORA.JK', 'EMTK.JK', 'SCMA.JK',
    # --- tambahan saham IDX lainnya ---
    'SUPR.JK', 'IBST.JK', 'MSIN.JK', 'WIFI.JK', 'FILM.JK', 'BALI.JK',
    'INET.JK', 'MDIA.JK', 'LINK.JK', 'RANS.JK', 'DOOH.JK', 'CENT.JK',
    'BMTR.JK', 'NETV.JK', 'MNCN.JK', 'VERN.JK', 'BOLA.JK', 'RAAM.JK',
    'GHON.JK', 'IPTV.JK', 'TMPO.JK', 'MSKY.JK', 'DYAN.JK', 'GOLD.JK',
    'TOSK.JK', 'TFAS.JK', 'LPLI.JK', 'KBLV.JK', 'YELO.JK', 'MARI.JK',
    'ABBA.JK', 'JAST.JK', 'TELE.JK', 'KJEN.JK', 'DIGI.JK', 'VIVA.JK',
]

# Energi & Tambang
ENERGY_STOCKS = [
    'ADRO.JK', 'PTBA.JK', 'ITMG.JK', 'BYAN.JK', 'DOID.JK', 'INDY.JK',
    'HRUM.JK', 'ADMR.JK', 'BUMI.JK', 'DEWA.JK', 'ENRG.JK', 'ESSA.JK',
    'AKRA.JK', 'MEDC.JK', 'PGAS.JK', 'MDKA.JK', 'ANTM.JK', 'INCO.JK',
    'TINS.JK', 'BRMS.JK', 'NCKL.JK', 'PBID.JK', 'CITA.JK', 'PTRO.JK',
    # --- tambahan saham IDX lainnya ---
    'AMMN.JK', 'BREN.JK', 'DSSA.JK', 'EMAS.JK', 'UNTR.JK', 'AADI.JK',
    'CUAN.JK', 'GEMS.JK', 'MBMA.JK', 'PGEO.JK', 'ARCI.JK', 'POWR.JK',
    'BSSR.JK', 'MCOL.JK', 'PSAB.JK', 'SGER.JK', 'RAJA.JK', 'SMMT.JK',
    'ABMM.JK', 'RATU.JK', 'RMKE.JK', 'BIPI.JK', 'BIKE.JK', 'ARKO.JK',
    'SURE.JK', 'SMIL.JK', 'ELSA.JK', 'IFSH.JK', 'DAAZ.JK', 'MKAP.JK',
    'DKFT.JK', 'NICL.JK', 'TOBA.JK', 'CBRE.JK', 'IATA.JK', 'KEEN.JK',
    'TEBE.JK', 'MAHA.JK', 'MYOH.JK', 'MBAP.JK', 'DWGL.JK', 'ARII.JK',
    'SUNI.JK', 'SQMI.JK', 'KKGI.JK', 'FUTR.JK', 'OASA.JK', 'MINE.JK',
    'ITMA.JK', 'ZINC.JK', 'INPS.JK', 'SMGA.JK', 'SOTS.JK', 'APEX.JK',
    'UVCR.JK', 'PIPA.JK', 'RIGS.JK', 'KOCI.JK', 'CNKO.JK', 'GTBO.JK',
    'OKAS.JK', 'REAL.JK', 'LAPD.JK', 'CGAS.JK', 'SOLA.JK', 'COAL.JK',
    'ATLA.JK', 'FIRE.JK', 'RUIS.JK', 'OILS.JK', 'OBMD.JK', 'LABA.JK',
    'KOPI.JK', 'RGAS.JK', 'SICO.JK', 'MIRA.JK', 'TGRA.JK', 'MPOW.JK',
    'LMAX.JK', 'HADE.JK', 'FIMP.JK', 'WOWS.JK',
]

# Consumer Goods
CONSUMER_STOCKS = [
    'UNVR.JK', 'ICBP.JK', 'INDF.JK', 'MYOR.JK', 'GGRM.JK', 'HMSP.JK',
    'WIIM.JK', 'DLTA.JK', 'MLBI.JK', 'ULTJ.JK', 'ROTI.JK', 'KEJU.JK',
    'CAMP.JK', 'SKBM.JK', 'ADES.JK', 'CPIN.JK', 'JPFA.JK', 'MAIN.JK',
    'SIDO.JK', 'KAEF.JK', 'KLBF.JK', 'MERK.JK', 'PYFA.JK', 'TSPC.JK',
    # --- tambahan saham IDX lainnya ---
    'CMRY.JK', 'STTP.JK', 'GOOD.JK', 'CLEO.JK', 'YUPI.JK', 'VICI.JK',
    'DMND.JK', 'BEEF.JK', 'NEST.JK', 'KINO.JK', 'AYAM.JK', 'UCID.JK',
    'TRGU.JK', 'CEKA.JK', 'SKLT.JK', 'SIPD.JK', 'STRK.JK', 'CPRO.JK',
    'TCID.JK', 'AISA.JK', 'RANC.JK', 'IBOS.JK', 'CRAB.JK', 'HOKI.JK',
    'COCO.JK', 'FOLK.JK', 'WAPO.JK', 'BEER.JK', 'MRAT.JK', 'ITIC.JK',
    'BOBA.JK', 'NAYZ.JK', 'FOOD.JK', 'RAFI.JK', 'PSDN.JK', 'MBTO.JK',
    'BRRC.JK', 'ALTO.JK',
]

# Property & Real Estate
PROPERTY_STOCKS = [
    'BSDE.JK', 'CTRA.JK', 'PWON.JK', 'SMRA.JK', 'LPKR.JK', 'DMAS.JK',
    'DILD.JK', 'MDLN.JK', 'KIJA.JK', 'RISE.JK', 'TARA.JK', 'SMMA.JK',
    'BSIM.JK', 'DSSA.JK', 'GEMS.JK',
    # --- tambahan saham IDX lainnya ---
    'MPRO.JK', 'MKPI.JK', 'JRPT.JK', 'RLCO.JK', 'PLIN.JK', 'DUTI.JK',
    'INPP.JK', 'BKSL.JK', 'CLAY.JK', 'MTLA.JK', 'CBDK.JK', 'ASLI.JK',
    'APLN.JK', 'ASRI.JK', 'OMRE.JK', 'LPCK.JK', 'RDTX.JK', 'NIRO.JK',
    'UANG.JK', 'ROCK.JK', 'BKDP.JK', 'ADCP.JK', 'KOTA.JK', 'GWSA.JK',
    'BEST.JK', 'ELTY.JK', 'PPRO.JK', 'GMTD.JK', 'BSBK.JK', 'JGLE.JK',
    'CITY.JK', 'URBN.JK', 'ATAP.JK', 'TRIN.JK', 'GTRA.JK', 'SWID.JK',
    'RODA.JK', 'HOPE.JK', 'GPRA.JK', 'DART.JK', 'ZATA.JK', 'VAST.JK',
    'BIPP.JK', 'SATU.JK', 'BBSS.JK', 'NZIA.JK', 'RELF.JK', 'EMDE.JK',
    'IPAC.JK', 'PGLI.JK', 'DADA.JK', 'PUDP.JK', 'PURI.JK', 'DFAM.JK',
    'MTSM.JK', 'RBMS.JK', 'LAND.JK', 'BAPI.JK', 'BCIP.JK', 'BAPA.JK',
    'PLAN.JK', 'NASA.JK', 'KDTN.JK', 'HRME.JK', 'MINA.JK', 'NICE.JK',
    'SMDM.JK', 'MMLP.JK', 'ARTA.JK', 'GRIA.JK',
]

# Infrastruktur & Konstruksi
INFRA_STOCKS = [
    'JSMR.JK', 'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK', 'INTP.JK',
    'SMCB.JK', 'SMGR.JK', 'SSIA.JK', 'TPIA.JK', 'BREN.JK', 'CUAN.JK',
    # --- tambahan saham IDX lainnya ---
    'CDIA.JK', 'CMNP.JK', 'KETR.JK', 'PBSA.JK', 'BUKK.JK', 'ACST.JK',
    'NRCA.JK', 'JKON.JK', 'SKRN.JK', 'BDKR.JK', 'PPRE.JK', 'WSBP.JK',
    'DGIK.JK', 'WTON.JK', 'IDPR.JK', 'DPUM.JK', 'KOKA.JK', 'WEGE.JK',
    'TAMA.JK', 'TRJA.JK', 'HILL.JK', 'GEMA.JK', 'WINR.JK', 'SMKM.JK',
    'KRYA.JK', 'ARKA.JK', 'TOPS.JK', 'TOTL.JK', 'RMKO.JK',
]

# Retail & Distribusi
RETAIL_STOCKS = [
    'AMRT.JK', 'ACES.JK', 'RALS.JK', 'MAPI.JK', 'ERAA.JK', 'LPPF.JK',
    'LPIN.JK', 'MAIN.JK', 'ASSA.JK', 'FAPA.JK',
    # --- tambahan saham IDX lainnya ---
    'MDIY.JK', 'MAPA.JK', 'MIDI.JK', 'HRTA.JK', 'EPMT.JK', 'TGKA.JK',
    'CSAP.JK', 'DEPO.JK', 'ERAL.JK', 'HERO.JK', 'BLUE.JK', 'MPIX.JK',
    'ZONE.JK', 'LIVE.JK', 'MPPA.JK', 'BABY.JK', 'WICO.JK', 'TGUK.JK',
    'SOFA.JK', 'SDPC.JK', 'APII.JK', 'MDRN.JK', 'ECII.JK', 'BATA.JK',
    'UFOE.JK',
]

# Otomotif
AUTOMOTIVE_STOCKS = [
    'ASII.JK', 'AUTO.JK', 'GDYR.JK', 'LPIN.JK', 'SMSM.JK', 'GJTL.JK',
    # --- tambahan saham IDX lainnya ---
    'VKTR.JK', 'MPMX.JK', 'DRMA.JK', 'BRAM.JK', 'BOLT.JK', 'IMAS.JK',
    'INDS.JK', 'CARS.JK', 'PMJS.JK', 'ASLC.JK', 'TYRE.JK', 'KOBX.JK',
    'INTA.JK', 'AEGS.JK', 'HEXA.JK',
]

# Healthcare
HEALTHCARE_STOCKS = [
    'SILO.JK', 'MIKA.JK', 'HEAL.JK', 'KAEF.JK', 'KLBF.JK', 'MERK.JK',
    'PYFA.JK', 'TSPC.JK', 'SIDO.JK',
    # --- tambahan saham IDX lainnya ---
    'SRAJ.JK', 'SOHO.JK', 'CARE.JK', 'PRAY.JK', 'OMED.JK', 'JECX.JK',
    'SAME.JK', 'MMIX.JK', 'PRDA.JK', 'MDLA.JK', 'RSCH.JK', 'BMHS.JK',
    'DVLA.JK', 'RSGK.JK', 'IRRA.JK', 'LABS.JK', 'HYGN.JK', 'CHEK.JK',
    'PRIM.JK', 'DGNS.JK', 'INAF.JK', 'DKHH.JK', 'PEHA.JK', 'IKPM.JK',
    'OBAT.JK', 'PRDL.JK', 'MEDS.JK', 'KKES.JK', 'EMMI.JK',
]

# Teknologi & Digital
TECH_STOCKS = [
    'DIVA.JK', 'BELI.JK', 'BUKA.JK', 'GOTO.JK', 'DNET.JK', 'PANI.JK',
    # --- tambahan saham IDX lainnya ---
    'DCII.JK', 'MLPT.JK', 'MGLV.JK', 'EDGE.JK', 'MTDL.JK', 'BOGA.JK',
    'CYBR.JK', 'MSTI.JK', 'ASGR.JK', 'NFCX.JK', 'DATA.JK', 'MFMI.JK',
    'DMMX.JK', 'ATIC.JK', 'KSIX.JK', 'AREA.JK', 'ASPI.JK', 'SEMA.JK',
    'WIRG.JK', 'CASH.JK', 'AWAN.JK', 'GLVA.JK', 'ELIT.JK', 'CHIP.JK',
    'JATI.JK', 'VTNY.JK', 'DOSS.JK', 'IOTF.JK', 'TRON.JK', 'MCAS.JK',
    'GLOB.JK', 'NINE.JK', 'ZYRX.JK', 'GPSO.JK', 'NANO.JK', 'KLIN.JK',
    'MENN.JK', 'KIOS.JK', 'LUCK.JK', 'RUNS.JK', 'HDIT.JK',
]

# Keuangan Non-Bank (multifinance, asuransi, sekuritas)
FINANCE_STOCKS = [
    'SMMA.JK', 'CASA.JK', 'LIFE.JK', 'BFIN.JK', 'ADMF.JK', 'BHAT.JK',
    'COIN.JK', 'YULE.JK', 'PNLF.JK', 'TUGU.JK', 'TRIM.JK', 'BPII.JK',
    'APIC.JK', 'ABDA.JK', 'SFAN.JK', 'AMAG.JK', 'NICK.JK', 'IMJS.JK',
    'GSMF.JK', 'PANS.JK', 'BBLD.JK', 'TIFA.JK', 'BCAP.JK', 'WOMF.JK',
    'RELI.JK', 'CFIN.JK', 'AMOR.JK', 'MTWI.JK', 'BPFI.JK', 'INDO.JK',
    'HDFA.JK', 'MGNA.JK', 'MREI.JK', 'PADI.JK', 'VRNA.JK', 'PEGE.JK',
    'MTFN.JK', 'POLA.JK', 'FUJI.JK', 'ASRM.JK', 'TRUS.JK', 'YOII.JK',
    'AHAP.JK', 'ASMI.JK', 'JMAS.JK', 'ASJT.JK', 'HALO.JK', 'AIMS.JK',
    'DEFI.JK', 'ASBI.JK', 'ASDM.JK', 'VINS.JK', 'LPGI.JK', 'PNIN.JK',
]

# Industri Dasar & Kimia (semen, baja, kertas, kimia, plastik)
BASIC_INDUSTRY_STOCKS = [
    'BRPT.JK', 'TPIA.JK', 'INKP.JK', 'AVIA.JK', 'IMPC.JK', 'TKIM.JK',
    'INTP.JK', 'FASW.JK', 'CMNT.JK', 'PACK.JK', 'AGII.JK', 'UNIC.JK',
    'ALDO.JK', 'MSJA.JK', 'JTPE.JK', 'PBID.JK', 'KRAS.JK', 'ARNA.JK',
    'ALKA.JK', 'ISSP.JK', 'TOTO.JK', 'FPNI.JK', 'CTBN.JK', 'IFII.JK',
    'BLES.JK', 'MLIA.JK', 'TRST.JK', 'AMFG.JK', 'SMBR.JK', 'LTLS.JK',
    'EKAD.JK', 'PDPP.JK', 'BUDI.JK', 'MOLI.JK', 'INRU.JK', 'GDST.JK',
    'TBMS.JK', 'SRSN.JK', 'IPOL.JK', 'YPAS.JK', 'PEVE.JK', 'BRNA.JK',
    'MDKI.JK', 'CLPI.JK', 'SMKL.JK', 'SULI.JK', 'KMDS.JK', 'NIKL.JK',
    'APLI.JK', 'SCNP.JK', 'JELI.JK', 'AKPI.JK', 'BAJA.JK', 'BMSR.JK',
    'KIAS.JK', 'ALMI.JK', 'IKAI.JK', 'INOV.JK', 'BTON.JK', 'BEBS.JK',
    'BINO.JK', 'CAKK.JK', 'INCI.JK', 'FWCT.JK', 'EPAC.JK', 'SBMA.JK',
    'PTMP.JK', 'PPRI.JK', 'FLMC.JK', 'CTTH.JK', 'DPNS.JK', 'ESIP.JK',
    'CHEM.JK', 'INAI.JK', 'PICO.JK', 'OPMS.JK', 'KICI.JK', 'IPPE.JK',
    'SWAT.JK', 'GGRP.JK',
]

# Perkebunan & Agribisnis
AGRI_STOCKS = [
    'PGUN.JK', 'TAPG.JK', 'FAPA.JK', 'JARR.JK', 'SMAR.JK', 'AALI.JK',
    'NSSS.JK', 'DSNG.JK', 'STAA.JK', 'LSIP.JK', 'SSMS.JK', 'SIMP.JK',
    'SGRO.JK', 'TLDN.JK', 'UNSP.JK', 'ANJT.JK', 'MGRO.JK', 'CBUT.JK',
    'FISH.JK', 'PNGO.JK', 'TBLA.JK', 'SAMF.JK', 'BWPT.JK', 'KMTR.JK',
    'BISI.JK', 'JAWA.JK', 'CSRA.JK', 'AGAR.JK', 'BUAH.JK', 'GULA.JK',
    'WMPP.JK', 'GZCO.JK', 'AMAN.JK', 'UDNG.JK', 'BTEK.JK', 'TIRT.JK',
    'WMUU.JK', 'SURI.JK', 'DEWI.JK', 'PSGO.JK', 'PALM.JK', 'MKTR.JK',
    'UNIQ.JK', 'ANDI.JK', 'DSFI.JK', 'NASI.JK', 'ISEA.JK', 'AMMS.JK',
    'ASHA.JK', 'IKAN.JK', 'PTPS.JK',
]

# Transportasi & Logistik
TRANSPORT_STOCKS = [
    'GIAA.JK', 'TCPI.JK', 'SHIP.JK', 'TMAS.JK', 'SMDR.JK', 'MBSS.JK',
    'GMFI.JK', 'HATM.JK', 'WBSA.JK', 'BULL.JK', 'CASS.JK', 'BIRD.JK',
    'ELPI.JK', 'SOCI.JK', 'BESS.JK', 'PORT.JK', 'WINS.JK', 'ASSA.JK',
    'HUMI.JK', 'IPCC.JK', 'PSSI.JK', 'GTSI.JK', 'TRUK.JK', 'IPCM.JK',
    'TPMA.JK', 'BLOG.JK', 'PSAT.JK', 'BSML.JK', 'TAMU.JK', 'HITS.JK',
    'BLTA.JK', 'CMPP.JK', 'PGJO.JK', 'MPXL.JK', 'SAFE.JK', 'GUNA.JK',
    'LEAD.JK', 'PPGL.JK', 'HAIS.JK', 'NELY.JK', 'BOAT.JK', 'SAPX.JK',
    'PJHB.JK', 'BPTR.JK', 'AKSI.JK', 'HELI.JK', 'WEHA.JK', 'TAXI.JK',
    'PMMP.JK', 'KARW.JK', 'CANI.JK', 'PTIS.JK', 'LAJU.JK', 'JAYA.JK',
    'LRNA.JK', 'LOPI.JK', 'KLAS.JK', 'ALII.JK',
]

# Pariwisata, Hotel & Restoran
HOSPITALITY_STOCKS = [
    'BUVA.JK', 'FORE.JK', 'CNMA.JK', 'BLTZ.JK', 'KPIG.JK', 'JSPT.JK',
    'DAYA.JK', 'MAPB.JK', 'PSKT.JK', 'SONA.JK', 'POLI.JK', 'GOLF.JK',
    'FAST.JK', 'SHID.JK', 'JIHD.JK', 'PJAA.JK', 'PTSP.JK', 'PZZA.JK',
    'PANR.JK', 'PNSE.JK', 'BAYU.JK', 'CSMI.JK', 'ENAK.JK', 'EAST.JK',
    'WINE.JK', 'HOMI.JK', 'MICE.JK', 'HAJJ.JK', 'PDES.JK', 'LUCY.JK',
    'SNLK.JK', 'ICON.JK',
]

# Manufaktur & Industri Lain (tekstil, kabel, elektronik)
MANUFACTURING_STOCKS = [
    'TFCO.JK', 'POLU.JK', 'ARGO.JK', 'EURO.JK', 'SPTO.JK', 'PTSN.JK',
    'FMII.JK', 'WOOD.JK', 'PTPW.JK', 'VOKS.JK', 'KING.JK', 'KDSI.JK',
    'PTMR.JK', 'IKBI.JK', 'BELL.JK', 'PBRX.JK', 'JECC.JK', 'TRIS.JK',
    'IGAR.JK', 'SSTM.JK', 'ASPR.JK', 'KBLM.JK', 'CCSI.JK', 'BATR.JK',
    'AMIN.JK', 'ESTI.JK', 'NAIK.JK', 'ERTX.JK', 'CINT.JK', 'ACRO.JK',
    'TIRA.JK', 'INTD.JK', 'SLIS.JK', 'LMPI.JK', 'LION.JK', 'ZBRA.JK',
    'TOOL.JK', 'POLY.JK', 'RICY.JK', 'LMSH.JK', 'SCCO.JK', 'KBLI.JK',
    'INDR.JK', 'MARK.JK', 'MYTX.JK',
]

# Holding, Jasa & Lainnya
OTHER_STOCKS = [
    'AKKU.JK', 'AYLS.JK', 'BACH.JK', 'BAIK.JK', 'BAUT.JK', 'BHIT.JK',
    'BIMA.JK', 'BMBL.JK', 'BNBR.JK', 'CBPE.JK', 'CRSN.JK', 'CSIS.JK',
    'DGWG.JK', 'ENZO.JK', 'ESTA.JK', 'FITT.JK', 'FORU.JK', 'GRPH.JK',
    'GRPM.JK', 'HBAT.JK', 'HGII.JK', 'IBFN.JK', 'IDEA.JK', 'INCF.JK',
    'INDX.JK', 'IRSX.JK', 'ISAP.JK', 'KAQI.JK', 'KBAG.JK', 'KOIN.JK',
    'KONI.JK', 'KREN.JK', 'KUAS.JK', 'LCKM.JK', 'LPPS.JK', 'MANG.JK',
    'MAXI.JK', 'MEJA.JK', 'MERI.JK', 'MHKI.JK', 'MITI.JK', 'MKNT.JK',
    'MLPL.JK', 'MSIE.JK', 'MTMH.JK', 'MTPS.JK', 'MUTU.JK', 'NATO.JK',
    'NPGF.JK', 'NTBK.JK', 'OLIV.JK', 'PADA.JK', 'PAMG.JK', 'PART.JK',
    'PCAR.JK', 'PKPK.JK', 'PMUI.JK', 'PTDU.JK', 'PURA.JK', 'RCCC.JK',
    'RONY.JK', 'SAGE.JK', 'SDMU.JK', 'SINI.JK', 'SMLE.JK', 'SOSS.JK',
    'SOUL.JK', 'SPRE.JK', 'SRTG.JK', 'STAR.JK', 'TAYS.JK', 'TNCA.JK',
    'TRUE.JK', 'UNTD.JK', 'VICO.JK', 'VISI.JK', 'WGSH.JK', 'WIDI.JK',
    'TECH.JK',
]

# ========== PETA SEKTOR (dipakai dropdown filter sektor) ==========
SECTOR_STOCKS = {
    'Perbankan': BANK_STOCKS,
    'Telekomunikasi & Media': TELCO_STOCKS,
    'Energi & Tambang': ENERGY_STOCKS,
    'Consumer Goods': CONSUMER_STOCKS,
    'Property & Real Estate': PROPERTY_STOCKS,
    'Infrastruktur & Konstruksi': INFRA_STOCKS,
    'Retail & Distribusi': RETAIL_STOCKS,
    'Otomotif': AUTOMOTIVE_STOCKS,
    'Healthcare': HEALTHCARE_STOCKS,
    'Teknologi & Digital': TECH_STOCKS,
    'Keuangan Non-Bank': FINANCE_STOCKS,
    'Industri Dasar & Kimia': BASIC_INDUSTRY_STOCKS,
    'Perkebunan & Agribisnis': AGRI_STOCKS,
    'Transportasi & Logistik': TRANSPORT_STOCKS,
    'Pariwisata, Hotel & Restoran': HOSPITALITY_STOCKS,
    'Manufaktur & Industri Lain': MANUFACTURING_STOCKS,
    'Holding, Jasa & Lainnya': OTHER_STOCKS,
}

# === SELURUH SAHAM IDX (905 kode, per 2 Nov 2026) ===
ALL_IDX_STOCKS = [
    'AADI.JK', 'AALI.JK', 'ABBA.JK', 'ABDA.JK', 'ABMM.JK', 'ACES.JK', 'ACRO.JK', 'ACST.JK', 'ADCP.JK', 'ADES.JK',
    'ADHI.JK', 'ADMF.JK', 'ADMR.JK', 'ADRO.JK', 'AEGS.JK', 'AGAR.JK', 'AGII.JK', 'AGRO.JK', 'AGRS.JK', 'AHAP.JK',
    'AIMS.JK', 'AISA.JK', 'AKKU.JK', 'AKPI.JK', 'AKRA.JK', 'AKSI.JK', 'ALDO.JK', 'ALII.JK', 'ALKA.JK', 'ALMI.JK',
    'ALTO.JK', 'AMAG.JK', 'AMAN.JK', 'AMAR.JK', 'AMFG.JK', 'AMIN.JK', 'AMMN.JK', 'AMMS.JK', 'AMOR.JK', 'AMRT.JK',
    'ANDI.JK', 'ANJT.JK', 'ANTM.JK', 'APEX.JK', 'APIC.JK', 'APII.JK', 'APLI.JK', 'APLN.JK', 'ARCI.JK', 'AREA.JK',
    'ARGO.JK', 'ARII.JK', 'ARKA.JK', 'ARKO.JK', 'ARNA.JK', 'ARTA.JK', 'ARTO.JK', 'ASBI.JK', 'ASDM.JK', 'ASGR.JK',
    'ASHA.JK', 'ASII.JK', 'ASJT.JK', 'ASLC.JK', 'ASLI.JK', 'ASMI.JK', 'ASPI.JK', 'ASPR.JK', 'ASRI.JK', 'ASRM.JK',
    'ASSA.JK', 'ATAP.JK', 'ATIC.JK', 'ATLA.JK', 'AUTO.JK', 'AVIA.JK', 'AWAN.JK', 'AYAM.JK', 'AYLS.JK', 'BABP.JK',
    'BABY.JK', 'BACA.JK', 'BACH.JK', 'BAIK.JK', 'BAJA.JK', 'BALI.JK', 'BANK.JK', 'BAPA.JK', 'BAPI.JK', 'BATA.JK',
    'BATR.JK', 'BAUT.JK', 'BAYU.JK', 'BBCA.JK', 'BBHI.JK', 'BBKP.JK', 'BBLD.JK', 'BBMD.JK', 'BBNI.JK', 'BBRI.JK',
    'BBSI.JK', 'BBSS.JK', 'BBTN.JK', 'BBYB.JK', 'BCAP.JK', 'BCIC.JK', 'BCIP.JK', 'BDKR.JK', 'BDMN.JK', 'BEBS.JK',
    'BEEF.JK', 'BEER.JK', 'BEKS.JK', 'BELI.JK', 'BELL.JK', 'BESS.JK', 'BEST.JK', 'BFIN.JK', 'BGTG.JK', 'BHAT.JK',
    'BHIT.JK', 'BIKE.JK', 'BIMA.JK', 'BINA.JK', 'BINO.JK', 'BIPI.JK', 'BIPP.JK', 'BIRD.JK', 'BISI.JK', 'BJBR.JK',
    'BJTM.JK', 'BKDP.JK', 'BKSL.JK', 'BKSW.JK', 'BLES.JK', 'BLOG.JK', 'BLTA.JK', 'BLTZ.JK', 'BLUE.JK', 'BMAS.JK',
    'BMBL.JK', 'BMHS.JK', 'BMRI.JK', 'BMSR.JK', 'BMTR.JK', 'BNBA.JK', 'BNBR.JK', 'BNGA.JK', 'BNII.JK', 'BNLI.JK',
    'BOAT.JK', 'BOBA.JK', 'BOGA.JK', 'BOLA.JK', 'BOLT.JK', 'BPFI.JK', 'BPII.JK', 'BPTR.JK', 'BRAM.JK', 'BREN.JK',
    'BRIS.JK', 'BRMS.JK', 'BRNA.JK', 'BRPT.JK', 'BRRC.JK', 'BSBK.JK', 'BSDE.JK', 'BSIM.JK', 'BSML.JK', 'BSSR.JK',
    'BSWD.JK', 'BTEK.JK', 'BTON.JK', 'BTPN.JK', 'BTPS.JK', 'BUAH.JK', 'BUDI.JK', 'BUKA.JK', 'BUKK.JK', 'BULL.JK',
    'BUMI.JK', 'BUVA.JK', 'BVIC.JK', 'BWPT.JK', 'BYAN.JK', 'CAKK.JK', 'CAMP.JK', 'CANI.JK', 'CARE.JK', 'CARS.JK',
    'CASA.JK', 'CASH.JK', 'CASS.JK', 'CBDK.JK', 'CBPE.JK', 'CBRE.JK', 'CBUT.JK', 'CCSI.JK', 'CDIA.JK', 'CEKA.JK',
    'CENT.JK', 'CFIN.JK', 'CGAS.JK', 'CHEK.JK', 'CHEM.JK', 'CHIP.JK', 'CINT.JK', 'CITA.JK', 'CITY.JK', 'CLAY.JK',
    'CLEO.JK', 'CLPI.JK', 'CMNP.JK', 'CMNT.JK', 'CMPP.JK', 'CMRY.JK', 'CNKO.JK', 'CNMA.JK', 'COAL.JK', 'COCO.JK',
    'COIN.JK', 'CPIN.JK', 'CPRO.JK', 'CRAB.JK', 'CRSN.JK', 'CSAP.JK', 'CSIS.JK', 'CSMI.JK', 'CSRA.JK', 'CTBN.JK',
    'CTRA.JK', 'CTTH.JK', 'CUAN.JK', 'CYBR.JK', 'DAAZ.JK', 'DADA.JK', 'DART.JK', 'DATA.JK', 'DAYA.JK', 'DCII.JK',
    'DEFI.JK', 'DEPO.JK', 'DEWA.JK', 'DEWI.JK', 'DFAM.JK', 'DGIK.JK', 'DGNS.JK', 'DGWG.JK', 'DIGI.JK', 'DILD.JK',
    'DIVA.JK', 'DKFT.JK', 'DKHH.JK', 'DLTA.JK', 'DMAS.JK', 'DMMX.JK', 'DMND.JK', 'DNAR.JK', 'DNET.JK', 'DOID.JK',
    'DOOH.JK', 'DOSS.JK', 'DPNS.JK', 'DPUM.JK', 'DRMA.JK', 'DSFI.JK', 'DSNG.JK', 'DSSA.JK', 'DUTI.JK', 'DVLA.JK',
    'DWGL.JK', 'DYAN.JK', 'EAST.JK', 'ECII.JK', 'EDGE.JK', 'EKAD.JK', 'ELIT.JK', 'ELPI.JK', 'ELSA.JK', 'ELTY.JK',
    'EMAS.JK', 'EMDE.JK', 'EMMI.JK', 'EMTK.JK', 'ENAK.JK', 'ENRG.JK', 'ENZO.JK', 'EPAC.JK', 'EPMT.JK', 'ERAA.JK',
    'ERAL.JK', 'ERTX.JK', 'ESIP.JK', 'ESSA.JK', 'ESTA.JK', 'ESTI.JK', 'EURO.JK', 'EXCL.JK', 'FAPA.JK', 'FAST.JK',
    'FASW.JK', 'FILM.JK', 'FIMP.JK', 'FIRE.JK', 'FISH.JK', 'FITT.JK', 'FLMC.JK', 'FMII.JK', 'FOLK.JK', 'FOOD.JK',
    'FORE.JK', 'FORU.JK', 'FPNI.JK', 'FUJI.JK', 'FUTR.JK', 'FWCT.JK', 'GDST.JK', 'GDYR.JK', 'GEMA.JK', 'GEMS.JK',
    'GGRM.JK', 'GGRP.JK', 'GHON.JK', 'GIAA.JK', 'GJTL.JK', 'GLOB.JK', 'GLVA.JK', 'GMFI.JK', 'GMTD.JK', 'GOLD.JK',
    'GOLF.JK', 'GOOD.JK', 'GOTO.JK', 'GPRA.JK', 'GPSO.JK', 'GRIA.JK', 'GRPH.JK', 'GRPM.JK', 'GSMF.JK', 'GTBO.JK',
    'GTRA.JK', 'GTSI.JK', 'GULA.JK', 'GUNA.JK', 'GWSA.JK', 'GZCO.JK', 'HADE.JK', 'HAIS.JK', 'HAJJ.JK', 'HALO.JK',
    'HATM.JK', 'HBAT.JK', 'HDFA.JK', 'HDIT.JK', 'HEAL.JK', 'HELI.JK', 'HERO.JK', 'HEXA.JK', 'HGII.JK', 'HILL.JK',
    'HITS.JK', 'HMSP.JK', 'HOKI.JK', 'HOMI.JK', 'HOPE.JK', 'HRME.JK', 'HRTA.JK', 'HRUM.JK', 'HUMI.JK', 'HYGN.JK',
    'IATA.JK', 'IBFN.JK', 'IBOS.JK', 'IBST.JK', 'ICBP.JK', 'ICON.JK', 'IDEA.JK', 'IDPR.JK', 'IFII.JK', 'IFSH.JK',
    'IGAR.JK', 'IKAI.JK', 'IKAN.JK', 'IKBI.JK', 'IKPM.JK', 'IMAS.JK', 'IMJS.JK', 'IMPC.JK', 'INAF.JK', 'INAI.JK',
    'INCF.JK', 'INCI.JK', 'INCO.JK', 'INDF.JK', 'INDO.JK', 'INDR.JK', 'INDS.JK', 'INDX.JK', 'INDY.JK', 'INET.JK',
    'INKP.JK', 'INOV.JK', 'INPC.JK', 'INPP.JK', 'INPS.JK', 'INRU.JK', 'INTA.JK', 'INTD.JK', 'INTP.JK', 'IOTF.JK',
    'IPAC.JK', 'IPCC.JK', 'IPCM.JK', 'IPOL.JK', 'IPPE.JK', 'IPTV.JK', 'IRRA.JK', 'IRSX.JK', 'ISAP.JK', 'ISAT.JK',
    'ISEA.JK', 'ISSP.JK', 'ITIC.JK', 'ITMA.JK', 'ITMG.JK', 'JARR.JK', 'JAST.JK', 'JATI.JK', 'JAWA.JK', 'JAYA.JK',
    'JECC.JK', 'JECX.JK', 'JELI.JK', 'JGLE.JK', 'JIHD.JK', 'JKON.JK', 'JMAS.JK', 'JPFA.JK', 'JRPT.JK', 'JSMR.JK',
    'JSPT.JK', 'JTPE.JK', 'KAEF.JK', 'KAQI.JK', 'KARW.JK', 'KBAG.JK', 'KBLI.JK', 'KBLM.JK', 'KBLV.JK', 'KDSI.JK',
    'KDTN.JK', 'KEEN.JK', 'KEJU.JK', 'KETR.JK', 'KIAS.JK', 'KICI.JK', 'KIJA.JK', 'KING.JK', 'KINO.JK', 'KIOS.JK',
    'KJEN.JK', 'KKES.JK', 'KKGI.JK', 'KLAS.JK', 'KLBF.JK', 'KLIN.JK', 'KMDS.JK', 'KMTR.JK', 'KOBX.JK', 'KOCI.JK',
    'KOIN.JK', 'KOKA.JK', 'KONI.JK', 'KOPI.JK', 'KOTA.JK', 'KPIG.JK', 'KRAS.JK', 'KREN.JK', 'KRYA.JK', 'KSIX.JK',
    'KUAS.JK', 'LABA.JK', 'LABS.JK', 'LAJU.JK', 'LAND.JK', 'LAPD.JK', 'LCKM.JK', 'LEAD.JK', 'LIFE.JK', 'LINK.JK',
    'LION.JK', 'LIVE.JK', 'LMAX.JK', 'LMPI.JK', 'LMSH.JK', 'LOPI.JK', 'LPCK.JK', 'LPGI.JK', 'LPIN.JK', 'LPKR.JK',
    'LPLI.JK', 'LPPF.JK', 'LPPS.JK', 'LRNA.JK', 'LSIP.JK', 'LTLS.JK', 'LUCK.JK', 'LUCY.JK', 'MAHA.JK', 'MAIN.JK',
    'MANG.JK', 'MAPA.JK', 'MAPB.JK', 'MAPI.JK', 'MARI.JK', 'MARK.JK', 'MASB.JK', 'MAXI.JK', 'MAYA.JK', 'MBAP.JK',
    'MBMA.JK', 'MBSS.JK', 'MBTO.JK', 'MCAS.JK', 'MCOL.JK', 'MCOR.JK', 'MDIA.JK', 'MDIY.JK', 'MDKA.JK', 'MDKI.JK',
    'MDLA.JK', 'MDLN.JK', 'MDRN.JK', 'MEDC.JK', 'MEDS.JK', 'MEGA.JK', 'MEJA.JK', 'MENN.JK', 'MERI.JK', 'MERK.JK',
    'MFMI.JK', 'MGLV.JK', 'MGNA.JK', 'MGRO.JK', 'MHKI.JK', 'MICE.JK', 'MIDI.JK', 'MIKA.JK', 'MINA.JK', 'MINE.JK',
    'MIRA.JK', 'MITI.JK', 'MKAP.JK', 'MKNT.JK', 'MKPI.JK', 'MKTR.JK', 'MLBI.JK', 'MLIA.JK', 'MLPL.JK', 'MLPT.JK',
    'MMIX.JK', 'MMLP.JK', 'MNCN.JK', 'MOLI.JK', 'MORA.JK', 'MPIX.JK', 'MPMX.JK', 'MPOW.JK', 'MPPA.JK', 'MPRO.JK',
    'MPXL.JK', 'MRAT.JK', 'MREI.JK', 'MSIE.JK', 'MSIN.JK', 'MSJA.JK', 'MSKY.JK', 'MSTI.JK', 'MTDL.JK', 'MTEL.JK',
    'MTFN.JK', 'MTLA.JK', 'MTMH.JK', 'MTPS.JK', 'MTSM.JK', 'MTWI.JK', 'MUTU.JK', 'MYOH.JK', 'MYOR.JK', 'MYTX.JK',
    'NAIK.JK', 'NANO.JK', 'NASA.JK', 'NASI.JK', 'NATO.JK', 'NAYZ.JK', 'NCKL.JK', 'NELY.JK', 'NEST.JK', 'NETV.JK',
    'NFCX.JK', 'NICE.JK', 'NICK.JK', 'NICL.JK', 'NIKL.JK', 'NINE.JK', 'NIRO.JK', 'NISP.JK', 'NOBU.JK', 'NPGF.JK',
    'NRCA.JK', 'NSSS.JK', 'NTBK.JK', 'NZIA.JK', 'OASA.JK', 'OBAT.JK', 'OBMD.JK', 'OILS.JK', 'OKAS.JK', 'OLIV.JK',
    'OMED.JK', 'OMRE.JK', 'OPMS.JK', 'PACK.JK', 'PADA.JK', 'PADI.JK', 'PALM.JK', 'PAMG.JK', 'PANI.JK', 'PANR.JK',
    'PANS.JK', 'PART.JK', 'PBID.JK', 'PBRX.JK', 'PBSA.JK', 'PCAR.JK', 'PDES.JK', 'PDPP.JK', 'PEGE.JK', 'PEHA.JK',
    'PEVE.JK', 'PGAS.JK', 'PGEO.JK', 'PGJO.JK', 'PGLI.JK', 'PGUN.JK', 'PICO.JK', 'PIPA.JK', 'PJAA.JK', 'PJHB.JK',
    'PKPK.JK', 'PLAN.JK', 'PLIN.JK', 'PMJS.JK', 'PMMP.JK', 'PMUI.JK', 'PNBN.JK', 'PNBS.JK', 'PNGO.JK', 'PNIN.JK',
    'PNLF.JK', 'PNSE.JK', 'POLA.JK', 'POLI.JK', 'POLU.JK', 'POLY.JK', 'PORT.JK', 'POWR.JK', 'PPGL.JK', 'PPRE.JK',
    'PPRI.JK', 'PPRO.JK', 'PRAY.JK', 'PRDA.JK', 'PRDL.JK', 'PRIM.JK', 'PSAB.JK', 'PSAT.JK', 'PSDN.JK', 'PSGO.JK',
    'PSKT.JK', 'PSSI.JK', 'PTBA.JK', 'PTDU.JK', 'PTIS.JK', 'PTMP.JK', 'PTMR.JK', 'PTPP.JK', 'PTPS.JK', 'PTPW.JK',
    'PTRO.JK', 'PTSN.JK', 'PTSP.JK', 'PUDP.JK', 'PURA.JK', 'PURI.JK', 'PWON.JK', 'PYFA.JK', 'PZZA.JK', 'RAAM.JK',
    'RAFI.JK', 'RAJA.JK', 'RALS.JK', 'RANC.JK', 'RANS.JK', 'RATU.JK', 'RBMS.JK', 'RCCC.JK', 'RDTX.JK', 'REAL.JK',
    'RELF.JK', 'RELI.JK', 'RGAS.JK', 'RICY.JK', 'RIGS.JK', 'RISE.JK', 'RLCO.JK', 'RMKE.JK', 'RMKO.JK', 'ROCK.JK',
    'RODA.JK', 'RONY.JK', 'ROTI.JK', 'RSCH.JK', 'RSGK.JK', 'RUIS.JK', 'RUNS.JK', 'SAFE.JK', 'SAGE.JK', 'SAME.JK',
    'SAMF.JK', 'SAPX.JK', 'SATU.JK', 'SBMA.JK', 'SCCO.JK', 'SCMA.JK', 'SCNP.JK', 'SDMU.JK', 'SDPC.JK', 'SDRA.JK',
    'SEMA.JK', 'SFAN.JK', 'SGER.JK', 'SGRO.JK', 'SHID.JK', 'SHIP.JK', 'SICO.JK', 'SIDO.JK', 'SILO.JK', 'SIMP.JK',
    'SINI.JK', 'SIPD.JK', 'SKLT.JK', 'SKRN.JK', 'SLIS.JK', 'SMAR.JK', 'SMBR.JK', 'SMCB.JK', 'SMDM.JK', 'SMDR.JK',
    'SMGA.JK', 'SMGR.JK', 'SMIL.JK', 'SMKL.JK', 'SMKM.JK', 'SMLE.JK', 'SMMA.JK', 'SMMT.JK', 'SMRA.JK', 'SMSM.JK',
    'SNLK.JK', 'SOCI.JK', 'SOFA.JK', 'SOHO.JK', 'SOLA.JK', 'SONA.JK', 'SOSS.JK', 'SOTS.JK', 'SOUL.JK', 'SPRE.JK',
    'SPTO.JK', 'SQMI.JK', 'SRAJ.JK', 'SRSN.JK', 'SRTG.JK', 'SSIA.JK', 'SSMS.JK', 'SSTM.JK', 'STAA.JK', 'STAR.JK',
    'STRK.JK', 'STTP.JK', 'SULI.JK', 'SUNI.JK', 'SUPA.JK', 'SUPR.JK', 'SURE.JK', 'SURI.JK', 'SWAT.JK', 'SWID.JK',
    'TAMA.JK', 'TAMU.JK', 'TAPG.JK', 'TARA.JK', 'TAXI.JK', 'TAYS.JK', 'TBIG.JK', 'TBLA.JK', 'TBMS.JK', 'TCID.JK',
    'TCPI.JK', 'TEBE.JK', 'TELE.JK', 'TFAS.JK', 'TFCO.JK', 'TGKA.JK', 'TGRA.JK', 'TGUK.JK', 'TIFA.JK', 'TINS.JK',
    'TIRA.JK', 'TIRT.JK', 'TKIM.JK', 'TLDN.JK', 'TLKM.JK', 'TMAS.JK', 'TMPO.JK', 'TNCA.JK', 'TOBA.JK', 'TOOL.JK',
    'TOPS.JK', 'TOSK.JK', 'TOTL.JK', 'TOTO.JK', 'TOWR.JK', 'TPIA.JK', 'TPMA.JK', 'TRGU.JK', 'TRIM.JK', 'TRIN.JK',
    'TRIS.JK', 'TRJA.JK', 'TRON.JK', 'TRST.JK', 'TRUE.JK', 'TRUK.JK', 'TRUS.JK', 'TSPC.JK', 'TUGU.JK', 'TYRE.JK',
    'UANG.JK', 'UCID.JK', 'UDNG.JK', 'UFOE.JK', 'ULTJ.JK', 'UNIC.JK', 'UNIQ.JK', 'UNSP.JK', 'UNTD.JK', 'UNTR.JK',
    'UNVR.JK', 'URBN.JK', 'UVCR.JK', 'VAST.JK', 'VERN.JK', 'VICI.JK', 'VICO.JK', 'VINS.JK', 'VISI.JK', 'VIVA.JK',
    'VKTR.JK', 'VOKS.JK', 'VRNA.JK', 'VTNY.JK', 'WAPO.JK', 'WBSA.JK', 'WEGE.JK', 'WEHA.JK', 'WGSH.JK', 'WICO.JK',
    'WIDI.JK', 'WIFI.JK', 'WIIM.JK', 'WIKA.JK', 'WINE.JK', 'WINR.JK', 'WINS.JK', 'WIRG.JK', 'WMPP.JK', 'WMUU.JK',
    'WOMF.JK', 'WOOD.JK', 'WOWS.JK', 'WSBP.JK', 'WTON.JK', 'YELO.JK', 'YOII.JK', 'YPAS.JK', 'YULE.JK', 'YUPI.JK',
    'ZATA.JK', 'ZBRA.JK', 'ZINC.JK', 'ZONE.JK', 'ZYRX.JK',
]

# === GABUNGAN SEMUA SAHAM (unik, urutan kapitalisasi dipertahankan) ===
ALL_STOCKS = list(dict.fromkeys(
    LARGE_CAP_STOCKS + MID_CAP_STOCKS + SMALL_CAP_STOCKS + MICRO_CAP_STOCKS + ALL_IDX_STOCKS
    + BANK_STOCKS + TELCO_STOCKS + ENERGY_STOCKS + CONSUMER_STOCKS
    + PROPERTY_STOCKS + INFRA_STOCKS + RETAIL_STOCKS + AUTOMOTIVE_STOCKS
    + HEALTHCARE_STOCKS + TECH_STOCKS
))
STOCKS = ALL_STOCKS  # Untuk file lama yang masih panggil STOCKS

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
