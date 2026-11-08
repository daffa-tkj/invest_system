# app/ui/styles.py
# Prinsip: tidak memaksa warna latar/teks. Permukaan memakai rgba netral dan teks 'inherit',
# jadi tampilan otomatis ikut tema Streamlit (gelap/terang). Warna sinyal dipilih agar terbaca di keduanya.
CSS_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
:root{
  --ok:#12a36b; --bad:#e5484d; --warn:#d99a0b;
  --line:rgba(127,127,127,.28); --surface:rgba(127,127,127,.07); --muted:rgba(127,127,127,.95);
}
html, body, .stApp, button, input, textarea { font-family:'IBM Plex Sans', system-ui, sans-serif; }
.block-container{ padding-top:1.4rem; padding-bottom:3rem; max-width:1180px; }
header[data-testid="stHeader"]{ background:transparent; }

/* Judul */
.brand{ display:flex; align-items:baseline; gap:.6rem; flex-wrap:wrap; margin-bottom:.2rem; }
.brand h1{ font-size:1.7rem; font-weight:700; margin:0; padding:0; letter-spacing:-.01em; }
.brand span{ color:var(--muted); font-size:.95rem; }

/* Kepala saham */
.quote{ display:flex; justify-content:space-between; align-items:flex-end; gap:1rem; flex-wrap:wrap;
        padding:.9rem 0 1rem; border-bottom:1px solid var(--line); margin-bottom:1rem; }
.quote .name{ font-size:.95rem; color:var(--muted); }
.quote .code{ font-size:1.5rem; font-weight:700; }
.quote .px{ font-size:2.1rem; font-weight:600; font-variant-numeric:tabular-nums; line-height:1.1; text-align:right; }
.quote .chg{ font-size:.95rem; font-weight:600; text-align:right; font-variant-numeric:tabular-nums; }
.up{ color:var(--ok); } .down{ color:var(--bad); }

/* Tiga gaya trading: elemen utama halaman */
.horizons{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin:.4rem 0 1.2rem; }
.horizons.one{ grid-template-columns:minmax(0,520px); }
.hz{ border:1px solid var(--line); border-radius:10px; background:var(--surface);
     padding:16px 16px 12px; border-top:5px solid var(--warn); min-width:0; }
.hz.buy{ border-top-color:var(--ok); } .hz.sell{ border-top-color:var(--bad); }
.hz .style{ font-weight:700; font-size:1.05rem; }
.hz .span{ color:var(--muted); font-size:.82rem; margin-bottom:.7rem; }
.hz .verdict{ font-size:1.35rem; font-weight:700; line-height:1.2; }
.hz.buy .verdict{ color:var(--ok); } .hz.sell .verdict{ color:var(--bad); } .hz.wait .verdict{ color:var(--warn); }
.hz .meta{ color:var(--muted); font-size:.85rem; margin:.25rem 0 .8rem; }
.lv{ display:grid; grid-template-columns:repeat(auto-fit,minmax(88px,1fr)); gap:8px; margin-bottom:.7rem; }
.lv div{ border:1px solid var(--line); border-radius:6px; padding:6px 8px; }
.lv small{ display:block; color:var(--muted); font-size:.72rem; }
.lv b{ font-variant-numeric:tabular-nums; font-size:.92rem; }
.hz details summary{ cursor:pointer; font-size:.88rem; font-weight:600; padding:4px 0; }
.hz details summary:focus-visible{ outline:2px solid var(--ok); outline-offset:2px; }
.hz details ul{ margin:.3rem 0 0; padding-left:1.1rem; font-size:.86rem; }
.hz details li{ margin-bottom:.2rem; }

.note{ border-left:4px solid var(--warn); background:var(--surface); padding:.6rem .9rem;
       border-radius:0 8px 8px 0; font-size:.88rem; margin:.6rem 0; }
.foot{ color:var(--muted); font-size:.8rem; margin-top:2rem; border-top:1px solid var(--line); padding-top:.8rem; }

/* Komponen Streamlit */
[data-testid="stMetric"]{ border:1px solid var(--line); border-radius:8px; padding:10px 14px; background:var(--surface); }
.stTabs [role="tablist"]{ overflow-x:auto; gap:4px; scrollbar-width:thin; }
.stTabs [role="tab"]{ white-space:nowrap; padding:8px 14px; }
.stButton button, .stDownloadButton button{ border-radius:8px; font-weight:600; min-height:44px; }
[data-testid="stTextInput"] input{ min-height:46px; font-size:1.05rem; }

[data-testid="stPills"]{ margin-bottom:.2rem; }

/* Responsif */
@media (max-width:900px){ .horizons, .horizons.one{ grid-template-columns:1fr; } }
@media (max-width:640px){
  .block-container{ padding-left:.8rem; padding-right:.8rem; }
  .brand h1{ font-size:1.35rem; }
  .quote .px{ font-size:1.7rem; } .quote .code{ font-size:1.25rem; }
  .quote > div:last-child{ width:100%; display:flex; justify-content:space-between; align-items:baseline; }
}
@media (prefers-reduced-motion:no-preference){ .hz{ transition:border-color .15s; } .hz:hover{ border-color:var(--muted); } }
</style>
"""
