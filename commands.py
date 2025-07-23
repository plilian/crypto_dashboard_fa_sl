import streamlit as st
import utils
import api_client
import pandas as pd
from datetime import datetime
import uuid

coin_name_translations = {
    "bitcoin": "بیت‌کوین",
    "ethereum": "اتریوم"
}

def display_introduction():
    st.header("👋 به گنجه خوش آمدید!")
    st.markdown(
        """
        من اینجا هستم تا به شما کمک کنم از آخرین اطلاعات ارزهای دیجیتال مطلع شوید.
        می‌توانید از منوی سمت چپ برای دسترسی به امکانات من استفاده کنید.
        """
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(
            "<div style='text-align: center;'>",
            unsafe_allow_html=True
        )
        st.image("https://i.postimg.cc/wM9hDkM8/photo-2024-12-05-16-24-30.jpg", width=250)
        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )
    st.markdown("<div style='margin-top: 20px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        💡 توضیحات دستورات:

        * **جستجوی کوین:** این گزینه را انتخاب کنید تا یک ارز دیجیتال را جستجو کرده و اطلاعات اولیه مانند نام، نماد و رتبه بازار آن را دریافت کنید.
        * **کوین‌های پرطرفدار:** این گزینه را برای مشاهده لیستی از ارزهای دیجیتال که در حال حاضر بر اساس فعالیت بازار ترند هستند، انتخاب کنید.
        * **سلطه بازار:** این نشان می‌دهد که ارزهای دیجیتال بزرگی مانند بیت‌کوین و اتریوم چقدر از بازار را کنترل می‌کنند.
        * **دارایی شرکت‌ها:** اطلاعاتی در مورد شرکت‌هایی که مقادیر زیادی از ارزهای دیجیتال خاص (مانند بیت‌کوین یا اتریوم) را نگهداری می‌کنند، دریافت کنید.
        * **دسته‌بندی کوین‌ها:** ۳ دسته‌بندی برتر ارزهای دیجیتال را بر اساس تغییرات ارزش بازار آن‌ها در ۲۴ ساعت گذشته نشان می‌دهد.
        * **جزئیات کوین (بر اساس نام):** اطلاعات دقیق در مورد یک کوین را فقط با تایپ نام آن دریافت کنید.
        * **جزئیات کوین (بر اساس آدرس):** اطلاعات دقیق در مورد یک کوین را با استفاده از آدرس قرارداد آن دریافت کنید (برای سولانا یا اتریوم کار می‌کند).
        * **تراز قدرت (BOP):** BOP را برای یک ارز دیجیتال در طی ۱، ۷ یا ۱۴ روز محاسبه می‌کند. این مربوط به فشار خرید/فروش است.
        * **شاخص قدرت نسبی (RSI):** RSI را برای یک ارز دیجیتال در ۱۴ روز گذشته محاسبه می‌کند. به تشخیص اینکه آیا بیش از حد خرید شده یا بیش از حد فروخته شده است، کمک می‌کند.
        * **توکن‌های برتر تقویت‌شده:** ببینید کدام توکن‌ها بیشترین "تقویت" را در DexScreener دریافت می‌کنند.
        * **آخرین توکن‌های تقویت‌شده:** جدیدترین توکن‌هایی که در DexScreener تقویت شده‌اند را بررسی کنید.
        * **سفارشات توکن:** جزئیات مربوط به سفارشات توکن برای اتریوم یا سولانا را دریافت کنید.
        * **اطلاعات معاملاتی:** این اطلاعات معاملاتی برای یک توکن مانند قیمت، حجم و تراکنش‌های اخیر را به شما می‌دهد.

        سوال یا نیاز به کمک بیشتر دارید؟ فقط بپرسید! ☺️
        """
    )

def display_search_coin():
    st.header("🔎 جستجوی کوین")
    coin_query = st.text_input("نام یا نماد کوین را وارد کنید (مانند: bitcoin, btc)", key="search_input")
    if st.button("جستجو"):
        if coin_query:
            utils.log_command_usage("/search", coin_query)
            with st.spinner(f"در حال جستجو برای {coin_query}..."):
                data, error = api_client.fetch_search_data(coin_query)
                if data:
                    st.success("نتایج جستجو یافت شد!")
                    st.markdown(f"""
                        🔎 نتایج جستجو
                        - شناسه: `{data['coin_id']}`
                        - نام: *{data['name']}*
                        - رتبه بازار: #{data['market_cap_rank']}
                        - نماد: `{data['symbol'].upper()}`

                        جزئیات قیمت (دلار آمریکا):
                        - قیمت فعلی: `${data['usd_price']:,.10f}`
                        - ارزش بازار: `${data['usd_market_cap']:,.2f}`
                        - حجم معاملات ۲۴ ساعته: `${data['usd_24h_vol']:,.2f}`
                        - تغییر ۲۴ ساعته: `{data['usd_24h_change']:.2f}%`
                    """)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک نام یا نماد کوین برای جستجو وارد کنید.")

def display_trending_coins():
    st.header("🔥 ارزهای دیجیتال پرطرفدار")
    if st.button("دریافت کوین‌های پرطرفدار"):
        utils.log_command_usage("/trending", "")
        with st.spinner("در حال دریافت کوین‌های پرطرفدار..."):
            data, error = api_client.fetch_trending_data()
            if data:
                st.success("کوین‌های پرطرفدار با موفقیت دریافت شدند!")
                message = "🔥 توکن‌های پرطرفدار:\n\n"
                for coin in data:
                    message += (
                        f"- نام: *{coin['name']}*\n"
                        f"- نماد: `{coin['symbol'].upper()}`\n"
                        f"- رتبه: #{coin['rank']}\n"
                        f"- قیمت فعلی: `${coin['usd_price']}`\n"
                        f"- ارزش بازار: `{coin['market_cap']}`\n"
                        f"- ارزش بازار (BTC): `{coin['market_cap_btc']} BTC`\n"
                        f"- حجم کل (USD): `{coin['total_volume']}`\n"
                        f"- حجم کل (BTC): `{coin['total_volume_btc']} BTC`\n"
                        "---------------------------\n"
                    )
                st.markdown(message)
            else:
                st.error(error)

def display_market_dominance():
    st.header("📊 سلطه بازار ارز دیجیتال")
    if st.button("دریافت داده‌های سلطه"):
        utils.log_command_usage("/dominance", "")
        with st.spinner("در حال دریافت داده‌های سلطه بازار..."):
            data, error = api_client.fetch_dominance_data()
            if data:
                st.success("داده‌های سلطه بازار با موفقیت دریافت شدند!")
                st.markdown(f"""
                    📊 سلطه بازار ارز دیجیتال
                    - ارزهای دیجیتال فعال: `{data['active_cryptocurrencies']}`
                    - سلطه بیت‌کوین: `{data['btc_dominance']:.2f}%`
                    - سلطه اتریوم: `{data['eth_dominance']:.2f}%`
                    - سلطه تتر: `{data['usdt_dominance']:.2f}%`
                    - تغییر ارزش بازار ۲۴ ساعته: `{data['market_cap_change_24h']:.2f}%`
                """)
            else:
                st.error(error)

def display_companies_holdings(coin_translations):
    st.header("🏦 دارایی‌های خزانه‌داری عمومی شرکت‌ها")
    company_coin_choice = st.selectbox(
        "انتخاب کوین:",
        ("bitcoin", "ethereum"),
        key="company_coin_select"
    )
    translated_coin_name = coin_translations.get(company_coin_choice, company_coin_choice.capitalize())
    if st.button("دریافت داده‌های شرکت‌ها"):
        utils.log_command_usage("/companies", company_coin_choice)
        with st.spinner(f"در حال دریافت شرکت‌های دارای {translated_coin_name}..."):
            data, error = api_client.fetch_companies_data(company_coin_choice)
            if data:
                st.success(f"شرکت‌های دارای {translated_coin_name} با موفقیت دریافت شدند!")
                message = (
                    f"🏦 شرکت‌های دارای {translated_coin_name} 🏦\n"
                    f"- کل دارایی‌ها: `{data['total_holdings']}`\n"
                    f"- ارزش کل (USD): `${data['total_value_usd']:,.2f}`\n"
                    f"- سلطه ارزش بازار: `{data['market_cap_dominance']}%`\n\n"
                    f"شرکت‌های برتر:\n\n"
                )
                for company in data['companies']:
                    message += (
                        f"- نام: *{company.get('name', 'N/A')}* ({company.get('symbol', 'N/A')})\n"
                        f"- کشور: `{company.get('country', 'N/A')}`\n"
                        f"- دارایی‌ها: `{company.get('total_holdings', 'N/A')}`\n"
                        f"- ارزش فعلی (USD): `${company.get('total_current_value_usd', 'N/A'):,.2f}`\n"
                        f"- درصد از کل عرضه: `{company.get('percentage_of_total_supply', 'N/A')}%`\n"
                        "---------------------------\n"
                    )
                st.markdown(message)
            else:
                st.error(error)

def display_coin_categories():
    st.header("🏅 دسته‌بندی‌های برتر کوین")
    if st.button("دریافت دسته‌بندی‌ها"):
        utils.log_command_usage("/categories", "")
        with st.spinner("در حال دریافت دسته‌بندی‌های برتر کوین..."):
            data, error = api_client.fetch_categories_data()
            if data:
                st.success("دسته‌بندی‌های کوین با موفقیت دریافت شدند!")
                message = "🏅 ۳ دسته‌بندی برتر کوین (بر اساس تغییر ارزش بازار ۲۴ ساعته) 🏅\n\n"
                for category in data:
                    name = category.get("name", "N/A")
                    market_cap = category.get("market_cap", 0)
                    market_cap_change = category.get("market_cap_change_24h", 0)
                    top_3_coins_id = category.get("top_3_coins_id", [])

                    message += (
                        f"- نام دسته‌بندی: `{name}`\n"
                        f"- ارزش بازار: `${market_cap:,.2f}`\n"
                        f"- تغییر ۲۴ ساعته: `{market_cap_change:.2f}%`\n"
                        f"- ۳ توکن برتر: `{', '.join(top_3_coins_id) if top_3_coins_id else 'N/A'}`\n"
                        "------------------------------------\n"
                    )
                st.markdown(message)
            else:
                st.error(error)

def display_coin_details_by_name():
    st.header("🪙 جزئیات کوین بر اساس نام/نماد")
    coin_name_query = st.text_input("نام یا نماد کوین را وارد کنید (مانند: btc, ethereum)", key="coin_details_name_input")
    if st.button("دریافت جزئیات بر اساس نام"):
        if coin_name_query:
            utils.log_command_usage("/coin_details_name", coin_name_query)
            with st.spinner(f"در حال دریافت جزئیات برای {coin_name_query}..."):
                data, error = api_client.fetch_coin_details_by_name(coin_name_query)
                if data:
                    st.success(f"جزئیات برای {coin_name_query} با موفقیت دریافت شد!")
                    description = data.get("description", {}).get("en", "توضیحاتی در دسترس نیست.")
                    truncated_description = description[:500] + "..." if len(description) > 500 else description

                    tickers = data.get("tickers", [])
                    first_ticker_info = {}
                    if tickers:
                        first_ticker = tickers[0]
                        first_ticker_info = {
                            "base": first_ticker.get("base"),
                            "target": first_ticker.get("target"),
                            "market_name": first_ticker.get("market", {}).get("name"),
                            "converted_last_usd": first_ticker.get("converted_last", {}).get("usd"),
                            "converted_volume_usd": first_ticker.get("converted_volume", {}).get("usd"),
                            "trust_score": first_ticker.get("trust_score"),
                            "trade_url": first_ticker.get("trade_url"),
                        }

                    st.markdown(f"""
                        🪙 جزئیات کوین 🪙

                        - نام: `{data.get('name')} ({data.get('symbol', '').upper()})`
                        - پلتفرم: `{data.get('asset_platform_id', 'N/A')}`

                        - رای‌های مثبت (احساسات): `{data.get('sentiment_votes_up_percentage', 'N/A')}%`
                        - رای‌های منفی (احساسات): `{data.get('sentiment_votes_down_percentage', 'N/A')}%`
                        - کاربران لیست پیگیری: `{data.get('watchlist_portfolio_users', 'N/A')}`

                        توضیحات: {truncated_description}

                        اطلاعات بازار 📊

                        - قیمت فعلی (USD): `${data.get('market_data', {}).get('current_price', {}).get('usd', 0):,.4f}`
                        - کل عرضه (#): `{data.get('market_data', {}).get('total_supply', 'N/A')}`
                        - حداکثر عرضه (#): `{data.get('market_data', {}).get('max_supply', 'N/A')}`
                        - عرضه در گردش (#): `{data.get('market_data', {}).get('circulating_supply', 'N/A')}`
                        - ارزش بازار (USD): `${data.get('market_data', {}).get('market_cap', {}).get('usd', 0):,.2f}`
                        - بالاترین قیمت تاریخ (USD): `${data.get('market_data', {}).get('ath', {}).get('usd', 0):,.8f}`
                        - پایین‌ترین قیمت تاریخ (USD): `${data.get('market_data', {}).get('atl', {}).get('usd', 0):,.8f}`
                        - تغییر قیمت ۲۴ ساعته: `{data.get('market_data', {}).get('price_change_percentage_24h', 0):.4f}%`

                        🏛️ اطلاعات صرافی برتر 🏛️

                        - نام صرافی: `{first_ticker_info.get('market_name', 'N/A')}`
                        - Base - آدرس توکن: `{first_ticker_info.get('base', 'N/A')}`
                        - آدرس توکن هدف: `{first_ticker_info.get('target', 'N/A')}`
                        - آخرین قیمت (USD): `${first_ticker_info.get('converted_last_usd', 0):,.8f}`
                        - حجم (USD): `${first_ticker_info.get('converted_volume_usd', 0):,.2f}`
                        - امتیاز اعتماد (صرافی): `{first_ticker_info.get('trust_score', 'N/A')}`
                        {f"- [اکنون معامله کنید]({first_ticker_info['trade_url']})" if first_ticker_info.get('trade_url') else ""}
                    """)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک نام یا نماد کوین وارد کنید.")

def display_coin_details_by_address():
    st.header("🪙 جزئیات کوین بر اساس آدرس قرارداد")
    platform_address = st.selectbox(
        "انتخاب پلتفرم:",
        ("ethereum", "solana"),
        key="platform_address_select"
    )
    contract_address_input = st.text_input("آدرس قرارداد را وارد کنید (مانند: 0x...)", key="contract_address_input")
    if st.button("دریافت جزئیات بر اساس آدرس"):
        if contract_address_input:
            utils.log_command_usage("/coin_details_address", f"{platform_address} {contract_address_input}")
            with st.spinner(f"در حال دریافت جزئیات برای {contract_address_input} در {platform_address}..."):
                data, error = api_client.fetch_coin_details_by_address(platform_address, contract_address_input)
                if data:
                    st.success(f"جزئیات برای {contract_address_input} با موفقیت دریافت شد!")
                    description = data.get("description", {}).get("en", "توضیحاتی در دسترس نیست.")
                    truncated_description = description[:500] + "..." if len(description) > 500 else description

                    tickers = data.get("tickers", [])
                    first_ticker_info = {}
                    if tickers:
                        first_ticker = tickers[0]
                        first_ticker_info = {
                            "base": first_ticker.get("base"),
                            "target": first_ticker.get("target"),
                            "market_name": first_ticker.get("market", {}).get("name"),
                            "converted_last_usd": first_ticker.get("converted_last", {}).get("usd"),
                            "converted_volume_usd": first_ticker.get("converted_volume", {}).get("usd"),
                            "trust_score": first_ticker.get("trust_score"),
                            "trade_url": first_ticker.get("trade_url"),
                        }

                    st.markdown(f"""
                        🪙 جزئیات کوین 🪙

                        - نام: `{data.get('name')} ({data.get('symbol', '').upper()})`
                        - پلتفرم: `{data.get('asset_platform_id', 'N/A')}`

                        - رای‌های مثبت (احساسات): `{data.get('sentiment_votes_up_percentage', 'N/A')}%`
                        - رای‌های منفی (احساسات): `{data.get('sentiment_votes_down_percentage', 'N/A')}%`
                        - کاربران لیست پیگیری: `{data.get('watchlist_portfolio_users', 'N/A')}`

                        توضیحات: {truncated_description}

                        اطلاعات بازار 📊

                        - قیمت فعلی (USD): `${data.get('market_data', {}).get('current_price', {}).get('usd', 0):,.4f}`
                        - کل عرضه (#): `{data.get('market_data', {}).get('total_supply', 'N/A')}`
                        - حداکثر عرضه (#): `{data.get('market_data', {}).get('max_supply', 'N/A')}`
                        - عرضه در گردش (#): `{data.get('market_data', {}).get('circulating_supply', 'N/A')}`
                        - ارزش بازار (USD): `${data.get('market_data', {}).get('market_cap', {}).get('usd', 0):,.2f}`
                        - بالاترین قیمت تاریخ (USD): `${data.get('market_data', {}).get('ath', {}).get('usd', 0):,.8f}`
                        - پایین‌ترین قیمت تاریخ (USD): `${data.get('market_data', {}).get('atl', {}).get('usd', 0):,.8f}`
                        - تغییر قیمت ۲۴ ساعته: `{data.get('market_data', {}).get('price_change_percentage_24h', 0):.4f}%`

                        🏛️ اطلاعات صرافی برتر 🏛️

                        - نام صرافی: `{first_ticker_info.get('market_name', 'N/A')}`
                        - Base - آدرس توکن: `{first_ticker_info.get('base', 'N/A')}`
                        - آدرس توکن هدف: `{first_ticker_info.get('target', 'N/A')}`
                        - آخرین قیمت (USD): `${first_ticker_info.get('converted_last_usd', 0):,.8f}`
                        - حجم (USD): `${first_ticker_info.get('converted_volume_usd', 0):,.2f}`
                        - امتیاز اعتماد (صرافی): `{first_ticker_info.get('trust_score', 'N/A')}`
                        {f"- [اکنون معامله کنید]({first_ticker_info['trade_url']})" if first_ticker_info.get('trade_url') else ""}
                    """)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک آدرس قرارداد وارد کنید.")

def display_bop():
    st.header("📊 تراز قدرت (BOP)")
    bop_coin_symbol = st.text_input("نماد کوین را وارد کنید (مانند: btc)", key="bop_coin_input")
    bop_days = st.selectbox("انتخاب روزها:", ("1", "7", "14"), key="bop_days_select")
    if st.button("محاسبه BOP"):
        if bop_coin_symbol:
            utils.log_command_usage("/bop", f"{bop_coin_symbol} {bop_days}")
            with st.spinner(f"در حال محاسبه BOP برای {bop_coin_symbol} در طی {bop_days} روز..."):
                data, error = api_client.fetch_ohlc_data(bop_coin_symbol, bop_days)
                if data:
                    st.success(f"BOP برای {bop_coin_symbol} با موفقیت محاسبه شد!")
                    message = f"📊 فشار کلی خرید/فروش (BOP) برای {data['name']} (OHLC {bop_days}-روزه):\n\n"
                    for date, avg_bop in sorted(data['bop_data'].items()):
                        pressure = "🔼 فشار خرید" if avg_bop > 0 else "🔽 فشار فروش"
                        message += f"- {date}: `{avg_bop:.4f}` {pressure}\n"
                    st.markdown(message)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک نماد کوین وارد کنید.")

def display_rsi():
    st.header("📉 شاخص قدرت نسبی (RSI)")
    rsi_coin_symbol = st.text_input("نماد کوین را وارد کنید (مانند: btc)", key="rsi_coin_input")
    rsi_days = st.slider("انتخاب روزها (۱-۱۴):", 1, 14, 14, key="rsi_days_slider")
    if st.button("محاسبه RSI"):
        if rsi_coin_symbol:
            utils.log_command_usage("/rsi", f"{rsi_coin_symbol} {rsi_days}d")
            with st.spinner(f"در حال محاسبه RSI برای {rsi_coin_symbol} در طی {rsi_days} روز..."):
                interval_type = 'daily'
                prices, error = api_client.fetch_market_chart_data(rsi_coin_symbol, rsi_days, interval_type)
                if prices:
                    total_rsi = utils.calculate_rsi(prices, period=rsi_days)
                    total_rsi_interpretation = utils.interpret_rsi(total_rsi)
                    st.success(f"RSI برای {rsi_coin_symbol} با موفقیت محاسبه شد!")
                    st.markdown(f"""
                        📉 شاخص قدرت نسبی (RSI) برای *{rsi_coin_symbol.upper()}* (۱۴ روز گذشته):

                        - 🔸 RSI: *{total_rsi:.2f}* {total_rsi_interpretation}

                        *توجه: RSI یک شاخص برای شناسایی قدرت مومنتوم است که برای ارزیابی اینکه آیا یک دارایی بیش از حد خرید شده (>70) یا بیش از حد فروخته شده (<30) استفاده می‌شود.*

                        *🔄 RSI بین ۳۰ تا ۷۰ نشان‌دهنده شرایط خنثی بازار است.*
                    """)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک نماد کوین وارد کنید.")

def display_top_boosted_tokens():
    st.header("🔥 توکن‌های برتر تقویت‌شده (DexScreener)")
    if st.button("دریافت توکن‌های برتر تقویت‌شده"):
        utils.log_command_usage("/top_boosted_tokens", "")
        with st.spinner("در حال دریافت توکن‌های برتر تقویت‌شده..."):
            data, error = api_client.fetch_top_boosted_tokens()
            if data:
                st.success("توکن‌های برتر تقویت‌شده با موفقیت دریافت شدند!")
                message = "🔥 توکن‌های برتر تقویت‌شده در DexScreener 🔥\n\n"
                for token in data:
                    links_message = ""
                    for link in token.get("links", []):
                        link_type = link.get("type", link.get("label", "Unknown"))
                        link_url = link.get("url", "N/A")
                        links_message += f"  - {link_type.capitalize()}: [لینک]({link_url})\n"

                    message += (
                        f"- آدرس توکن در DexScreener: [لینک]({token.get('url', 'N/A')})\n"
                        f"- پلتفرم: `{token.get('chainId', 'N/A')}`\n"
                        f"- آدرس توکن: `{token.get('tokenAddress', 'N/A')}`\n\n"
                        f"توضیحات: {token.get('description', 'توضیحاتی در دسترس نیست')}\n\n"
                        f"لینک‌ها:\n{links_message}\n"
                        "---------------------------\n"
                    )
                st.markdown(message)
            else:
                st.error(error)

def display_latest_boosted_tokens():
    st.header("🔥 آخرین توکن‌های تقویت‌شده (DexScreener)")
    if st.button("دریافت آخرین توکن‌های تقویت‌شده"):
        utils.log_command_usage("/latest_boosted_tokens", "")
        with st.spinner("در حال دریافت آخرین توکن‌های تقویت‌شده..."):
            data, error = api_client.fetch_latest_boosted_tokens()
            if data:
                st.success("آخرین توکن‌های تقویت‌شده با موفقیت دریافت شدند!")
                message = "🔥 آخرین توکن‌های تقویت‌شده در DexScreener 🔥\n\n"
                for token in data:
                    links_message = ""
                    for link in token.get("links", []):
                        link_type = link.get("type", link.get("label", "Unknown"))
                        link_url = link.get("url", "N/A")
                        links_message += f"  - {link_type.capitalize()}: [لینک]({link_url})\n"

                    message += (
                        f"- آدرس توکن در DexScreener: [لینک]({token.get('url', 'N/A')})\n"
                        f"- پلتفرم: `{token.get('chainId', 'N/A')}`\n"
                        f"- آدرس توکن: `{token.get('tokenAddress', 'N/A')}`\n\n"
                        f"توضیحات: {token.get('description', 'توضیحاتی در دسترس نیست')}\n\n"
                        f"لینک‌ها:\n{links_message}\n"
                        "---------------------------\n"
                    )
                st.markdown(message)
            else:
                st.error(error)

def display_token_orders():
    st.header("📋 سفارشات توکن (DexScreener)")
    token_order_chain_id = st.selectbox(
        "انتخاب شناسه زنجیره:",
        ("ethereum", "solana"),
        key="token_order_chain_select"
    )
    token_order_address = st.text_input("آدرس توکن را وارد کنید:", key="token_order_address_input")
    if st.button("دریافت سفارشات توکن"):
        if token_order_address:
            utils.log_command_usage("/token_orders", f"{token_order_chain_id} {token_order_address}")
            with st.spinner(f"در حال دریافت سفارشات توکن برای {token_order_address} در {token_order_chain_id}..."):
                data, error = api_client.fetch_token_orders(token_order_chain_id, token_order_address)
                if data:
                    st.success("سفارشات توکن با موفقیت دریافت شدند!")
                    message = f"📋 سفارشات توکن در DexScreener\n"
                    message += (
                        f"- زنجیره: `{token_order_chain_id}`\n"
                        f"- آدرس توکن: `{token_order_address}`\n\n"
                    )
                    type_mapping = {
                        "tokenProfile": "پروفایل توکن به Dex Screener اضافه شد",
                        "communityTakeover": "تسخیر جامعه",
                        "tokenAd": "تبلیغ در Dex Screener",
                        "trendingBarAd": "تبلیغ نوار ترند در Dex Screener"
                    }
                    for order in data:
                        order_type = order.get("type", "Unknown")
                        status = order.get("status", "Unknown")
                        timestamp = order.get("paymentTimestamp", 0)
                        datetime_str = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")

                        message += (
                            f"- نوع: `{type_mapping.get(order_type, order_type)}`\n"
                            f"- وضعیت: `{status.capitalize()}`\n"
                            f"- تاریخ/زمان: `{datetime_str}`\n"
                            "------------------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک آدرس توکن وارد کنید.")

def display_trade_info():
    st.header("📊 اطلاعات معاملاتی (DexScreener)")
    trade_info_token_address = st.text_input("آدرس توکن را وارد کنید:", key="trade_info_token_address_input")
    if st.button("دریافت اطلاعات معاملاتی"):
        if trade_info_token_address:
            utils.log_command_usage("/trade_info", trade_info_token_address)
            with st.spinner(f"در حال دریافت اطلاعات معاملاتی برای {trade_info_token_address}..."):
                data, error = api_client.fetch_trade_info(trade_info_token_address)
                if data:
                    st.success("اطلاعات معاملاتی با موفقیت دریافت شدند!")
                    message = f"📊 تاریخچه معاملات برای {trade_info_token_address} 📊\n\n"
                    for pair in data:
                        txns_message = "\n".join(
                            [
                                f"- {key}: خریدها: `{value.get('buys', 0)}`، فروش‌ها: `{value.get('sells', 0)}`"
                                for key, value in pair.get("txns", {}).items()
                            ]
                        )
                        volume_message = "\n".join(
                            [f"- {key}: `${value:,.2f}`" for key, value in pair.get("volume", {}).items()]
                        )
                        price_change_message = "\n".join(
                            [f"- {key}: `{value:.2f}%`" for key, value in pair.get("priceChange", {}).items()]
                        )

                        message += (
                            f"- دکس: `{pair.get('dexId', 'N/A')}`\n"
                            f"- لینک Dex Screener: [لینک]({pair.get('url', 'N/A')})\n"
                            f"- آدرس جفت: `{pair.get('pairAddress', 'N/A')}`\n"
                            f"- توکن پایه - توکن مظنه: `{pair.get('baseToken', {}).get('symbol', 'N/A')} / {pair.get('quoteToken', {}).get('symbol', 'N/A')}`\n"
                            f"- قیمت (بومی): `{pair.get('priceNative', 'N/A')}`\n"
                            f"- قیمت (USD): `${pair.get('priceUsd', 'N/A')}`\n\n"
                            f"تراکنش‌ها:\n{txns_message}\n\n"
                            f"حجم (USD):\n{volume_message}\n\n"
                            f"تغییر قیمت (%):\n{price_change_message}\n\n"
                            f"- نقدینگی (USD): `${pair.get('liquidity', {}).get('usd', 0):,.2f}`\n"
                            f"- ارزش بازار: `${pair.get('marketCap', 'N/A')}`\n"
                            f"- FDV: `${pair.get('fdv', 'N/A')}`\n"
                            f"- تقویت‌های فعال: `{pair.get('boosts', {}).get('active', 'N/A')}`\n"
                            "---------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)
        else:
            st.warning("لطفاً یک آدرس توکن وارد کنید.")
