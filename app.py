import streamlit as st
import commands
import utils

st.set_page_config(
    page_title="داشبورد رمزارز گنجه",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
        color: #e0f2f7;
        direction: rtl; /* Apply RTL to the entire body */
        text-align: right; /* Align text to the right */
    }}

    .main {{
        background-color: #34495e;
        padding: 20px;
        border-radius: 10px;
    }}
    .stApp {{
        background-color: #34495e;
    }}

    .sidebar .sidebar-content {{
        background-color: #000000;
        color: #e0f2f7;
    }}
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {{
        color: #e0f2f7;
        text-align: right; /* Ensure sidebar headers are right-aligned */
    }}
    .stRadio > label {{
        color: #e0f2f7;
        text-align: right; /* Ensure radio button text is right-aligned */
    }}
    .stRadio [data-testid="stRadio"] > div > label {{
        color: #e0f2f7;
        text-align: right; /* Specific selector for radio button text alignment */
    }}
    /* Ensure radio button options themselves are right-aligned */
    .stRadio > div[data-baseweb="radio"] > label {{
        flex-direction: row-reverse; /* Swap icon and text direction */
        justify-content: flex-end; /* Align content to the right */
    }}


    h1, h2, h3, h4, h5, h6 {{
        color: #e94560;
        text-align: right; /* Align headings to the right */
    }}

    .stButton>button {{
        background-color: #a7d9e8;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        direction: rtl; /* Apply RTL to button text */
    }}
    .stButton>button:hover {{
        background-color: #7bc6e0;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }}

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div {{
        background-color: #16213e;
        color: #e0e0e0;
        border-radius: 8px;
        border: 1px solid #533483;
        padding: 10px;
        direction: rtl; /* Apply RTL to input fields */
        text-align: right; /* Align text within input fields to the right */
    }}
    .stSelectbox > div[data-baseweb="select"] ul {{
        background-color: #16213e;
        color: #e0e0e0;
        direction: rtl; /* Apply RTL to selectbox dropdown options */
        text-align: right; /* Align text within selectbox dropdown options to the right */
    }}
    .stSelectbox > div[data-baseweb="select"] li:hover {{
        background-color: #0f3460;
    }}

    .stAlert {{
        border-radius: 8px;
        direction: rtl; /* Apply RTL to alerts */
        text-align: right; /* Align alert text to the right */
    }}
    .stCode {{
        background-color: #16213e;
        border-radius: 8px;
        padding: 15px;
        direction: rtl; /* Apply RTL to code blocks */
        text-align: right; /* Align code block text to the right */
    }}
    .stExpander {{
        background-color: #16213e;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        direction: rtl; /* Apply RTL to expanders */
        text-align: right; /* Align expander text to the right */
    }}
    .stExpander > div > div > p {{
        color: #e0e0e0;
    }}

    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #16213e;
        color: #e0e0e0;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9em;
        direction: rtl; /* Apply RTL to footer */
    }}
    .footer a {{
        color: #e94560;
        text-decoration: none;
    }}
    .footer a:hover {{
        text-decoration: underline;
    }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("📈 داشبورد رمزارز گنجه")
st.markdown("به داشبورد جامع رمزارز گنجه خوش آمدید! از ابزارهای زیر برای دریافت اطلاعات لحظه‌ای بازار استفاده کنید.")

st.sidebar.header("دستورات")
command_choice = st.sidebar.radio(
    "یک دستور را انتخاب کنید:",
    (
        "مقدمه",
        "جستجوی کوین",
        "کوین‌های پرطرفدار",
        "سلطه بازار",
        "دارایی شرکت‌ها",
        "دسته‌بندی‌های کوین",
        "جزئیات کوین (بر اساس نام)",
        "جزئیات کوین (بر اساس آدرس)",
        "تراز قدرت (BOP)",
        "شاخص قدرت نسبی (RSI)",
        "توکن‌های برتر تقویت‌شده",
        "آخرین توکن‌های تقویت‌شده",
        "سفارشات توکن",
        "اطلاعات معاملاتی"
    ),
    index=0
)

coin_name_translations = {
    "bitcoin": "بیت‌کوین",
    "ethereum": "اتریوم"
}

if command_choice == "مقدمه":
    commands.display_introduction()

elif command_choice == "جستجوی کوین":
    commands.display_search_coin()

elif command_choice == "کوین‌های پرطرفدار":
    commands.display_trending_coins()

elif command_choice == "سلطه بازار":
    commands.display_market_dominance()

elif command_choice == "دارایی شرکت‌ها":
    commands.display_companies_holdings(coin_name_translations)

elif command_choice == "دسته‌بندی‌های کوین":
    commands.display_coin_categories()

elif command_choice == "جزئیات کوین (بر اساس نام)":
    commands.display_coin_details_by_name()

elif command_choice == "جزئیات کوین (بر اساس آدرس)":
    commands.display_coin_details_by_address()

elif command_choice == "تراز قدرت (BOP)":
    commands.display_bop()

elif command_choice == "شاخص قدرت نسبی (RSI)":
    commands.display_rsi()

elif command_choice == "توکن‌های برتر تقویت‌شده":
    commands.display_top_boosted_tokens()

elif command_choice == "آخرین توکن‌های تقویت‌شده":
    commands.display_latest_boosted_tokens()

elif command_choice == "سفارشات توکن":
    commands.display_token_orders()

elif command_choice == "اطلاعات معاملاتی":
    commands.display_trade_info()

st.markdown(
    """
    <div class='footer'>
        توسعه‌دهنده: پرهام لیلیان
        <br>
        اینستاگرام: <a href='https://instagram.com/parhamlilian' target='_blank' style='color: #e94560;'>@parhamlilian</a>
        <br>
        لینکدین: <a href='https://www.linkedin.com/in/parhamlilian' target='_blank' style='color: #e94560;'>linkedin.com/in/parhamlilian</a>
    </div>
    """, unsafe_allow_html=True
)
