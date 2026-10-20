
import streamlit.components.v1 as components

st.subheader("តារាងតម្លៃមាសអន្តរជាតិ")

components.html(
    """
    <div class="tradingview-widget-container"
         style="height:500px;width:100%">
      <div id="tradingview_gold_chart"
           style="height:100%;width:100%"></div>
      <script
        type="text/javascript"
        src="https://s3.tradingview.com/tv.js">
      </script>
      <script type="text/javascript">
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
      </script>
    </div>
    """,
    height=520,
)
