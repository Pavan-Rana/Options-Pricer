import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from domain.option import Option

def generate_option_price_grid(pricing_engine, option, option_type, rate, min_spot, max_spot, min_vol, max_vol, purchase_price):
    spot_range = np.linspace(min_spot, max_spot, 10)
    vol_range = np.linspace(min_vol, max_vol, 10)
    price_matrix = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            call_result, put_result = pricing_engine.calculate(
                option, volatility=vol, risk_free_rate=rate, spot=spot
            )
            price_matrix[i, j] = call_result['price'] - purchase_price if option_type == "call" else put_result['price'] - purchase_price

    return spot_range, vol_range, price_matrix


def plot_heatmaps(pricing_engine, option_template, rate, option_type="call", min_spot=90, max_spot=120, min_vol=0.05, purchase_price=0.0, max_vol=0.5):
    if option_type == "call":
        spot_range, vol_range, call_prices = generate_option_price_grid(pricing_engine, option_template, "call", rate, min_spot, max_spot, min_vol, max_vol, purchase_price)
    else:
        spot_range, vol_range, put_prices = generate_option_price_grid(pricing_engine, option_template, "put", rate, min_spot, max_spot, min_vol, max_vol, purchase_price)

    fig, axes = plt.subplots(1, 1, figsize=(14, 6))

    cmap = sns.diverging_palette(10, 150, as_cmap=True)
    if option_type == "call":
        sns.heatmap(call_prices, annot=True, fmt=".2f", xticklabels=np.round(spot_range, 2),
                    yticklabels=np.round(vol_range, 2), ax=axes, cmap=cmap, center=0)
        axes.set_title("Call Price Heatmap")
        axes.set_xlabel("Spot Price")
        axes.set_ylabel("Volatility")
    else:
        sns.heatmap(put_prices, annot=True, fmt=".2f", xticklabels=np.round(spot_range, 2),
                    yticklabels=np.round(vol_range, 2), ax=axes, cmap=cmap, center=0)
        axes.set_title("Put Price Heatmap")
        axes.set_xlabel("Spot Price")
        axes.set_ylabel("Volatility")

    # plt.tight_layout()
    return fig


def plot_price_vs_strike(engine, option, vol, rate):
    strikes = np.linspace(option.strike_price * 0.8, option.strike_price * 1.2, 50)
    prices_call = []
    prices_put = []

    for k in strikes:
        opt = option.copy_with_new_strike(k)
        call, put = engine.calculate(opt, model_name="Black-Scholes", volatility=vol, risk_free_rate=rate)
        prices_call.append(call['price'])
        prices_put.append(put['price'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=prices_call, name="Call Price", line=dict(color='green')))
    fig.add_trace(go.Scatter(x=strikes, y=prices_put, name="Put Price", line=dict(color='red')))
    fig.update_layout(title="Option Prices vs Strike Price", xaxis_title="Strike Price", yaxis_title="Option Price")
    return fig


def plot_greeks_vs_strike(engine, option, vol, rate, greek="Delta"):
    strikes = np.linspace(option.strike_price * 0.8, option.strike_price * 1.2, 50)
    greek_call = []
    greek_put = []

    for k in strikes:
        opt = option.copy_with_new_strike(k)
        call, put = engine.calculate(opt, model_name="Black-Scholes", volatility=vol, risk_free_rate=rate)
        greek_call.append(call[greek.lower()])
        greek_put.append(put[greek.lower()])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=greek_call, name=f"Call {greek}", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=strikes, y=greek_put, name=f"Put {greek}", line=dict(color='orange')))
    fig.update_layout(title=f"{greek} vs Strike Price", xaxis_title="Strike Price", yaxis_title=greek)
    return fig
