
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

# -----------------------------
# Auto refresh every 30 seconds
# -----------------------------
st_autorefresh(interval=30_000, key="gold_price_refresh")

# -----------------------------
# Styling
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
# Fetch gold price
# -----------------------------
@st.cache_data(ttl=30, show_spinner=False)
def get_gold_price():
    url = "https://xaus.com/api/v1/spot?compact=1"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        timeout=15,
    )

    response.raise_for_status()
    data = response.json()

    # Accept common response formats
    possible_prices = [
        data.get("price"),
        data.get("spot"),
        data.get("xau_usd"),
        data.get("XAUUSD"),
    ]

    # Some APIs return the values inside a nested object
    if isinstance(data.get("data"), dict):
        nested = data["data"]
        possible_prices.extend([
            nested.get("price"),
            nested.get("spot"),
            nested.get("xau_usd"),
            nested.get("XAUUSD"),
        ])

    for value in possible_prices:
        if value is not None:
            try:
                price = float(value)
                if price > 0:
                    return price
            except (TypeError, ValueError):
                continue

    raise ValueError(
        "The API response did not contain a recognized gold price."
    )


# -----------------------------
# Display prices
# -----------------------------
try:
    with st.spinner("កំពុងទាញយកតម្លៃមាស..."):
        xau_usd = get_gold_price()

    # User-requested calculation
    calculated_value = xau_usd / 0.83

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">តម្លៃមាសអន្តរជាតិ (XAU/USD)</div>
                <div class="price-value">${xau_usd:,.2f}</div>
                <div class="price-unit">ដុល្លារអាមេរិក / អោន</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">តម្លៃគណនាតាមរូបមន្ត ÷ 0.83</div>
                <div class="price-value">${calculated_value:,.2f}</div>
                <div class="price-unit">តម្លៃគណនា មិនមែនជាតម្លៃលក់រាយដែលបានបញ្ជាក់</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success("បានទាញយកទិន្នន័យតម្លៃមាស")

    st.caption(
        "ពេលវេលាដែលបង្ហាញខាងក្រោម គឺជាពេលដែលកម្មវិធីបានទាញយកទិន្នន័យ "
        "មិនមែនជាពេលដែលទីផ្សារបានធ្វើបច្ចុប្បន្នភាពតម្លៃនោះទេ។"
    )
    st.caption(
        "ម៉ោងទាញយក៖ "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

except requests.exceptions.HTTPError as e:
    status_code = (
        e.response.status_code
        if e.response is not None
        else "មិនស្គាល់"
    )
    st.error(f"ប្រភពតម្លៃមាសបានឆ្លើយតបដោយកំហុស HTTP: {status_code}")
    st.caption(f"ព័ត៌មានបច្ចេកទេស៖ {e}")

except requests.exceptions.Timeout:
    st.error("ការទាញយកតម្លៃមាសចំណាយពេលយូរពេក។ សូមសាកល្បងម្ដងទៀត។")

except requests.exceptions.RequestException as e:
    st.error("មិនអាចភ្ជាប់ទៅប្រភពតម្លៃមាសបានទេ។")
    st.caption(f"ប្រភេទកំហុស៖ {type(e).__name__}")
    st.caption(f"ព័ត៌មានបច្ចេកទេស៖ {e}")

except (ValueError, TypeError) as e:
    st.error("ទិន្នន័យតម្លៃមាសដែលទទួលបានមិនត្រឹមត្រូវទេ។")
    st.caption(f"ព័ត៌មានបច្ចេកទេស៖ {e}")

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
