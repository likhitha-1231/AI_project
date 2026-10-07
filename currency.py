import streamlit as st
import requests

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Likhitha Currency Converter",
    page_icon="💱",
    layout="centered"
)

# ==================================================
# CUSTOM DESIGN
# ==================================================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f2027,
        #203a43,
        #2c5364
    );
}

/* Title */
.title {
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: bold;
    margin-top: 20px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #d9f7ff;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Metric Card */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.20);
}

/* Metric Value */
div[data-testid="stMetricValue"] {
    color: #0f766e;
    font-weight: bold;
}

/* Convert Button */
.stButton > button {
    background: #14b8a6;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    padding: 12px;
}

/* Button Hover */
.stButton > button:hover {
    background: #0d9488;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #d9f7ff;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# TITLE
# ==================================================
st.markdown(
    '<div class="title">💱 Likhitha Currency Converter</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '🌍 Convert currencies quickly and easily'
    '</div>',
    unsafe_allow_html=True
)

# ==================================================
# CURRENCY LIST
# ==================================================
currencies = {
    "🇮🇳 INR - Indian Rupee": "INR",
    "🇺🇸 USD - US Dollar": "USD",
    "🇪🇺 EUR - Euro": "EUR",
    "🇬🇧 GBP - British Pound": "GBP",
    "🇯🇵 JPY - Japanese Yen": "JPY",
    "🇦🇺 AUD - Australian Dollar": "AUD",
    "🇨🇦 CAD - Canadian Dollar": "CAD",
    "🇸🇬 SGD - Singapore Dollar": "SGD",
    "🇦🇪 AED - UAE Dirham": "AED",
    "🇸🇦 SAR - Saudi Riyal": "SAR",
    "🇨🇭 CHF - Swiss Franc": "CHF",
    "🇨🇳 CNY - Chinese Yuan": "CNY",
    "🇰🇷 KRW - South Korean Won": "KRW",
    "🇳🇿 NZD - New Zealand Dollar": "NZD"
}

currency_list = list(currencies.keys())

# ==================================================
# AMOUNT INPUT
# ==================================================
amount = st.number_input(
    "💰 Enter Amount",
    min_value=0.01,
    value=100.0,
    step=1.0
)

# ==================================================
# CURRENCY SELECTION
# ==================================================
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox(
        "💵 From Currency",
        currency_list,
        index=0
    )

with col2:
    to_currency = st.selectbox(
        "💶 To Currency",
        currency_list,
        index=1
    )

from_code = currencies[from_currency]
to_code = currencies[to_currency]

# ==================================================
# CONVERT BUTTON
# ==================================================
if st.button(
    "💱 CONVERT",
    use_container_width=True
):

    # ------------------------------------------------
    # SAME CURRENCY
    # ------------------------------------------------
    if from_code == to_code:

        converted = amount
        rate = 1.0

        st.success("✅ Conversion Successful!")

        st.subheader("💰 Conversion Result")

        st.metric(
            label=f"{amount:,.2f} {from_code}",
            value=f"{converted:,.2f} {to_code}"
        )

        st.info(
            f"💱 1 {from_code} = 1 {to_code}"
        )

    # ------------------------------------------------
    # DIFFERENT CURRENCIES
    # ------------------------------------------------
    else:

        try:

            # Exchange rate API
            url = (
                "https://api.frankfurter.app/latest"
                f"?amount={amount}"
                f"&from={from_code}"
                f"&to={to_code}"
            )

            response = requests.get(
                url,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            # Check response
            if (
                "rates" not in data
                or to_code not in data["rates"]
            ):

                st.error(
                    "❌ Exchange rate is currently unavailable."
                )

            else:

                converted = data["rates"][to_code]

                # Get rate for 1 unit
                rate_url = (
                    "https://api.frankfurter.app/latest"
                    f"?from={from_code}"
                    f"&to={to_code}"
                )

                rate_response = requests.get(
                    rate_url,
                    timeout=15
                )

                rate_response.raise_for_status()

                rate_data = rate_response.json()

                rate = rate_data["rates"][to_code]

                # ------------------------------------------------
                # RESULT
                # ------------------------------------------------

                st.success("✅ Conversion Successful!")

                st.subheader("💰 Conversion Result")

                st.metric(
                    label=f"{amount:,.2f} {from_code}",
                    value=f"{converted:,.2f} {to_code}"
                )

                st.info(
                    f"💱 1 {from_code} = "
                    f"{rate:.4f} {to_code}"
                )

                st.write(
                    f"📌 {amount:,.2f} {from_code} = "
                    f"**{converted:,.2f} {to_code}**"
                )

        # ------------------------------------------------
        # ERROR HANDLING
        # ------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "⏳ The exchange-rate server took too long to respond."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "🌐 Cannot connect to the exchange-rate server."
            )

        except requests.exceptions.HTTPError:

            st.error(
                "⚠️ Exchange-rate service returned an error."
            )

        except Exception as e:

            st.error(
                "❌ Unable to get the exchange rate."
            )

            st.caption(
                f"Technical error: {e}"
            )

# ==================================================
# INFORMATION
# ==================================================
st.divider()

st.info(
    "💡 Live exchange rates require an internet connection."
)

# ==================================================
# FOOTER
# ==================================================
st.markdown(
    '<div class="footer">'
    '💜 Likhitha Currency Converter • 🌍 Live Exchange Rates'
    '</div>',
    unsafe_allow_html=True
)