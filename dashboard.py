import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard ความก้าวหน้าทางหลวง",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun', sans-serif !important; }

/* ── Animations ── */
@keyframes livePulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.35; transform: scale(1.5); }
}
@keyframes stripeScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(60px); }
}
@keyframes riskGlow {
    0%, 100% { transform: scale(1);     opacity: 1; }
    50%       { transform: scale(1.007); opacity: 0.93; }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideInDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideInUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes popIn {
    0%   { opacity: 0; transform: scale(0.88); }
    60%  { transform: scale(1.03); }
    100% { opacity: 1; transform: scale(1); }
}

/* ── Page background — dot grid ── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #e8edf4 !important;
    background-image: radial-gradient(#c0cfe0 1px, transparent 1px) !important;
    background-size: 26px 26px !important;
}

/* ── Dark sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1a3151 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] p { color: #94a3b8 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #7a9abf !important; font-size: 11px !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.6px !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
    color: #cbd5e1 !important; text-transform: none !important;
    letter-spacing: 0 !important; font-size: 13px !important; font-weight: 400 !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #475569 !important; }

/* ── Section headers ── */
.section-header {
    font-size: 13px; font-weight: 700; color: #0f172a;
    margin-bottom: 12px; padding: 9px 16px;
    border-left: 4px solid #1A5276;
    background: linear-gradient(90deg, #dbeafe 0%, #eff6ff 50%, rgba(248,250,252,0) 100%);
    border-radius: 0 8px 8px 0;
    letter-spacing: 0.3px;
}

/* ── Metric containers ── */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 12px; padding: 14px;
    box-shadow: 0 4px 16px rgba(15,23,42,0.08);
}

/* ── Expanders ── */
div[data-testid="stExpander"],
details[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.9) !important;
    border-radius: 10px !important; margin-bottom: 6px !important;
    overflow: hidden !important;
    background: rgba(255,255,255,0.82) !important;
    backdrop-filter: blur(8px) !important; -webkit-backdrop-filter: blur(8px) !important;
    box-shadow: 0 2px 8px rgba(15,23,42,0.07) !important;
}
div[data-testid="stExpander"] summary,
details[data-testid="stExpander"] summary,
div[data-testid="stExpander"] details summary {
    background: transparent !important; padding: 11px 16px !important; cursor: pointer !important;
}
div[data-testid="stExpander"] summary:hover,
details[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] details summary:hover {
    background: rgba(219,234,254,0.5) !important;
}
div[data-testid="stExpander"] summary p,
details[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] details summary p {
    font-size: 13px !important; font-weight: 700 !important;
    color: #1e293b !important; letter-spacing: 0.2px !important;
}
div[data-testid="stExpander"] summary:hover p,
details[data-testid="stExpander"] summary:hover p,
div[data-testid="stExpander"] details summary:hover p { color: #1A5276 !important; }

/* ── Sidebar multiselect — dark inputs ── */
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(255,255,255,0.14) !important;
    border-radius: 8px !important;
}
/* All text nodes inside the sidebar select box */
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #cbd5e1 !important; }
/* Selected tags */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(30,64,175,0.55) !important;
    border-radius: 5px !important;
    border: none !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span  { color: #93c5fd !important; font-size:11px !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] button { color: #93c5fd !important; }
/* Search / placeholder text */
[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #e2e8f0 !important;
    caret-color: #e2e8f0 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] input::placeholder { color: #64748b !important; }
/* The single-value / no-selection label */
[data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"] { color: #64748b !important; }
[data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"]  { color: #e2e8f0 !important; }
/* Dropdown arrow icon */
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #64748b !important; }
/* Sidebar checkbox label */
[data-testid="stSidebar"] [data-testid="stCheckbox"] label span { color: #cbd5e1 !important; }
/* Sidebar checkbox wrapper */
[data-testid="stSidebar"] [data-testid="stCheckbox"] {
    padding: 8px 10px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
}

/* ── Pagination buttons ── */
div[data-testid="stButton"] button {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid #dde3ed !important;
    border-radius: 8px !important;
    color: #1e293b !important; font-weight: 600 !important;
    backdrop-filter: blur(8px) !important;
    transition: background 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="stButton"] button:hover {
    background: rgba(219,234,254,0.9) !important;
    box-shadow: 0 2px 8px rgba(26,82,118,0.15) !important;
}

/* ── Hide Streamlit chrome ── */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu                       { display: none !important; }
footer                          { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Status-colour expander labels (JS, runs continuously via setInterval) ─────
components.html("""
<script>
(function() {
    var COLOR = {
        'ล่าช้าเล็กน้อย': '#d97706',
        'ล่าช้าปานกลาง': '#d97706',
        'ล่าช้า': '#d97706',
        'วิกฤต': '#dc2626',
        'ตามแผน': '#16a34a'
    };
    var PAT = /(ล่าช้าเล็กน้อย|ล่าช้าปานกลาง|ล่าช้า|วิกฤต|ตามแผน)/g;
    function run() {
        var doc;
        try { doc = window.parent.document; } catch(e) { doc = document; }
        doc.querySelectorAll('details summary p:not([data-sc])').forEach(function(p) {
            p.setAttribute('data-sc', '1');
            p.innerHTML = p.innerHTML.replace(PAT, function(m) {
                return '<span style="color:' + COLOR[m] + ';font-weight:700">' + m + '</span>';
            });
        });
    }
    setInterval(run, 800);
})();
</script>
""", height=0, scrolling=False)

# ── Province Coords ───────────────────────────────────────────────────────────
PROVINCE_COORDS = {
    "กรุงเทพมหานคร":(13.7563,100.5018),"กระบี่":(8.0863,98.9063),
    "กาญจนบุรี":(14.0023,99.5328),"กาฬสินธุ์":(16.4314,103.5058),
    "กำแพงเพชร":(16.4827,99.5122),"ขอนแก่น":(16.4419,102.8360),
    "จันทบุรี":(12.6105,102.1039),"ฉะเชิงเทรา":(13.6904,101.0779),
    "ชลบุรี":(13.3611,100.9847),"ชัยนาท":(15.1851,100.1252),
    "ชัยภูมิ":(15.8068,102.0317),"ชุมพร":(10.4930,99.1800),
    "เชียงราย":(19.9105,99.8406),"เชียงใหม่":(18.7883,98.9853),
    "ตรัง":(7.5593,99.6113),"ตราด":(12.2428,102.5175),
    "ตาก":(16.8798,99.1257),"นครนายก":(14.2057,101.2132),
    "นครปฐม":(13.8199,100.0624),"นครพนม":(17.4101,104.7731),
    "นครราชสีมา":(14.9799,102.0978),"นครศรีธรรมราช":(8.4324,99.9631),
    "นครสวรรค์":(15.7030,100.1372),"นนทบุรี":(13.8621,100.5144),
    "นราธิวาส":(6.4255,101.8253),"น่าน":(18.7756,100.7730),
    "บึงกาฬ":(18.3609,103.6466),"บุรีรัมย์":(14.9930,103.1029),
    "ปทุมธานี":(14.0208,100.5250),"ประจวบคีรีขันธ์":(11.8126,99.7975),
    "ปราจีนบุรี":(14.0509,101.3649),"ปัตตานี":(6.8695,101.2500),
    "พระนครศรีอยุธยา":(14.3692,100.5877),"พะเยา":(19.1665,99.9017),
    "พังงา":(8.4511,98.5253),"พัทลุง":(7.6166,100.0740),
    "พิจิตร":(16.4419,100.3487),"พิษณุโลก":(16.8211,100.2659),
    "เพชรบุรี":(13.1119,99.9393),"เพชรบูรณ์":(16.4189,101.1591),
    "แพร่":(18.1445,100.1403),"ภูเก็ต":(7.8804,98.3923),
    "มหาสารคาม":(16.1851,103.3017),"มุกดาหาร":(16.5426,104.7236),
    "แม่ฮ่องสอน":(19.3020,97.9654),"ยโสธร":(15.7922,104.1452),
    "ยะลา":(6.5413,101.2804),"ร้อยเอ็ด":(16.0538,103.6520),
    "ระนอง":(9.9528,98.6085),"ระยอง":(12.6814,101.2816),
    "ราชบุรี":(13.5282,99.8134),"ลพบุรี":(14.7995,100.6534),
    "ลำปาง":(18.2888,99.4900),"ลำพูน":(18.5744,99.0087),
    "เลย":(17.4860,101.7223),"ศรีสะเกษ":(15.1186,104.3221),
    "สกลนคร":(17.1664,104.1486),"สงขลา":(7.1756,100.6142),
    "สตูล":(6.6238,100.0673),"สมุทรปราการ":(13.5991,100.5998),
    "สมุทรสงคราม":(13.4098,99.9975),"สมุทรสาคร":(13.5475,100.2747),
    "สระแก้ว":(13.8240,102.0645),"สระบุรี":(14.5289,100.9109),
    "สิงห์บุรี":(14.8936,100.3967),"สุโขทัย":(17.0069,99.8265),
    "สุพรรณบุรี":(14.4744,100.1177),"สุราษฎร์ธานี":(9.1382,99.3217),
    "สุรินทร์":(14.8820,103.4930),"หนองคาย":(17.8783,102.7417),
    "หนองบัวลำภู":(17.2218,102.4260),"อ่างทอง":(14.5896,100.4549),
    "อำนาจเจริญ":(15.8656,104.6257),"อุดรธานี":(17.4138,102.7872),
    "อุตรดิตถ์":(17.6200,100.0993),"อุทัยธานี":(15.3835,100.0248),
    "อุบลราชธานี":(15.2287,104.8563),
    "ราชบุรี, เพชรบุรี":(13.5282,99.8134),
}

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("รายงานความก้าวหน้า_67-69.xlsx", header=0)
    RENAME = {
        "ปีงบประมาณ":"ปีงบประมาณ","เดือน":"เดือน",
        "โครงการ":"โครงการ","กิจกรรม":"กิจกรรม",
        "หมายเลข\nทางหลวง":"หมายเลขทางหลวง",
        "ชื่อสายทาง":"ชื่อสายทาง","จังหวัด":"จังหวัด",
        "เริ่มต้น - สิ้นสุด\nกม.- กม.":"ช่วง กม.",
        "ระยะทาง\n(กม.) / (แห่ง)":"ระยะทาง (กม.)",
        "ค่างานตามสัญญา\n(บาท)":"ค่างานตามสัญญา (บาท)",
        "ก่อสร้างโดย":"ผู้รับจ้าง",
        "หน่วยงานที่\nรับผิดชอบ":"หน่วยงานรับผิดชอบ",
        "วันเริ่ม\nสัญญา":"วันเริ่มสัญญา",
        "วันสิ้นสุด\nสัญญา":"วันสิ้นสุดสัญญา",
        "เวลาทำงาน\n(วัน)":"เวลาทำงาน (วัน)",
        "สะสมแผน":"ตามแผน (%)",
        "สะสมผล":"จริง (%)",
        "ช้า-เร็ว":"ส่วนต่าง (%)",
        "สถานะโครงการ/ปัญหาอุปสรรค":"ปัญหาอุปสรรค",
        "หมายเหตุ /แนวทางแก้ไข":"แนวทางแก้ไข",
    }
    df = df.rename(columns=RENAME)
    df["ปีงบประมาณ"] = pd.to_numeric(df["ปีงบประมาณ"], errors="coerce").fillna(0).astype(int)
    for col in ["ระยะทาง (กม.)","เวลาทำงาน (วัน)"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.split("\n").str[0], errors="coerce")
    for col in ["โครงการ","ชื่อสายทาง","จังหวัด","ผู้รับจ้าง","หน่วยงานรับผิดชอบ","ปัญหาอุปสรรค","แนวทางแก้ไข"]:
        df[col] = df[col].astype(str).str.strip().replace("nan","")
    MONTH_ORDER = ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
                   "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]
    df["เดือน"] = pd.Categorical(df["เดือน"], categories=MONTH_ORDER, ordered=True)
    PROJECT_SHORT = {
        "โครงการก่อสร้างโครงข่ายทางหลวงแผ่นดิน":"โครงข่ายทางหลวงแผ่นดิน",
        "โครงการบูรณะโครงข่ายทางหลวงเชื่อมโยงระหว่างภาค":"บูรณะทางหลวงระหว่างภาค",
        "โครงการพัฒนาทางหลวงรองรับระเบียงเศรษฐกิจภาคตะวันออก":"ระเบียงเศรษฐกิจ (EEC)",
    }
    df["ประเภทโครงการ"] = df["โครงการ"].map(PROJECT_SHORT).fillna(df["โครงการ"].str[:30])
    def status_tag(v):
        if pd.isna(v): return "ไม่มีข้อมูล"
        if v >= 100:   return "แล้วเสร็จ"
        if v >= -5:    return "เป็นไปตามแผน"
        if v >= -10:   return "ล่าช้าปานกลาง"
        return "ล่าช้าวิกฤต"
    df["สถานะ"] = df["ส่วนต่าง (%)"].apply(status_tag)
    return df

def format_thai_baht(value):
    if value >= 1_000_000_000_000:
        return f"{value/1_000_000_000_000:,.2f} ล้านล้านบาท"
    elif value >= 100_000_000_000:
        return f"{value/100_000_000_000:,.2f} แสนล้านบาท"
    elif value >= 10_000_000_000:
        return f"{value/10_000_000_000:,.2f} หมื่นล้านบาท"
    elif value >= 1_000_000_000:
        return f"{value/1_000_000_000:,.2f} พันล้านบาท"
    elif value >= 100_000_000:
        return f"{value/100_000_000:,.2f} ร้อยล้านบาท"
    elif value >= 10_000_000:
        return f"{value/10_000_000:,.2f} สิบล้านบาท"
    elif value >= 1_000_000:
        return f"{value/1_000_000:,.2f} ล้านบาท"
    return f"{value:,.0f} บาท"

def kpi_card(title, value, subtitle=None, border_color="#1A5276", icon="", pulse=False):
    anim = "animation:riskGlow 2s ease-in-out infinite;will-change:transform,opacity;" if pulse else ""
    sub_html  = f'<div style="margin-top:7px;font-size:11px">{subtitle}</div>' if subtitle else ""
    icon_html = f'<div style="font-size:26px;line-height:1;margin-bottom:8px">{icon}</div>' if icon else ""
    # No newlines inside — blank lines in Markdown cause Streamlit to escape closing tags as text
    return (
        f'<div style="background:rgba(255,255,255,0.82);backdrop-filter:blur(12px);'
        f'-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.9);'
        f'border-top:4px solid {border_color};border-radius:14px;padding:14px;text-align:center;'
        f'box-shadow:0 8px 32px rgba(15,23,42,0.1),inset 0 1px 0 rgba(255,255,255,0.6);'
        f'animation:fadeUp 0.5s ease;{anim}'
        f'min-height:150px;display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;gap:4px;">'
        f'{icon_html}'
        f'<div style="font-size:10px;color:#64748b;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:0.8px">{title}</div>'
        f'<div style="font-size:21px;font-weight:700;color:#0f172a;line-height:1.2">{value}</div>'
        f'{sub_html}'
        f'</div>'
    )

def progress_ring_card(title, pct, subtitle, ring_color, border_color):
    safe_pct = min(max(pct if not pd.isna(pct) else 0, 0), 100)
    r = 22
    circumference = 138.2   # 2 * pi * 22
    offset = circumference * (1 - safe_pct / 100)
    return f"""
    <div style="background:rgba(255,255,255,0.82);
                backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
                border:1px solid rgba(255,255,255,0.9);border-top:4px solid {border_color};
                border-radius:14px;padding:14px;text-align:center;
                box-shadow:0 8px 32px rgba(15,23,42,0.1),inset 0 1px 0 rgba(255,255,255,0.6);
                animation:fadeUp 0.5s ease;
                min-height:150px;display:flex;flex-direction:column;
                align-items:center;justify-content:center;gap:4px;">
        <div style="font-size:10px;color:#64748b;font-weight:700;
                    text-transform:uppercase;letter-spacing:0.8px">{title}</div>
        <svg width="58" height="58" viewBox="0 0 58 58" style="display:block;margin:0 auto">
            <circle cx="29" cy="29" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="5"/>
            <circle cx="29" cy="29" r="{r}" fill="none" stroke="{ring_color}" stroke-width="5"
                    stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
                    stroke-linecap="round" transform="rotate(-90 29 29)"/>
            <text x="29" y="34" text-anchor="middle" font-family="Sarabun,sans-serif"
                  font-size="12" font-weight="700" fill="#0f172a">{safe_pct:.1f}%</text>
        </svg>
        {subtitle}
    </div>
    """

df_all = load_data()
latest = (df_all.sort_values(["ปีงบประมาณ","เดือน"])
                .groupby("ชื่อสายทาง", sort=False).last().reset_index())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Branded header ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:22px 12px 18px;
                border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:6px">
        <div style="font-size:40px;margin-bottom:8px;
                    filter:drop-shadow(0 3px 10px rgba(0,0,0,0.5))">🛣️</div>
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;letter-spacing:0.4px">
            กรมทางหลวง
        </div>
        <div style="font-size:11px;color:#64748b;margin-top:3px;letter-spacing:0.3px">
            ระบบติดตามความก้าวหน้า
        </div>
        <div style="margin-top:12px;display:inline-flex;align-items:center;gap:6px;
                    background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.22);
                    border-radius:999px;padding:4px 12px">
            <div style="width:6px;height:6px;border-radius:50%;background:#22c55e;
                        animation:livePulse 2s ease-in-out infinite;
                        box-shadow:0 0 6px rgba(34,197,94,0.6)"></div>
            <span style="font-size:10px;color:#4ade80;font-weight:600;letter-spacing:1.5px">LIVE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Year filter ───────────────────────────────────────────────────────────
    st.markdown("""<div style="display:flex;align-items:center;gap:8px;margin:14px 0 5px;padding:0 2px">
        <span style="font-size:15px">📅</span>
        <span style="font-size:11px;font-weight:700;color:#7a9abf;
                     text-transform:uppercase;letter-spacing:1px">ปีงบประมาณ</span>
    </div>""", unsafe_allow_html=True)
    years     = sorted(df_all["ปีงบประมาณ"].unique())
    sel_years = st.multiselect("ปีงบประมาณ", years, default=[2569] if 2569 in years else years,
                               label_visibility="collapsed")

    # ── Province filter ───────────────────────────────────────────────────────
    st.markdown("""<div style="display:flex;align-items:center;gap:8px;margin:12px 0 5px;padding:0 2px">
        <span style="font-size:15px">📍</span>
        <span style="font-size:11px;font-weight:700;color:#7a9abf;
                     text-transform:uppercase;letter-spacing:1px">จังหวัด</span>
    </div>""", unsafe_allow_html=True)
    provinces = sorted(latest["จังหวัด"].dropna().unique())
    sel_prov  = st.multiselect("จังหวัด", provinces, default=[],
                               label_visibility="collapsed")

    # ── Project type filter ───────────────────────────────────────────────────
    st.markdown("""<div style="display:flex;align-items:center;gap:8px;margin:12px 0 5px;padding:0 2px">
        <span style="font-size:15px">🏗️</span>
        <span style="font-size:11px;font-weight:700;color:#7a9abf;
                     text-transform:uppercase;letter-spacing:1px">ประเภทโครงการ</span>
    </div>""", unsafe_allow_html=True)
    proj_types = sorted(latest["ประเภทโครงการ"].dropna().unique())
    sel_proj   = st.multiselect("ประเภทโครงการ", proj_types, default=[],
                                label_visibility="collapsed")

    # ── Unit filter ───────────────────────────────────────────────────────────
    st.markdown("""<div style="display:flex;align-items:center;gap:8px;margin:12px 0 5px;padding:0 2px">
        <span style="font-size:15px">🏢</span>
        <span style="font-size:11px;font-weight:700;color:#7a9abf;
                     text-transform:uppercase;letter-spacing:1px">หน่วยงานรับผิดชอบ</span>
    </div>""", unsafe_allow_html=True)
    units     = sorted(latest["หน่วยงานรับผิดชอบ"].dropna().unique())
    sel_unit  = st.multiselect("หน่วยงานรับผิดชอบ", units, default=[],
                               label_visibility="collapsed")

    # ── Risk-only toggle ──────────────────────────────────────────────────────
    st.markdown("""<div style="display:flex;align-items:center;gap:8px;margin:14px 0 5px;padding:0 2px">
        <span style="font-size:15px">⚠️</span>
        <span style="font-size:11px;font-weight:700;color:#7a9abf;
                     text-transform:uppercase;letter-spacing:1px">ตัวกรองพิเศษ</span>
    </div>""", unsafe_allow_html=True)
    risk_only = st.checkbox("แสดงเฉพาะโครงการที่ล่าช้า", value=False)

    # ── Active-filter result count ────────────────────────────────────────────
    _sb = latest.copy()
    if sel_years: _sb = _sb[_sb["ปีงบประมาณ"].isin(sel_years)]
    if sel_prov:  _sb = _sb[_sb["จังหวัด"].isin(sel_prov)]
    if sel_proj:  _sb = _sb[_sb["ประเภทโครงการ"].isin(sel_proj)]
    if sel_unit:  _sb = _sb[_sb["หน่วยงานรับผิดชอบ"].isin(sel_unit)]
    if risk_only: _sb = _sb[_sb["ส่วนต่าง (%)"] < -5]
    _sb_n     = len(_sb)
    _sb_base  = latest[latest["ปีงบประมาณ"].isin(sel_years)] if sel_years else latest
    _sb_total = len(_sb_base)
    _bar_w    = max(4, int((_sb_n / _sb_total * 100) if _sb_total else 0))
    _bar_c    = "#22c55e" if _bar_w > 60 else "#f59e0b" if _bar_w > 30 else "#ef4444"

    st.markdown(f"""
    <div style="margin:16px 0 10px;padding:12px 14px;
                background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.09);border-radius:10px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
            <span style="font-size:11px;color:#64748b;font-weight:600;
                         text-transform:uppercase;letter-spacing:0.8px">ผลลัพธ์</span>
            <div style="display:flex;align-items:baseline;gap:3px">
                <span style="font-size:20px;font-weight:700;color:#38bdf8">{_sb_n:,}</span>
                <span style="font-size:11px;color:#475569">/ {_sb_total:,} โครงการ</span>
            </div>
        </div>
        <div style="height:4px;background:rgba(255,255,255,0.07);border-radius:999px;overflow:hidden">
            <div style="height:100%;width:{_bar_w}%;background:{_bar_c};border-radius:999px"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Legend card ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:14px;background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08);border-radius:10px">
        <div style="font-size:11px;font-weight:700;color:#64748b;
                    text-transform:uppercase;letter-spacing:1px;margin-bottom:10px">
            📖 คำอธิบาย
        </div>
        <div style="font-size:12px;color:#94a3b8;line-height:2.0">
            <span style="color:#7dd3fc;font-weight:600">ตามแผน (%)</span><br>
            % ที่ควรแล้วเสร็จตามสัญญา<br>
            <span style="color:#7dd3fc;font-weight:600">จริง (%)</span><br>
            % งานที่ทำได้จริง<br>
            <span style="color:#7dd3fc;font-weight:600">ส่วนต่าง (%)</span>&nbsp;&nbsp;
            <span style="color:#f87171">ติดลบ = ล่าช้า</span><br>
            <span style="padding-left:72px;color:#4ade80">บวก = เร็วกว่าแผน</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:14px;padding-top:12px;
                border-top:1px solid rgba(255,255,255,0.06);text-align:center">
        <div style="font-size:10px;color:#334155;letter-spacing:0.3px;line-height:1.8">
            ข้อมูล: กรมทางหลวง<br>ปีงบประมาณ 2567–2569
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = latest.copy()
if sel_years: filtered = filtered[filtered["ปีงบประมาณ"].isin(sel_years)]
if sel_prov:  filtered = filtered[filtered["จังหวัด"].isin(sel_prov)]
if sel_proj:  filtered = filtered[filtered["ประเภทโครงการ"].isin(sel_proj)]
if sel_unit:  filtered = filtered[filtered["หน่วยงานรับผิดชอบ"].isin(sel_unit)]
if risk_only: filtered = filtered[filtered["ส่วนต่าง (%)"] < -5]

# ── KPI calculations ──────────────────────────────────────────────────────────
total_proj = len(filtered)
total_val  = filtered["ค่างานตามสัญญา (บาท)"].sum()
avg_actual = filtered["จริง (%)"].mean()
avg_plan   = filtered["ตามแผน (%)"].mean()
variance   = avg_actual - avg_plan
risk_count = (filtered["ส่วนต่าง (%)"] < -5).sum()
done_count = (filtered["จริง (%)"] >= 100).sum()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg, #0f172a 0%, #1e3a5f 55%, #1A5276 100%);
            border-radius:16px;padding:26px 32px 22px;margin-bottom:10px;color:white;
            position:relative;overflow:hidden;
            box-shadow:0 20px 60px rgba(15,23,42,0.35);">
    <!-- animated amber stripe (translateX for GPU compositing, period=60px) -->
    <div style="position:absolute;bottom:0;left:-60px;width:calc(100% + 60px);height:4px;
                background:repeating-linear-gradient(90deg,
                    #f59e0b 0px,#f59e0b 30px,transparent 30px,transparent 60px);
                animation:stripeScroll 1.5s linear infinite;opacity:0.9;
                will-change:transform;">
    </div>
    <!-- decorative glow circles -->
    <div style="position:absolute;top:-60px;right:-60px;width:220px;height:220px;
                border-radius:50%;background:radial-gradient(circle,rgba(41,128,185,0.18),transparent 70%);">
    </div>
    <div style="position:absolute;bottom:-40px;left:30%;width:160px;height:160px;
                border-radius:50%;background:radial-gradient(circle,rgba(245,158,11,0.08),transparent 70%);">
    </div>
    <!-- LIVE indicator -->
    <div style="position:absolute;top:22px;right:28px;display:flex;align-items:center;gap:7px;">
        <div style="width:9px;height:9px;border-radius:50%;background:#22c55e;
                    animation:livePulse 2s ease-in-out infinite;
                    box-shadow:0 0 6px rgba(34,197,94,0.7);
                    will-change:transform,opacity;"></div>
        <span style="font-size:10px;color:rgba(255,255,255,0.55);letter-spacing:2px;
                     text-transform:uppercase;font-weight:600">LIVE</span>
    </div>
    <!-- content -->
    <div style="display:flex;align-items:center;gap:18px;position:relative">
        <div style="font-size:46px;line-height:1;filter:drop-shadow(0 3px 8px rgba(0,0,0,0.4))">🛣️</div>
        <div>
            <div style="font-size:10px;letter-spacing:2.5px;text-transform:uppercase;
                        opacity:0.5;margin-bottom:7px;font-weight:500">
                กรมทางหลวง &nbsp;·&nbsp; แผนงานก่อสร้างทางหลวง
            </div>
            <div style="font-size:22px;font-weight:700;letter-spacing:0.3px;line-height:1.3">
                Dashboard ความก้าวหน้าโครงการก่อสร้างทางหลวง
            </div>
            <div style="font-size:11px;opacity:0.45;margin-top:7px;letter-spacing:0.5px">
                ปีงบประมาณ 2567–2569 &nbsp;·&nbsp; อัปเดตล่าสุด: กุมภาพันธ์ 2569
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

var_color = "#16a34a" if variance >= 0 else "#dc2626"
var_bg    = "#dcfce7" if variance >= 0 else "#fee2e2"
var_sub   = (f'<span style="background:{var_bg};color:{var_color};padding:2px 8px;'
             f'border-radius:999px;font-size:11px;font-weight:600">'
             f'{variance:+.1f}% vs แผน</span>')
risk_border = "#dc2626" if risk_count > 0 else "#16a34a"

ring_color  = "#16a34a" if variance >= 0 else "#f59e0b" if variance >= -10 else "#dc2626"

with k1:
    st.markdown(kpi_card("โครงการทั้งหมด", f"{total_proj:,} โครงการ",
                         border_color="#1A5276", icon="🏗️"),
                unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card("มูลค่าสัญญารวม", format_thai_baht(total_val),
                         border_color="#0e7490", icon="💰"),
                unsafe_allow_html=True)
with k3:
    st.markdown(progress_ring_card(
        "ความคืบหน้าจริงเฉลี่ย", avg_actual, var_sub,
        ring_color=ring_color, border_color=var_color,
    ), unsafe_allow_html=True)
with k4:
    st.markdown(kpi_card("ล่าช้า >5%", f"{risk_count:,} โครงการ",
                         border_color=risk_border, icon="⚠️",
                         pulse=(risk_count > 0)),
                unsafe_allow_html=True)
with k5:
    st.markdown(kpi_card("แล้วเสร็จ 100%", f"{done_count:,} โครงการ",
                         border_color="#16a34a", icon="✅"),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Map (full width) ─────────────────────────────────────────────────────────
st.markdown('<p class="section-header">แผนที่ความคืบหน้าตามจังหวัด</p>', unsafe_allow_html=True)
map_df = (
    filtered.groupby("จังหวัด")
            .agg(avg_actual=("จริง (%)","mean"),
                 avg_plan=("ตามแผน (%)","mean"),
                 avg_var=("ส่วนต่าง (%)","mean"),
                 count=("ชื่อสายทาง","count"),
                 total_val=("ค่างานตามสัญญา (บาท)","sum"))
            .round(2).reset_index()
)
map_df["lat"]    = map_df["จังหวัด"].map(lambda p: PROVINCE_COORDS.get(p,(None,None))[0])
map_df["lon"]    = map_df["จังหวัด"].map(lambda p: PROVINCE_COORDS.get(p,(None,None))[1])
map_df           = map_df.dropna(subset=["lat","lon"])
map_df["val_mb"] = (map_df["total_val"]/1e6).round(0)

def dot_color(v):
    if v < -10: return "#dc2626"
    if v < -5:  return "#f59e0b"
    if v < 0:   return "#facc15"
    return "#22c55e"

def dot_label(v):
    if v < -10: return "ล่าช้าวิกฤต (< -10%)"
    if v < -5:  return "ล่าช้าปานกลาง (-5 ถึง -10%)"
    if v < 0:   return "ล่าช้าเล็กน้อย (0 ถึง -5%)"
    return "เป็นไปตามแผน / เร็วกว่า"

map_df["dot_color"]  = map_df["avg_var"].apply(dot_color)
map_df["dot_status"] = map_df["avg_var"].apply(dot_label)

MAP_STYLES = {
    "🗺️ มาตรฐาน": "carto-positron",
    "🌙 โหมดมืด": "carto-darkmatter",
    "🛣️ ถนน":     "open-street-map",
}
_map_style_label = st.radio(
    "รูปแบบแผนที่",
    list(MAP_STYLES.keys()),
    horizontal=True,
    index=0,
    key="map_style_selector",
)
_selected_style = MAP_STYLES[_map_style_label]

fig_map = go.Figure()
STATUS_GROUPS = [
    ("ล่าช้าวิกฤต (< -10%)",        "#dc2626"),
    ("ล่าช้าปานกลาง (-5 ถึง -10%)", "#f59e0b"),
    ("ล่าช้าเล็กน้อย (0 ถึง -5%)",   "#facc15"),
    ("เป็นไปตามแผน / เร็วกว่า",      "#22c55e"),
]
for label, color in STATUS_GROUPS:
    sub = map_df[map_df["dot_status"]==label]
    if sub.empty: continue
    fig_map.add_trace(go.Scattermapbox(
        lat=sub["lat"], lon=sub["lon"],
        mode="markers",
        marker=dict(size=12, color=color, opacity=0.85),
        name=label,
        customdata=sub[["avg_plan","avg_actual","avg_var","count","val_mb"]].values,
        text=sub["จังหวัด"],
        hovertemplate=(
            "<b>%{text}</b><br>──────────────────<br>"
            "ตามแผน  : %{customdata[0]:.1f}%<br>"
            "จริง     : %{customdata[1]:.1f}%<br>"
            "ส่วนต่าง : <b>%{customdata[2]:+.1f}%</b><br>"
            "โครงการ : %{customdata[3]} โครงการ<br>"
            "มูลค่า   : %{customdata[4]:,.0f} ล้านบาท<extra></extra>"
        ),
        selected=dict(marker=dict(size=22, opacity=1.0)),
        unselected=dict(marker=dict(size=10, opacity=0.4)),
    ))
# Zoom + highlight driven by session state (set before the figure renders)
_ss_prov = st.session_state.get("_map_sel_prov")
if _ss_prov is not None and _ss_prov in map_df["จังหวัด"].values:
    _sp_row     = map_df[map_df["จังหวัด"] == _ss_prov].iloc[0]
    _map_center = {"lat": float(_sp_row["lat"]), "lon": float(_sp_row["lon"])}
    _map_zoom   = 7.5
    # White halo ring behind the selected dot
    fig_map.add_trace(go.Scattermapbox(
        lat=[float(_sp_row["lat"])], lon=[float(_sp_row["lon"])],
        mode="markers",
        marker=dict(size=36, color="white", opacity=0.55),
        hoverinfo="skip", showlegend=False,
    ))
    # Enlarged coloured dot on top
    fig_map.add_trace(go.Scattermapbox(
        lat=[float(_sp_row["lat"])], lon=[float(_sp_row["lon"])],
        mode="markers",
        marker=dict(size=24, color=str(_sp_row["dot_color"]), opacity=1.0),
        text=[_ss_prov],
        hovertemplate=(
            "<b>%{text}</b><br>──────────────────<br>"
            f"ตามแผนเฉลี่ย  : {_sp_row['avg_plan']:.1f}%<br>"
            f"จริงเฉลี่ย     : {_sp_row['avg_actual']:.1f}%<br>"
            f"ส่วนต่างเฉลี่ย : {_sp_row['avg_var']:+.1f}%<br>"
            f"โครงการ : {int(_sp_row['count'])} โครงการ<br>"
            f"มูลค่า   : {_sp_row['val_mb']:,.0f} ล้านบาท<extra></extra>"
        ),
        showlegend=False,
    ))
else:
    _map_center = {"lat": 13.0, "lon": 101.5}
    _map_zoom   = 4.8

fig_map.update_layout(
    mapbox=dict(style=_selected_style, zoom=_map_zoom, center=_map_center),
    margin=dict(l=0,r=0,t=0,b=0), height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    clickmode="event+select",
    legend=dict(
        title=dict(text="<b>สถานะ (จริง − แผน)</b>", font=dict(size=12)),
        orientation="v", x=0.01, y=0.99,
        xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#e2e8f0", borderwidth=1,
        font=dict(family="Sarabun", size=11),
    ),
    font=dict(family="Sarabun"),
)
map_event = st.plotly_chart(
    fig_map, use_container_width=True,
    config={"scrollZoom": True},
    on_select="rerun",
    key="province_map",
)
st.markdown("""
<div style="display:flex;gap:20px;flex-wrap:wrap;padding:8px 4px;font-size:12px;color:#475569;">
  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#dc2626;display:inline-block;"></span><b style="color:#dc2626;">ล่าช้าวิกฤต</b> &lt; −10%</span>
  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#f59e0b;display:inline-block;"></span><b style="color:#b45309;">ล่าช้าปานกลาง</b> −5 ถึง −10%</span>
  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#facc15;display:inline-block;"></span><b style="color:#854d0e;">ล่าช้าเล็กน้อย</b> 0 ถึง −5%</span>
  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#22c55e;display:inline-block;"></span><b style="color:#166534;">ตามแผน / เร็วกว่า</b></span>
  <span style="margin-left:auto;opacity:0.6;font-style:italic">💡 คลิกที่จุดบนแผนที่เพื่อดูรายละเอียดโครงการ</span>
</div>
""", unsafe_allow_html=True)

# ── Province Detail Panel (shown on map click) ────────────────────────────────
selected_province = None
if (map_event
        and hasattr(map_event, "selection")
        and map_event.selection
        and map_event.selection.points):
    pt = map_event.selection.points[0]
    # Primary: text field holds the province name directly (set via text= in the trace)
    _prov_from_text = pt.get("text")
    if _prov_from_text and _prov_from_text in map_df["จังหวัด"].values:
        selected_province = _prov_from_text
    else:
        # Fallback: nearest-province lookup via lat/lon
        sel_lat = pt.get("lat")
        sel_lon = pt.get("lon")
        if sel_lat is not None and sel_lon is not None:
            dists = (map_df["lat"] - sel_lat) ** 2 + (map_df["lon"] - sel_lon) ** 2
            selected_province = map_df.loc[dists.idxmin(), "จังหวัด"]
    if selected_province:
        _prev_prov = st.session_state.get("_map_sel_prov")
        st.session_state["_map_sel_prov"] = selected_province
        # Only rerun when the selection changed — this applies the server-side zoom
        # (_map_zoom = 7.5 from session state) which renders on the next pass.
        if _prev_prov != selected_province:
            st.rerun()

# Fallback: selection is absent on the rerun that applies the zoom; use session state
# so the detail panel still renders.
if selected_province is None:
    selected_province = st.session_state.get("_map_sel_prov")

if selected_province:
    prov_row      = map_df[map_df["จังหวัด"] == selected_province].iloc[0]
    prov_projects = filtered[filtered["จังหวัด"] == selected_province].copy()
    avg_var       = prov_row["avg_var"]

    v_color = "#dc2626" if avg_var < -10 else "#f59e0b" if avg_var < -5 else "#facc15" if avg_var < 0 else "#22c55e"
    v_label = "ล่าช้าวิกฤต" if avg_var < -10 else "ล่าช้าปานกลาง" if avg_var < -5 else "ล่าช้าเล็กน้อย" if avg_var < 0 else "เป็นไปตามแผน"

    # Close button to clear the selection
    _close_col, _ = st.columns([1, 8])
    with _close_col:
        if st.button("✕ ปิด", key="close_province_panel", use_container_width=True):
            st.session_state.pop("_map_sel_prov", None)
            st.rerun()

    # Province header banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 55%,#1A5276 100%);
                border-radius:16px;padding:22px 28px;color:white;
                margin:18px 0 14px;box-shadow:0 20px 60px rgba(15,23,42,0.35);
                position:relative;overflow:hidden;
                animation:slideInDown 0.5s cubic-bezier(0.22,1,0.36,1) both;">
        <div style="position:absolute;top:-55px;right:-55px;width:210px;height:210px;border-radius:50%;
                    background:radial-gradient(circle,rgba(41,128,185,0.22),transparent 70%)"></div>
        <div style="position:absolute;bottom:-35px;left:28%;width:150px;height:150px;border-radius:50%;
                    background:radial-gradient(circle,rgba(245,158,11,0.10),transparent 70%)"></div>
        <div style="display:flex;align-items:center;justify-content:space-between;position:relative;flex-wrap:wrap;gap:14px">
            <div style="display:flex;align-items:center;gap:18px">
                <div style="font-size:44px;filter:drop-shadow(0 4px 10px rgba(0,0,0,0.45))">📍</div>
                <div>
                    <div style="font-size:10px;opacity:0.5;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:6px">จังหวัดที่เลือก</div>
                    <div style="font-size:28px;font-weight:700;letter-spacing:0.3px;line-height:1.2">{selected_province}</div>
                    <div style="font-size:12px;opacity:0.55;margin-top:6px">
                        {int(prov_row['count'])} โครงการ &nbsp;·&nbsp; {prov_row['val_mb']:,.0f} ล้านบาท
                    </div>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.18);
                        border-radius:14px;padding:12px 22px;text-align:center;backdrop-filter:blur(8px)">
                <div style="font-size:10px;opacity:0.55;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:5px">สถานะภาพรวม</div>
                <div style="font-size:13px;font-weight:600;color:{v_color}">{v_label}</div>
                <div style="font-size:26px;font-weight:800;color:{v_color};margin-top:2px;line-height:1">{avg_var:+.1f}%</div>
                <div style="font-size:10px;opacity:0.45;margin-top:4px">จริง − แผน</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI mini row — each card slides up with a staggered delay
    dk1, dk2, dk3, dk4 = st.columns(4)
    ring_c = "#16a34a" if avg_var >= 0 else "#f59e0b" if avg_var >= -10 else "#dc2626"
    vbg    = "#dcfce7" if avg_var >= 0 else "#fee2e2"
    vc2    = "#16a34a" if avg_var >= 0 else "#dc2626"
    _wrap  = lambda html, delay: (
        f'<div style="animation:slideInUp 0.45s cubic-bezier(0.22,1,0.36,1) both;'
        f'animation-delay:{delay}s">{html}</div>'
    )
    with dk1:
        st.markdown(_wrap(kpi_card("ตามแผนเฉลี่ย", f"{prov_row['avg_plan']:.1f}%",
                                   border_color="#1A5276", icon="📋"), 0.05),
                    unsafe_allow_html=True)
    with dk2:
        st.markdown(_wrap(progress_ring_card(
            "จริงเฉลี่ย", prov_row["avg_actual"],
            f'<span style="font-size:11px;color:#64748b">{selected_province}</span>',
            ring_color=ring_c, border_color=v_color,
        ), 0.12), unsafe_allow_html=True)
    with dk3:
        st.markdown(_wrap(kpi_card(
            "ส่วนต่างเฉลี่ย", f"{avg_var:+.1f}%",
            subtitle=(f'<span style="background:{vbg};color:{vc2};padding:2px 8px;'
                      f'border-radius:999px;font-size:11px;font-weight:600">vs แผน</span>'),
            border_color=vc2, icon="📊",
        ), 0.19), unsafe_allow_html=True)
    with dk4:
        st.markdown(_wrap(kpi_card("มูลค่ารวม", f"{prov_row['val_mb']:,.0f} ล้าน",
                                   border_color="#0e7490", icon="💰"), 0.26),
                    unsafe_allow_html=True)

    st.markdown(
        f'<p class="section-header" style="animation:slideInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;'
        f'animation-delay:0.32s">รายละเอียดโครงการใน {selected_province} — {len(prov_projects)} โครงการ</p>',
        unsafe_allow_html=True,
    )

    # Inject animation for the project expanders that follow
    st.markdown("""
    <style>
    div[data-testid="stExpander"] {
        animation: slideInUp 0.38s cubic-bezier(0.22,1,0.36,1) both;
    }
    </style>
    """, unsafe_allow_html=True)

    for _row_idx, row in prov_projects.sort_values("ส่วนต่าง (%)").iterrows():
        v    = row["ส่วนต่าง (%)"] if not pd.isna(row["ส่วนต่าง (%)"]) else 0
        dot  = "🔴" if v < -10 else "🟠" if v < -5 else "🟡" if v < 0 else "🟢"
        stxt = "วิกฤต" if v < -10 else "ล่าช้า" if v < -5 else "ล่าช้าเล็กน้อย" if v < 0 else "ตามแผน"
        with st.expander(f"{dot}  {row['ชื่อสายทาง']}  ·  {stxt} ({v:+.1f}%)", key=f"prov_exp_{_row_idx}"):
            m1, m2, m3 = st.columns(3)
            m1.metric("ตามแผน (%)", f"{row['ตามแผน (%)']:.1f}%")
            m2.metric("จริง (%)",   f"{row['จริง (%)']:.1f}%")
            m3.metric("ส่วนต่าง",   f"{v:+.1f}%", delta_color="inverse")

            i1, i2, i3 = st.columns(3)
            with i1:
                contractor = str(row.get("ผู้รับจ้าง", "")).strip() or "–"
                st.markdown(f"**📋 ผู้รับจ้าง:** {contractor}")
            with i2:
                unit = str(row.get("หน่วยงานรับผิดชอบ", "")).strip() or "–"
                st.markdown(f"**🏢 หน่วยงาน:** {unit}")
            with i3:
                dist = row.get("ระยะทาง (กม.)")
                dist_txt = f"{dist:,.3f} กม." if pd.notna(dist) else "–"
                st.markdown(f"**📏 ระยะทาง:** {dist_txt}")

            prob = str(row.get("ปัญหาอุปสรรค", "")).strip()
            sol  = str(row.get("แนวทางแก้ไข",  "")).strip()
            prob_text = prob if prob and prob not in ("nan", "") else "ไม่มีข้อมูล"
            sol_text  = sol  if sol  and sol  not in ("nan", "") else "ไม่มีข้อมูล"

            st.markdown(
                f'<div style="background:#fefce8;border-left:4px solid #f59e0b;'
                f'border-radius:0 8px 8px 0;padding:10px 14px;margin-top:10px;font-size:13px;'
                f'box-shadow:0 1px 4px rgba(245,158,11,0.12)">'
                f'⚠️&nbsp;<b>สาเหตุความล่าช้า:</b>&nbsp;{prob_text}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="background:#f0fdf4;border-left:4px solid #16a34a;'
                f'border-radius:0 8px 8px 0;padding:10px 14px;margin-top:6px;font-size:13px;'
                f'box-shadow:0 1px 4px rgba(22,163,74,0.12)">'
                f'✅&nbsp;<b>แนวทางแก้ไข:</b>&nbsp;{sol_text}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

st.markdown("---")

# ── Donut + Trend ─────────────────────────────────────────────────────────────
donut_col, trend_col = st.columns([1, 2])

with donut_col:
    st.markdown('<p class="section-header">สถานะโครงการทั้งหมด</p>', unsafe_allow_html=True)
    sc = filtered["สถานะ"].value_counts().reset_index()
    sc.columns = ["สถานะ","count"]
    CM = {"แล้วเสร็จ":"#16a34a","เป็นไปตามแผน":"#2563eb",
          "ล่าช้าปานกลาง":"#f59e0b","ล่าช้าวิกฤต":"#dc2626","ไม่มีข้อมูล":"#9ca3af"}
    fig_donut = go.Figure(go.Pie(
        labels=sc["สถานะ"], values=sc["count"], hole=0.6,
        marker=dict(colors=[CM.get(s,"#9ca3af") for s in sc["สถานะ"]],
                    line=dict(color="white", width=2)),
        textinfo="percent",
        hovertemplate="%{label}: %{value} โครงการ (%{percent})<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>{total_proj:,}</b><br>โครงการ",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="Sarabun", color="#1e293b", size=16),
        align="center",
    )
    fig_donut.update_layout(
        height=340, margin=dict(l=0,r=0,t=0,b=0),
        legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=11)),
        paper_bgcolor="white", font=dict(family="Sarabun"),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with trend_col:
    st.markdown('<p class="section-header">แนวโน้มความคืบหน้าตามแผน vs จริง รายเดือน</p>', unsafe_allow_html=True)
    df_trend = (
        df_all[df_all["ปีงบประมาณ"].isin(sel_years if sel_years else years)]
        .groupby(["ปีงบประมาณ","เดือน"], observed=True)
        .agg(plan=("ตามแผน (%)","mean"), actual=("จริง (%)","mean"))
        .round(2).reset_index()
    )
    fig_trend = go.Figure()
    colors = ["#1A5276","#27AE60","#E67E22"]

    for i, yr in enumerate(sorted(df_trend["ปีงบประมาณ"].unique())):
        sub = df_trend[df_trend["ปีงบประมาณ"]==yr].copy()
        c = colors[i % 3]
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        months_list = sub["เดือน"].astype(str).tolist()

        x_fill = months_list + months_list[::-1]
        y_fill = sub["actual"].tolist() + sub["plan"].tolist()[::-1]
        fig_trend.add_trace(go.Scatter(
            x=x_fill, y=y_fill,
            fill="toself",
            fillcolor=f"rgba({r},{g},{b},0.08)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
            hoverinfo="skip",
        ))
        fig_trend.add_trace(go.Scatter(
            x=months_list, y=sub["actual"],
            name=f"จริง {yr}", line=dict(color=c, width=2.5),
            mode="lines+markers", marker=dict(size=6),
        ))
        fig_trend.add_trace(go.Scatter(
            x=months_list, y=sub["plan"],
            name=f"แผน {yr}", line=dict(color=c, width=2, dash="dot"),
            mode="lines+markers", marker=dict(size=5),
        ))

    fig_trend.update_layout(
        height=340, margin=dict(l=0,r=0,t=10,b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        yaxis=dict(ticksuffix="%", range=[0,105]),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Sarabun"),
    )
    fig_trend.update_xaxes(showgrid=False)
    fig_trend.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("""
    <div style="background:#fefce8;border-left:4px solid #f59e0b;
                border-radius:0 8px 8px 0;padding:10px 16px;font-size:12px;
                color:#78350f;line-height:1.7;margin-top:-8px">
        <b>⚠️ หมายเหตุ:</b> กราฟแสดงค่าเฉลี่ย % ความคืบหน้าของโครงการที่มีข้อมูลในแต่ละเดือน
        โครงการที่แล้วเสร็จ (100%) มักหยุดรายงานในช่วงกลางปี ทำให้ค่าเฉลี่ยหลังเดือนมิถุนายนลดลง
        และโครงการใหม่ที่เริ่มในช่วง กรกฎาคม–กันยายน จะเข้าสู่ฐานข้อมูลด้วยความคืบหน้าต่ำ
        ส่งผลให้เส้นกราฟดูเหมือนถดถอย <b>แต่ไม่ได้สะท้อนผลการดำเนินงานที่แย่ลงจริง</b>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Type Bar + Province Bar ───────────────────────────────────────────────────
type_col, prov_col = st.columns([1, 2])

with type_col:
    st.markdown('<p class="section-header">แผน vs จริง ตามประเภทโครงการ</p>', unsafe_allow_html=True)
    proj_df = (
        filtered.groupby("ประเภทโครงการ")
                .agg(avg_plan=("ตามแผน (%)","mean"), avg_actual=("จริง (%)","mean"))
                .round(1).reset_index().sort_values("avg_actual", ascending=True)
    )
    fig_proj = go.Figure()
    fig_proj.add_trace(go.Bar(
        y=proj_df["ประเภทโครงการ"], x=proj_df["avg_plan"],
        name="ตามแผน", orientation="h", marker_color="#CBD5E1", opacity=0.8,
    ))
    fig_proj.add_trace(go.Bar(
        y=proj_df["ประเภทโครงการ"], x=proj_df["avg_actual"],
        name="จริง", orientation="h", marker_color="#1A5276",
        text=proj_df["avg_actual"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
    ))
    fig_proj.update_layout(
        barmode="overlay", height=430,
        margin=dict(l=0,r=60,t=10,b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Sarabun"),
        xaxis=dict(range=[0,115], ticksuffix="%", title=""),
        yaxis=dict(title=""),
    )
    fig_proj.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_proj, use_container_width=True)

with prov_col:
    st.markdown('<p class="section-header">ความคืบหน้าตามจังหวัด (Top 15) — แผน vs จริง</p>', unsafe_allow_html=True)
    prov_df = (
        filtered.groupby("จังหวัด")
                .agg(avg_actual=("จริง (%)","mean"),
                     avg_plan=("ตามแผน (%)","mean"),
                     count=("ชื่อสายทาง","count"))
                .round(1).reset_index()
                .sort_values("avg_actual", ascending=True).tail(15)
    )
    bar_colors = [
        "#dc2626" if v < 50 else "#f59e0b" if v < 75 else "#16a34a"
        for v in prov_df["avg_actual"]
    ]
    fig_prov = go.Figure()
    fig_prov.add_trace(go.Bar(
        y=prov_df["จังหวัด"], x=prov_df["avg_plan"],
        name="ตามแผน", orientation="h",
        marker_color="#CBD5E1", opacity=0.8,
        hovertemplate="%{y}: แผน %{x:.1f}%<extra></extra>",
    ))
    fig_prov.add_trace(go.Bar(
        y=prov_df["จังหวัด"], x=prov_df["avg_actual"],
        name="จริง", orientation="h",
        marker_color=bar_colors,
        text=prov_df["avg_actual"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="%{y}: จริง %{x:.1f}%<extra></extra>",
    ))
    fig_prov.update_layout(
        barmode="overlay", height=430,
        margin=dict(l=0,r=70,t=10,b=0),
        legend=dict(orientation="h", y=1.02, x=0),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Sarabun"),
        xaxis=dict(range=[0,120], ticksuffix="%", title=""),
        yaxis=dict(title=""),
    )
    fig_prov.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_prov, use_container_width=True)

# ── Scatter + At-Risk ─────────────────────────────────────────────────────────
col_s1, col_s2 = st.columns([1.5, 1])

with col_s1:
    st.markdown('<p class="section-header">ภาพรวมพอร์ตโฟลิโอโครงการ (มูลค่าสัญญา)</p>', unsafe_allow_html=True)
    tree_df = filtered[
        ["ประเภทโครงการ","จังหวัด","ชื่อสายทาง",
         "ค่างานตามสัญญา (บาท)","ตามแผน (%)","ส่วนต่าง (%)","จริง (%)"]
    ].copy()
    tree_df = tree_df[
        tree_df["ค่างานตามสัญญา (บาท)"].notna() &
        (tree_df["ค่างานตามสัญญา (บาท)"] > 0) &
        (tree_df["ชื่อสายทาง"].str.strip() != "")
    ].copy()
    tree_df["val_mb"] = (tree_df["ค่างานตามสัญญา (บาท)"] / 1e6).round(1)

    # ── 3-level treemap with maxdepth=2: all data kept, only 2 levels rendered ───
    # maxdepth=2 means the browser draws ~20-30 tiles at a time instead of
    # hundreds. Clicking a project type reveals provinces+routes for that branch.

    # Route nodes (leaves)
    lf = tree_df.copy()
    lf["_id"]  = (lf["ประเภทโครงการ"].astype(str) + "||" +
                  lf["จังหวัด"].astype(str) + "||" +
                  lf.index.astype(str))
    lf["_par"] = lf["ประเภทโครงการ"].astype(str) + "||" + lf["จังหวัด"].astype(str)
    _d    = lf["ส่วนต่าง (%)"].fillna(0)
    _a    = lf["จริง (%)"].fillna(0)
    _pl   = lf["ตามแผน (%)"].fillna(0)
    _mb   = (lf["ค่างานตามสัญญา (บาท)"] / 1e6).round(1)
    _dr   = _d.round(1)
    _icon = pd.Series("🟢", index=lf.index)
    _icon = _icon.where(_d >= 0,   "🟡")
    _icon = _icon.where(_d >= -5,  "🟠")
    _icon = _icon.where(_d >= -10, "🔴")
    _sign = pd.Series("+", index=lf.index).where(_dr >= 0, "")
    lf["_txt"] = (lf["ชื่อสายทาง"] + "<br>" +
                  "💰 " + _mb.astype(str) + " ล้าน<br>" +
                  "📋 " + _pl.round(1).astype(str) + "%" +
                  "  📊 " + _a.round(1).astype(str) + "%<br>" +
                  _icon + " " + (_sign + _dr.astype(str)) + "%")
    lf["_val"] = lf["ค่างานตามสัญญา (บาท)"]
    lf["_c0"]  = _d;  lf["_c1"] = _a;  lf["_c2"] = _mb;  lf["_c3"] = _pl
    lf["_lbl"] = lf["ชื่อสายทาง"]

    # Province nodes
    pv = (lf.groupby(["ประเภทโครงการ","จังหวัด"], sort=False)
            .agg(_c0=("_c0","mean"), _c1=("_c1","mean"),
                 _c2=("_c2","sum"),  _c3=("_c3","mean"))
            .reset_index())
    pv["_id"]  = pv["ประเภทโครงการ"].astype(str) + "||" + pv["จังหวัด"].astype(str)
    pv["_par"] = pv["ประเภทโครงการ"].astype(str)
    pv["_lbl"] = pv["จังหวัด"].astype(str)
    pv["_txt"] = pv["จังหวัด"].astype(str)   # overview: name only
    pv["_val"] = 0.0

    # Project type nodes
    pt = (lf.groupby("ประเภทโครงการ", sort=False)
            .agg(_c0=("_c0","mean"), _c1=("_c1","mean"),
                 _c2=("_c2","sum"),  _c3=("_c3","mean"))
            .reset_index())
    pt["_id"]  = pt["ประเภทโครงการ"].astype(str)
    pt["_par"] = ""
    pt["_lbl"] = pt["ประเภทโครงการ"].astype(str)
    pt["_txt"] = pt["ประเภทโครงการ"].astype(str)
    pt["_val"] = 0.0

    _cols = ["_id","_lbl","_par","_val","_c0","_c1","_c2","_c3","_txt"]
    nodes = pd.concat([pt[_cols], pv[_cols], lf[_cols]], ignore_index=True)

    fig_tree = go.Figure(go.Treemap(
        ids          = nodes["_id"].tolist(),
        labels       = nodes["_lbl"].tolist(),
        parents      = nodes["_par"].tolist(),
        values       = nodes["_val"].tolist(),
        branchvalues = "remainder",
        maxdepth     = 2,
        text         = nodes["_txt"].tolist(),
        textinfo     = "text",
        customdata   = nodes[["_c0","_c1","_c2","_c3"]].values.tolist(),
        hovertemplate=(
            "<b>%{label}</b><br>──────────────────<br>"
            "มูลค่า   : %{customdata[2]:,.1f} ล้านบาท<br>"
            "แผน      : %{customdata[3]:.1f}%<br>"
            "จริง     : %{customdata[1]:.1f}%<br>"
            "ส่วนต่าง : %{customdata[0]:+.1f}%"
            "<extra></extra>"
        ),
        marker=dict(
            colors    = nodes["_c0"].tolist(),
            colorscale=[
                [0.0,  "#dc2626"],
                [0.35, "#f59e0b"],
                [0.55, "#facc15"],
                [1.0,  "#16a34a"],
            ],
            cmin=-15, cmax=5,
            line=dict(width=2, color="white"),
            colorbar=dict(title="ส่วนต่าง<br>(%)", ticksuffix="%",
                          thickness=12, len=0.7),
        ),
        textfont     = dict(family="Sarabun", size=13),
        textposition = "middle center",
    ))
    fig_tree.update_layout(
        height=700,
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Sarabun"),
    )
    st.plotly_chart(fig_tree, use_container_width=True)
    st.caption("ขนาด = มูลค่าสัญญา · สี = ส่วนต่างเฉลี่ย (แดง = ล่าช้า · เขียว = เร็วกว่าแผน)")

with col_s2:
    st.markdown('<p class="section-header">โครงการที่ล่าช้ามากที่สุด</p>', unsafe_allow_html=True)
    risk_df = (
        filtered[filtered["ส่วนต่าง (%)"] < -5]
        [["ชื่อสายทาง","จังหวัด","ตามแผน (%)","จริง (%)","ส่วนต่าง (%)","ปัญหาอุปสรรค"]]
        .sort_values("ส่วนต่าง (%)").head(10)
    )
    if risk_df.empty:
        st.success("ไม่มีโครงการที่ล่าช้าเกิน 5% ในตัวกรองที่เลือก")
    else:
        for rank, (_row_idx, row) in enumerate(risk_df.iterrows(), start=1):
            v     = row["ส่วนต่าง (%)"]
            plan  = row["ตามแผน (%)"]
            actual= row["จริง (%)"]
            if pd.isna(v): continue
            icon  = "🔴" if v < -10 else "🟠"
            label = "⚠ วิกฤต" if v < -10 else "⚠ ล่าช้า"
            title = f"{icon}  #{rank}  {row['ชื่อสายทาง']}  ·  {row['จังหวัด']}  ·  {label} {v:+.1f}%"
            with st.expander(title, key=f"risk_exp_{_row_idx}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("ตามแผน (%)", f"{plan:.1f}%"   if pd.notna(plan)   else "–")
                c2.metric("จริง (%)",   f"{actual:.1f}%" if pd.notna(actual) else "–")
                c3.metric("ส่วนต่าง",   f"{v:+.1f}%", delta_color="inverse")
                st.caption(f"📍 จังหวัด: {row['จังหวัด']}")
                prob = str(row.get("ปัญหาอุปสรรค", "")).strip()
                if prob and prob not in ("nan", ""):
                    st.info(f"สาเหตุ: {prob}", icon="ℹ️")

st.markdown("---")

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">ตารางข้อมูลละเอียด</p>', unsafe_allow_html=True)
search = st.text_input("", placeholder="🔎  ค้นหาชื่อสายทาง / จังหวัด / ผู้รับจ้าง...", label_visibility="collapsed")
table_cols = ["ปีงบประมาณ","จังหวัด","ชื่อสายทาง","ระยะทาง (กม.)","ค่างานตามสัญญา (บาท)",
              "ตามแผน (%)","จริง (%)","ส่วนต่าง (%)","สถานะ","ผู้รับจ้าง",
              "ปัญหาอุปสรรค","แนวทางแก้ไข"]
table_df = filtered[table_cols].copy()
table_df["ปัญหาอุปสรรค"] = table_df["ปัญหาอุปสรรค"].fillna("").replace("", "ไม่มีข้อมูล")
table_df["แนวทางแก้ไข"]  = table_df["แนวทางแก้ไข"].fillna("").replace("", "ไม่มีข้อมูล")
if search:
    mask = (
        table_df["ชื่อสายทาง"].str.contains(search, na=False) |
        table_df["จังหวัด"].str.contains(search, na=False) |
        table_df["ผู้รับจ้าง"].str.contains(search, na=False)
    )
    table_df = table_df[mask]

def color_variance(val):
    if pd.isna(val): return ""
    if val < -10: return "background-color:#fee2e2; color:#991b1b; font-weight:bold"
    if val < -5:  return "background-color:#fef3c7; color:#92400e; font-weight:bold"
    if val >= 0:  return "background-color:#dcfce7; color:#166534"
    return ""

PAGE_SIZE = 10
total_rows = len(table_df)
total_pages = max(1, -(-total_rows // PAGE_SIZE))  # ceiling division

if "table_page" not in st.session_state:
    st.session_state.table_page = 0
# reset to page 0 whenever filters or search change
if st.session_state.get("_last_table_len") != total_rows:
    st.session_state.table_page = 0
    st.session_state["_last_table_len"] = total_rows

page = st.session_state.table_page
start = page * PAGE_SIZE
end   = min(start + PAGE_SIZE, total_rows)
page_df = table_df.iloc[start:end]

styled = (
    page_df.style
    .map(color_variance, subset=["ส่วนต่าง (%)"])
    .format({
        "ค่างานตามสัญญา (บาท)":"{:,.0f}",
        "ระยะทาง (กม.)":"{:.2f}",
        "ตามแผน (%)":"{:.1f}%",
        "จริง (%)":"{:.1f}%",
        "ส่วนต่าง (%)":"{:+.1f}%",
    }, na_rep="-")
)
st.dataframe(styled, use_container_width=True, hide_index=True)

# Pagination controls
pc_left, pc_mid, pc_right = st.columns([1, 2, 1])
with pc_left:
    if st.button("← ก่อนหน้า", disabled=(page == 0), use_container_width=True):
        st.session_state.table_page -= 1
        st.rerun()
with pc_mid:
    st.markdown(
        f'<div style="text-align:center;padding:6px 0;font-size:13px;color:#64748b;">'
        f'หน้า <b style="color:#0f172a">{page+1}</b> จาก <b style="color:#0f172a">{total_pages}</b>'
        f'&nbsp;·&nbsp; แสดง {start+1}–{end} จาก {total_rows:,} โครงการ</div>',
        unsafe_allow_html=True,
    )
with pc_right:
    if st.button("ถัดไป →", disabled=(page >= total_pages - 1), use_container_width=True):
        st.session_state.table_page += 1
        st.rerun()

