import streamlit as st
import commands
import utils

# --- Initial Page Config ---
st.set_page_config(
    page_title="داشبورد رمزارز گنجه",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dark Theme CSS ---
custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* General styling for text and font */
    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
        color: #e0f2f7;
    }}

    /* Main content area styling */
    .main {{
        background-color: #34495e;
        padding: 20px;
        border-radius: 10px;
    }}
    .stApp {{
        background-color: #34495e;
    }}

    /* Sidebar styling (Commands Menu) */
    .sidebar .sidebar-content {{
        background-color: #000000;
        color: #e0f2f7;
    }}
    /* Adjust sidebar header and radio button text color for consistency */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {{
        color: #e0f2f7; /* Ensure sidebar headers are light */
    }}
    .stRadio > label {{ /* Targeting radio button labels in sidebar */
        color: #e0f2f7; /* Ensure radio button text is light */
    }}
    .stRadio [data-testid="stRadio"] > div > label {{
        color: #e0f2f7; /* Specific selector for radio button text */
    }}


    /* Titles and headings styling */
    h1, h2, h3, h4, h5, h6 {{
        color: #e94560; /* Vibrant accent color for titles */
        text-align: left;
    }}

    /* Button styling */
    .stButton>button {{
        background-color: #a7d9e8; /* Dark blue for buttons */
        color: white; /* White text on buttons for good contrast */
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button:hover {{
        background-color: #7bc6e0; /* Purple on hover for interactivity */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }}

    /* Input fields and Selectboxes styling */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div {{
        background-color: #16213e; /* Slightly lighter dark blue for input fields */
        color: #e0e0e0; /* Light text color for input */
        border-radius: 8px;
        border: 1px solid #533483; /* Accent border color */
        padding: 10px;
    }}
    /* Styling for dropdown options in selectbox */
    .stSelectbox > div[data-baseweb="select"] ul {{
        background-color: #16213e; /* Dropdown menu background */
        color: #e0e0e0; /* Dropdown menu text color */
    }}
    .stSelectbox > div[data-baseweb="select"] li:hover {{
        background-color: #0f3460; /* Dropdown menu item hover */
    }}


    /* Other Streamlit elements styling */
    .stAlert {{
        border-radius: 8px;
    }}
    .stCode {{
        background-color: #16213e; /* Darker background for code blocks */
        border-radius: 8px;
        padding: 15px;
    }}
    .stExpander {{
        background-color: #16213e; /* Darker background for expanders */
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }}
    .stExpander > div > div > p {{
        color: #e0e0e0;
    }}

    /* Footer styling */
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #16213e; /* Footer background */
        color: #e0e0e0;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9em;
    }}
    .footer a {{
        color: #e94560; /* Accent color for footer links */
        text-decoration: none;
    }}
    .footer a:hover {{
        text-decoration: underline;
    }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Main Dashboard Title and Welcome Message ---
st.title("📈 داشبورد رمزارز گنجه")
st.markdown("به داشبورد جامع رمزارز گنجه خوش آمدید! از ابزارهای زیر برای دریافت اطلاعات لحظه‌ای بازار استفاده کنید.")

# --- Sidebar Navigation (Commands Menu) ---
st.sidebar.header("دستورات")
# This is for picking what command to run from the sidebar.
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
    index=0 # Starts on the Introduction page
)

# Small helper for coin names (not a big deal, just for display)
coin_name_translations = {
    "bitcoin": "بیت‌کوین",
    "ethereum": "اتریوم"
}

# --- Command Logic: What happens when you pick a command ---
# Now calling functions from the 'commands' module for each choice.

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

# --- Footer Section ---
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
