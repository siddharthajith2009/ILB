# Flask API for Job Status Prediction 🚀

## Overview
A simple and beginner-friendly Flask web application that uses your trained machine learning model to predict job status (Increasing, Declining, or Stable) based on job characteristics.

## 📁 Files Created

1. **`app.py`** - Main Flask application with all API endpoints
2. **`test_api.py`** - Comprehensive test script for the API
3. **`API_TESTING_GUIDE.md`** - Detailed testing documentation

## 🎯 What the App Does

### Input Features:
- **Job Title** (e.g., "Software Engineer", "Investment analyst")
- **Required Education** (e.g., "Bachelor's Degree", "Master's Degree")
- **Experience Required** (years as a number)

### Output:
- **Prediction**: Job status (Increasing/Declining/Stable)
- **Confidence**: Percentage confidence of the prediction
- **Probabilities**: Breakdown of probabilities for all classes

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Flask App
```bash
python app.py
```

### 3. Test the API
In a new terminal:
```bash
python test_api.py
```

Or use curl:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Investment analyst",
    "education": "Master'\''s Degree",
    "experience_years": 5
  }'
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API information |
| GET | `/options` | Get all available job titles and education levels |
| POST | `/predict` | Make a job status prediction |

## 💡 Example Request & Response

### Request:
```json
{
  "job_title": "Investment analyst",
  "education": "Master's Degree",
  "experience_years": 5
}
```

### Response:
```json
{
  "success": true,
  "input": {
    "job_title": "Investment analyst",
    "education": "Master's Degree",
    "experience_years": 5
  },
  "prediction": "Increasing",
  "confidence": 85.5,
  "probabilities": {
    "Increasing": 85.5,
    "Declining": 10.2,
    "Stable": 4.3
  },
  "message": "The job 'Investment analyst' is predicted to be Increasing"
}
```

## 🛡️ Error Handling

The API includes comprehensive error handling for:
- ✅ Missing required fields
- ✅ Invalid job titles
- ✅ Invalid education levels
- ✅ Invalid experience years (non-numeric)
- ✅ Server errors

### Example Error Response:
```json
{
  "error": "Invalid job title",
  "message": "Job title 'Nonexistent Job' not found in our database",
  "suggestion": "Use GET / to see available options or check spelling"
}
```

## 🎓 Code Highlights (For Learning)

### How the App Works:

1. **Model Loading** (when server starts):
   - Loads the trained ML model from `models/job_status_predictor.pkl`
   - Loads status mappings and encoding dictionaries
   - Creates lookup tables for job titles and education levels

2. **Request Processing**:
   - Receives JSON data from client
   - Validates all required fields are present
   - Validates data types and values

3. **Feature Encoding**:
   - Converts job title text → number (using lookup table)
   - Converts education text → number (using lookup table)
   - Keeps experience years as-is (already numeric)

4. **Prediction**:
   - Creates feature array: `[job_title_encoded, education_encoded, experience_years]`
   - Passes to ML model for prediction
   - Gets prediction and probabilities

5. **Response Formatting**:
   - Converts prediction number → text (Increasing/Declining/Stable)
   - Calculates confidence percentage
   - Returns JSON response with all details

## 📚 Available Education Levels

- High School Diploma
- Associate Degree
- Bachelor's Degree
- Master's Degree
- PhD

## 🔧 Troubleshooting

### "Module not found" errors:
```bash
pip install flask pandas numpy scikit-learn requests
```

### "Connection refused":
- Make sure `app.py` is running
- Check http://localhost:5000 in browser
- Verify port 5000 is not in use

### "Model file not found":
- Ensure model exists at: `models/job_status_predictor.pkl`
- Make sure you've trained the model first using `train_job_status_model.py`

## 🎯 Next Steps

### Beginner Level:
- ✅ Run the Flask app
- ✅ Test with provided test script
- ✅ Try different job titles and education levels

### Intermediate Level:
- 🔨 Create a simple HTML frontend
- 🔨 Add more endpoints (batch predictions)
- 🔨 Add request logging

### Advanced Level:
- 🚀 Deploy to cloud (Heroku, Railway, PythonAnywhere)
- 🚀 Add authentication (API keys)
- 🚀 Create a React/Vue.js frontend
- 🚀 Add database for storing prediction history

## 📖 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **REST API Basics**: https://restfulapi.net/
- **JSON Tutorial**: https://www.json.org/

## 🤝 Need Help?

1. Check the `API_TESTING_GUIDE.md` for detailed examples
2. Run `python test_api.py` to see if the API is working
3. Visit http://localhost:5000 in your browser for API info

---

**Happy Coding! 🎉**

*This Flask API was designed with beginners in mind - every section is well-commented and easy to understand.*

