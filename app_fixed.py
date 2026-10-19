
import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(
    page_title="ស៊ុនលី សម័យថ្មី | តម្លៃមាស",
    page_icon="🟡",
    layout="wide",
)

# Refresh dashboard every 30 seconds
st_autorefresh(interval=30_000, key="gold_price_refresh")

# Free gold price API — no API key required
API_URL = "https://xaus.com/api/v1/spot?compact=1"


# -------------------------------
# FETCH GOLD PRICE
# -------------------------------
@st.cache_data(ttl=30)
def fetch_gold_price():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()

    data = response.json()

    price = data.get("spot_usd_oz")

    if price is None:
        raise ValueError("Gold price is missing from the API response.")

    state = data.get("data_state") or {}

    updated_at = (
        data.get("price_as_of")
        or state.get("as_of")
        or data.get("updated_at")
        or ""
    )

    return {
        "price": float(price),
        "status": state.get("status", "unknown"),
        "updated_at": updated_at,
        "age_seconds": state.get("age_seconds"),
    }


# -------------------------------
# DESIGN
# -------------------------------
st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;500;600;700&display=swap'
    );

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
        border: 1px solid rgba(181, 138, 32, 0.5);
        border-radius: 16px;
        padding: 24px 12px;
        text-align: center;
        margin-bottom: 16px;
        min-height: 145px;
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

    .price-note {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------
# DASHBOARD HEADER
# -------------------------------
st.markdown(
    '<div class="main-title">Sunly សម័យថ្មី</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">តម្លៃមាសអន្តរជាតិ និងតម្លៃក្នុងមួយតម្លឹង</div>',
    unsafe_allow_html=True,
)


# -------------------------------
# DISPLAY GOLD PRICES
# -------------------------------
try:
    gold = fetch_gold_price()

    xau_usd = gold["price"]

    # Requested calculation formula
    calculated_tael_price = xau_usd / 0.83

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">
                    តម្លៃមាសអន្តរជាតិ XAU/USD
                </div>
                <div class="price-value">
                    ${xau_usd:,.2f}
                </div>
                <div class="price-note">
                    ក្នុងមួយត្រយអោន
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">
                    តម្លៃគណនាក្នុងមួយតម្លឹង
                </div>
                <div class="price-value">
                    ${calculated_tael_price:,.2f}
                </div>
                <div class="price-note">
                    គណនាតាមរូបមន្ត ÷ 0.83
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Data freshness status
    if gold["status"] == "fresh":
        st.success("ស្ថានភាពទិន្នន័យ៖ ទិន្នន័យថ្មី")

    elif gold["status"] == "stale":
        st.warning(
            "ទិន្នន័យចាស់ពីប្រភពចុងក្រោយ "
            "មិនមែនតម្លៃថ្មីបំផុតទេ។"
        )

    elif gold["status"] == "unavailable":
        st.warning(
            "ប្រភពមិនអាចបញ្ជាក់ទិន្នន័យបច្ចុប្បន្នបានទេ។"
        )

    else:
        st.info("សូមពិនិត្យស្ថានភាពទិន្នន័យពីប្រភព។")

    if gold["updated_at"]:
        st.caption(f"ពេលវេលាតម្លៃ៖ {gold['updated_at']}")

    st.caption("ប្រភពទិន្នន័យ៖ XAUS · XAU/USD")

except requests.exceptions.Timeout:
    st.error(
        "ការភ្ជាប់ទៅប្រភពតម្លៃមាសចំណាយពេលយូរ។ "
        "សូមសាកល្បងម្ដងទៀត។"
    )

except requests.exceptions.RequestException:
    st.error(
        "មិនអាចភ្ជាប់ទៅប្រភពតម្លៃមាសបានទេ។ "
        "សូមពិនិត្យការតភ្ជាប់ ហើយសាកល្បងម្ដងទៀត។"
    )

except (ValueError, TypeError, KeyError):
    st.error(
        "ទិន្នន័យតម្លៃមាសមិនត្រឹមត្រូវ "
        "ឬមិនពេញលេញទេ។"
    )

except Exception:
    st.error("មានបញ្ហាមិនរំពឹងទុក។ សូមព្យាយាមម្ដងទៀត។")


# -------------------------------
# FOOTER
# -------------------------------
st.caption(
    "ចំណាំ៖ តម្លៃមាសអន្តរជាតិអាចខុសពីតម្លៃទិញលក់ជាក់ស្តែងនៅកម្ពុជា។"
)
