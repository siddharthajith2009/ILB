"""
Data Preprocessing Script for AI Job Impact Predictor
This script preprocesses the job dataset for machine learning
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings
warnings.filterwarnings('ignore')

def load_data(filepath):
    """Load the dataset from CSV file"""
    print("Loading dataset...")
    df = pd.read_csv(filepath)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    print("\n" + "="*50)
    print("HANDLING MISSING VALUES")
    print("="*50)
    
    # Check for missing values
    missing_counts = df.isnull().sum()
    print("\nMissing values per column:")
    print(missing_counts[missing_counts > 0])
    
    if missing_counts.sum() == 0:
        print("No missing values found!")
    else:
        # For numerical columns: fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                print(f"Filled {col} with median: {median_val:.2f}")
        
        # For categorical columns: fill with mode (most frequent value)
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()[0]
                df[col].fillna(mode_val, inplace=True)
                print(f"Filled {col} with mode: {mode_val}")
    
    return df

def detect_outliers(df):
    """Flag obvious outliers using IQR method"""
    print("\n" + "="*50)
    print("DETECTING OUTLIERS")
    print("="*50)
    
    # Numerical columns to check for outliers
    numerical_cols = ['Median Salary (USD)', 'Experience Required (Years)', 
                      'Job Openings (2024)', 'Projected Openings (2030)',
                      'Remote Work Ratio (%)', 'Automation Risk (%)', 
                      'Gender Diversity (%)']
    
    # Create a column to flag outliers
    df['Has_Outlier'] = False
    outlier_details = []
    
    for col in numerical_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Flag outliers
            outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            df.loc[outliers, 'Has_Outlier'] = True
            
            num_outliers = outliers.sum()
            if num_outliers > 0:
                print(f"\n{col}:")
                print(f"  Range: [{lower_bound:.2f}, {upper_bound:.2f}]")
                print(f"  Outliers found: {num_outliers} ({num_outliers/len(df)*100:.2f}%)")
                outlier_details.append({
                    'column': col,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'num_outliers': num_outliers
                })
    
    total_outliers = df['Has_Outlier'].sum()
    print(f"\nTotal rows with at least one outlier: {total_outliers} ({total_outliers/len(df)*100:.2f}%)")
    
    return df, outlier_details

def encode_categorical_features(df):
    """Encode non-numerical (categorical) features"""
    print("\n" + "="*50)
    print("ENCODING CATEGORICAL FEATURES")
    print("="*50)
    
    # Dictionary to store encoders for later use
    encoders = {}
    
    # Categorical columns to encode
    categorical_cols = ['Job Title', 'Industry', 'Job Status', 'AI Impact Level', 
                       'Required Education', 'Location']
    
    for col in categorical_cols:
        if col in df.columns:
            print(f"\nEncoding {col}...")
            print(f"  Unique values: {df[col].nunique()}")
            
            # Create and fit label encoder
            le = LabelEncoder()
            df[f'{col}_Encoded'] = le.fit_transform(df[col])
            encoders[col] = le
            
            # Show first few mappings as examples
            unique_values = df[col].unique()[:5]
            encoded_values = le.transform(unique_values)
            print(f"  Examples: {dict(zip(unique_values, encoded_values))}")
    
    print("\n✓ All categorical features encoded successfully!")
    return df, encoders

def normalize_numerical_features(df):
    """Normalize appropriate numeric features using StandardScaler"""
    print("\n" + "="*50)
    print("NORMALIZING NUMERICAL FEATURES")
    print("="*50)
    
    # Numerical columns to normalize
    cols_to_normalize = ['Median Salary (USD)', 'Experience Required (Years)', 
                        'Job Openings (2024)', 'Projected Openings (2030)',
                        'Remote Work Ratio (%)', 'Automation Risk (%)', 
                        'Gender Diversity (%)']
    
    scaler = StandardScaler()
    
    for col in cols_to_normalize:
        if col in df.columns:
            print(f"\nNormalizing {col}...")
            print(f"  Original - Mean: {df[col].mean():.2f}, Std: {df[col].std():.2f}")
            
            # Normalize the column
            df[f'{col}_Normalized'] = scaler.fit_transform(df[[col]])
            
            print(f"  Normalized - Mean: {df[f'{col}_Normalized'].mean():.2f}, Std: {df[f'{col}_Normalized'].std():.2f}")
    
    print("\n✓ All numerical features normalized successfully!")
    return df, scaler

def generate_summary_report(df, outlier_details):
    """Generate a summary report of the preprocessing"""
    print("\n" + "="*50)
    print("PREPROCESSING SUMMARY REPORT")
    print("="*50)
    
    print(f"\nTotal records: {len(df)}")
    print(f"Total features: {len(df.columns)}")
    print(f"\nNew encoded features created: {len([col for col in df.columns if 'Encoded' in col])}")
    print(f"New normalized features created: {len([col for col in df.columns if 'Normalized' in col])}")
    print(f"Records flagged with outliers: {df['Has_Outlier'].sum()}")
    
    # Input and output features
    print("\n--- INPUT FEATURES (for model) ---")
    input_features = ['Job Title_Encoded', 'Required Education_Encoded', 'Experience Required (Years)']
    for feat in input_features:
        if feat in df.columns:
            print(f"  ✓ {feat}")
    
    print("\n--- OUTPUT FEATURES (to predict) ---")
    output_features = ['AI Impact Level_Encoded', 'Median Salary (USD)_Normalized', 
                      'Projected Openings (2030)_Normalized', 'Remote Work Ratio (%)_Normalized',
                      'Automation Risk (%)_Normalized']
    for feat in output_features:
        if feat in df.columns:
            print(f"  ✓ {feat}")

def save_preprocessed_data(df, output_filepath):
    """Save the preprocessed dataset"""
    print("\n" + "="*50)
    print("SAVING PREPROCESSED DATA")
    print("="*50)
    
    df.to_csv(output_filepath, index=False)
    print(f"✓ Preprocessed data saved to: {output_filepath}")
    print(f"  File size: {len(df)} rows × {len(df.columns)} columns")

def main():
    """Main preprocessing pipeline"""
    print("\n" + "="*60)
    print("  AI JOB IMPACT PREDICTOR - DATA PREPROCESSING")
    print("="*60)
    
    # File paths
    input_file = '../data/ai_job_trends_dataset 2.csv'
    output_file = '../data/preprocessed_job_data.csv'
    
    try:
        # Step 1: Load data
        df = load_data(input_file)
        
        # Step 2: Handle missing values
        df = handle_missing_values(df)
        
        # Step 3: Detect and flag outliers
        df, outlier_details = detect_outliers(df)
        
        # Step 4: Encode categorical features
        df, encoders = encode_categorical_features(df)
        
        # Step 5: Normalize numerical features
        df, scaler = normalize_numerical_features(df)
        
        # Step 6: Generate summary report
        generate_summary_report(df, outlier_details)
        
        # Step 7: Save preprocessed data
        save_preprocessed_data(df, output_file)
        
        print("\n" + "="*60)
        print("  ✓ PREPROCESSING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nYou can now use the preprocessed data for training your AI model.")
        print("Next steps:")
        print("  1. Review the preprocessed_job_data.csv file")
        print("  2. Build your machine learning model")
        print("  3. Train the model using the encoded and normalized features")
        
    except Exception as e:
        print(f"\n❌ Error during preprocessing: {str(e)}")
        raise

if __name__ == "__main__":
    main()

