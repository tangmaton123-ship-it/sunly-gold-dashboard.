
import streamlit as st
import streamlit.components.v1 as components
import requests
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="ស៊ុនលី សម័យថ្មី | តម្លៃមាស",
    page_icon="🟡",
    layout="wide",
)

# Refresh dashboard every 5 seconds
st_autorefresh(interval=5_000, key="gold_refresh")

# -----------------------------
# DESIGN
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Kantumruy Pro', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #fffdf6, #f8f3e5);
}
.main-title {
    text-align: center;
    font-size: 2.1rem;
    font-weight: 700;
    color: #8b6914;
    margin-bottom: 8px;
}
.sub-title {
    text-align: center;
    color: #b58a20;
    font-size: 1.1rem;
    margin-bottom: 24px;
}
.price-card {
    background: #ffffff;
    border: 1px solid rgba(181, 138, 32, 0.5);
    border-radius: 16px;
    padding: 24px 12px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(80, 60, 10, 0.06);
    margin-bottom: 12px;
}
.price-label {
    color: #78652f;
    font-size: 1.05rem;
    font-weight: 500;
    margin-bottom: 12px;
}
.price-value {
    color: #9a7415;
    font-size: 2rem;
    font-weight: 700;
    overflow-wrap: anywhere;
}
.small-note {
    text-align: center;
    color: #777;
    font-size: 0.9rem;
    margin-top: 14px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">ស៊ុនលី សម័យថ្មី</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">តម្លៃមាសអន្តរជាតិ និងតម្លៃមាសក្នុងមួយតម្លឹង</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# INTERNATIONAL GOLD PRICE API
# -----------------------------
@st.cache_data(ttl=0, show_spinner=False)
def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, dict) or "price" not in data:
        raise RuntimeError("The API response did not include a price.")

    price = float(data["price"])
    if price <= 0:
        raise RuntimeError("The API returned an invalid price.")

    # Use the provider's update timestamp when available
    updated_at = data.get("updatedAtReadable") or data.get("updatedAt")
    return price, updated_at

# -----------------------------
# PRICE CARDS
# -----------------------------
try:
    xau_usd, api_updated_at = get_gold_price()

    # Requested calculation; this is not an official local retail quote
    tael_value = xau_usd / 0.83

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">តម្លៃមាសអន្តរជាតិ (XAU/USD)</div>
            <div class="price-value">${xau_usd:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">តម្លៃគណនាក្នុងមួយតម្លឹង</div>
            <div class="price-value">${tael_value:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    if api_updated_at:
        st.caption(f"API data timestamp: {api_updated_at}")

    now = datetime.now(ZoneInfo("Asia/Phnom_Penh"))
    st.markdown(
        f'<div class="small-note">ម៉ោងពិនិត្យ API៖ '
        f'{now.strftime("%H:%M:%S")}</div>',
        unsafe_allow_html=True,
    )

except Exception as exc:
    st.error("មិនអាចទាញយកតម្លៃមាសបានទេ។")
    st.warning("សូមពិនិត្យការតភ្ជាប់អ៊ីនធឺណិត ឬសេវា API។")
    with st.expander("មើលព័ត៌មានបច្ចេកទេស"):
        st.code(str(exc), language="text")

# -----------------------------
# TRADINGVIEW GOLD SPOT CHART
# -----------------------------
st.subheader("តារាងតម្លៃមាសអន្តរជាតិ")

components.html(
    """
    <div class="tradingview-widget-container"
         style="height:500px;width:100%">
      <div id="tradingview_gold_chart"
           style="height:100%;width:100%"></div>
      <script src="https://s3.tradingview.com/tv.js"></script>
      <script>
        if (typeof TradingView !== "undefined") {
          new TradingView.widget({
            "autosize": true,
            "symbol": "OANDA:XAUUSD",
            "interval": "1",
            "timezone": "Asia/Phnom_Penh",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_gold_chart"
          });
        }
      </script>
    </div>
    """,
    height=520,
)

st.markdown(
    '<div class="small-note">តម្លៃ API និងតារាង TradingView '
    'អាចខុសគ្នា ព្រោះប្រើប្រភពទិន្នន័យផ្សេងគ្នា។</div>',
    unsafe_allow_html=True,
)
