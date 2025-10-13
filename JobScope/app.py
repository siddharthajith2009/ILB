"""
Flask Web Application for Job Status Prediction
This app uses a machine learning model to predict if a job is Increasing, Declining, or Stable
"""

# Import necessary libraries
from flask import Flask, request, jsonify  # Flask for web app, request for getting data, jsonify for JSON responses
from flask_cors import CORS  # For handling Cross-Origin requests from the HTML page
import pickle  # For loading the saved machine learning model
import pandas as pd  # For data handling
import os  # For file path operations

# Create Flask application
app = Flask(__name__)

# Enable CORS to allow the HTML page to make requests
CORS(app)

# Global variables to store model and mappings
model = None
status_mapping = None
job_title_to_encoded = None
education_to_encoded = None
status_encoded_to_text = None


def load_model_and_mappings():
    """
    Load the trained model and all necessary mappings when the app starts
    This function runs once when the server starts up
    """
    global model, status_mapping, job_title_to_encoded, education_to_encoded, status_encoded_to_text
    
    print("Loading model and mappings...")
    
    # Define the path to models folder
    models_dir = '/Users/siddharthajith/Documents/JobScope/models'
    
    # Step 1: Load the trained model
    model_path = os.path.join(models_dir, 'job_status_predictor.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully!")
    
    # Step 2: Load the status mapping (to convert numbers back to text)
    mapping_path = os.path.join(models_dir, 'status_mapping.pkl')
    with open(mapping_path, 'rb') as f:
        status_mapping = pickle.load(f)
    print("✓ Status mapping loaded!")
    
    # Step 3: Load the preprocessed data to get encoding mappings
    data_path = '/Users/siddharthajith/Documents/JobScope/data/preprocessed_job_data.csv'
    df = pd.read_csv(data_path)
    
    # Step 4: Create Job Title mapping (text → number)
    job_title_map = df[['Job Title', 'Job Title_Encoded']].drop_duplicates()
    job_title_to_encoded = dict(zip(job_title_map['Job Title'], job_title_map['Job Title_Encoded']))
    print(f"✓ Job Title mappings created: {len(job_title_to_encoded)} titles")
    
    # Step 5: Create Education mapping (text → number)
    education_map = df[['Required Education', 'Required Education_Encoded']].drop_duplicates()
    education_to_encoded = dict(zip(education_map['Required Education'], education_map['Required Education_Encoded']))
    print(f"✓ Education mappings created: {len(education_to_encoded)} levels")
    
    # Step 6: Create Status mapping (number → text) for predictions
    status_encoded_to_text = dict(zip(
        status_mapping['Job Status_Encoded'], 
        status_mapping['Job Status']
    ))
    print(f"✓ Status decoding mapping created: {status_encoded_to_text}")
    
    print("All models and mappings loaded successfully!\n")


# ========== ROUTE 1: Welcome Message (GET) ==========
@app.route('/', methods=['GET'])
def home():
    """
    Simple welcome route that returns information about the API
    Access this at: http://localhost:5000/
    """
    return jsonify({
        'message': 'Welcome to the Job Status Prediction API!',
        'description': 'This API predicts whether a job is Increasing, Declining, or Stable',
        'endpoints': {
            '/': 'GET - This welcome message',
            '/predict': 'POST - Make a prediction'
        },
        'how_to_use': {
            'method': 'POST',
            'url': '/predict',
            'body': {
                'job_title': 'e.g., Software Engineer',
                'education': 'e.g., Bachelor\'s Degree',
                'experience_years': 'e.g., 5'
            }
        },
        'available_education_levels': sorted(list(education_to_encoded.keys())),
        'total_job_titles_available': len(job_title_to_encoded)
    })


# ========== ROUTE 2: Prediction Endpoint (POST) ==========
@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction route that accepts JSON data and returns a prediction
    
    Expected JSON format:
    {
        "job_title": "Software Engineer",
        "education": "Bachelor's Degree",
        "experience_years": 5
    }
    """
    
    try:
        # Step 1: Get JSON data from the request
        data = request.get_json()
        
        # Step 2: Validate that all required fields are present
        required_fields = ['job_title', 'education', 'experience_years']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'required_fields': required_fields
            }), 400  # 400 = Bad Request
        
        # Step 3: Extract input values from JSON
        job_title = data['job_title']
        education = data['education']
        experience_years = data['experience_years']
        
        # Step 4: Validate experience_years is a number
        try:
            experience_years = float(experience_years)
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Invalid input',
                'message': 'experience_years must be a number'
            }), 400
        
        # Step 5: Encode Job Title (convert text to number)
        if job_title not in job_title_to_encoded:
            return jsonify({
                'error': 'Invalid job title',
                'message': f'Job title "{job_title}" not found in our database',
                'suggestion': 'Use GET / to see available options or check spelling'
            }), 400
        
        job_title_encoded = job_title_to_encoded[job_title]
        
        # Step 6: Encode Education (convert text to number)
        if education not in education_to_encoded:
            return jsonify({
                'error': 'Invalid education level',
                'message': f'Education level "{education}" not found',
                'available_options': sorted(list(education_to_encoded.keys()))
            }), 400
        
        education_encoded = education_to_encoded[education]
        
        # Step 7: Create feature array in the correct order
        # Order: [Job Title Encoded, Education Encoded, Experience Years]
        features = [[job_title_encoded, education_encoded, experience_years]]
        
        # Step 8: Make prediction using the model
        prediction_encoded = model.predict(features)[0]
        prediction_probabilities = model.predict_proba(features)[0]
        
        # Step 9: Convert prediction from number to text
        prediction_text = status_encoded_to_text[prediction_encoded]
        
        # Step 10: Calculate confidence (highest probability)
        confidence = float(max(prediction_probabilities)) * 100
        
        # Step 11: Create probability dictionary for all classes
        probability_dict = {}
        for encoded_val, prob in enumerate(prediction_probabilities):
            status_text = status_encoded_to_text[encoded_val]
            probability_dict[status_text] = round(float(prob) * 100, 2)
        
        # Step 12: Return successful prediction result
        return jsonify({
            'success': True,
            'input': {
                'job_title': job_title,
                'education': education,
                'experience_years': experience_years
            },
            'prediction': prediction_text,
            'confidence': round(confidence, 2),
            'probabilities': probability_dict,
            'message': f'The job "{job_title}" is predicted to be {prediction_text}'
        })
    
    except Exception as e:
        # Step 13: Handle any unexpected errors
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e),
            'type': type(e).__name__
        }), 500  # 500 = Internal Server Error


# ========== ROUTE 3: Get Available Options (GET) ==========
@app.route('/options', methods=['GET'])
def get_options():
    """
    Returns all available job titles and education levels
    This is helpful for users to know what values they can use
    """
    return jsonify({
        'education_levels': sorted(list(education_to_encoded.keys())),
        'job_titles': sorted(list(job_title_to_encoded.keys())),
        'total_job_titles': len(job_title_to_encoded),
        'total_education_levels': len(education_to_encoded)
    })


# ========== ROUTE 4: Get Valid Combinations (POST) ==========
@app.route('/valid-options', methods=['POST'])
def get_valid_options():
    """
    Returns valid education levels and experience years for a given job title
    This helps create dependent dropdowns
    """
    try:
        data = request.get_json()
        
        # Load the preprocessed data to find valid combinations
        data_path = '/Users/siddharthajith/Documents/JobScope/data/preprocessed_job_data.csv'
        df = pd.read_csv(data_path)
        
        response_data = {}
        
        # If job title is provided, filter valid education and experience
        if 'job_title' in data and data['job_title']:
            job_title = data['job_title']
            
            # Filter data for this job title
            job_data = df[df['Job Title'] == job_title]
            
            if len(job_data) > 0:
                # Get valid education levels for this job
                valid_education = sorted(job_data['Required Education'].unique().tolist())
                response_data['education_levels'] = valid_education
                
                # Get valid experience years for this job
                valid_experience = sorted(job_data['Experience Required (Years)'].unique().tolist())
                response_data['experience_years'] = [int(x) for x in valid_experience]
                
                # If education is also provided, filter experience further
                if 'education' in data and data['education']:
                    education = data['education']
                    job_edu_data = job_data[job_data['Required Education'] == education]
                    
                    if len(job_edu_data) > 0:
                        valid_experience = sorted(job_edu_data['Experience Required (Years)'].unique().tolist())
                        response_data['experience_years'] = [int(x) for x in valid_experience]
            else:
                # Job title not found, return all options
                response_data['education_levels'] = sorted(list(education_to_encoded.keys()))
                response_data['experience_years'] = list(range(0, 21))
        else:
            # No job title provided, return all options
            response_data['education_levels'] = sorted(list(education_to_encoded.keys()))
            response_data['experience_years'] = list(range(0, 21))
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get valid options',
            'message': str(e)
        }), 500


# ========== MAIN: Start the Flask Server ==========
if __name__ == '__main__':
    # Load model and mappings before starting the server
    load_model_and_mappings()
    
    # Start the Flask development server
    print("\n" + "="*60)
    print("  JOB STATUS PREDICTION API SERVER")
    print("="*60)
    print("Server starting on http://localhost:5001")
    print("\nAvailable endpoints:")
    print("  - GET  /             : Welcome message and API info")
    print("  - POST /predict      : Make a prediction")
    print("  - GET  /options      : Get all available job titles and education levels")
    print("  - POST /valid-options: Get valid options based on selections (smart filtering)")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run the app (debug=True shows helpful error messages)
    app.run(debug=True, host='0.0.0.0', port=5001)

