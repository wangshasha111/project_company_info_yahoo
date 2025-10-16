from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    """Root endpoint - API information"""
    return jsonify({
        "message": "Stock Market API",
        "version": "1.0",
        "endpoints": {
            "company_info": "/api/company/<symbol>",
            "market_data": "/api/market/<symbol>",
            "historical_data": "/api/historical/<symbol>",
            "analysis": "/api/analysis/<symbol>"
        },
        "documentation": "See Streamlit UI for detailed API documentation"
    })


@app.route('/api/company/<symbol>', methods=['GET'])
def get_company_info(symbol):
    """
    Endpoint 1: Retrieve detailed company information by stock symbol.
    
    Args:
        symbol (str): Valid company stock symbol (e.g., AAPL, MSFT, GOOGL)
    
    Returns:
        JSON response with company information including:
        - Full company name
        - Business summary
        - Industry
        - Sector
        - Key officers (names and titles)
    """
    try:
        # Validate symbol parameter
        if not symbol or symbol.strip() == '':
            return jsonify({
                'error': 'Invalid symbol',
                'message': 'Please provide a valid company symbol'
            }), 400
        
        # Fetch company data from Yahoo Finance
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        # Check if the ticker is valid
        if not info or 'symbol' not in info:
            return jsonify({
                'error': 'Symbol not found',
                'message': f'No data found for symbol: {symbol}'
            }), 404
        
        # Extract company information
        company_data = {
            'symbol': info.get('symbol', symbol.upper()),
            'company_name': info.get('longName', 'N/A'),
            'business_summary': info.get('longBusinessSummary', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'country': info.get('country', 'N/A'),
            'website': info.get('website', 'N/A'),
            'key_officers': []
        }
        
        # Extract key officers information
        officers = info.get('companyOfficers', [])
        if officers:
            for officer in officers:
                officer_info = {
                    'name': officer.get('name', 'N/A'),
                    'title': officer.get('title', 'N/A'),
                    'age': officer.get('age', 'N/A')
                }
                company_data['key_officers'].append(officer_info)
        
        return jsonify({
            'success': True,
            'data': company_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/market/<symbol>', methods=['GET'])
def get_market_data(symbol):
    """
    Endpoint 2: Fetch real-time stock market data.
    
    Args:
        symbol (str): Valid company stock symbol
    
    Returns:
        JSON response with market data including:
        - Market state
        - Current market price
        - Price change
        - Percentage change
        - Volume, high, low, etc.
    """
    try:
        # Validate symbol parameter
        if not symbol or symbol.strip() == '':
            return jsonify({
                'error': 'Invalid symbol',
                'message': 'Please provide a valid company symbol'
            }), 400
        
        # Fetch market data from Yahoo Finance
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        # Check if the ticker is valid
        if not info or 'symbol' not in info:
            return jsonify({
                'error': 'Symbol not found',
                'message': f'No data found for symbol: {symbol}'
            }), 404
        
        # Extract market data
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        previous_close = info.get('previousClose', 0)
        
        # Calculate change and percentage change
        if previous_close and previous_close != 0:
            price_change = current_price - previous_close
            percentage_change = (price_change / previous_close) * 100
        else:
            price_change = 0
            percentage_change = 0
        
        market_data = {
            'symbol': info.get('symbol', symbol.upper()),
            'company_name': info.get('longName', 'N/A'),
            'market_state': info.get('marketState', 'N/A'),
            'current_price': current_price,
            'previous_close': previous_close,
            'price_change': round(price_change, 2),
            'percentage_change': round(percentage_change, 2),
            'day_high': info.get('dayHigh', 'N/A'),
            'day_low': info.get('dayLow', 'N/A'),
            'volume': info.get('volume', 'N/A'),
            'average_volume': info.get('averageVolume', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'currency': info.get('currency', 'USD')
        }
        
        return jsonify({
            'success': True,
            'data': market_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/historical/<symbol>', methods=['POST'])
def get_historical_data(symbol):
    """
    Endpoint 3: Return historical market data for specified date range.
    
    Args:
        symbol (str): Valid company stock symbol
        JSON payload:
            - start_date (str): Start date in YYYY-MM-DD format
            - end_date (str): End date in YYYY-MM-DD format
    
    Returns:
        JSON response with historical data array
    """
    try:
        # Validate symbol parameter
        if not symbol or symbol.strip() == '':
            return jsonify({
                'error': 'Invalid symbol',
                'message': 'Please provide a valid company symbol'
            }), 400
        
        # Get JSON payload
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Please provide JSON payload with start_date and end_date'
            }), 400
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Validate dates
        if not start_date or not end_date:
            return jsonify({
                'error': 'Missing parameters',
                'message': 'Both start_date and end_date are required'
            }), 400
        
        try:
            # Validate date format
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'error': 'Invalid date format',
                'message': 'Dates must be in YYYY-MM-DD format'
            }), 400
        
        # Fetch historical data from Yahoo Finance
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(start=start_date, end=end_date)
        
        if hist.empty:
            return jsonify({
                'error': 'No data found',
                'message': f'No historical data found for {symbol} in the specified date range'
            }), 404
        
        # Convert to list of dictionaries
        historical_data = []
        for date, row in hist.iterrows():
            historical_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(row['Open'], 2),
                'high': round(row['High'], 2),
                'low': round(row['Low'], 2),
                'close': round(row['Close'], 2),
                'volume': int(row['Volume'])
            })
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol.upper(),
                'start_date': start_date,
                'end_date': end_date,
                'records_count': len(historical_data),
                'historical_data': historical_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/analysis/<symbol>', methods=['POST'])
def get_analytical_insights(symbol):
    """
    Endpoint 4: Perform comprehensive analysis and deliver actionable insights.
    
    Args:
        symbol (str): Valid company stock symbol
        JSON payload (optional):
            - start_date (str): Start date for analysis (default: 1 year ago)
            - end_date (str): End date for analysis (default: today)
    
    Returns:
        JSON response with analytical insights including:
        - Price trends
        - Volatility metrics
        - Trading volume analysis
        - Performance metrics
        - Recommendations
    """
    try:
        # Validate symbol parameter
        if not symbol or symbol.strip() == '':
            return jsonify({
                'error': 'Invalid symbol',
                'message': 'Please provide a valid company symbol'
            }), 400
        
        # Get JSON payload (optional)
        data = request.get_json() or {}
        
        # Default to 1 year of data
        end_date = data.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        start_date = data.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
        
        # Fetch data
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        hist = ticker.history(start=start_date, end=end_date)
        
        if hist.empty:
            return jsonify({
                'error': 'No data found',
                'message': f'No data found for {symbol}'
            }), 404
        
        # Calculate analytics
        current_price = hist['Close'].iloc[-1]
        start_price = hist['Close'].iloc[0]
        price_change = current_price - start_price
        percentage_change = (price_change / start_price) * 100
        
        # Volatility (standard deviation of returns)
        returns = hist['Close'].pct_change().dropna()
        volatility = returns.std() * 100
        
        # Average volume
        avg_volume = hist['Volume'].mean()
        
        # High and low in period
        period_high = hist['High'].max()
        period_low = hist['Low'].min()
        
        # Moving averages
        ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
        ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else None
        
        # Generate insights
        insights = []
        
        # Price trend
        if percentage_change > 0:
            insights.append(f"📈 Stock has gained {abs(percentage_change):.2f}% over the analyzed period")
        else:
            insights.append(f"📉 Stock has declined {abs(percentage_change):.2f}% over the analyzed period")
        
        # Volatility assessment
        if volatility < 1:
            insights.append(f"🔹 Low volatility ({volatility:.2f}%) - relatively stable stock")
        elif volatility < 2:
            insights.append(f"🔸 Moderate volatility ({volatility:.2f}%) - normal price fluctuations")
        else:
            insights.append(f"🔺 High volatility ({volatility:.2f}%) - significant price swings")
        
        # Moving average signals
        if ma_50 and ma_200:
            if ma_50 > ma_200:
                insights.append("✅ Golden Cross: 50-day MA above 200-day MA (bullish signal)")
            else:
                insights.append("⚠️ Death Cross: 50-day MA below 200-day MA (bearish signal)")
        
        # Current price position
        distance_from_high = ((period_high - current_price) / period_high) * 100
        if distance_from_high < 5:
            insights.append(f"🎯 Trading near period high (within {distance_from_high:.1f}%)")
        elif distance_from_high > 20:
            insights.append(f"💡 Trading {distance_from_high:.1f}% below period high - potential opportunity")
        
        analysis_data = {
            'symbol': symbol.upper(),
            'company_name': info.get('longName', 'N/A'),
            'analysis_period': {
                'start_date': start_date,
                'end_date': end_date,
                'days_analyzed': len(hist)
            },
            'price_analysis': {
                'current_price': round(current_price, 2),
                'start_price': round(start_price, 2),
                'price_change': round(price_change, 2),
                'percentage_change': round(percentage_change, 2),
                'period_high': round(period_high, 2),
                'period_low': round(period_low, 2)
            },
            'technical_indicators': {
                'volatility': round(volatility, 2),
                'moving_average_50': round(ma_50, 2) if ma_50 else 'N/A',
                'moving_average_200': round(ma_200, 2) if ma_200 else 'N/A'
            },
            'volume_analysis': {
                'average_volume': int(avg_volume),
                'latest_volume': int(hist['Volume'].iloc[-1])
            },
            'insights': insights,
            'recommendation': _generate_recommendation(percentage_change, volatility, info)
        }
        
        return jsonify({
            'success': True,
            'data': analysis_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


def _generate_recommendation(percentage_change, volatility, info):
    """Generate investment recommendation based on analysis."""
    score = 0
    
    # Price trend score
    if percentage_change > 20:
        score += 2
    elif percentage_change > 0:
        score += 1
    elif percentage_change > -10:
        score += 0
    else:
        score -= 1
    
    # Volatility score (prefer moderate volatility)
    if volatility < 1:
        score += 1
    elif volatility > 3:
        score -= 1
    
    # Generate recommendation
    if score >= 2:
        return {
            'rating': 'BUY',
            'confidence': 'High',
            'note': 'Strong positive indicators suggest buying opportunity'
        }
    elif score >= 1:
        return {
            'rating': 'HOLD',
            'confidence': 'Medium',
            'note': 'Mixed signals - consider holding current position'
        }
    else:
        return {
            'rating': 'WATCH',
            'confidence': 'Low',
            'note': 'Cautious approach recommended - monitor closely'
        }


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Stock Market API is running',
        'endpoints': {
            'company_info': '/api/company/<symbol>',
            'market_data': '/api/market/<symbol>',
            'historical_data': '/api/historical/<symbol> (POST)',
            'analysis': '/api/analysis/<symbol> (POST)'
        }
    }), 200


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API documentation.
    """
    return jsonify({
        'message': 'Welcome to the Stock Market Analysis API',
        'version': '1.0.0',
        'endpoints': {
            '/api/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            '/api/company/<symbol>': {
                'method': 'GET',
                'description': 'Get detailed company information',
                'example': '/api/company/AAPL'
            },
            '/api/market/<symbol>': {
                'method': 'GET',
                'description': 'Get real-time market data',
                'example': '/api/market/AAPL'
            },
            '/api/historical/<symbol>': {
                'method': 'POST',
                'description': 'Get historical market data for date range',
                'payload': {
                    'start_date': 'YYYY-MM-DD',
                    'end_date': 'YYYY-MM-DD'
                },
                'example': '/api/historical/AAPL'
            },
            '/api/analysis/<symbol>': {
                'method': 'POST',
                'description': 'Get analytical insights and recommendations',
                'payload_optional': {
                    'start_date': 'YYYY-MM-DD',
                    'end_date': 'YYYY-MM-DD'
                },
                'example': '/api/analysis/AAPL'
            }
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
