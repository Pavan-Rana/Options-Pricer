# app.py
import streamlit as st
from datetime import date
from domain.option import Option
from pricing.pricing_engine import PricingEngine

# Initialize engine (with strategies and data provider)
engine = PricingEngine()

st.title("Options Pricing Calculator")
st.markdown("Calculate European option prices and Greeks using Black-Scholes or Monte Carlo.")

# Sidebar or main inputs
ticker = st.text_input("Underlying Ticker", value="AAPL")
option_type = st.selectbox("Option Type", ["Call", "Put"])
strike = st.number_input("Strike Price", min_value=0.0, value=100.0)
expiry = st.date_input("Expiration Date", value=date.today())
vol = st.number_input("Volatility (%)", min_value=0.0, value=20.0) / 100.0
rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, value=1.0) / 100.0
model = st.selectbox("Pricing Model", ["Black-Scholes", "Monte Carlo"])
if model == "Monte Carlo":
    paths = st.slider("Monte Carlo paths", min_value=1000, max_value=100000, value=10000, step=1000)
    # update engine's Monte Carlo strategy paths if needed
    engine.strategies["Monte Carlo"].num_paths = paths

# When the user clicks "Calculate", perform pricing
if st.button("Calculate Price"):
    # Create Option object
    opt = Option(underlying_symbol=ticker, strike_price=strike, expiration_date=expiry, option_type=option_type.lower())
    # Calculate price and Greeks
    result = engine.calculate(opt, model_name=model, volatility=vol, risk_free_rate=rate)
    # Display results
    st.subheader(f"Option Price and Greeks ({model})")
    st.write(f"**Price:** {result['price']:.4f}")
    st.write(f"Delta: {result['delta']:.4f}")
    st.write(f"Gamma: {result['gamma']:.4f}")
    st.write(f"Vega: {result['vega']:.4f}")
    st.write(f"Theta: {result['theta']:.4f}")
    st.write(f"Rho: {result['rho']:.4f}")
    # Or use st.metric / st.table for nicer formatting as desired.
