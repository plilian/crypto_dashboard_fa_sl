import streamlit as st
import uuid
from datetime import datetime
import os

def get_session_id():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def log_command_usage(command: str, query: str):
    session_id = get_session_id()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"Session ID: {session_id}, Command: {command}, Query: {query}, Timestamp: {timestamp}"
    print(log_entry)

def calculate_rsi(prices: list[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 0.0

    price_changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]

    gains = [change if change > 0 else 0 for change in price_changes]
    losses = [abs(change) if change < 0 else 0 for change in price_changes]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def interpret_rsi(rsi: float) -> str:
    if rsi > 70:
        return "بیش از حد خرید شده - ممکن است دارایی بیش از ارزش واقعی باشد و احتمال اصلاح قیمت وجود دارد."
    elif rsi < 30:
        return "بیش از حد فروخته شده - ممکن است دارایی کمتر از ارزش واقعی باشد و احتمال افزایش قیمت وجود دارد."
    else:
        return "خنثی - دارایی در حالت متعادل قرار دارد."
