"""
AI Clinical Decision Support Tool
Prototype symptom checker using decision trees and machine learning
"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
from pathlib import Path


class SymptomChecker:
    """Symptom-based disease prediction system"""

    def __init__(self, model_type='decision_tree'):
        """
        Initialize symptom checker

        Args:
            model_type: 'decision_tree' or 'random_forest'
        """
        self.model_type = model_type
        self.model = None
        self.symptom_list = []
        self.disease_list = []
        self.feature_names = []

    def load_data(self, filepath='data/symptom_data.csv'):
        """Load symptom dataset"""
        try:
            df = pd.read_csv(filepath)
            print(f"Loaded {len(df)} records from {filepath}")
            return df
        except FileNotFoundError:
            print(f"Data file not found: {filepath}")
            print("Generating sample data...")
            return self.generate_sample_data()

    def generate_sample_data(self, n_samples=1000):
        """Generate sample symptom-disease data for demonstration"""
        np.random.seed(42)

        # Define symptoms and diseases
        symptoms = [
            'fever', 'cough', 'fatigue', 'difficulty_breathing', 'headache',
            'sore_throat', 'runny_nose', 'nausea', 'vomiting', 'diarrhea',
            'chest_pain', 'abdominal_pain', 'rash', 'joint_pain', 'chills'
        ]

        diseases = [
            'Common Cold', 'Influenza', 'COVID-19', 'Pneumonia',
            'Gastroenteritis', 'Migraine', 'Strep Throat', 'Allergies'
        ]

        # Disease-symptom patterns (simplified for demo)
        disease_patterns = {
            'Common Cold': ['runny_nose', 'sore_throat', 'cough', 'fatigue'],
            'Influenza': ['fever', 'cough', 'fatigue', 'headache', 'chills', 'joint_pain'],
            'COVID-19': ['fever', 'cough', 'fatigue', 'difficulty_breathing'],
            'Pneumonia': ['fever', 'cough', 'difficulty_breathing', 'chest_pain', 'fatigue'],
            'Gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'abdominal_pain', 'fever'],
            'Migraine': ['headache', 'nausea', 'fatigue'],
            'Strep Throat': ['sore_throat', 'fever', 'headache'],
            'Allergies': ['runny_nose', 'sore_throat', 'cough', 'rash']
        }

        data = []

        for _ in range(n_samples):
            # Randomly select a disease
            disease = np.random.choice(diseases)

            # Create symptom vector
            symptom_vector = {}
            for symptom in symptoms:
                if symptom in disease_patterns[disease]:
                    # High probability for characteristic symptoms
                    symptom_vector[symptom] = 1 if np.random.random() > 0.2 else 0
                else:
                    # Low probability for other symptoms
                    symptom_vector[symptom] = 1 if np.random.random() > 0.85 else 0

            symptom_vector['disease'] = disease
            data.append(symptom_vector)

        df = pd.DataFrame(data)

        # Save for future use
        Path('data').mkdir(exist_ok=True)
        df.to_csv('data/symptom_data.csv', index=False)
        print("Sample data generated and saved to data/symptom_data.csv")

        return df

    def train_model(self, df):
        """Train the prediction model"""
        # Separate features and target
        X = df.drop('disease', axis=1)
        y = df['disease']

        self.feature_names = X.columns.tolist()
        self.disease_list = y.unique().tolist()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        if self.model_type == 'decision_tree':
            self.model = DecisionTreeClassifier(max_depth=10, random_state=42)
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

        print(f"\nTraining {self.model_type} model...")
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\nModel Accuracy: {accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        return accuracy

    def predict(self, symptoms):
        """
        Predict disease based on symptoms

        Args:
            symptoms: Dictionary of symptoms {symptom_name: 1/0}

        Returns:
            Dictionary with prediction and probability
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")

        # Create feature vector
        feature_vector = []
        for feature in self.feature_names:
            feature_vector.append(symptoms.get(feature, 0))

        # Reshape for prediction
        X = np.array(feature_vector).reshape(1, -1)

        # Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [
            {
                'disease': self.model.classes_[idx],
                'probability': probabilities[idx]
            }
            for idx in top_indices
        ]

        return {
            'primary_diagnosis': prediction,
            'confidence': max(probabilities),
            'top_predictions': top_predictions
        }

    def get_feature_importance(self):
        """Get feature importance scores"""
        if self.model is None:
            raise ValueError("Model not trained.")

        if hasattr(self.model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'symptom': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)

            return importance_df

        return None

    def save_model(self, filepath='models/symptom_checker.pkl'):
        """Save trained model"""
        Path('models').mkdir(exist_ok=True)

        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'disease_list': self.disease_list,
            'model_type': self.model_type
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"Model saved to {filepath}")

    def load_model(self, filepath='models/symptom_checker.pkl'):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.disease_list = model_data['disease_list']
        self.model_type = model_data['model_type']

        print(f"Model loaded from {filepath}")


def main():
    """Main execution"""
    print("=" * 80)
    print(" " * 20 + "AI CLINICAL DECISION SUPPORT TOOL")
    print("=" * 80 + "\n")

    # Initialize checker
    checker = SymptomChecker(model_type='random_forest')

    # Load data
    df = checker.load_data()

    # Train model
    checker.train_model(df)

    # Save model
    checker.save_model()

    # Show feature importance
    print("\nTop 10 Most Important Symptoms:")
    importance = checker.get_feature_importance()
    print(importance.head(10))

    # Example prediction
    print("\n" + "=" * 80)
    print("EXAMPLE PREDICTION")
    print("=" * 80)

    test_symptoms = {
        'fever': 1,
        'cough': 1,
        'fatigue': 1,
        'difficulty_breathing': 1
    }

    print(f"\nSymptoms: {[k for k, v in test_symptoms.items() if v == 1]}")

    result = checker.predict(test_symptoms)

    print(f"\nPrimary Diagnosis: {result['primary_diagnosis']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nTop 3 Possible Conditions:")
    for i, pred in enumerate(result['top_predictions'], 1):
        print(f"{i}. {pred['disease']}: {pred['probability']:.2%}")

    print("\n" + "=" * 80)
    print("DISCLAIMER: This is a prototype for educational purposes only.")
    print("Always consult with healthcare professionals for medical advice.")
    print("=" * 80)


if __name__ == "__main__":
    main()
