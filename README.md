
# Options Pricer

A Streamlit-based web application for pricing European call and put options using the Black-Scholes model. This tool computes both the option price and Greeks, and visualizes the results with heatmaps.

## Features

- Calculate call and put option prices using the Black-Scholes formula
- Compute option Greeks: Delta, Gamma, Vega, Theta, Rho
- Support for dynamic volatility and interest rate inputs
- Real-time spot price fetching using Yahoo Finance
- Interactive visualizations with Streamlit and Matplotlib

## Project Structure

```
Options-Pricer/
├── app.py                    # Streamlit frontend for the app
├── pricing/
│   ├── black_scholes.py      # Black-Scholes pricing logic
│   ├── pricing_engine.py     # Pricing engine coordinating data and models
│   └── strategy_base.py      # Base class for pricing strategies
├── data_fetchers/
│   ├── base_fetcher.py       # Abstract class for data fetching
│   └── yahoo_fetcher.py      # Fetches market data using yfinance
├── domain/
│   └── option.py             # Option data model
├── ui/
│   └── plots.py              # Heatmap plotting functions
├── tests/                    # Unit tests
└── requirements.txt          # Dependencies
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Options-Pricer.git
cd Options-Pricer

# Create a virtual environment
python -m venv venv
source venv/bin/activate
`venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the Streamlit app
streamlit run app.py
```

## Tests

To run unit tests:

```bash
pytest tests/
```

## License

MIT License
