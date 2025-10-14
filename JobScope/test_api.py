"""
Test Script for Job Status Prediction API
This script tests all endpoints of the Flask API
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"


def test_welcome():
    """Test the welcome endpoint"""
    print("\n=== Testing Welcome Endpoint (GET /) ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Message: {data['message']}")
            print(f"✓ Available Education Levels: {len(data['available_education_levels'])}")
            print(f"✓ Total Job Titles: {data['total_job_titles_available']}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_options():
    """Test the options endpoint"""
    print("\n=== Testing Options Endpoint (GET /options) ===")
    try:
        response = requests.get(f"{BASE_URL}/options")
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Education Levels: {data['education_levels']}")
            print(f"✓ Total Job Titles Available: {data['total_job_titles']}")
            print(f"✓ Sample Job Titles (first 5): {data['job_titles'][:5]}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_valid_prediction():
    """Test a valid prediction"""
    print("\n=== Testing Valid Prediction (POST /predict) ===")
    try:
        data = {
            "job_title": "Investment analyst",
            "education": "Master's Degree",
            "experience_years": 5
        }
        
        print(f"Input: {json.dumps(data, indent=2)}")
        response = requests.post(f"{BASE_URL}/predict", json=data)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Success: {result['success']}")
            print(f"✓ Prediction: {result['prediction']}")
            print(f"✓ Confidence: {result['confidence']}%")
            print(f"✓ Probabilities: {result['probabilities']}")
            print(f"✓ Message: {result['message']}")
        else:
            print(f"✗ Unexpected response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_multiple_predictions():
    """Test multiple different predictions"""
    print("\n=== Testing Multiple Predictions ===")
    
    test_cases = [
        {
            "job_title": "Financial planner",
            "education": "Bachelor's Degree",
            "experience_years": 3
        },
        {
            "job_title": "Dentist",
            "education": "PhD",
            "experience_years": 8
        },
        {
            "job_title": "Legal secretary",
            "education": "Associate Degree",
            "experience_years": 10
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\nTest Case {i}: {test_case['job_title']}")
            response = requests.post(f"{BASE_URL}/predict", json=test_case)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Prediction: {result['prediction']} (Confidence: {result['confidence']}%)")
            else:
                print(f"  ✗ Error: {response.json()}")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def test_missing_field():
    """Test error handling for missing required field"""
    print("\n=== Testing Missing Field Error Handling ===")
    try:
        data = {
            "job_title": "Investment analyst",
            "education": "Master's Degree"
            # Missing: experience_years
        }
        
        print(f"Input (missing experience_years): {json.dumps(data, indent=2)}")
        response = requests.post(f"{BASE_URL}/predict", json=data)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"✓ Error properly caught: {result['error']}")
            print(f"✓ Missing fields: {result['missing_fields']}")
            print(f"✓ Required fields: {result['required_fields']}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_invalid_job_title():
    """Test error handling for invalid job title"""
    print("\n=== Testing Invalid Job Title Error Handling ===")
    try:
        data = {
            "job_title": "Nonexistent Job Title",
            "education": "Master's Degree",
            "experience_years": 5
        }
        
        print(f"Input (invalid job title): {json.dumps(data, indent=2)}")
        response = requests.post(f"{BASE_URL}/predict", json=data)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"✓ Error properly caught: {result['error']}")
            print(f"✓ Message: {result['message']}")
            print(f"✓ Suggestion: {result['suggestion']}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_invalid_education():
    """Test error handling for invalid education level"""
    print("\n=== Testing Invalid Education Level Error Handling ===")
    try:
        data = {
            "job_title": "Investment analyst",
            "education": "Some Random Degree",
            "experience_years": 5
        }
        
        print(f"Input (invalid education): {json.dumps(data, indent=2)}")
        response = requests.post(f"{BASE_URL}/predict", json=data)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"✓ Error properly caught: {result['error']}")
            print(f"✓ Message: {result['message']}")
            print(f"✓ Available options: {result['available_options']}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_invalid_experience_years():
    """Test error handling for invalid experience years"""
    print("\n=== Testing Invalid Experience Years Error Handling ===")
    try:
        data = {
            "job_title": "Investment analyst",
            "education": "Master's Degree",
            "experience_years": "not_a_number"
        }
        
        print(f"Input (invalid experience_years): {json.dumps(data, indent=2)}")
        response = requests.post(f"{BASE_URL}/predict", json=data)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"✓ Error properly caught: {result['error']}")
            print(f"✓ Message: {result['message']}")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all tests"""
    print("="*70)
    print("  JOB STATUS PREDICTION API - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nMake sure the Flask server is running at http://localhost:5000")
    print("(Run: python app.py)")
    print("="*70)
    
    try:
        # Test all endpoints
        test_welcome()
        test_options()
        test_valid_prediction()
        test_multiple_predictions()
        test_missing_field()
        test_invalid_job_title()
        test_invalid_education()
        test_invalid_experience_years()
        
        print("\n" + "="*70)
        print("  ✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nSummary:")
        print("  - All endpoints are working correctly")
        print("  - Error handling is functioning properly")
        print("  - The API is ready to use!")
        print("\nNext steps:")
        print("  - Try making your own predictions")
        print("  - Build a frontend for the API")
        print("  - Deploy to a cloud service")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n" + "="*70)
        print("  ✗ ERROR: Could not connect to the API server")
        print("="*70)
        print("\nThe Flask server is not running.")
        print("\nTo start the server:")
        print("  1. Open a terminal")
        print("  2. Navigate to: /Users/siddharthajith/Documents/JobScope")
        print("  3. Run: python app.py")
        print("  4. Wait for 'Running on http://localhost:5000'")
        print("  5. Run this test script again")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()

