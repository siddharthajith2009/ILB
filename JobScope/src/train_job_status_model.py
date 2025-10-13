"""
AI Model to Predict Job Status
Inputs: Job Title, Required Education, Experience Required (Years)
Output: Job Status (Increasing/Declining/Stable)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

def load_data():
    """Load preprocessed data"""
    data_path = '/Users/siddharthajith/Documents/JobScope/data/preprocessed_job_data.csv'
    df = pd.read_csv(data_path)
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def prepare_features(df):
    """Select relevant features for prediction"""
    # Input features: Job Title (encoded), Required Education (encoded), Experience Required (Years)
    X = df[['Job Title_Encoded', 'Required Education_Encoded', 'Experience Required (Years)']]
    
    # Target: Job Status (encoded)
    y = df['Job Status_Encoded']
    
    print(f"\nFeature columns: {X.columns.tolist()}")
    print(f"Target column: Job Status_Encoded")
    print(f"\nTarget distribution:")
    print(y.value_counts())
    
    # Get unique job statuses for reference
    status_mapping = df[['Job Status', 'Job Status_Encoded']].drop_duplicates().sort_values('Job Status_Encoded')
    print(f"\nJob Status Mapping:")
    print(status_mapping)
    
    return X, y, status_mapping

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and compare performance"""
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    results = {}
    
    print("\n" + "="*80)
    print("MODEL TRAINING AND EVALUATION")
    print("="*80)
    
    for name, model in models.items():
        print(f"\n>>> Training {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Evaluation
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = {'model': model, 'accuracy': accuracy}
        
        print(f"\n{name} Results:")
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
    
    # Select best model
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['model']
    best_accuracy = results[best_model_name]['accuracy']
    
    print("\n" + "="*80)
    print(f"BEST MODEL: {best_model_name} with accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
    print("="*80)
    
    return best_model, best_model_name, results

def save_model(model, status_mapping, model_name):
    """Save the trained model and mappings"""
    models_dir = '/Users/siddharthajith/Documents/JobScope/models'
    os.makedirs(models_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(models_dir, 'job_status_predictor.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n✓ Model saved to: {model_path}")
    
    # Save status mapping
    mapping_path = os.path.join(models_dir, 'status_mapping.pkl')
    with open(mapping_path, 'wb') as f:
        pickle.dump(status_mapping, f)
    print(f"✓ Status mapping saved to: {mapping_path}")
    
    # Save model info
    info_path = os.path.join(models_dir, 'model_info.txt')
    with open(info_path, 'w') as f:
        f.write(f"Job Status Prediction Model\n")
        f.write(f"="*50 + "\n")
        f.write(f"Model Type: {model_name}\n")
        f.write(f"Input Features:\n")
        f.write(f"  - Job Title (encoded)\n")
        f.write(f"  - Required Education (encoded)\n")
        f.write(f"  - Experience Required (Years)\n")
        f.write(f"\nTarget: Job Status (Increasing/Declining/Stable)\n")
    print(f"✓ Model info saved to: {info_path}")

def main():
    print("="*80)
    print("JOB STATUS PREDICTION MODEL TRAINING")
    print("="*80)
    
    # Load data
    df = load_data()
    
    # Prepare features
    X, y, status_mapping = prepare_features(df)
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nData split:")
    print(f"  Training set: {X_train.shape[0]} samples")
    print(f"  Test set: {X_test.shape[0]} samples")
    
    # Train models
    best_model, best_model_name, results = train_models(X_train, X_test, y_train, y_test)
    
    # Save best model
    save_model(best_model, status_mapping, best_model_name)
    
    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print("="*80)
    
    return best_model, status_mapping

if __name__ == "__main__":
    model, mapping = main()

