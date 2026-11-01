# app/ui/styles.py
# Tema dark yang tenang: satu warna aksen, kontras jelas, tanpa glow/animasi.
# Class lama (.buy-signal, .sell-signal, .neutral-signal, .card, .info-box*) tetap
# ada supaya tabs.py tidak perlu diubah.

CSS_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg:          #0d1117;
    --surface:     #151b23;
    --surface-2:   #1c242e;
    --border:      #2a3441;
    --text:        #e6edf3;
    --text-muted:  #8b98a8;
    --accent:      #2dd4bf;
    --accent-soft: rgba(45, 212, 191, 0.12);
    --buy:         #4ade80;
    --buy-soft:    rgba(74, 222, 128, 0.12);
    --sell:        #f87171;
    --sell-soft:   rgba(248, 113, 113, 0.12);
    --warn:        #fbbf24;
    --warn-soft:   rgba(251, 191, 36, 0.12);
    --radius:      12px;
}

/* ───────── Dasar ───────── */
.stApp {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}

.stApp p, .stApp label, .stApp li {
    font-family: inherit;
}

.main .block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

footer { visibility: hidden; }

/* ───────── Judul ───────── */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: var(--text);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    letter-spacing: -0.01em;
}
.stApp h1 { font-size: 1.9rem; }
.stApp h2 { font-size: 1.45rem; }
.stApp h3 { font-size: 1.15rem; margin-top: 0.4rem; }

[data-testid="stCaptionContainer"],
.stApp small {
    color: var(--text-muted);
}

hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.25rem 0;
    opacity: 1;
}

/* ───────── Tab navigasi ───────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
    scrollbar-width: none;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.92rem;
    padding: 10px 16px;
    border-radius: 8px 8px 0 0;
    white-space: nowrap;
    transition: color .15s, background .15s;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text);
    background: var(--surface);
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    font-weight: 600;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--accent);
    height: 2px;
}
.stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.25rem; }

/* ───────── Kartu metrik ───────── */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 18px;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-size: 0.8rem;
    font-weight: 500;
}
[data-testid="stMetricLabel"] p { font-size: 0.8rem; }
[data-testid="stMetricValue"] {
    color: var(--text);
    font-size: 1.6rem;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}
[data-testid="stMetricDelta"] {
    font-size: 0.8rem;
    font-weight: 500;
}

/* ───────── Badge sinyal ───────── */
.buy-signal, .sell-signal, .neutral-signal {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.95rem;
    text-align: center;
    line-height: 1.4;
    border: 1px solid transparent;
}
.buy-signal     { background: var(--buy-soft);  color: var(--buy);  border-color: rgba(74,222,128,.35); }
.sell-signal    { background: var(--sell-soft); color: var(--sell); border-color: rgba(248,113,113,.35); }
.neutral-signal { background: var(--warn-soft); color: var(--warn); border-color: rgba(251,191,36,.35); }

/* Kartu hasil sinyal (dipakai signal_card) */
.signal-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    margin: 12px 0;
    text-align: center;
}
.signal-meta {
    display: flex;
    justify-content: center;
    gap: 28px;
    margin-top: 12px;
    color: var(--text-muted);
    font-size: 0.88rem;
}
.signal-meta strong {
    color: var(--text);
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}

/* ───────── Kartu umum & kotak info ───────── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 20px;
    margin: 10px 0;
}

.info-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    margin: 10px 0;
    color: var(--text);
    font-size: 0.92rem;
    line-height: 1.5;
}
.info-box-info    { border-left: 3px solid var(--accent); }
.info-box-warning { border-left: 3px solid var(--warn); }
.info-box-error   { border-left: 3px solid var(--sell); }

/* HTML inline di tabs.py (kartu dengan background #1a1a2e) ikut diselaraskan */
[data-testid="stMarkdownContainer"] div[style*="#1a1a2e"] {
    background: var(--surface) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stMarkdownContainer"] div[style*="linear-gradient"][style*="#1a1a2e"] {
    background: var(--surface) !important;
}

/* ───────── Sidebar ───────── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container,
[data-testid="stSidebarContent"] {
    padding-top: 1.5rem;
}

/* ───────── Expander ───────── */
[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
}
[data-testid="stExpander"] summary {
    color: var(--text);
    font-weight: 500;
}
[data-testid="stExpander"] summary:hover { color: var(--accent); }

/* ───────── Alert bawaan Streamlit (success/warning/error/info) ───────── */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ───────── Tabel & grafik ───────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}
[data-testid="stPlotlyChart"] {
    background: #0a0a0a;               /* sama dengan paper_bgcolor chart di tabs.py */
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 6px;
    overflow: hidden;
}

/* ───────── Input ───────── */
[data-testid="stWidgetLabel"] p,
.stApp label {
    color: var(--text);
    font-weight: 500;
    font-size: 0.88rem;
}

div[data-baseweb="select"] > div,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
}

div[data-baseweb="select"] > div:hover,
[data-testid="stTextInput"] input:hover,
[data-testid="stNumberInput"] input:hover {
    border-color: var(--text-muted);
}

div[data-baseweb="select"] > div:focus-within,
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: var(--text-muted);
}

div[data-baseweb="select"] svg { fill: var(--text-muted); }

/* Daftar dropdown */
div[data-baseweb="popover"] ul[role="listbox"],
div[data-baseweb="popover"] div[data-baseweb="menu"] {
    background-color: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
}
div[data-baseweb="popover"] li[role="option"] {
    color: var(--text);
    background-color: transparent;
}
div[data-baseweb="popover"] li[role="option"]:hover,
div[data-baseweb="popover"] li[role="option"][aria-selected="true"] {
    background-color: var(--accent-soft);
    color: var(--accent);
}

/* Slider */
[data-testid="stSlider"] [role="slider"] {
    background-color: var(--accent);
    box-shadow: none;
}
[data-testid="stSlider"] [data-testid="stThumbValue"],
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: var(--text-muted);
    font-variant-numeric: tabular-nums;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] { color: var(--accent); }

/* ───────── Tombol ───────── */
.stButton > button,
.stDownloadButton > button {
    background: var(--surface-2);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    font-weight: 500;
    padding: 0.45rem 1rem;
    transition: border-color .15s, color .15s, background .15s;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--surface-2);
}
.stButton > button:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--accent);
    border-color: var(--accent);
    color: #04201c;
    font-weight: 600;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #5eead4;
    color: #04201c;
}

/* ───────── Progress & spinner ───────── */
[data-testid="stProgress"] > div > div > div > div {
    background-color: var(--accent);
}

/* ───────── Mobile ───────── */
@media (max-width: 640px) {
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    [data-testid="stMetricValue"] { font-size: 1.3rem; }
    .stTabs [data-baseweb="tab"] { padding: 8px 12px; font-size: 0.85rem; }
    .signal-meta { gap: 16px; flex-wrap: wrap; }
}
</style>
"""
