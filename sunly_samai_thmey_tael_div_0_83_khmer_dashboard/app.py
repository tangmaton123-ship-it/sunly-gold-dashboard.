
import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="ស៊ុនលី សម័យថ្មី | តម្លៃមាស",
    page_icon="🟡",
    layout="wide",
)

# Refresh every 60 seconds
st_autorefresh(interval=60_000, key="gold_refresh")

# -----------------------------
# Dashboard design
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Kantumruy Pro', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #b58a20;
        font-size: 1.05rem;
        margin-bottom: 28px;
    }

    .price-card {
        border: 1px solid rgba(181, 138, 32, 0.5);
        border-radius: 16px;
        padding: 24px 12px;
        text-align: center;
        margin-bottom: 14px;
    }

    .price-label {
        font-size: 1rem;
        color: #888888;
        margin-bottom: 12px;
    }

    .price-value {
        font-size: 2rem;
        font-weight: 700;
        color: #b58a20;
        overflow-wrap: anywhere;
    }

    .price-unit {
        font-size: 0.9rem;
        color: #888888;
        margin-top: 8px;
    }

    .footer {
        text-align: center;
        color: #888888;
        font-size: 0.85rem;
        margin-top: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🟡 ស៊ុនលី សម័យថ្មី</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">តម្លៃមាសអន្តរជាតិ និងតម្លៃគណនា</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Gold price API
# -----------------------------
@st.cache_data(ttl=60, show_spinner=False)
def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        timeout=15,
    )

    # Show the real HTTP error if the API is unavailable
    if response.status_code != 200:
        details = response.text[:300]
        raise RuntimeError(
            f"Gold API returned HTTP {response.status_code}. "
            f"Response: {details}"
        )

    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError(
            "The gold API returned invalid JSON."
        ) from e

    if not isinstance(data, dict) or "price" not in data:
        raise RuntimeError(
            f"Price field missing. API response: {str(data)[:300]}"
        )

    try:
        price = float(data["price"])
    except (TypeError, ValueError) as e:
        raise RuntimeError(
            "The gold API returned an invalid price value."
        ) from e

    if price <= 0:
        raise RuntimeError("The gold API returned a non-positive price.")

    return price


# -----------------------------
# Display prices
# -----------------------------
try:
    with st.spinner("កំពុងទាញយកតម្លៃមាស..."):
        xau_usd = get_gold_price()

    # Requested calculation
    calculated_value = xau_usd / 0.83

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">
                    តម្លៃមាសអន្តរជាតិ (XAU/USD)
                </div>
                <div class="price-value">
                    ${xau_usd:,.2f}
                </div>
                <div class="price-unit">
                    ដុល្លារអាមេរិក / អោន
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
                    តម្លៃគណនាតាមរូបមន្ត ÷ 0.83
                </div>
                <div class="price-value">
                    ${calculated_value:,.2f}
                </div>
                <div class="price-unit">
                    តម្លៃគណនាតាមរូបមន្តរបស់អ្នក
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success("បានទាញយកទិន្នន័យតម្លៃមាស")

    st.caption(
        "ម៉ោងទាញយក៖ "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    st.caption(
        "តម្លៃអាចប្រែប្រួល ហើយអាចមិនមានទិន្នន័យ "
        "នៅពេលប្រភពសេវាមិនដំណើរការ។"
    )

except RuntimeError as e:
    st.error("មិនអាចទាញយកតម្លៃមាសបានទេ។")
    st.code(str(e), language="text")

except requests.exceptions.Timeout:
    st.error("ការទាញយកតម្លៃមាសចំណាយពេលយូរពេក។")
    st.caption("សូមសាកល្បងម្ដងទៀតនៅពេលក្រោយ។")

except requests.exceptions.RequestException as e:
    st.error("មិនអាចភ្ជាប់ទៅប្រភពតម្លៃមាសបានទេ។")
    st.caption(f"ប្រភេទកំហុស៖ {type(e).__name__}")
    st.code(str(e), language="text")

except (ValueError, TypeError, KeyError) as e:
    st.error("ទិន្នន័យតម្លៃមាសមិនត្រឹមត្រូវទេ។")
    st.code(str(e), language="text")

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """
    <div class="footer">
        ស៊ុនលី សម័យថ្មី · តម្លៃមាសអាចប្រែប្រួលតាមទីផ្សារ
    </div>
    """,
    unsafe_allow_html=True,
)
