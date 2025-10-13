# Job Status Prediction API - Testing Guide

## 🚀 How to Run the Flask App

### Step 1: Install Flask
```bash
pip install flask
```

### Step 2: Start the Server
```bash
cd /Users/siddharthajith/Documents/JobScope
python app.py
```

You should see:
```
Server starting on http://localhost:5000
```

---

## 📡 API Endpoints

### 1. Welcome Message (GET /)
Get API information and available education levels.

**Using Browser:**
- Open: `http://localhost:5000/`

**Using curl:**
```bash
curl http://localhost:5000/
```

---

### 2. Get Available Options (GET /options)
See all available job titles and education levels.

**Using curl:**
```bash
curl http://localhost:5000/options
```

---

### 3. Make Prediction (POST /predict)
Predict job status for given inputs.

**Using curl:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Investment analyst",
    "education": "Master'\''s Degree",
    "experience_years": 5
  }'
```

**Using Python:**
```python
import requests

url = "http://localhost:5000/predict"
data = {
    "job_title": "Investment analyst",
    "education": "Master's Degree",
    "experience_years": 5
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 📋 Example Test Cases

### Test Case 1: Valid Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "education": "Bachelor'\''s Degree",
    "experience_years": 3
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "input": {
    "job_title": "Software Engineer",
    "education": "Bachelor's Degree",
    "experience_years": 3
  },
  "prediction": "Increasing",
  "confidence": 85.5,
  "probabilities": {
    "Increasing": 85.5,
    "Declining": 10.2,
    "Stable": 4.3
  },
  "message": "The job 'Software Engineer' is predicted to be Increasing"
}
```

### Test Case 2: Missing Field (Error Handling)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "education": "Bachelor'\''s Degree"
  }'
```

**Expected Response:**
```json
{
  "error": "Missing required fields",
  "missing_fields": ["experience_years"],
  "required_fields": ["job_title", "education", "experience_years"]
}
```

### Test Case 3: Invalid Job Title (Error Handling)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Nonexistent Job",
    "education": "Bachelor'\''s Degree",
    "experience_years": 5
  }'
```

**Expected Response:**
```json
{
  "error": "Invalid job title",
  "message": "Job title 'Nonexistent Job' not found in our database",
  "suggestion": "Use GET / to see available options or check spelling"
}
```

### Test Case 4: Invalid Experience Years (Error Handling)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Investment analyst",
    "education": "Master'\''s Degree",
    "experience_years": "abc"
  }'
```

**Expected Response:**
```json
{
  "error": "Invalid input",
  "message": "experience_years must be a number"
}
```

---

## 🧪 Python Test Script

Create a file `test_api.py`:

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

def test_welcome():
    """Test the welcome endpoint"""
    print("\n=== Testing Welcome Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_options():
    """Test the options endpoint"""
    print("\n=== Testing Options Endpoint ===")
    response = requests.get(f"{BASE_URL}/options")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Education Levels: {data['education_levels']}")
    print(f"Total Job Titles: {data['total_job_titles']}")

def test_valid_prediction():
    """Test a valid prediction"""
    print("\n=== Testing Valid Prediction ===")
    data = {
        "job_title": "Investment analyst",
        "education": "Master's Degree",
        "experience_years": 5
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_missing_field():
    """Test error handling for missing field"""
    print("\n=== Testing Missing Field Error ===")
    data = {
        "job_title": "Investment analyst",
        "education": "Master's Degree"
        # Missing experience_years
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_invalid_job_title():
    """Test error handling for invalid job title"""
    print("\n=== Testing Invalid Job Title Error ===")
    data = {
        "job_title": "Nonexistent Job",
        "education": "Master's Degree",
        "experience_years": 5
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("="*60)
    print("  JOB STATUS PREDICTION API - TEST SUITE")
    print("="*60)
    
    try:
        test_welcome()
        test_options()
        test_valid_prediction()
        test_missing_field()
        test_invalid_job_title()
        
        print("\n" + "="*60)
        print("  ALL TESTS COMPLETED!")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: python app.py")
```

Run tests:
```bash
python test_api.py
```

---

## 🌐 Testing with Postman

1. **Install Postman** (https://www.postman.com/downloads/)

2. **Create a new request:**
   - Method: `POST`
   - URL: `http://localhost:5000/predict`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
   ```json
   {
     "job_title": "Investment analyst",
     "education": "Master's Degree",
     "experience_years": 5
   }
   ```

3. **Click Send** and view the prediction result!

---

## 📝 Available Education Levels

Based on your model, these are the valid education levels:
- High School Diploma
- Associate Degree
- Bachelor's Degree
- Master's Degree
- PhD

---

## 🔍 Troubleshooting

### Error: "Module not found: flask"
```bash
pip install flask
```

### Error: "Module not found: pandas"
```bash
pip install pandas
```

### Error: "Connection refused"
- Make sure the Flask app is running
- Check if port 5000 is available
- Try accessing http://localhost:5000 in your browser

### Error: "Model file not found"
- Ensure the model file exists at: `/Users/siddharthajith/Documents/JobScope/models/job_status_predictor.pkl`
- Make sure you've trained the model first

---

## 🎯 Next Steps

1. **Deploy the API** (optional):
   - Use services like Heroku, Railway, or PythonAnywhere
   - Add environment variables for file paths
   - Use gunicorn as production server

2. **Build a Frontend** (optional):
   - Create a simple HTML form
   - Use React, Vue, or vanilla JavaScript
   - Connect to this API

3. **Add Features** (optional):
   - Authentication (API keys)
   - Rate limiting
   - Logging and analytics
   - Database to store predictions

---

Happy Testing! 🚀

