# AI Job Impact Predictor - Bootcamp Project

## Project Overview
This project predicts whether AI will impact a given job based on job title, required education, and experience.

### Inputs
- Job Title
- Required Education
- Required Experience (Years)

### Outputs (Predictions)
- AI Impact Level (Low/Moderate/High)
- Median Salary
- Projected Openings (2030)
- Remote Work Ratio
- Automation Risk

---

## Setup Instructions

### 1. Install Required Packages

Open your terminal in Visual Studio Code and run:

```bash
python3 -m pip install pandas numpy scikit-learn
```

Or install from the requirements file:

```bash
python3 -m pip install -r requirements.txt
```

### 2. Run the Preprocessing Script

Navigate to the `src` folder and run the preprocessing script:

```bash
cd src
python3 preprocess_data.py
```

This will:
- ✅ Handle missing values
- ✅ Encode categorical features (like job titles and education levels)
- ✅ Flag outliers in the data
- ✅ Normalize numerical values
- ✅ Save a new file: `preprocessed_job_data.csv`

---

## What the Preprocessing Script Does

### 1. **Handles Missing Values**
   - Fills missing numbers with the median (middle value)
   - Fills missing text with the mode (most common value)

### 2. **Encodes Categorical Features**
   - Converts text data (like "Bachelor's Degree") into numbers
   - Example: High School → 0, Bachelor's → 1, Master's → 2, PhD → 3

### 3. **Flags Outliers**
   - Identifies unusual data points (like an unrealistically high salary)
   - Uses the IQR (Interquartile Range) method
   - Creates a `Has_Outlier` flag

### 4. **Normalizes Numerical Values**
   - Scales all numbers to have mean = 0 and standard deviation = 1
   - Makes it easier for AI models to learn patterns
   - Creates new columns with `_Normalized` suffix

---

## File Structure

```
JobScope/
├── data/
│   ├── ai_job_trends_dataset 2.csv    # Original data
│   └── preprocessed_job_data.csv       # Processed data (created after running script)
├── src/
│   └── preprocess_data.py              # Preprocessing script
├── models/                              # Future: Save trained models here
├── requirements.txt                     # Python packages needed
└── README.md                            # This file
```

---

## Next Steps

After preprocessing:
1. Review the `preprocessed_job_data.csv` file
2. Build your machine learning model
3. Train using the encoded and normalized features
4. Create a web interface for users to input job details

Good luck with your bootcamp! 🚀

