# AI Clinical Decision Support Tool

Prototype symptom checker using decision trees and machine learning for educational purposes.

**⚠️ DISCLAIMER: This is a prototype for educational and demonstration purposes only. Always consult with qualified healthcare professionals for medical advice, diagnosis, and treatment.**

## Features

- Machine learning-based symptom analysis
- Decision tree and random forest classifiers
- Interactive CLI interface
- Confidence scores for predictions
- Top 3 differential diagnoses
- General health recommendations
- Feature importance analysis
- Model persistence (save/load)

## Tech Stack

- **Python** - Core programming language
- **Scikit-learn** - Machine learning models
- **Pandas** - Data handling
- **NumPy** - Numerical computations

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create data directory:
```bash
mkdir -p data models
```

## Usage

### Train the Model

```bash
python symptom_checker.py
```

This will:
- Generate sample symptom-disease data (or load existing data)
- Train a Random Forest classifier
- Display model accuracy and classification metrics
- Show feature importance
- Save the model for future use
- Run an example prediction

### Interactive Symptom Checker

```bash
python interactive_checker.py
```

Follow the prompts to:
1. Select your symptoms from the list
2. View prediction results with confidence scores
3. Get general recommendations

## Example Session

```
================================================================================
                         SYMPTOM CHECKER
                    AI Clinical Decision Support
================================================================================

Select your symptoms (enter the number, or 'done' when finished):

1. Fever
2. Cough
3. Fatigue
4. Difficulty Breathing
5. Headache
...

Enter symptom number (or 'done'): 1
✓ Added: Fever

Enter symptom number (or 'done'): 2
✓ Added: Cough

Enter symptom number (or 'done'): done

Analyzing symptoms...

Primary Assessment: Influenza
Confidence Level: 87.5%

Possible Conditions (in order of likelihood):
1. Influenza
   [███████████████████████████████████████░░░░░░░░░░] 87.5%

2. COVID-19
   [█████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 8.2%

3. Common Cold
   [███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 4.3%
```

## Supported Symptoms

- Fever
- Cough
- Fatigue
- Difficulty Breathing
- Headache
- Sore Throat
- Runny Nose
- Nausea
- Vomiting
- Diarrhea
- Chest Pain
- Abdominal Pain
- Rash
- Joint Pain
- Chills

## Supported Diagnoses

- Common Cold
- Influenza
- COVID-19
- Pneumonia
- Gastroenteritis
- Migraine
- Strep Throat
- Allergies

## How It Works

1. **Data Generation**: Creates synthetic symptom-disease patterns based on medical knowledge
2. **Feature Engineering**: Converts symptoms into binary feature vectors
3. **Model Training**: Uses Random Forest or Decision Tree classifier
4. **Prediction**: Analyzes symptom patterns to suggest possible conditions
5. **Confidence Scoring**: Provides probability estimates for each diagnosis

## Model Performance

The model achieves approximately 85-90% accuracy on test data. However, this is with simplified synthetic data and should NOT be relied upon for real medical decisions.

## Project Structure

```
04-clinical-decision-support/
├── symptom_checker.py          # Core ML model and logic
├── interactive_checker.py      # Interactive CLI interface
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/                       # Training data (generated)
│   └── symptom_data.csv
└── models/                     # Trained models (generated)
    └── symptom_checker.pkl
```

## Customization

### Adding New Symptoms

1. Edit `generate_sample_data()` in `symptom_checker.py`
2. Add symptoms to the `symptoms` list
3. Update disease patterns accordingly
4. Retrain the model

### Adding New Diseases

1. Add disease to `diseases` list
2. Define symptom patterns in `disease_patterns`
3. Retrain the model

### Using Real Data

Replace `generate_sample_data()` with real medical datasets:
- Ensure proper data privacy and compliance
- Format: CSV with symptom columns (0/1) and disease column
- Much larger dataset recommended for production use

## Ethical Considerations

- This tool is for educational purposes ONLY
- NOT a substitute for professional medical advice
- Should not be used for self-diagnosis
- Always consult healthcare professionals
- Be transparent about AI limitations
- Protect patient privacy and data

## Future Enhancements

- [ ] Integration with real medical datasets (with proper permissions)
- [ ] Natural language processing for symptom input
- [ ] Severity assessment
- [ ] Age/gender-specific considerations
- [ ] Drug interaction checker
- [ ] Urgency triage (ER vs. urgent care vs. PCP)
- [ ] Multi-language support
- [ ] Clinical guidelines integration
- [ ] Explainable AI features

## Medical Disclaimer

This software is provided for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or seen in this application.
