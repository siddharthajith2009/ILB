# 🚀 Quick Start - Flask API in 3 Minutes

## Step 1: Install Flask (30 seconds)
```bash
pip install flask requests
```

## Step 2: Start the Server (10 seconds)
```bash
cd /Users/siddharthajith/Documents/JobScope
python app.py
```

You should see:
```
✓ Model loaded successfully!
✓ Status mapping loaded!
Server starting on http://localhost:5000
```

## Step 3: Test It! (2 minutes)

### Option A: Use the Test Script (Easiest)
Open a **NEW terminal** and run:
```bash
cd /Users/siddharthajith/Documents/JobScope
python test_api.py
```

### Option B: Use Your Browser
Open: http://localhost:5000

### Option C: Use curl
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Investment analyst",
    "education": "Master'\''s Degree",
    "experience_years": 5
  }'
```

## ✅ You're Done!

Your Flask API is now running and ready to make predictions! 🎉

---

## 📋 What You Just Created

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application (9KB, 250+ lines) |
| `test_api.py` | Comprehensive test suite (9KB) |
| `API_TESTING_GUIDE.md` | Detailed testing documentation |
| `FLASK_API_README.md` | Complete API documentation |

---

## 🎯 Example API Call

### Using Python:
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    "job_title": "Software Engineer",
    "education": "Bachelor's Degree",
    "experience_years": 3
})

print(response.json())
```

### Expected Output:
```json
{
  "success": true,
  "prediction": "Increasing",
  "confidence": 85.5,
  "probabilities": {
    "Increasing": 85.5,
    "Declining": 10.2,
    "Stable": 4.3
  }
}
```

---

## 🔍 API Endpoints Summary

1. **GET /** - Welcome & API info
2. **GET /options** - List all job titles & education levels
3. **POST /predict** - Make a prediction

---

## 🛠️ Troubleshooting

**Can't connect?**
- ✅ Make sure `python app.py` is running
- ✅ Check http://localhost:5000 in browser

**Import errors?**
```bash
pip install -r requirements.txt
```

**Need help?**
- Read: `FLASK_API_README.md` for complete guide
- Read: `API_TESTING_GUIDE.md` for testing examples

---

## 🎓 What's Inside app.py

The Flask app includes:
- ✅ Model loading and initialization
- ✅ 3 API endpoints (GET /, GET /options, POST /predict)
- ✅ Input validation and error handling
- ✅ Feature encoding (text → numbers)
- ✅ ML prediction with confidence scores
- ✅ JSON response formatting
- ✅ 250+ lines of well-commented code

---

**You're all set! Happy coding! 🎉**

