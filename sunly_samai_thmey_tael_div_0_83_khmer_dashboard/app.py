import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timezone

st.set_page_config(
    page_title="ស៊ុនលី សម័យថ្មី | តម្លៃមាស",
    page_icon="🟡",
    layout="wide",
)

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
    margin-bottom: 8px;
}
.sub-title {
    text-align: center;
    color: #b58a20;
    margin-bottom: 28px;
}
.price-card {
    border: 1px solid rgba(181,138,32,0.5);
    border-radius: 16px;
    padding: 24px 12px;
    text-align: center;
    min-height: 170px;
}
.price-label {
    font-size: 1rem;
    margin-bottom: 14px;
}
.price-value {
    font-size: 2rem;
    font-weight: 700;
    color: #b58a20;
    overflow-wrap: anywhere;
}
.price-unit {
    font-size: 0.95rem;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">ហាងមាស ស៊ុនលី សម័យថ្មី</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">តម្លៃមាសអន្តរជាតិ និងតម្លៃមាសក្នុងមួយដំឡឹង</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("ការកំណត់")
    api_key = st.text_input(
        "លេខកូដ API",
        type="password",
        help="បញ្ចូលលេខកូដ GoldAPI.io ដើម្បីទទួលតម្លៃមាសផ្ទាល់។",
    )
    refresh_seconds = st.selectbox(
        "ចន្លោះពេលធ្វើបច្ចុប្បន្នភាព",
        [30, 60, 120, 300],
        index=1,
        format_func=lambda n: f"រៀងរាល់ {n} វិនាទី",
    )
    st.divider()
    st.markdown("**សម្រាប់សាកល្បងប៉ុណ្ណោះ**")
    manual_price = st.number_input(
        "តម្លៃអន្តរជាតិក្នុងមួយអោន (ដុល្លារ)",
        min_value=0.0,
        value=0.0,
        step=10.0,
        help="ប្រើសម្រាប់សាកល្បងនៅពេលមិនទាន់មានលេខកូដ API។",
    )

st_autorefresh(interval=refresh_seconds * 1000, key="gold_price_refresh")

def fetch_gold_price(api_token):
    response = requests.get(
        "https://www.goldapi.io/api/XAU/USD",
        headers={
            "x-access-token": api_token,
            "Content-Type": "application/json",
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    return float(data["price"]), data.get("timestamp")

gold_price_ounce = None
updated_timestamp = None
source_label = ""

if api_key.strip():
    try:
        gold_price_ounce, updated_timestamp = fetch_gold_price(api_key.strip())
        source_label = "តម្លៃផ្ទាល់ពី GoldAPI.io"
    except Exception:
        st.error(
            "មិនអាចទាញយកតម្លៃមាសបានទេ។ "
            "សូមពិនិត្យលេខកូដ API និងការភ្ជាប់អ៊ីនធឺណិត។"
        )

if gold_price_ounce is None and manual_price > 0:
    gold_price_ounce = float(manual_price)
    source_label = "តម្លៃបញ្ចូលដោយដៃ មិនមែនតម្លៃផ្ទាល់"

if gold_price_ounce is None:
    st.info("សូមបញ្ចូលលេខកូដ API នៅផ្នែកខាងឆ្វេង ដើម្បីបង្ហាញតម្លៃមាសអន្តរជាតិ។")
    st.markdown(
        "**រូបមន្តតម្លៃមាសក្នុងមួយដំឡឹង៖** "
        "តម្លៃមាសដែលបង្ហាញ ÷ 0.83"
    )
else:
    # តាមរូបមន្តដែលបានស្នើ៖ តម្លៃដែលបង្ហាញ ÷ 0.83
    gold_price_tael = gold_price_ounce / 0.83

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">តម្លៃមាសអន្តរជាតិ (XAU/USD)</div>
                <div class="price-value">${gold_price_ounce:,.2f}</div>
                <div class="price-unit">ដុល្លារអាមេរិក ក្នុងមួយអោន</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="price-card">
                <div class="price-label">តម្លៃមាសក្នុងមួយដំឡឹង</div>
                <div class="price-value">${gold_price_tael:,.2f}</div>
                <div class="price-unit">ដុល្លារអាមេរិក ក្នុងមួយដំឡឹង</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("ប្រភព៖ " + source_label)
    if updated_timestamp:
        try:
            local_time = datetime.fromtimestamp(
                int(updated_timestamp), timezone.utc
            ).astimezone()
            st.caption(
                "ពេលធ្វើបច្ចុប្បន្នភាព៖ "
                + local_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        except (ValueError, TypeError, OSError):
            pass

st.divider()
st.subheader("ព័ត៌មានសំខាន់")
st.markdown("""
- បង្ហាញតែតម្លៃមាសអន្តរជាតិ និងតម្លៃមាសក្នុងមួយដំឡឹង។
- រូបមន្តគណនា៖ តម្លៃមាសដែលបង្ហាញ ÷ 0.83។
- មិនបង្ហាញតម្លៃទិញចូល ឬលក់ចេញរបស់ហាងទេ។
- តម្លៃមាសក្នុងមួយដំឡឹងនេះជាតម្លៃគណនាតាមរូបមន្តដែលបានកំណត់ មិនមែនជាតម្លៃទិញលក់ក្នុងស្រុកដែលបានបញ្ជាក់ឡើយ។
""")
st.caption("ស៊ុនលី សម័យថ្មី • កម្មវិធីតម្លៃមាស")
