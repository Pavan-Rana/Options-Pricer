import streamlit as st
from datetime import date
from domain.option import Option
from pricing.pricing_engine import PricingEngine
import pandas as pd
from ui.plots import plot_call_heatmap, plot_put_heatmap

# Initialize pricing engine
engine = PricingEngine()

# Streamlit page configuration
st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(layout="wide")
st.title("Black-Scholes Options Pricing Calculator")
st.markdown("Option Valuations and Greeks")
st.sidebar.title("By Pavan Singh Rana")
st.sidebar.divider(width="stretch")
st.sidebar.subheader("Input Parameters")

#  Sidebar inputs for option parameters
ticker = st.sidebar.text_input("Underlying Ticker", value="AAPL")
strike = st.sidebar.number_input("Strike Price", min_value=0.0, value=100.0)
expiry = st.sidebar.date_input("Expiration Date", value=date.today())
vol = st.sidebar.number_input("Volatility (%)", min_value=1.0, value=20.0) / 100.0
rate = st.sidebar.number_input("Risk-Free Rate (%)", min_value=0.0, value=0.01) / 100.0

# Heatmap parameters
st.sidebar.subheader("P&L Heatmap Parameters")
min_spot_price = st.sidebar.number_input("Min Spot Price", min_value=1.0, value=90.0)
max_spot_price = st.sidebar.number_input("Max Spot Price", min_value=1.0, value=120.0)
min_vol, max_vol = st.sidebar.slider(
    "Volatility Range (%)",
    min_value=0.1,
    max_value=100.0,
    value=(10.0, 50.0),
    step=0.5
)
min_vol /= 100.0
max_vol /= 100.0

heatmap_ranges = {'min_spot': min_spot_price, 'max_spot': max_spot_price,
                  'min_vol': min_vol, 'max_vol': max_vol}

call_purchase_price = st.sidebar.number_input("Call Purchase Price", min_value=0.0, value=90.0)
put_purchase_price = st.sidebar.number_input("Put Purchase Price", min_value=0.0, value=90.0)


opt = Option(underlying_symbol=ticker, strike_price=strike, expiration_date=expiry)

call_results = engine.calculate_call(opt, volatility=vol, risk_free_rate=rate)
put_results = engine.calculate_put(opt, volatility=vol, risk_free_rate=rate)

call_col, put_col = st.columns([1, 1])

with call_col:
    # Display as a static table
    st.markdown(
        f"""
        <div style='background-color:#90ee90;padding:10px;border-radius:10px;text-align:center'>
            <p style='color:black; font-size:20px''>CALL Value</p>
            <p style='color:black; font-size:30px'><b>${call_results["price"]:.2f}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

with put_col:
    st.markdown(
        f"""
            <div style='background-color:#fbb6b6;padding:10px;border-radius:10px;text-align:center'>
                <p style='color:black; font-size:20px''>PUT Value</p>
                <p style='color:black; font-size:30px'><b>${put_results["price"]:.2f}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br><br>", unsafe_allow_html=True) 
st.title("Options P&L Heatmaps")
st.markdown("Visualize PNL across different spot prices and volatilities whilst considering purchase prices.")
call_hm_col, put_hm_col = st.columns([1, 1])

with call_hm_col:
    st.markdown("### Call Heatmap")
    fig_call = plot_call_heatmap(
        pricing_engine=engine,
        option_template=opt,
        rate=rate,
        heatmap_ranges=heatmap_ranges,
        purchase_price=call_purchase_price
    )
    st.pyplot(fig_call)

with put_hm_col:
    st.markdown("### Put Heatmap")
    fig_put = plot_put_heatmap(
        pricing_engine=engine,
        option_template=opt,
        rate=rate,
        heatmap_ranges=heatmap_ranges,
        purchase_price=put_purchase_price
    )
    st.pyplot(fig_put)


greeks = ["Delta", "Gamma", "Vega", "Theta", "Rho"]
greeks_call_table = pd.DataFrame([{greek: f"{call_results[greek.lower()]:.4f}" for greek in greeks}])
greeks_put_table = pd.DataFrame([{greek: f"{put_results[greek.lower()]:.4f}" for greek in greeks}])

st.markdown("<br>", unsafe_allow_html=True)
st.title("Greeks")
greeks_call_col, greeks_put_col = st.columns([1, 1])

with greeks_call_col:
    st.markdown("### Call Greeks")
    st.markdown(greeks_call_table.style.hide(axis="index").to_html(), unsafe_allow_html=True)

with greeks_put_col:
    st.markdown("### Put Greeks")
    st.markdown(greeks_put_table.style.hide(axis="index").to_html(), unsafe_allow_html=True)