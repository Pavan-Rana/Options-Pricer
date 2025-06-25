# ui/plots.py
import numpy as np
import plotly.graph_objects as go

def plot_price_vs_strike(engine, base_option, volatility, risk_free_rate, strikes_delta=0.2, points=21):
    """Generate a Plotly figure for option price vs strike."""
    base_strike = base_option.strike
    # Create an array of strikes around the base strike (e.g., ±20%)
    low = base_strike * (1 - strikes_delta)
    high = base_strike * (1 + strikes_delta)
    strikes = np.linspace(low, high, points)
    prices_call = []
    prices_put = []
    # Compute prices for call and put at each strike
    for K in strikes:
        opt_call = base_option  # copy might be needed if base_option is used repeatedly
        opt_call.strike = K
        opt_call.option_type = "call"
        result_call = engine.calculate(opt_call, model_name="Black-Scholes", 
                                       volatility=volatility, risk_free_rate=risk_free_rate)
        prices_call.append(result_call["price"])
        opt_put = base_option
        opt_put.strike = K
        opt_put.option_type = "put"
        result_put = engine.calculate(opt_put, model_name="Black-Scholes", 
                                      volatility=volatility, risk_free_rate=risk_free_rate)
        prices_put.append(result_put["price"])
    # Build Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=prices_call, mode='lines', name='Call Price'))
    fig.add_trace(go.Scatter(x=strikes, y=prices_put, mode='lines', name='Put Price'))
    fig.update_layout(title="Option Price vs Strike", xaxis_title="Strike Price", yaxis_title="Option Price")
    return fig

def plot_greeks_vs_strike(engine, base_option, volatility, risk_free_rate, greek="Delta", strikes_delta=0.2, points=21):
    """Generate a Plotly figure for a given Greek vs strike."""
    base_strike = base_option.strike
    strikes = np.linspace(base_strike*(1-strikes_delta), base_strike*(1+strikes_delta), points)
    greek_values_call = []
    greek_values_put = []
    for K in strikes:
        opt_call = base_option
        opt_call.strike = K
        opt_call.option_type = "call"
        res_c = engine.calculate(opt_call, model_name="Black-Scholes", volatility=volatility, risk_free_rate=risk_free_rate)
        greek_values_call.append(res_c[greek.lower()])  # dictionary keys are lowercase
        opt_put = base_option
        opt_put.strike = K
        opt_put.option_type = "put"
        res_p = engine.calculate(opt_put, model_name="Black-Scholes", volatility=volatility, risk_free_rate=risk_free_rate)
        greek_values_put.append(res_p[greek.lower()])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=greek_values_call, mode='lines', name=f'Call {greek}'))
    fig.add_trace(go.Scatter(x=strikes, y=greek_values_put, mode='lines', name=f'Put {greek}'))
    fig.update_layout(title=f"{greek} vs Strike", xaxis_title="Strike Price", yaxis_title=f"{greek} value")
    return fig
