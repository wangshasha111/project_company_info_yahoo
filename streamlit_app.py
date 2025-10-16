import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
import time
import os

# Conditional import of plotly with fallback
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    st.error("📦 Plotly is not installed. Charts will be disabled.")
    st.info("🔄 Please wait while dependencies are being installed...")
    PLOTLY_AVAILABLE = False

# Check if running in Streamlit Cloud
IS_CLOUD_DEPLOYMENT = os.getenv('STREAMLIT_SHARING_MODE') == 'cloud' or 'streamlit.app' in os.getenv('HOSTNAME', '')

# Initialize app with error handling
def check_core_dependencies():
    """Check if core dependencies are available"""
    if not PLOTLY_AVAILABLE:
        st.warning("⚠️ Plotly is not available - charts will be limited")
        st.info("🔄 If this persists, try refreshing the page")
        return False
    return True

# Run dependency check
check_core_dependencies()

# Helper function for safe plotting
def safe_plotly_chart(fig, **kwargs):
    """Safely display plotly chart with fallback"""
    if PLOTLY_AVAILABLE:
        safe_plotly_chart(fig, **kwargs)
    else:
        st.error("📊 Chart cannot be displayed - Plotly is not available")
        st.info("🔄 Please refresh the page or check the app logs")

# Page configuration
st.set_page_config(
    page_title="Stock Market Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main header styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 5px;
        transition: all 0.3s;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
    }
    
    /* Better spacing */
    h1, h2, h3 {
        padding-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 添加缓存装饰器，减少 API 调用
@st.cache_data(ttl=300, show_spinner=False)  # 缓存5分钟
def get_ticker_data(symbol):
    """获取股票数据并缓存"""
    try:
        if not symbol or len(symbol) < 1:
            return None
        ticker = yf.Ticker(symbol)
        # Test if ticker is valid by trying to get basic info
        info = ticker.info
        if info and len(info) > 0:
            return ticker
        return None
    except Exception as e:
        # Don't show error on initial load, only when user actually searches
        return None

# Title and description - Compact version
st.title("📊 Stock Market Analysis Dashboard")
st.caption("Real-time stock analysis powered by Yahoo Finance API")

# Add rate limit notice - collapsed by default
with st.expander("ℹ️ About Rate Limits & Usage Tips"):
    st.markdown("""
    **Yahoo Finance API Information**
    
    - ✅ **5-10 minute caching** enabled to minimize API calls
    - ⚠️ If you see rate limit errors, wait 30-60 seconds
    - 💡 Use sidebar buttons for quick access to popular stocks
    - 🔄 Clear cache from menu (top right) if data seems outdated
    """)

# Sidebar
st.sidebar.title("🎯 Navigation")

# Initialize tab selection in session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Navigation buttons with better styling
nav_buttons = [
    ("🏢", "Company Info"),
    ("📈", "Market Data"),
    ("📊", "Historical"),
    ("🔍", "Analysis"),
    ("🔌", "Developer API")
]

for idx, (icon, label) in enumerate(nav_buttons):
    button_type = "primary" if st.session_state.active_tab == idx else "secondary"
    if st.sidebar.button(f"{icon} {label}", use_container_width=True, key=f"nav_{idx}", type=button_type):
        st.session_state.active_tab = idx
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌟 Quick Access")
st.sidebar.caption("Popular stocks:")

popular_stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Meta": "META",
    "NVIDIA": "NVDA",
    "Netflix": "NFLX"
}

# Initialize session state
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = 'AAPL'

# Quick access buttons in sidebar - compact 2-column layout
stock_items = list(popular_stocks.items())
for i in range(0, len(stock_items), 2):
    col1, col2 = st.sidebar.columns(2)
    
    # First stock in row
    name1, symbol1 = stock_items[i]
    with col1:
        if st.button(symbol1, key=f"btn_{symbol1}", use_container_width=True):
            st.session_state.selected_symbol = symbol1
            st.rerun()
    
    # Second stock in row (if exists)
    if i + 1 < len(stock_items):
        name2, symbol2 = stock_items[i + 1]
        with col2:
            if st.button(symbol2, key=f"btn_{symbol2}", use_container_width=True):
                st.session_state.selected_symbol = symbol2
                st.rerun()

st.sidebar.markdown("---")

# Main input - cleaner layout
st.markdown("### 🔍 Stock Symbol Search")
col1, col2 = st.columns([4, 1])
with col1:
    symbol = st.text_input(
        "Enter symbol:",
        value=st.session_state.selected_symbol,
        placeholder="e.g., AAPL, MSFT, GOOGL",
        key='symbol_input',
        label_visibility="collapsed"
    ).upper()
    
    if symbol != st.session_state.selected_symbol:
        st.session_state.selected_symbol = symbol

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

st.markdown("---")

# Helper Functions
@st.cache_data(ttl=300)  # 缓存5分钟
def get_company_info(symbol):
    """Fetch company information from Yahoo Finance"""
    try:
        time.sleep(0.5)  # 添加延迟避免速率限制
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info or 'symbol' not in info:
            return None
        return info
    except Exception as e:
        st.warning(f"⚠️ Error fetching company data: {str(e)}")
        st.info("💡 Tip: Wait a moment and try again, or try a different stock symbol.")
        return None

@st.cache_data(ttl=300)  # 缓存5分钟
def get_market_data(symbol):
    """Fetch real-time market data"""
    try:
        time.sleep(0.5)  # 添加延迟避免速率限制
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info or 'symbol' not in info:
            return None
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        previous_close = info.get('previousClose', 0)
        
        if previous_close and previous_close != 0:
            price_change = current_price - previous_close
            percentage_change = (price_change / previous_close) * 100
        else:
            price_change = 0
            percentage_change = 0
        
        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'price_change': price_change,
            'percentage_change': percentage_change,
            'day_high': info.get('dayHigh', 'N/A'),
            'day_low': info.get('dayLow', 'N/A'),
            'volume': info.get('volume', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'info': info
        }
    except Exception as e:
        st.warning(f"⚠️ Error fetching market data: {str(e)}")
        st.info("💡 Tip: Yahoo Finance may be rate limiting. Please wait a moment and try again.")
        return None

@st.cache_data(ttl=600)  # 缓存10分钟
def get_historical_data(symbol, start_date, end_date):
    """Fetch historical data for date range"""
    try:
        time.sleep(0.5)  # 添加延迟避免速率限制
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=end_date)
        return hist if not hist.empty else None
    except Exception as e:
        st.warning(f"⚠️ Error fetching historical data: {str(e)}")
        st.info("💡 Tip: Try a shorter date range or wait a moment before trying again.")
        return None

def calculate_analysis(hist, info):
    """Calculate analytical insights from historical data"""
    if hist is None or hist.empty:
        return None
    
    current_price = hist['Close'].iloc[-1]
    start_price = hist['Close'].iloc[0]
    price_change = current_price - start_price
    percentage_change = (price_change / start_price) * 100
    
    returns = hist['Close'].pct_change().dropna()
    volatility = returns.std() * 100
    
    avg_volume = hist['Volume'].mean()
    period_high = hist['High'].max()
    period_low = hist['Low'].min()
    
    ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
    ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else None
    
    insights = []
    
    if percentage_change > 0:
        insights.append(f"📈 Stock has gained {abs(percentage_change):.2f}% over the analyzed period")
    else:
        insights.append(f"📉 Stock has declined {abs(percentage_change):.2f}% over the analyzed period")
    
    if volatility < 1:
        insights.append(f"🔹 Low volatility ({volatility:.2f}%) - relatively stable stock")
    elif volatility < 2:
        insights.append(f"🔸 Moderate volatility ({volatility:.2f}%) - normal price fluctuations")
    else:
        insights.append(f"🔺 High volatility ({volatility:.2f}%) - significant price swings")
    
    if ma_50 and ma_200:
        if ma_50 > ma_200:
            insights.append("✅ Golden Cross: 50-day MA above 200-day MA (bullish signal)")
        else:
            insights.append("⚠️ Death Cross: 50-day MA below 200-day MA (bearish signal)")
    
    distance_from_high = ((period_high - current_price) / period_high) * 100
    if distance_from_high < 5:
        insights.append(f"🎯 Trading near period high (within {distance_from_high:.1f}%)")
    elif distance_from_high > 20:
        insights.append(f"💡 Trading {distance_from_high:.1f}% below period high")
    
    return {
        'current_price': current_price,
        'start_price': start_price,
        'price_change': price_change,
        'percentage_change': percentage_change,
        'volatility': volatility,
        'avg_volume': avg_volume,
        'period_high': period_high,
        'period_low': period_low,
        'ma_50': ma_50,
        'ma_200': ma_200,
        'insights': insights
    }

# Get the selected tab from session state
selected_tab = st.session_state.active_tab

# Render the selected tab content
if selected_tab == 0:
    # TAB 1: Company Information
    st.header("🏢 Company Information")
    
    if symbol:
        with st.spinner(f'Fetching company data for {symbol}...'):
            info = get_company_info(symbol)
            
            if info:
                # Company Header - more prominent
                st.markdown(f"# {info.get('longName', symbol)}")
                st.caption(f"**{info.get('symbol', symbol)}** | {info.get('exchange', 'N/A')}")
                
                st.markdown("---")
                
                # Key Metrics - Better visual hierarchy with 3 columns
                st.markdown("### 📈 Key Metrics")
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    market_cap = info.get('marketCap', 'N/A')
                    if isinstance(market_cap, (int, float)):
                        # Format large numbers
                        if market_cap >= 1e12:
                            cap_str = f"${market_cap/1e12:.2f}T"
                        elif market_cap >= 1e9:
                            cap_str = f"${market_cap/1e9:.2f}B"
                        elif market_cap >= 1e6:
                            cap_str = f"${market_cap/1e6:.2f}M"
                        else:
                            cap_str = f"${market_cap:,.0f}"
                        st.metric("Market Cap", cap_str)
                    else:
                        st.metric("Market Cap", market_cap)
                
                with metric_col2:
                    sector = info.get('sector', 'N/A')
                    st.metric("Sector", sector)
                
                with metric_col3:
                    country = info.get('country', 'N/A')
                    st.metric("Country", country)
                
                # Second row of metrics
                metric_col4, metric_col5, metric_col6 = st.columns(3)
                
                with metric_col4:
                    employees = info.get('fullTimeEmployees', 'N/A')
                    if isinstance(employees, int):
                        st.metric("Employees", f"{employees:,}")
                    else:
                        st.metric("Employees", employees)
                
                with metric_col5:
                    industry = info.get('industry', 'N/A')
                    st.metric("Industry", industry)
                
                with metric_col6:
                    currency = info.get('currency', 'N/A')
                    st.metric("Currency", currency)
                
                st.markdown("---")
                
                # Business Summary - better formatting
                st.markdown("### 📋 Business Summary")
                business_summary = info.get('longBusinessSummary', 'No business summary available.')
                with st.container():
                    st.write(business_summary)
                
                st.markdown("---")
                
                # Two column layout for officers and details
                col_left, col_right = st.columns([3, 2])
                
                with col_left:
                    # Key Officers
                    st.markdown("### 👥 Key Officers")
                    officers = info.get('companyOfficers', [])
                    
                    if officers:
                        officers_data = []
                        for officer in officers[:5]:  # Show top 5
                            officers_data.append({
                                'Name': officer.get('name', 'N/A'),
                                'Title': officer.get('title', 'N/A'),
                                'Age': str(officer.get('age', 'N/A'))
                            })
                        df_officers = pd.DataFrame(officers_data)
                        st.dataframe(df_officers, hide_index=True, use_container_width=True)
                        
                        if len(officers) > 5:
                            with st.expander(f"View {len(officers) - 5} more officers"):
                                more_officers = []
                                for officer in officers[5:]:
                                    more_officers.append({
                                        'Name': officer.get('name', 'N/A'),
                                        'Title': officer.get('title', 'N/A'),
                                        'Age': str(officer.get('age', 'N/A'))
                                    })
                                df_more = pd.DataFrame(more_officers)
                                st.dataframe(df_more, hide_index=True, use_container_width=True)
                    else:
                        st.info("No officer information available.")
                
                with col_right:
                    # Contact & Location Information
                    st.markdown("### 📍 Contact & Location")
                    contact_info = {
                        "Website": info.get('website', 'N/A'),
                        "Phone": info.get('phone', 'N/A'),
                        "City": info.get('city', 'N/A'),
                        "Exchange": info.get('exchange', 'N/A')
                    }
                    
                    for label, value in contact_info.items():
                        if value and value != 'N/A':
                            st.text(f"{label}: {value}")
            else:
                st.error(f"❌ No data found for: **{symbol}**")

elif selected_tab == 1:
    # TAB 2: Market Data
    st.header("📈 Real-Time Market Data")
    
    if symbol:
        with st.spinner(f'Fetching market data for {symbol}...'):
            market_data = get_market_data(symbol)
            
            if market_data:
                info = market_data['info']
                
                # Current Price Display
                st.markdown("### 💰 Current Price")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    current_price = market_data['current_price']
                    st.metric(
                        "Current Price",
                        f"${current_price:.2f}",
                        f"{market_data['price_change']:.2f} ({market_data['percentage_change']:.2f}%)"
                    )
                
                with col2:
                    st.metric("Previous Close", f"${market_data['previous_close']:.2f}")
                
                with col3:
                    market_state = info.get('marketState', 'N/A')
                    state_color = "🟢" if market_state == "REGULAR" else "🔴"
                    st.metric("Market State", f"{state_color} {market_state}")
                
                # Trading Metrics
                st.markdown("### 📊 Trading Metrics")
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    if market_data['day_high'] != 'N/A':
                        st.metric("Day High", f"${market_data['day_high']:.2f}")
                    else:
                        st.metric("Day High", "N/A")
                
                with metric_col2:
                    if market_data['day_low'] != 'N/A':
                        st.metric("Day Low", f"${market_data['day_low']:.2f}")
                    else:
                        st.metric("Day Low", "N/A")
                
                with metric_col3:
                    if market_data['volume'] != 'N/A':
                        st.metric("Volume", f"{market_data['volume']:,}")
                    else:
                        st.metric("Volume", "N/A")
                
                with metric_col4:
                    if market_data['market_cap'] != 'N/A':
                        st.metric("Market Cap", f"${market_data['market_cap']:,.0f}")
                    else:
                        st.metric("Market Cap", "N/A")
                
                # 52 Week Range
                st.markdown("### 📅 52-Week Range")
                col1, col2 = st.columns(2)
                
                with col1:
                    week_high = info.get('fiftyTwoWeekHigh', 'N/A')
                    if week_high != 'N/A':
                        st.metric("52-Week High", f"${week_high:.2f}")
                    else:
                        st.metric("52-Week High", "N/A")
                
                with col2:
                    week_low = info.get('fiftyTwoWeekLow', 'N/A')
                    if week_low != 'N/A':
                        st.metric("52-Week Low", f"${week_low:.2f}")
                    else:
                        st.metric("52-Week Low", "N/A")
                
                # Price Chart (Last 5 days)
                st.markdown("### 📈 Recent Price Movement (5 Days)")
                try:
                    ticker = yf.Ticker(symbol)
                    recent_hist = ticker.history(period="5d")
                    
                    if not recent_hist.empty:
                        fig = go.Figure()
                        fig.add_trace(go.Candlestick(
                            x=recent_hist.index,
                            open=recent_hist['Open'],
                            high=recent_hist['High'],
                            low=recent_hist['Low'],
                            close=recent_hist['Close'],
                            name=symbol
                        ))
                        fig.update_layout(
                            title=f"{symbol} - Last 5 Days",
                            yaxis_title="Price (USD)",
                            xaxis_title="Date",
                            height=450,
                            template="plotly_white"
                        )
                        safe_plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No recent price data available")
                except Exception as e:
                    st.error(f"Error loading chart: {str(e)}")
                
            else:
                st.error(f"❌ No market data found for: **{symbol}**")


elif selected_tab == 2:
    # TAB 3: Historical Data
    st.header("📊 Historical Market Data")
    
    if symbol:
        # Date range selector
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.now() - timedelta(days=365),
                max_value=datetime.now()
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now(),
                max_value=datetime.now()
            )
        
        if st.button("📥 Fetch Historical Data", type="primary"):
            with st.spinner(f'Fetching historical data for {symbol}...'):
                hist = get_historical_data(symbol, start_date, end_date)
                
                if hist is not None and not hist.empty:
                    # Summary metrics
                    st.markdown("### 📈 Period Summary")
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("Records", len(hist))
                    
                    with metric_col2:
                        avg_close = hist['Close'].mean()
                        st.metric("Avg Close", f"${avg_close:.2f}")
                    
                    with metric_col3:
                        max_high = hist['High'].max()
                        st.metric("Highest", f"${max_high:.2f}")
                    
                    with metric_col4:
                        min_low = hist['Low'].min()
                        st.metric("Lowest", f"${min_low:.2f}")
                    
                    # Price Chart
                    st.markdown("### 📊 Price Chart")
                    fig = go.Figure()
                    
                    fig.add_trace(go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name=symbol
                    ))
                    
                    fig.update_layout(
                        title=f"{symbol} - Historical Price ({start_date} to {end_date})",
                        yaxis_title="Price (USD)",
                        xaxis_title="Date",
                        height=500,
                        xaxis_rangeslider_visible=False,
                        template="plotly_white"
                    )
                    
                    safe_plotly_chart(fig, use_container_width=True)
                    
                    # Volume Chart
                    st.markdown("### 📊 Volume Chart")
                    fig_volume = go.Figure()
                    fig_volume.add_trace(go.Bar(
                        x=hist.index,
                        y=hist['Volume'],
                        name='Volume',
                        marker_color='lightblue'
                    ))
                    
                    fig_volume.update_layout(
                        title=f"{symbol} - Trading Volume",
                        yaxis_title="Volume",
                        xaxis_title="Date",
                        height=350,
                        template="plotly_white"
                    )
                    
                    safe_plotly_chart(fig_volume, use_container_width=True)
                    
                    # Data Table
                    st.markdown("### 📋 Historical Data Table")
                    
                    # Prepare data for display
                    hist_display = hist.copy()
                    hist_display.index = hist_display.index.strftime('%Y-%m-%d')
                    hist_display = hist_display[['Open', 'High', 'Low', 'Close', 'Volume']]
                    hist_display = hist_display.round(2)
                    
                    st.dataframe(hist_display, use_container_width=True)
                    
                    # Download button
                    csv = hist_display.to_csv()
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{symbol}_historical_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.error(f"❌ No historical data found for: **{symbol}** in the specified date range")


elif selected_tab == 3:
    # TAB 4: Analysis & Insights
    st.header("🔍 Analytical Insights")
    
    if symbol:
        # Analysis period selector
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_start = st.date_input(
                "Analysis Start Date",
                value=datetime.now() - timedelta(days=365),
                max_value=datetime.now(),
                key="analysis_start"
            )
        
        with col2:
            analysis_end = st.date_input(
                "Analysis End Date",
                value=datetime.now(),
                max_value=datetime.now(),
                key="analysis_end"
            )
        
        if st.button("🔍 Generate Analysis", type="primary"):
            with st.spinner(f'Analyzing {symbol}...'):
                # Fetch data
                info = get_company_info(symbol)
                hist = get_historical_data(symbol, analysis_start, analysis_end)
                
                if hist is not None and not hist.empty and info:
                    analysis = calculate_analysis(hist, info)
                    
                    if analysis:
                        # Header
                        st.markdown(f"### Analysis Report: {info.get('longName', symbol)}")
                        st.caption(f"Period: {analysis_start} to {analysis_end} ({len(hist)} trading days)")
                        
                        st.markdown("---")
                        
                        # Key Metrics
                        st.markdown("### 📊 Performance Metrics")
                        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                        
                        with metric_col1:
                            st.metric(
                                "Current Price",
                                f"${analysis['current_price']:.2f}",
                                f"{analysis['price_change']:.2f} ({analysis['percentage_change']:.2f}%)"
                            )
                        
                        with metric_col2:
                            st.metric("Period Start", f"${analysis['start_price']:.2f}")
                        
                        with metric_col3:
                            st.metric("Period High", f"${analysis['period_high']:.2f}")
                        
                        with metric_col4:
                            st.metric("Period Low", f"${analysis['period_low']:.2f}")
                        
                        # Technical Indicators
                        st.markdown("### 📈 Technical Indicators")
                        tech_col1, tech_col2, tech_col3 = st.columns(3)
                        
                        with tech_col1:
                            st.metric("Volatility", f"{analysis['volatility']:.2f}%")
                        
                        with tech_col2:
                            if analysis['ma_50']:
                                st.metric("50-Day MA", f"${analysis['ma_50']:.2f}")
                            else:
                                st.metric("50-Day MA", "N/A")
                        
                        with tech_col3:
                            if analysis['ma_200']:
                                st.metric("200-Day MA", f"${analysis['ma_200']:.2f}")
                            else:
                                st.metric("200-Day MA", "N/A")
                        
                        # Price Chart with Moving Averages
                        st.markdown("### 📊 Price Trend with Moving Averages")
                        fig = go.Figure()
                        
                        # Closing price
                        fig.add_trace(go.Scatter(
                            x=hist.index,
                            y=hist['Close'],
                            mode='lines',
                            name='Close Price',
                            line=dict(color='blue', width=2)
                        ))
                        
                        # 50-day MA
                        if len(hist) >= 50:
                            ma50 = hist['Close'].rolling(window=50).mean()
                            fig.add_trace(go.Scatter(
                                x=hist.index,
                                y=ma50,
                                mode='lines',
                                name='50-Day MA',
                                line=dict(color='orange', width=1, dash='dash')
                            ))
                        
                        # 200-day MA
                        if len(hist) >= 200:
                            ma200 = hist['Close'].rolling(window=200).mean()
                            fig.add_trace(go.Scatter(
                                x=hist.index,
                                y=ma200,
                                mode='lines',
                                name='200-Day MA',
                                line=dict(color='red', width=1, dash='dot')
                            ))
                        
                        fig.update_layout(
                            title=f"{symbol} - Price with Moving Averages",
                            yaxis_title="Price (USD)",
                            xaxis_title="Date",
                            height=500,
                            hovermode='x unified',
                            template="plotly_white"
                        )
                        
                        safe_plotly_chart(fig, use_container_width=True)
                        
                        # Insights
                        st.markdown("### 💡 Key Insights")
                        for insight in analysis['insights']:
                            st.info(insight)
                        
                        # Recommendation
                        st.markdown("### 🎯 Recommendation")
                        
                        # Simple recommendation logic
                        score = 0
                        if analysis['percentage_change'] > 20:
                            score += 2
                        elif analysis['percentage_change'] > 0:
                            score += 1
                        elif analysis['percentage_change'] > -10:
                            score += 0
                        else:
                            score -= 1
                        
                        if analysis['volatility'] < 1:
                            score += 1
                        elif analysis['volatility'] > 3:
                            score -= 1
                        
                        if score >= 2:
                            st.success("🟢 **BUY** - Strong positive indicators suggest buying opportunity")
                        elif score >= 1:
                            st.warning("🟡 **HOLD** - Mixed signals - consider holding current position")
                        else:
                            st.info("🔵 **WATCH** - Cautious approach recommended - monitor closely")
                        
                        st.caption("⚠️ Disclaimer: This is for educational purposes only. Not financial advice.")
                        
                else:
                    st.error(f"❌ Unable to generate analysis for: **{symbol}**")

elif selected_tab == 4:
    # TAB 5: Developer API
    st.header("🔌 Developer API Documentation")
    
    st.markdown("""
    ### 🚀 Getting Started
    
    This API provides comprehensive stock market data including company information, 
    real-time market data, historical prices, and technical analysis.
    """)
    
    st.info("💡 **Note:** This API documentation shows examples for local development. In production, replace `localhost:5001` with your actual API server URL.")
    
    st.warning("⚠️ **Cloud Deployment:** This Streamlit app works standalone with Yahoo Finance data. The Flask API examples below are for local development reference only.")
    
    st.markdown("---")
    
    # Endpoint 1
    st.subheader("1️⃣ Company Information")
    st.code("GET /api/company/<symbol>", language="http")
    st.markdown("Get detailed company information for a given stock symbol.")
    
    with st.expander("📋 View Details"):
        st.markdown("**Parameters:**")
        st.table({
            "Name": ["symbol"],
            "Type": ["string"],
            "Required": ["Yes"],
            "Description": ["Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)"]
        })
        
        st.markdown("**Example Request (curl):**")
        st.code("curl http://localhost:5001/api/company/AAPL", language="bash")
        
        st.markdown("**Example Request (Python):**")
        st.code("""import requests

response = requests.get('http://localhost:5001/api/company/AAPL')
data = response.json()
print(data)""", language="python")
        
        st.markdown("**Example Response:**")
        st.json({
            "symbol": "AAPL",
            "longName": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "marketCap": 3000000000000,
            "website": "https://www.apple.com",
            "description": "Apple Inc. designs, manufactures...",
            "country": "United States",
            "city": "Cupertino",
            "employees": 164000
        })
    
    st.markdown("---")
    
    # Endpoint 2
    st.subheader("2️⃣ Real-Time Market Data")
    st.code("GET /api/market/<symbol>", language="http")
    st.markdown("Get real-time market data and current trading information.")
    
    with st.expander("📋 View Details"):
        st.markdown("**Parameters:**")
        st.table({
            "Name": ["symbol"],
            "Type": ["string"],
            "Required": ["Yes"],
            "Description": ["Stock ticker symbol"]
        })
        
        st.markdown("**Example Request (curl):**")
        st.code("curl http://localhost:5001/api/market/AAPL", language="bash")
        
        st.markdown("**Example Request (Python):**")
        st.code("""import requests

response = requests.get('http://localhost:5001/api/market/AAPL')
data = response.json()
print(f"Current Price: ${data['current_price']}")""", language="python")
        
        st.markdown("**Example Response:**")
        st.json({
            "symbol": "AAPL",
            "current_price": 175.50,
            "previous_close": 174.20,
            "price_change": 1.30,
            "percentage_change": 0.75,
            "day_high": 176.80,
            "day_low": 174.50,
            "volume": 52000000,
            "market_cap": 3000000000000,
            "info": {
                "marketState": "REGULAR",
                "currency": "USD"
            }
        })
    
    st.markdown("---")
    
    # Endpoint 3
    st.subheader("3️⃣ Historical Data")
    st.code("POST /api/historical/<symbol>", language="http")
    st.markdown("Get historical OHLC (Open, High, Low, Close) price data with volume.")
    
    with st.expander("📋 View Details"):
        st.markdown("**Parameters:**")
        st.table({
            "Name": ["symbol", "period", "interval"],
            "Type": ["string", "string", "string"],
            "Required": ["Yes", "No", "No"],
            "Description": [
                "Stock ticker symbol (URL parameter)",
                "Time period (default: '1mo')\nOptions: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max",
                "Data interval (default: '1d')\nOptions: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo"
            ]
        })
        
        st.markdown("**Example Request (curl):**")
        st.code("""curl -X POST http://localhost:5001/api/historical/AAPL \\
  -H "Content-Type: application/json" \\
  -d '{"period": "1mo", "interval": "1d"}'""", language="bash")
        
        st.markdown("**Example Request (Python):**")
        st.code("""import requests

url = 'http://localhost:5001/api/historical/AAPL'
payload = {
    "period": "1mo",
    "interval": "1d"
}

response = requests.post(url, json=payload)
data = response.json()
print(f"Retrieved {len(data['dates'])} data points")""", language="python")
        
        st.markdown("**Example Response:**")
        st.json({
            "symbol": "AAPL",
            "period": "1mo",
            "interval": "1d",
            "dates": ["2024-09-15", "2024-09-16", "..."],
            "open": [174.20, 175.30, "..."],
            "high": [176.50, 177.20, "..."],
            "low": [173.80, 174.90, "..."],
            "close": [175.50, 176.80, "..."],
            "volume": [52000000, 48000000, "..."]
        })
    
    st.markdown("---")
    
    # Endpoint 4
    st.subheader("4️⃣ Technical Analysis")
    st.code("POST /api/analysis/<symbol>", language="http")
    st.markdown("Get comprehensive technical analysis with indicators and trading recommendations.")
    
    with st.expander("📋 View Details"):
        st.markdown("**Parameters:**")
        st.table({
            "Name": ["symbol", "period"],
            "Type": ["string", "string"],
            "Required": ["Yes", "No"],
            "Description": [
                "Stock ticker symbol (URL parameter)",
                "Analysis period (default: '1mo')"
            ]
        })
        
        st.markdown("**Example Request (curl):**")
        st.code("""curl -X POST http://localhost:5001/api/analysis/AAPL \\
  -H "Content-Type: application/json" \\
  -d '{"period": "1mo"}'""", language="bash")
        
        st.markdown("**Example Request (Python):**")
        st.code("""import requests

url = 'http://localhost:5001/api/analysis/AAPL'
payload = {"period": "1mo"}

response = requests.post(url, json=payload)
data = response.json()
print(f"Recommendation: {data['recommendation']}")""", language="python")
        
        st.markdown("**Example Response:**")
        st.json({
            "symbol": "AAPL",
            "current_price": 175.50,
            "sma_20": 173.25,
            "sma_50": 171.80,
            "rsi": 65.5,
            "volatility": 0.025,
            "trend": "Bullish",
            "recommendation": "BUY",
            "insights": [
                "Price is above 20-day SMA - Bullish signal",
                "RSI indicates moderate strength"
            ]
        })
    
    st.markdown("---")
    
    # Error Handling
    st.subheader("⚠️ Error Handling")
    st.markdown("""
    The API returns standard HTTP status codes:
    
    - **200 OK:** Successful request
    - **400 Bad Request:** Invalid parameters or missing required fields
    - **404 Not Found:** Stock symbol not found
    - **500 Internal Server Error:** Server error or Yahoo Finance API issue
    """)
    
    st.markdown("**Error Response Format:**")
    st.json({
        "error": "Description of the error",
        "symbol": "INVALID"
    })
    
    st.markdown("---")
    
    # Best Practices
    st.subheader("🚦 Rate Limiting & Best Practices")
    st.warning("""
    **Important:** This API relies on Yahoo Finance data. To avoid rate limiting:
    
    - Don't make more than 1-2 requests per second
    - Implement caching on the client side for frequently accessed data
    - Use appropriate time periods to avoid excessive data transfer
    - Handle 429 (Too Many Requests) errors gracefully with retry logic
    """)
    
    st.markdown("---")
    
    # Quick Start
    st.subheader("🎯 Quick Start Example")
    st.markdown("Complete Python script to get started:")
    
    st.code("""import requests

# Base URL
BASE_URL = 'http://localhost:5001/api'

# 1. Get company information
company = requests.get(f'{BASE_URL}/company/AAPL').json()
print(f"Company: {company['longName']}")

# 2. Get current market data
market = requests.get(f'{BASE_URL}/market/AAPL').json()
print(f"Current Price: ${market['current_price']}")

# 3. Get historical data
historical = requests.post(
    f'{BASE_URL}/historical/AAPL',
    json={'period': '1mo', 'interval': '1d'}
).json()
print(f"Data points: {len(historical['dates'])}")

# 4. Get analysis
analysis = requests.post(
    f'{BASE_URL}/analysis/AAPL',
    json={'period': '1mo'}
).json()
print(f"Recommendation: {analysis['recommendation']}")
print(f"Trend: {analysis['trend']}")""", language="python")
    
    st.success("💡 **Tip:** Copy any code example above and run it in your Python environment to get started!")

# Footer
st.markdown("---")
if IS_CLOUD_DEPLOYMENT:
    footer_text = """
    <div style='text-align: center; color: gray;'>
        <p>📊 Real-time Stock Analysis Dashboard</p>
        <p>Data by Yahoo Finance API | Built with Streamlit & Plotly | Deployed on Streamlit Cloud</p>
    </div>
    """
else:
    footer_text = """
    <div style='text-align: center; color: gray;'>
        <p>Data by Yahoo Finance API | Built with Streamlit & Plotly</p>
        <p>💡 For local API access, check the Flask API running on port 5001</p>
    </div>
    """

st.markdown(footer_text, unsafe_allow_html=True)

# Global error handler for debugging in cloud
if IS_CLOUD_DEPLOYMENT:
    st.sidebar.success("✅ App running on Streamlit Cloud")
else:
    st.sidebar.info("🏠 Running locally")
