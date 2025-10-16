# Stock Market Analysis API & Dashboard

A complete stock market analysis system with RESTful API and interactive web interface.

For Chinese documentation, see [USER_GUIDE_CN.md](USER_GUIDE_CN.md).

## Features

### Four Core API Endpoints

1. **Company Information** (`/api/company/<symbol>`)
   - Detailed company information
   - Business summary, industry, sector
   - Key management personnel

2. **Market Data** (`/api/market/<symbol>`)
   - Real-time stock market data
   - Current price, changes, volume
   - Daily high/low, 52-week range

3. **Historical Data** (`/api/historical/<symbol>`)
   - Historical data for specified date range
   - Open, close, high, low prices
   - Volume data

4. **Analysis & Insights** (`/api/analysis/<symbol>`)
   - Comprehensive technical analysis
   - Price trends, volatility indicators
   - Moving averages, investment recommendations

### Interactive Streamlit Interface

**Five Functional Tabs**:
- Company Info
- Real-time Market Data
- Historical Data Visualization
- Analysis & Insights
- Developer API Documentation

**Data Visualizations**:
- Candlestick Charts
- Price Trend Charts
- Volume Charts
- Moving Average Lines

## Quick Start

### Option A: One-Click Setup (macOS - Recommended)

Double-click `setup.command` to automatically:
- Create conda environment `projAPI` with Python 3.12
- Install all dependencies (Flask, Streamlit, yfinance, pandas, plotly)
- Set up the complete environment

### Option B: Manual Installation

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements_streamlit.txt
```

##### 2. Start Flask API

```bash
python app.py
```

Or on macOS: `./run_flask.command`

API runs at: http://localhost:5001

#### 3. Start Streamlit Interface

```bash
streamlit run streamlit_app.py
```

Or on macOS: `./run_streamlit.command`

Interface opens at: http://localhost:8501

## API Usage Examples

### Get Company Information

```bash
curl http://localhost:5001/api/company/AAPL
```

```python
import requests
response = requests.get('http://localhost:5001/api/company/AAPL')
data = response.json()
```

### Get Market Data

```bash
curl http://localhost:5001/api/market/AAPL
```

### Get Historical Data

```bash
curl -X POST http://localhost:5001/api/historical/AAPL \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01", "end_date": "2024-12-31"}'
```

### Get Analysis

```bash
curl -X POST http://localhost:5001/api/analysis/AAPL \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01", "end_date": "2024-12-31"}'
```

## Run Tests

```bash
python test_all_apis.py
```

## Project Structure

```
.
├── app.py                      # Flask API (4 endpoints)
├── streamlit_app.py            # Streamlit UI (5 tabs)
├── test_all_apis.py            # API tests
├── test_api.py                 # Basic test
├── requirements.txt            # Flask dependencies
├── requirements_streamlit.txt  # Streamlit dependencies
├── run_flask.command          # Flask launcher
├── run_streamlit.command      # Streamlit launcher
├── run_tests.command          # Test launcher
├── setup.command              # Setup script
├── README.md                  # This file
├── USER_GUIDE_CN.md           # Chinese guide
└── PROJECT_FILES.md           # File overview
```

## API Endpoints

**Endpoint 1: Company Information**
- URL: `/api/company/<symbol>`
- Method: GET
- Returns: Company details

**Endpoint 2: Market Data**
- URL: `/api/market/<symbol>`
- Method: GET
- Returns: Real-time market data

**Endpoint 3: Historical Data**
- URL: `/api/historical/<symbol>`
- Method: POST
- Body: `{"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}`
- Returns: Historical OHLCV data

**Endpoint 4: Analysis**
- URL: `/api/analysis/<symbol>`
- Method: POST
- Body: `{"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}`
- Returns: Technical analysis

## Popular Stock Symbols

- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- AMZN (Amazon)
- TSLA (Tesla)
- META (Meta)
- NVDA (NVIDIA)

## Tech Stack

- Backend: Flask 3.0.0
- Frontend: Streamlit 1.40.0
- Data Source: yfinance 0.2.32
- Data Processing: Pandas 2.2.0
- Visualization: Plotly 5.18.0

## Troubleshooting

**Flask won't start**
- Check port 5001: `lsof -i :5001`
- Install dependencies: `pip install -r requirements.txt`

**Streamlit can't connect**
- Ensure Flask is running
- Visit: http://localhost:5001/

**Can't fetch data**
- Check stock symbol
- Verify network connection
- Yahoo Finance may have rate limits

## License

For educational purposes only.

Made with Flask, Streamlit, and Yahoo Finance API.
