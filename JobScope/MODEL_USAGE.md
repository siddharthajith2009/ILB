# Job Status Prediction Model - Usage Guide

## Overview
This AI model predicts whether a job's status will be **Increasing** or **Decreasing** based on:
- Job Title
- Required Education Level
- Experience Required (in years)

## Model Performance
- **Best Model**: Random Forest Classifier
- **Accuracy**: 51.42%
- **Training Data**: 30,000 job records

## Files Created
1. **`src/train_job_status_model.py`** - Script to train the model
2. **`src/predict_job_status.py`** - Script to make predictions
3. **`models/job_status_predictor.pkl`** - Trained model file
4. **`models/status_mapping.pkl`** - Job status mappings
5. **`models/model_info.txt`** - Model information

## Quick Start

### 1. Run Example Predictions
```bash
cd /Users/siddharthajith/Documents/JobScope
python3 src/predict_job_status.py
```

### 2. Use in Your Own Code
```python
from predict_job_status import JobStatusPredictor

# Initialize predictor
predictor = JobStatusPredictor()

# Make a single prediction
prediction, confidence = predictor.predict(
    job_title="Investment analyst",
    education="Master's Degree",
    experience_years=5
)

print(f"Predicted Status: {prediction}")
print(f"Confidence: {max(confidence)*100:.2f}%")
```

### 3. Batch Predictions
```python
import pandas as pd
from predict_job_status import JobStatusPredictor

predictor = JobStatusPredictor()

# Create a DataFrame with your data
data = pd.DataFrame({
    'Job Title': ['Dentist', 'Town planner', 'Legal secretary'],
    'Required Education': ['PhD', 'Bachelor's Degree', 'Associate Degree'],
    'Experience Required (Years)': [8, 5, 10]
})

# Get predictions
results = predictor.predict_batch(data)
print(results)
```

### 4. Get Available Values
```python
predictor = JobStatusPredictor()

# See all available job titles (639 unique titles)
job_titles = predictor.get_available_job_titles()
print(f"Total job titles: {len(job_titles)}")

# See available education levels
education_levels = predictor.get_available_educations()
print("Education levels:", education_levels)
# Output: ['Associate Degree', 'Bachelor's Degree', 'High School', 'Master's Degree', 'PhD']
```

## Important Notes

⚠️ **Character Encoding**: The education levels in the dataset use the right single quotation mark (') character:
- Correct: `"Master's Degree"` (right single quote)
- Incorrect: `"Master's Degree"` (regular apostrophe)

⚠️ **Job Titles**: Must exactly match titles from the training data. Use `get_available_job_titles()` to see all valid options.

## Retrain the Model

If you want to retrain the model with updated data:
```bash
python3 src/train_job_status_model.py
```

This will:
- Load the preprocessed data
- Train multiple models (Random Forest, Gradient Boosting, Logistic Regression)
- Compare their performance
- Save the best performing model

## Model Insights

The model's accuracy of ~51% suggests that job title, education, and experience alone are moderate predictors of job status trends. For better predictions, consider:
- Adding more features (industry, location, salary, automation risk, etc.)
- Using ensemble methods
- Incorporating time-series analysis
- Adding external economic indicators

## Example Output

```
Input:
  Job Title: Investment analyst
  Education: Master's Degree
  Experience: 5 years
Prediction: Decreasing (Confidence: 50.52%)

Input:
  Job Title: Financial planner
  Education: Bachelor's Degree
  Experience: 3 years
Prediction: Increasing (Confidence: 52.57%)
```

## Next Steps

To improve the model, you could:
1. Add more input features from the dataset
2. Try different machine learning algorithms
3. Perform feature engineering
4. Use hyperparameter tuning
5. Collect more training data
6. Consider time-series forecasting approaches

## Questions?

Check the model training output or examine:
- `models/model_info.txt` for model details
- Training script for implementation details
- Preprocessed data for available features

