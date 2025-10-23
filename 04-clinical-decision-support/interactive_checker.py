"""
Interactive Symptom Checker CLI
User-friendly interface for symptom checking
"""

from symptom_checker import SymptomChecker
from pathlib import Path


def print_header():
    """Print welcome header"""
    print("\n" + "=" * 80)
    print(" " * 25 + "SYMPTOM CHECKER")
    print(" " * 20 + "AI Clinical Decision Support")
    print("=" * 80)
    print("\nDISCLAIMER: This is an educational tool only.")
    print("Always consult healthcare professionals for medical advice.")
    print("=" * 80 + "\n")


def get_symptoms(available_symptoms):
    """Collect symptoms from user"""
    print("Select your symptoms (enter the number, or 'done' when finished):\n")

    for i, symptom in enumerate(available_symptoms, 1):
        display_name = symptom.replace('_', ' ').title()
        print(f"{i}. {display_name}")

    print()

    selected_symptoms = {}

    while True:
        choice = input("Enter symptom number (or 'done'): ").strip().lower()

        if choice == 'done':
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_symptoms):
                symptom = available_symptoms[idx]
                selected_symptoms[symptom] = 1
                display_name = symptom.replace('_', ' ').title()
                print(f"✓ Added: {display_name}")
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number or 'done'.")

    return selected_symptoms


def display_results(result):
    """Display prediction results"""
    print("\n" + "=" * 80)
    print(" " * 30 + "RESULTS")
    print("=" * 80 + "\n")

    print(f"Primary Assessment: {result['primary_diagnosis']}")
    print(f"Confidence Level: {result['confidence']:.1%}")

    print("\nPossible Conditions (in order of likelihood):")
    print("-" * 80)

    for i, pred in enumerate(result['top_predictions'], 1):
        bar_length = int(pred['probability'] * 50)
        bar = '█' * bar_length + '░' * (50 - bar_length)

        print(f"\n{i}. {pred['disease']}")
        print(f"   [{bar}] {pred['probability']:.1%}")

    print("\n" + "=" * 80)


def get_recommendations(diagnosis):
    """Provide general recommendations based on diagnosis"""
    recommendations = {
        'Common Cold': [
            "Rest and stay hydrated",
            "Over-the-counter cold medications may help",
            "Usually resolves in 7-10 days",
            "See a doctor if symptoms worsen or persist beyond 10 days"
        ],
        'Influenza': [
            "Rest and drink plenty of fluids",
            "Antiviral medications may be prescribed if caught early",
            "Isolate to prevent spreading to others",
            "Seek immediate care if difficulty breathing develops"
        ],
        'COVID-19': [
            "Get tested for COVID-19",
            "Isolate from others",
            "Monitor oxygen levels if possible",
            "Seek immediate care if severe symptoms develop"
        ],
        'Pneumonia': [
            "Seek medical attention promptly",
            "May require antibiotics if bacterial",
            "Rest and stay hydrated",
            "Go to ER if severe breathing difficulty"
        ],
        'Gastroenteritis': [
            "Stay hydrated - drink water, clear broths, or electrolyte solutions",
            "Eat bland foods when ready (BRAT diet: Bananas, Rice, Applesauce, Toast)",
            "Rest and avoid solid foods initially",
            "See a doctor if symptoms persist beyond 2-3 days"
        ],
        'Migraine': [
            "Rest in a quiet, dark room",
            "Apply cold compress to head",
            "Stay hydrated",
            "Consult doctor about preventive medications if frequent"
        ],
        'Strep Throat': [
            "See a doctor for throat culture",
            "Antibiotics typically required",
            "Rest and stay hydrated",
            "Avoid close contact with others until 24 hours after starting antibiotics"
        ],
        'Allergies': [
            "Identify and avoid triggers if possible",
            "Antihistamines may provide relief",
            "Consider seeing an allergist",
            "Monitor for worsening symptoms"
        ]
    }

    return recommendations.get(diagnosis, ["Consult with a healthcare professional for proper diagnosis and treatment"])


def main():
    """Main interactive interface"""
    print_header()

    # Load or train model
    model_path = Path('models/symptom_checker.pkl')

    checker = SymptomChecker(model_type='random_forest')

    if model_path.exists():
        print("Loading trained model...\n")
        checker.load_model()
    else:
        print("No trained model found. Training new model...\n")
        df = checker.load_data()
        checker.train_model(df)
        checker.save_model()

    # Get user symptoms
    symptoms = get_symptoms(checker.feature_names)

    if not symptoms:
        print("\nNo symptoms selected. Exiting.")
        return

    print(f"\nYou selected {len(symptoms)} symptom(s):")
    for symptom in symptoms:
        display_name = symptom.replace('_', ' ').title()
        print(f"  - {display_name}")

    # Get prediction
    print("\nAnalyzing symptoms...")
    result = checker.predict(symptoms)

    # Display results
    display_results(result)

    # Show recommendations
    print("\nGENERAL RECOMMENDATIONS:")
    print("-" * 80)
    recommendations = get_recommendations(result['primary_diagnosis'])
    for rec in recommendations:
        print(f"• {rec}")

    print("\n" + "=" * 80)
    print("IMPORTANT: This tool is for educational purposes only.")
    print("Please consult with a qualified healthcare provider for proper medical advice.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
