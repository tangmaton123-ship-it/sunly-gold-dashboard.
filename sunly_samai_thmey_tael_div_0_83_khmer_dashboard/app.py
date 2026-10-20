
import streamlit as st
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

# Refresh the dashboard every 5 seconds
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
# GOLD PRICE API
# -----------------------------
@st.cache_data(ttl=0, show_spinner=False)
def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"API returned HTTP {response.status_code}: "
            f"{response.text[:300]}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("API returned invalid JSON.") from exc

    if not isinstance(data, dict) or "price" not in data:
        raise RuntimeError(
            f"Price field missing in API response: {str(data)[:300]}"
        )

    try:
        price = float(data["price"])
    except (TypeError, ValueError) as exc:
        raise RuntimeError("API returned an invalid price.") from exc

    if price <= 0:
        raise RuntimeError("API returned a non-positive price.")

    return price

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
# FETCH AND DISPLAY PRICE
# -----------------------------
try:
    xau_usd = get_gold_price()

    # Requested calculation
    tael_value = xau_usd / 0.83

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">តម្លៃមាសអន្តរជាតិ (XAU/USD)</div>
            <div class="price-value">${xau_usd:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">តម្លៃគណនាក្នុងមួយតម្លឹង</div>
            <div class="price-value">${tael_value:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    cambodia_time = datetime.now(ZoneInfo("Asia/Phnom_Penh"))
    st.markdown(
        f'<div class="small-note">ម៉ោងអាប់ដេតចុងក្រោយ៖ '
        f'{cambodia_time.strftime("%H:%M:%S")}</div>',
        unsafe_allow_html=True,
    )

except Exception as e:
    st.error("មិនអាចទាញយកតម្លៃមាសបានទេ។")
    st.warning("សូមពិនិត្យការតភ្ជាប់អ៊ីនធឺណិត ឬសេវា API។")
    with st.expander("មើលព័ត៌មានបច្ចេកទេស"):
        st.code(str(e), language="text")

st.markdown(
    '<div class="small-note">ទិន្នន័យអាស្រ័យលើសេវា API '
    'ហើយតម្លៃអាចមិនផ្លាស់ប្តូររាល់ ៥ វិនាទីទេ។</div>',
    unsafe_allow_html=True,
)
