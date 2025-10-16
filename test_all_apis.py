"""
Comprehensive API Testing Script for Stock Market Analysis API

This script tests all four endpoints:
1. Company Information
2. Market Data
3. Historical Data
4. Analytical Insights
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5001"
TEST_SYMBOL = "AAPL"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def test_health_check():
    """Test the health check endpoint"""
    print_section("1. Testing Health Check Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_company_info(symbol=TEST_SYMBOL):
    """Test the company information endpoint"""
    print_section(f"2. Testing Company Information Endpoint (Symbol: {symbol})")
    
    try:
        response = requests.get(f"{BASE_URL}/api/company/{symbol}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success! Company Information Retrieved:")
            print(f"   Company Name: {data['data']['company_name']}")
            print(f"   Sector: {data['data']['sector']}")
            print(f"   Industry: {data['data']['industry']}")
            print(f"   Country: {data['data']['country']}")
            print(f"   Number of Officers: {len(data['data']['key_officers'])}")
            
            # Show first officer
            if data['data']['key_officers']:
                officer = data['data']['key_officers'][0]
                print(f"\n   First Officer:")
                print(f"   - Name: {officer['name']}")
                print(f"   - Title: {officer['title']}")
            
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_market_data(symbol=TEST_SYMBOL):
    """Test the market data endpoint"""
    print_section(f"3. Testing Market Data Endpoint (Symbol: {symbol})")
    
    try:
        response = requests.get(f"{BASE_URL}/api/market/{symbol}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            market_data = data['data']
            
            print(f"\n✅ Success! Market Data Retrieved:")
            print(f"   Company: {market_data['company_name']}")
            print(f"   Market State: {market_data['market_state']}")
            print(f"   Current Price: ${market_data['current_price']:.2f}")
            print(f"   Previous Close: ${market_data['previous_close']:.2f}")
            print(f"   Price Change: ${market_data['price_change']:.2f}")
            print(f"   Percentage Change: {market_data['percentage_change']:.2f}%")
            print(f"   Day High: ${market_data['day_high']}")
            print(f"   Day Low: ${market_data['day_low']}")
            print(f"   Volume: {market_data['volume']:,}" if market_data['volume'] != 'N/A' else "   Volume: N/A")
            
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_historical_data(symbol=TEST_SYMBOL):
    """Test the historical data endpoint"""
    print_section(f"4. Testing Historical Data Endpoint (Symbol: {symbol})")
    
    # Set date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    payload = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d')
    }
    
    print(f"Request Payload:")
    print(f"   Start Date: {payload['start_date']}")
    print(f"   End Date: {payload['end_date']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/historical/{symbol}",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            hist_data = data['data']
            
            print(f"\n✅ Success! Historical Data Retrieved:")
            print(f"   Symbol: {hist_data['symbol']}")
            print(f"   Start Date: {hist_data['start_date']}")
            print(f"   End Date: {hist_data['end_date']}")
            print(f"   Total Records: {hist_data['records_count']}")
            
            # Show first and last records
            if hist_data['historical_data']:
                first_record = hist_data['historical_data'][0]
                last_record = hist_data['historical_data'][-1]
                
                print(f"\n   First Record ({first_record['date']}):")
                print(f"   - Open: ${first_record['open']:.2f}")
                print(f"   - Close: ${first_record['close']:.2f}")
                print(f"   - High: ${first_record['high']:.2f}")
                print(f"   - Low: ${first_record['low']:.2f}")
                
                print(f"\n   Last Record ({last_record['date']}):")
                print(f"   - Open: ${last_record['open']:.2f}")
                print(f"   - Close: ${last_record['close']:.2f}")
                print(f"   - High: ${last_record['high']:.2f}")
                print(f"   - Low: ${last_record['low']:.2f}")
            
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_analysis(symbol=TEST_SYMBOL):
    """Test the analytical insights endpoint"""
    print_section(f"5. Testing Analytical Insights Endpoint (Symbol: {symbol})")
    
    # Set date range (last 1 year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    payload = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d')
    }
    
    print(f"Request Payload:")
    print(f"   Start Date: {payload['start_date']}")
    print(f"   End Date: {payload['end_date']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analysis/{symbol}",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            analysis = data['data']
            
            print(f"\n✅ Success! Analysis Retrieved:")
            print(f"   Company: {analysis['company_name']}")
            print(f"   Analysis Period: {analysis['analysis_period']['days_analyzed']} days")
            
            # Price Analysis
            print(f"\n   📊 Price Analysis:")
            price_data = analysis['price_analysis']
            print(f"   - Current Price: ${price_data['current_price']:.2f}")
            print(f"   - Start Price: ${price_data['start_price']:.2f}")
            print(f"   - Price Change: ${price_data['price_change']:.2f} ({price_data['percentage_change']:.2f}%)")
            print(f"   - Period High: ${price_data['period_high']:.2f}")
            print(f"   - Period Low: ${price_data['period_low']:.2f}")
            
            # Technical Indicators
            print(f"\n   📈 Technical Indicators:")
            tech = analysis['technical_indicators']
            print(f"   - Volatility: {tech['volatility']:.2f}%")
            print(f"   - 50-Day MA: ${tech['moving_average_50']}")
            print(f"   - 200-Day MA: ${tech['moving_average_200']}")
            
            # Volume Analysis
            print(f"\n   📊 Volume Analysis:")
            vol = analysis['volume_analysis']
            print(f"   - Average Volume: {vol['average_volume']:,}")
            print(f"   - Latest Volume: {vol['latest_volume']:,}")
            
            # Insights
            print(f"\n   💡 Key Insights:")
            for insight in analysis['insights']:
                print(f"   - {insight}")
            
            # Recommendation
            print(f"\n   🎯 Recommendation:")
            rec = analysis['recommendation']
            print(f"   - Rating: {rec['rating']}")
            print(f"   - Confidence: {rec['confidence']}")
            print(f"   - Note: {rec['note']}")
            
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*70)
    print("  STOCK MARKET ANALYSIS API - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Test Symbol: {TEST_SYMBOL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "Health Check": test_health_check(),
        "Company Information": test_company_info(),
        "Market Data": test_market_data(),
        "Historical Data": test_historical_data(),
        "Analytical Insights": test_analysis()
    }
    
    # Summary
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    
    for test, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test}: {status}")
    
    print(f"\n{'='*70}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print("="*70 + "\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! 🎉\n")
    else:
        print("⚠️  SOME TESTS FAILED - Please check the output above.\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.\n")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}\n")
