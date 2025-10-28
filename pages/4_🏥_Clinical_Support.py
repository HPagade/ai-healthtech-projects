"""
AI Clinical Decision Support Tool
Prototype symptom checker using machine learning
⚠️ EDUCATIONAL PURPOSES ONLY - NOT FOR ACTUAL MEDICAL USE
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_css, add_page_header, add_footer

st.set_page_config(page_title="AI Clinical Decision Support", page_icon="🏥", layout="wide")
apply_custom_css()

# Medical disclaimer
st.markdown("""
<div style="background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 1rem;">
    <strong>⚠️ MEDICAL DISCLAIMER</strong><br/>
    This tool is for <strong>EDUCATIONAL PURPOSES ONLY</strong>. It is NOT a substitute for professional medical advice,
    diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any medical questions.
</div>
""", unsafe_allow_html=True)

add_page_header("AI Clinical Decision Support", "Symptom-based assessment using machine learning", "🏥")

# Generate and cache sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    symptoms = ['fever', 'cough', 'fatigue', 'difficulty_breathing', 'headache',
                'sore_throat', 'runny_nose', 'nausea', 'vomiting', 'diarrhea',
                'chest_pain', 'abdominal_pain', 'rash', 'joint_pain', 'chills']

    diseases = ['Common Cold', 'Influenza', 'COVID-19', 'Pneumonia',
                'Gastroenteritis', 'Migraine', 'Strep Throat', 'Allergies']

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
    for _ in range(1000):
        disease = np.random.choice(diseases)
        symptom_vector = {}
        for symptom in symptoms:
            if symptom in disease_patterns[disease]:
                symptom_vector[symptom] = 1 if np.random.random() > 0.2 else 0
            else:
                symptom_vector[symptom] = 1 if np.random.random() > 0.85 else 0
        symptom_vector['disease'] = disease
        data.append(symptom_vector)

    return pd.DataFrame(data), symptoms, diseases

df, symptoms, diseases = generate_sample_data()

# Train model
@st.cache_resource
def train_model(df, symptoms):
    X = df[symptoms]
    y = df['disease']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_model(df, symptoms)

# Sidebar
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This AI-powered tool uses machine learning to suggest possible conditions based on symptoms.

    **Model:** Random Forest Classifier
    **Training Data:** 1,000 symptom-disease patterns
    **Conditions:** 8 common illnesses
    """)
    st.markdown("---")
    st.markdown("### How to Use")
    st.markdown("""
    1. Select your symptoms
    2. Click "Analyze Symptoms"
    3. Review the predictions
    4. See recommendations

    **Remember:** This is educational only!
    """)

# Main interface
tab1, tab2, tab3 = st.tabs(["🔍 Symptom Checker", "📊 Model Insights", "📚 Learn More"])

with tab1:
    st.markdown("### Select Your Symptoms")

    # Symptom selection in columns
    col1, col2, col3 = st.columns(3)
    selected_symptoms = {}

    for i, symptom in enumerate(symptoms):
        col_index = i % 3
        with [col1, col2, col3][col_index]:
            selected_symptoms[symptom] = st.checkbox(
                symptom.replace('_', ' ').title(),
                key=symptom
            )

    st.markdown("---")

    if st.button("🔬 Analyze Symptoms", type="primary", use_container_width=True):
        # Prepare input
        input_data = np.array([[1 if selected_symptoms[s] else 0 for s in symptoms]])
        selected_count = sum(selected_symptoms.values())

        if selected_count == 0:
            st.warning("⚠️ Please select at least one symptom to analyze.")
        else:
            st.markdown("### 📋 Analysis Results")

            # Get predictions and probabilities
            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]

            # Display results
            col1, col2 = st.columns([2, 1])

            with col1:
                # Top predictions
                st.markdown("#### Most Likely Conditions")

                prob_df = pd.DataFrame({
                    'Condition': model.classes_,
                    'Probability': probabilities
                }).sort_values('Probability', ascending=False)

                # Top 3 predictions
                for i, row in prob_df.head(3).iterrows():
                    confidence = row['Probability'] * 100
                    if i == prob_df.index[0]:
                        st.success(f"**{row['Condition']}** - {confidence:.1f}% confidence")
                    elif confidence > 10:
                        st.info(f"**{row['Condition']}** - {confidence:.1f}% confidence")
                    else:
                        st.warning(f"**{row['Condition']}** - {confidence:.1f}% confidence")

                # Probability chart
                fig = px.bar(
                    prob_df.head(5),
                    x='Probability',
                    y='Condition',
                    orientation='h',
                    title="Top 5 Condition Probabilities",
                    color='Probability',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Your Symptoms")
                active_symptoms = [s.replace('_', ' ').title() for s, v in selected_symptoms.items() if v]
                for symptom in active_symptoms:
                    st.markdown(f"✓ {symptom}")

                st.metric("Symptoms Selected", selected_count)

            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 Recommendations")

            if prob_df.iloc[0]['Probability'] > 0.7:
                st.markdown("""
                **High Confidence Prediction:**
                - Consider consulting a healthcare provider
                - Monitor your symptoms closely
                - Stay hydrated and rest
                - Take note of any symptom changes
                """)
            else:
                st.markdown("""
                **Multiple Possible Conditions:**
                - Symptoms match several conditions
                - Professional medical evaluation recommended
                - Track symptom progression
                - Seek immediate care if symptoms worsen
                """)

            # When to seek immediate care
            emergency_symptoms = ['difficulty_breathing', 'chest_pain', 'severe_headache']
            has_emergency = any(selected_symptoms.get(s, False) for s in emergency_symptoms)

            if has_emergency:
                st.error("""
                🚨 **SEEK IMMEDIATE MEDICAL ATTENTION**

                You have symptoms that require immediate evaluation:
                - Difficulty breathing
                - Chest pain
                - Severe symptoms

                Call emergency services or go to the nearest emergency room.
                """)

with tab2:
    st.markdown("### Model Performance & Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Feature importance
        feature_importance = pd.DataFrame({
            'Symptom': symptoms,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)

        fig = px.bar(
            feature_importance.head(10),
            x='Importance',
            y='Symptom',
            orientation='h',
            title="Top 10 Most Important Symptoms for Diagnosis",
            color='Importance',
            color_continuous_scale='Reds'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Disease distribution in training data
        disease_counts = df['disease'].value_counts()
        fig = px.pie(
            values=disease_counts.values,
            names=disease_counts.index,
            title="Training Data Distribution",
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Model stats
    st.markdown("#### Model Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Model Type", "Random Forest")
    with col2:
        st.metric("Training Samples", "1,000")
    with col3:
        st.metric("Features", len(symptoms))
    with col4:
        st.metric("Conditions", len(diseases))

with tab3:
    st.markdown("### About Clinical Decision Support Systems")

    st.markdown("""
    #### What is AI in Healthcare?

    Clinical Decision Support Systems (CDSS) use AI and machine learning to assist healthcare
    professionals in making diagnostic and treatment decisions.

    #### How This Tool Works

    1. **Data Collection:** Symptoms are collected from the user
    2. **Feature Encoding:** Symptoms are converted to numerical format
    3. **ML Prediction:** Random Forest model analyzes patterns
    4. **Probability Calculation:** Likelihood of each condition is computed
    5. **Result Display:** Top predictions are shown with confidence scores

    #### Limitations

    - **Training Data:** Uses synthetic data, not real medical records
    - **Simplified Model:** Real diagnosis requires much more information
    - **No Context:** Doesn't consider age, medical history, or physical examination
    - **Educational Only:** Not validated for clinical use

    #### Real-World Applications

    Professional CDSS systems are used for:
    - Diagnostic assistance
    - Treatment recommendations
    - Drug interaction checking
    - Clinical pathway guidance
    - Risk stratification

    #### Learn More

    - [FDA Guidance on AI/ML in Medical Devices](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices)
    - [WHO Guidelines on AI for Health](https://www.who.int/publications/i/item/9789240029200)
    - [Clinical Decision Support at Stanford](https://aimi.stanford.edu/)
    """)

add_footer()
