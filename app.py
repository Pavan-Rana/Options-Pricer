import streamlit as st
from datetime import date
from domain.option import Option
from pricing.pricing_engine import PricingEngine
import pandas as pd
from ui.plots import plot_price_vs_strike, plot_greeks_vs_strike

# Initialize engine (with strategies and data provider)
engine = PricingEngine()

st.set_page_config(layout="wide")
st.title("Options Pricing Calculator")
st.markdown("Calculate European option prices and Greeks using Black-Scholes or Monte Carlo.")
st.sidebar.title("By Pavan Singh Rana")
st.sidebar.divider(width="stretch")
st.sidebar.subheader("Input Parameters")

# Sidebar or main inputs
ticker = st.sidebar.text_input("Underlying Ticker", value="AAPL")
strike = st.sidebar.number_input("Strike Price", min_value=0.0, value=100.0)
expiry = st.sidebar.date_input("Expiration Date", value=date.today())
vol = st.sidebar.number_input("Volatility (%)", min_value=0.0, value=20.0) / 100.0
rate = st.sidebar.number_input("Risk-Free Rate (%)", min_value=0.0, value=1.0) / 100.0
model = st.sidebar.selectbox("Pricing Model", ["Black-Scholes", "Monte Carlo"])

st.sidebar.divider(width="stretch")
st.sidebar.subheader("Heatmap Parameters")
rate = st.sidebar.date_input("Starting Expiration Date", value=date.today())
rate = st.sidebar.date_input("Ending Expiration Date", value=date.today())
rate = st.sidebar.number_input("Starting Strike Price", min_value=0.0, value=100.0) / 100.0
rate = st.sidebar.number_input("Ending Strike Price", min_value=0.0, value=100.0) / 100.0

if model == "Monte Carlo":
    paths = st.slider("Monte Carlo paths", min_value=1000, max_value=100000, value=10000, step=1000)
    # update engine's Monte Carlo strategy paths if needed
    engine.strategies["Monte Carlo"].num_paths = paths

# When the user clicks "Calculate", perform pricing
if st.sidebar.button("Calculate Price"):
    # Create Option object
    opt = Option(underlying_symbol=ticker, strike_price=strike, expiration_date=expiry)
    # Calculate price and Greeks
    call_results, put_results = engine.calculate(opt, model_name=model, volatility=vol, risk_free_rate=rate)
    col1, col2 = st.columns([1, 1])
    # Display results
    greeks_table = pd.DataFrame([{
        "Delta": f"{call_results['delta']:.4f}",
        "Gamma": f"{call_results['gamma']:.4f}",
        "Vega": f"{call_results['vega']:.4f}",
        "Theta": f"{call_results['theta']:.4f}",
        "Rho": f"{call_results['rho']:.4f}"
    }])
    greeks_table.index = ['']

    with col1:
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
        st.markdown("### Call Option Greeks")
        st.markdown(greeks_table.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    greeks_table = pd.DataFrame([{
        "Delta": f"{put_results['delta']:.4f}",
        "Gamma": f"{put_results['gamma']:.4f}",
        "Vega": f"{put_results['vega']:.4f}",
        "Theta": f"{put_results['theta']:.4f}",
        "Rho": f"{put_results['rho']:.4f}"
    }])
    greeks_table.index = ['']

    with col2:
        st.markdown(
            f"""
            <div style='background-color:#fbb6b6;padding:10px;border-radius:10px;text-align:center'>
                <p style='color:black; font-size:20px''>PUT Value</p>
                <p style='color:black; font-size:30px'><b>${put_results["price"]:.2f}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Display as a static table
        st.markdown("### Put Option Greeks")
        st.markdown(greeks_table.style.hide(axis="index").to_html(), unsafe_allow_html=True)