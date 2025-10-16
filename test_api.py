"""
Test script for Company Information API
Run this script to test the Flask API endpoints
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:5001"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓ {message}{END}")

def print_error(message):
    print(f"{RED}✗ {message}{END}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{END}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{END}")

def print_json(data):
    print(json.dumps(data, indent=2))

def test_health_check():
    """Test the health check endpoint"""
    print_info("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print_success(f"Health check passed (Status: {response.status_code})")
            print_json(response.json())
            return True
        else:
            print_error(f"Health check failed (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Make sure the Flask server is running.")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_home_endpoint():
    """Test the home endpoint"""
    print_info("Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success(f"Home endpoint working (Status: {response.status_code})")
            print_json(response.json())
            return True
        else:
            print_error(f"Home endpoint failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_company_info(symbol):
    """Test getting company information"""
    print_info(f"Testing company info for {symbol}...")
    try:
        response = requests.get(f"{BASE_URL}/api/company/{symbol}")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Successfully retrieved data for {symbol}")
            print_json(data)
            
            # Verify required fields
            if data.get('success') and data.get('data'):
                company_data = data['data']
                print_info("\nKey Information:")
                print(f"  Company: {company_data.get('company_name', 'N/A')}")
                print(f"  Symbol: {company_data.get('symbol', 'N/A')}")
                print(f"  Sector: {company_data.get('sector', 'N/A')}")
                print(f"  Industry: {company_data.get('industry', 'N/A')}")
                print(f"  Officers: {len(company_data.get('key_officers', []))} found")
            return True
        elif response.status_code == 404:
            print_warning(f"Symbol {symbol} not found (Status: {response.status_code})")
            print_json(response.json())
            return False
        else:
            print_error(f"Failed to get data (Status: {response.status_code})")
            print_json(response.json())
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_invalid_symbol():
    """Test with invalid symbol"""
    print_info("Testing with invalid symbol...")
    try:
        response = requests.get(f"{BASE_URL}/api/company/INVALID123")
        if response.status_code == 404:
            print_success("Invalid symbol correctly handled (404)")
            print_json(response.json())
            return True
        else:
            print_warning(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_empty_symbol():
    """Test with empty symbol"""
    print_info("Testing with empty symbol...")
    try:
        response = requests.get(f"{BASE_URL}/api/company/")
        # This should return 404 (endpoint not found)
        if response.status_code == 404:
            print_success("Empty symbol correctly handled")
            return True
        else:
            print_warning(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Company Information API - Test Suite")
    print("="*60 + "\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health Check
    print("\n" + "-"*60)
    print("Test 1: Health Check")
    print("-"*60)
    if test_health_check():
        tests_passed += 1
    else:
        tests_failed += 1
        print_error("Stopping tests - API is not running")
        return
    
    # Test 2: Home Endpoint
    print("\n" + "-"*60)
    print("Test 2: Home Endpoint")
    print("-"*60)
    if test_home_endpoint():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Valid Company - Apple
    print("\n" + "-"*60)
    print("Test 3: Get Company Info (AAPL)")
    print("-"*60)
    if test_company_info("AAPL"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Valid Company - Microsoft
    print("\n" + "-"*60)
    print("Test 4: Get Company Info (MSFT)")
    print("-"*60)
    if test_company_info("MSFT"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 5: Valid Company - Tesla
    print("\n" + "-"*60)
    print("Test 5: Get Company Info (TSLA)")
    print("-"*60)
    if test_company_info("TSLA"):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 6: Invalid Symbol
    print("\n" + "-"*60)
    print("Test 6: Invalid Symbol")
    print("-"*60)
    if test_invalid_symbol():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 7: Empty Symbol
    print("\n" + "-"*60)
    print("Test 7: Empty Symbol")
    print("-"*60)
    if test_empty_symbol():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    print(f"{GREEN}Tests Passed: {tests_passed}{END}")
    print(f"{RED}Tests Failed: {tests_failed}{END}")
    print(f"Total Tests: {tests_passed + tests_failed}")
    print("="*60 + "\n")
    
    if tests_failed == 0:
        print_success("All tests passed! 🎉")
    else:
        print_warning(f"{tests_failed} test(s) failed. Please review the output above.")

if __name__ == "__main__":
    print_info("Make sure the Flask API is running on http://localhost:5001")
    print_info("Start the API with: python app.py\n")
    
    run_all_tests()
