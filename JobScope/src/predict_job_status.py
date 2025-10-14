"""
Job Status Prediction Script
Use the trained model to predict job status for new data
"""

import pandas as pd
import pickle
import os

class JobStatusPredictor:
    """Class to make job status predictions"""
    
    def __init__(self):
        """Load the trained model and mappings"""
        models_dir = '/Users/siddharthajith/Documents/JobScope/models'
        
        # Load model
        model_path = os.path.join(models_dir, 'job_status_predictor.pkl')
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        # Load status mapping
        mapping_path = os.path.join(models_dir, 'status_mapping.pkl')
        with open(mapping_path, 'rb') as f:
            self.status_mapping = pickle.load(f)
        
        # Load original data to get encoding mappings
        data_path = '/Users/siddharthajith/Documents/JobScope/data/preprocessed_job_data.csv'
        self.df = pd.read_csv(data_path)
        
        # Create reverse mappings
        self._create_mappings()
        
        print("✓ Model loaded successfully!")
        print(f"✓ Status mapping: {dict(zip(self.status_mapping['Job Status_Encoded'], self.status_mapping['Job Status']))}")
    
    def _create_mappings(self):
        """Create mappings from text to encoded values"""
        # Job Title mapping
        job_title_map = self.df[['Job Title', 'Job Title_Encoded']].drop_duplicates()
        self.job_title_to_encoded = dict(zip(job_title_map['Job Title'], job_title_map['Job Title_Encoded']))
        
        # Required Education mapping
        education_map = self.df[['Required Education', 'Required Education_Encoded']].drop_duplicates()
        self.education_to_encoded = dict(zip(education_map['Required Education'], education_map['Required Education_Encoded']))
        
        # Job Status mapping (for decoding predictions)
        self.status_encoded_to_text = dict(zip(
            self.status_mapping['Job Status_Encoded'], 
            self.status_mapping['Job Status']
        ))
    
    def predict(self, job_title, education, experience_years):
        """
        Predict job status for given inputs
        
        Args:
            job_title (str): Job title (e.g., "Software Engineer")
            education (str): Required education (e.g., "Bachelor’s Degree")
            experience_years (int): Years of experience required
        
        Returns:
            str: Predicted job status ("Increasing" or "Decreasing")
        """
        # Encode inputs
        try:
            job_title_encoded = self.job_title_to_encoded[job_title]
        except KeyError:
            raise ValueError(f"Job title '{job_title}' not found in training data. Available titles: {len(self.job_title_to_encoded)}")
        
        try:
            education_encoded = self.education_to_encoded[education]
        except KeyError:
            raise ValueError(f"Education '{education}' not found. Available: {list(self.education_to_encoded.keys())}")
        
        # Create feature array
        features = [[job_title_encoded, education_encoded, experience_years]]
        
        # Make prediction
        prediction_encoded = self.model.predict(features)[0]
        prediction_proba = self.model.predict_proba(features)[0]
        
        # Decode prediction
        prediction_text = self.status_encoded_to_text[prediction_encoded]
        
        return prediction_text, prediction_proba
    
    def predict_batch(self, data):
        """
        Predict job status for multiple entries
        
        Args:
            data (pd.DataFrame): DataFrame with columns 'Job Title', 'Required Education', 'Experience Required (Years)'
        
        Returns:
            pd.DataFrame: Original data with predictions
        """
        predictions = []
        probabilities = []
        
        for _, row in data.iterrows():
            try:
                pred, proba = self.predict(
                    row['Job Title'],
                    row['Required Education'],
                    row['Experience Required (Years)']
                )
                predictions.append(pred)
                probabilities.append(max(proba))
            except ValueError as e:
                predictions.append(f"Error: {str(e)}")
                probabilities.append(None)
        
        data['Predicted Job Status'] = predictions
        data['Prediction Confidence'] = probabilities
        
        return data
    
    def get_available_job_titles(self):
        """Get list of available job titles"""
        return sorted(self.job_title_to_encoded.keys())
    
    def get_available_educations(self):
        """Get list of available education levels"""
        return sorted(self.education_to_encoded.keys())


def example_predictions():
    """Run example predictions"""
    print("\n" + "="*80)
    print("EXAMPLE PREDICTIONS")
    print("="*80)
    
    # Initialize predictor
    predictor = JobStatusPredictor()
    
    # Example 1: Single predictions
    print("\n>>> Single Predictions:")
    
    examples = [
        ("Investment analyst", "Master’s Degree", 5),
        ("Financial planner", "Bachelor’s Degree", 3),
        ("Legal secretary", "Associate Degree", 10),
        ("Dentist", "PhD", 8),
    ]
    
    for job_title, education, years in examples:
        try:
            prediction, proba = predictor.predict(job_title, education, years)
            confidence = max(proba) * 100
            print(f"\nInput:")
            print(f"  Job Title: {job_title}")
            print(f"  Education: {education}")
            print(f"  Experience: {years} years")
            print(f"Prediction: {prediction} (Confidence: {confidence:.2f}%)")
        except ValueError as e:
            print(f"\nInput: {job_title}, {education}, {years} years")
            print(f"Error: {e}")
    
    # Example 2: Batch prediction
    print("\n\n>>> Batch Prediction:")
    batch_data = pd.DataFrame({
        'Job Title': ['Aeronautical engineer', 'Visual merchandiser', 'Town planner'],
        'Required Education': ["Master’s Degree", "Bachelor’s Degree", "Bachelor’s Degree"],
        'Experience Required (Years)': [7, 3, 5]
    })
    
    results = predictor.predict_batch(batch_data)
    print("\n" + results.to_string(index=False))
    
    print("\n" + "="*80)


def interactive_prediction():
    """Interactive prediction mode"""
    print("\n" + "="*80)
    print("INTERACTIVE JOB STATUS PREDICTION")
    print("="*80)
    
    predictor = JobStatusPredictor()
    
    print("\nAvailable Education Levels:")
    for edu in predictor.get_available_educations():
        print(f"  - {edu}")
    
    print(f"\nTotal Job Titles Available: {len(predictor.get_available_job_titles())}")
    print("(To see all job titles, use: predictor.get_available_job_titles())")
    
    print("\n" + "="*80)
    print("Enter job details to predict status:")
    print("="*80)
    
    try:
        job_title = input("\nJob Title: ").strip()
        education = input("Required Education: ").strip()
        years = int(input("Experience Required (Years): ").strip())
        
        prediction, proba = predictor.predict(job_title, education, years)
        confidence = max(proba) * 100
        
        print("\n" + "="*80)
        print("PREDICTION RESULT")
        print("="*80)
        print(f"Predicted Job Status: {prediction}")
        print(f"Confidence: {confidence:.2f}%")
        print("="*80)
        
    except ValueError as e:
        print(f"\nError: {e}")
    except KeyboardInterrupt:
        print("\n\nPrediction cancelled.")


if __name__ == "__main__":
    # Run example predictions
    example_predictions()
    
    # Uncomment to run interactive mode
    # interactive_prediction()

