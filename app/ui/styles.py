# app/ui/styles.py
CSS_STYLES = """
<style>
    /* Global dark theme dengan kontras tinggi */
    .stApp {
        background-color: #0a0a0a !important;
    }
    
    /* Main content background */
    .main .block-container {
        background-color: #0a0a0a !important;
    }
    
    /* Text colors biar keliatan */
    body, p, span, div, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Headers pake warna cerah */
    h1, h2, h3, h4, h5, h6 {
        color: #00ffcc !important;
        background: none !important;
        -webkit-text-fill-color: #00ffcc !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border: 1px solid #00ffcc !important;
        box-shadow: 0 4px 10px rgba(0,255,204,0.1) !important;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #ff00ff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #aaaaaa !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ffcc !important;
        font-size: 36px !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #ffaa00 !important;
    }
    
    /* Signal badges */
    .buy-signal {
        background: linear-gradient(135deg, #00cc88, #00ffaa);
        color: #000000 !important;
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.3rem;
        text-align: center;
        display: inline-block;
        box-shadow: 0 0 15px #00ffaa;
        animation: pulse 2s infinite;
    }
    
    .sell-signal {
        background: linear-gradient(135deg, #ff3366, #ff6633);
        color: #ffffff !important;
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.3rem;
        text-align: center;
        display: inline-block;
        box-shadow: 0 0 15px #ff3366;
        animation: pulse 2s infinite;
    }
    
    .neutral-signal {
        background: linear-gradient(135deg, #ffaa00, #ffdd44);
        color: #000000 !important;
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.3rem;
        text-align: center;
        display: inline-block;
        box-shadow: 0 0 10px #ffaa00;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.02); opacity: 0.95; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Cards */
    .card {
        background: #1a1a2e;
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #333;
        transition: all 0.3s;
    }
    
    .card:hover {
        border-color: #00ffcc;
        box-shadow: 0 8px 25px rgba(0,255,204,0.15);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0a0a !important;
        border-right: 1px solid #00ffcc !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }
    
    /* Expander */
    [data-testid="stExpander"] {
        background: #1a1a2e !important;
        border-radius: 12px;
        border: 1px solid #333;
    }
    
    [data-testid="stExpander"] summary {
        color: #00ffcc !important;
        font-weight: bold;
    }
    
    /* Divider */
    hr {
        border-color: #00ffcc;
        margin: 20px 0;
        opacity: 0.3;
    }
    
    /* Info boxes */
    .info-box {
        background: #1a1a2e;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        color: #e0e0e0;
    }
    .info-box-info {
        border-left: 4px solid #00ffcc;
    }
    .info-box-warning {
        border-left: 4px solid #ffaa00;
    }
    .info-box-error {
        border-left: 4px solid #ff3366;
    }
    
    /* Dataframe / table */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame th {
        background: #00ffcc !important;
        color: #000000 !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    
    .stDataFrame td {
        color: #e0e0e0 !important;
        background: #1a1a2e !important;
    }
    
    /* Selectbox, slider, text input labels */
    [data-testid="stSelectbox"] label,
    [data-testid="stSlider"] label,
    [data-testid="stTextInput"] label {
        color: #00ffcc !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox value */
    [data-testid="stSelectbox"] .st-emotion-cache-ue6h4q {
        color: #ffffff !important;
    }
    
    /* Slider value */
    [data-testid="stSlider"] .st-emotion-cache-1gv3huu {
        color: #00ffcc !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a1a2e;
        border-radius: 8px;
        color: #aaaaaa;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00cc88, #00ffaa);
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Streamlit alerts */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #00ffcc;
    }
    
    /* Button */
    .stButton button {
        background: linear-gradient(135deg, #00cc88, #00ffaa);
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 10px #00ffcc;
    }
      /* ========== SELECTBOX / DROPDOWN FIX ========== */
    /* Label selectbox */
    [data-testid="stSelectbox"] label {
        color: #00ffcc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Selectbox container */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
        border-radius: 8px !important;
    }
    
    /* Selectbox value / selected text */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="ValueContainer"] {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="singleValue"] {
        color: #ffffff !important;
    }
    
    /* Selectbox placeholder */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="placeholder"] {
        color: #888888 !important;
    }
    
    /* Selectbox dropdown menu */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="menu"] {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
        border-radius: 8px !important;
    }
    
    /* Dropdown options */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="option"] {
        color: #e0e0e0 !important;
        background-color: #1a1a2e !important;
    }
    
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="option"]:hover {
        background-color: #00ffcc !important;
        color: #000000 !important;
    }
    
    /* Selected option in dropdown */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div[class*="option"][aria-selected="true"] {
        background-color: #00ffcc !important;
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Selectbox arrow icon */
    [data-testid="stSelectbox"] svg {
        fill: #00ffcc !important;
    }
    
    /* ========== TEXT INPUT FIX ========== */
    [data-testid="stTextInput"] label {
        color: #00ffcc !important;
    }
    
    [data-testid="stTextInput"] input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #00ffcc !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stTextInput"] input::placeholder {
        color: #888888 !important;
    }
    
    /* ========== SLIDER FIX ========== */
    [data-testid="stSlider"] label {
        color: #00ffcc !important;
    }
    
    [data-testid="stSlider"] div[data-baseweb="slider"] div[class*="track"] {
        background-color: #333333 !important;
    }
    
    [data-testid="stSlider"] div[data-baseweb="slider"] div[class*="thumb"] {
        background-color: #00ffcc !important;
    }
    
    /* Slider value display */
    [data-testid="stSlider"] div[class*="value"] {
        color: #00ffcc !important;
    }
    
    /* ========== RADIO BUTTON FIX ========== */
    [data-testid="stRadio"] label {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] label {
        color: #e0e0e0 !important;
    }
    
    /* ========== MULTISELECT FIX ========== */
    [data-testid="stMultiSelect"] label {
        color: #00ffcc !important;
    }
    
    [data-testid="stMultiSelect"] div[data-baseweb="select"] {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* ========== NUMBER INPUT FIX ========== */
    [data-testid="stNumberInput"] label {
        color: #00ffcc !important;
    }
    
    [data-testid="stNumberInput"] input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* ========== DATE INPUT FIX ========== */
    [data-testid="stDateInput"] label {
        color: #00ffcc !important;
    }
    
    [data-testid="stDateInput"] input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* ========== TEXT AREA FIX ========== */
    [data-testid="stTextArea"] label {
        color: #00ffcc !important;
    }
    
    [data-testid="stTextArea"] textarea {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* ========== TOOLTIP / INFO HOVER ========== */
    [data-testid="stTooltipIcon"] svg {
        fill: #00ffcc !important;
    }
        /* FIX SELECTBOX - Target lebih agresif */
    div[data-baseweb="select"] {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    
    div[data-baseweb="select"] [role="combobox"] {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    
    /* Dropdown menu container */
    div[data-baseweb="popover"] div[data-baseweb="menu"] {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* Dropdown option items */
    div[data-baseweb="popover"] li[role="option"] {
        color: #e0e0e0 !important;
        background-color: #1a1a2e !important;
    }
    
    div[data-baseweb="popover"] li[role="option"]:hover {
        background-color: #00ffcc !important;
        color: #000000 !important;
    }
    
    div[data-baseweb="popover"] li[role="option"][aria-selected="true"] {
        background-color: #00ffcc !important;
        color: #000000 !important;
    }
    
    /* Selectbox arrow icon */
    div[data-baseweb="select"] svg {
        fill: #00ffcc !important;
    }
</style>
"""