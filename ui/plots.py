import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_option_price_grid(pricing_engine, option, option_type, rate, purchase_price, vol_range, spot_range):
    price_matrix = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            if option_type == "call":
                option_price = pricing_engine.calculate_call(
                    option, volatility=vol, risk_free_rate=rate, spot=spot
                )
            else:
                option_price = pricing_engine.calculate_put(
                    option, volatility=vol, risk_free_rate=rate, spot=spot
                )
            price_matrix[i, j] = option_price['price'] - purchase_price
            
    return price_matrix


def plot_call_heatmap(pricing_engine, option_template, rate, heatmap_ranges, purchase_price=0.0):
    vol_range, spot_range = get_heatmap_ranges(heatmap_ranges)
    call_prices = generate_option_price_grid(pricing_engine, option_template, "call", rate, purchase_price, vol_range, spot_range)
    fig, axes = plt.subplots(1, 1, figsize=(14, 6))

    cmap = sns.diverging_palette(10, 150, as_cmap=True)
    sns.heatmap(call_prices, annot=True, fmt=".2f", xticklabels=np.round(spot_range, 2),
                yticklabels=np.round(vol_range, 2), ax=axes, cmap=cmap, center=0)
    axes.set_title("Call Price Heatmap")
    axes.set_xlabel("Spot Price")
    axes.set_ylabel("Volatility")

    return fig

def plot_put_heatmap(pricing_engine, option_template, rate, heatmap_ranges, purchase_price=0.0):
    vol_range, spot_range = get_heatmap_ranges(heatmap_ranges)
    put_prices = generate_option_price_grid(pricing_engine, option_template, "put", rate, purchase_price, vol_range, spot_range)
    fig, axes = plt.subplots(1, 1, figsize=(14, 6))

    cmap = sns.diverging_palette(10, 150, as_cmap=True)
    sns.heatmap(put_prices, annot=True, fmt=".2f", xticklabels=np.round(spot_range, 2),
                yticklabels=np.round(vol_range, 2), ax=axes, cmap=cmap, center=0)
    axes.set_title("Put Price Heatmap")
    axes.set_xlabel("Spot Price")
    axes.set_ylabel("Volatility")

    return fig

def get_heatmap_ranges(heatmap_ranges):
    spot_range = np.linspace(heatmap_ranges['min_spot'], heatmap_ranges['max_spot'], 10)
    vol_range = np.linspace(heatmap_ranges['min_vol'], heatmap_ranges['max_vol'], 10)
    return vol_range, spot_range
