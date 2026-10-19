
import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="ស៊ុនលី សម័យថ្មី | តម្លៃមាស",
    page_icon="🟡",
    layout="wide",
)

# Refresh dashboard every 30 seconds
st_autorefresh(interval=30_000, key="gold_refresh")

API_URL = "https://xaus.com/api/v1/spot?compact=1"

# -----------------------------
# GOLD PRICE FETCH
# -----------------------------
@st.cache_data(ttl=30)
def fetch_gold_price():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()

    price = data.get("spot_usd_oz")
    if price is None:
        raise ValueError("API មិនបានផ្តល់តម្លៃមាស")

    state = data.get("data_state") or {}

    return {
        "price": float(price),
        "status": state.get("status", "unknown"),
        "updated_at": data.get("price_as_of")
        or state.get("as_of")
        or data.get("updated_at", ""),
        "age_seconds": state.get("age_seconds"),
    }

# -----------------------------
# DESIGN
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Kantumruy Pro', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 2.1rem;
    font-weight: 700;
    color: #b58a20;
    margin-bottom: 4px;
}

.sub-title {
    text-align: center;
    color: #b58a20;
    font-size: 1rem;
    margin-bottom: 28px;
}

.price-card {
    border: 1px solid rgba(181,138,32,0.5);
    border-radius: 16px;
    padding: 24px 12px;
    text-align: center;
    margin-bottom: 16px;
}

.price-label {
    color: #b58a20;
    font-size: 1.05rem;
    font-weight: 600;
}

.price-value {
    font-size: 2rem;
    font-weight: 700;
    margin-top: 10px;
    overflow-wrap: anywhere;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">Sunly សម័យថ្មី</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">តម្លៃមាសអន្តរជាតិ និងតម្លៃក្នុងមួយតម្លឹង</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# DISPLAY LIVE DATA
# -----------------------------
try:
    gold = fetch_gold_price()
    xau_usd = gold["price"]

    # User-requested calculation.
    # This is not a verified Cambodian market-price conversion.
    per_tael = xau_usd / 0.83

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">តម្លៃមាសអន្តរជាតិ XAU/USD</div>
            <div class="price-value">${xau_usd:,.2f}</div>
            <div>ក្នុងមួយត្រយអោន</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">តម្លៃគណនាក្នុងមួយតម្លឹង</div>
            <div class="price-value">${per_tael:,.2f}</div>
            <div>តម្លៃគណនាតាមរូបមន្ត ÷ 0.83</div>
        </div>
        """, unsafe_allow_html=True)

    if gold["status"] == "fresh":
        st.success("ស្ថានភាពទិន្នន័យ៖ ថ្មី")
    elif gold["status"] == "stale":
        st.warning("ទិន្នន័យចាស់ពីប្រភពចុងក្រោយ មិនមែនតម្លៃបន្តផ្ទាល់ថ្មីទេ")
    else:
        st.warning("មិនអាចបញ្ជាក់ថាទិន្នន័យថ្មីឬអត់បានទេ")

    if gold["updated_at"]:
        st.caption(f"ពេលវេលាតម្លៃ៖ {gold['updated_at']}")

    st.caption("ប្រភពទិន្នន័យ៖ XAUS · XAU/USD")

except requests.RequestException:
    st.error("មិនអាចភ្ជាប់ទៅប្រភពតម្លៃមាសបានទេ។ សូមពិនិត្យការតភ្ជាប់ ហើយសាកល្បងម្ដងទៀត។")
except (ValueError, TypeError, KeyError):
    st.error("ទិន្នន័យតម្លៃមាសមិនត្រឹមត្រូវ ឬមិនពេញលេញទេ។")
except Exception:
    st.error("មានបញ្ហាមិនរំពឹងទុក។ សូមព្យាយាមម្ដងទៀត។")

st.caption("តម្លៃអន្តរជាតិអាចខុសពីតម្លៃទិញលក់ជាក់ស្តែងនៅកម្ពុជា។")
