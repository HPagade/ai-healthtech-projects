"""
Customer Health Score Calculator - Streamlit Dashboard
Interactive dashboard for predicting customer churn using usage metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from health_score import HealthScoreCalculator
from data_generator import generate_sample_data


# Page configuration
st.set_page_config(
    page_title="Customer Health Score Calculator",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Customer Health Score Calculator")
st.markdown("Predict customer churn risk using usage metrics and engagement data")

# Sidebar
st.sidebar.header("⚙️ Configuration")

# Data source selection
data_source = st.sidebar.radio(
    "Data Source",
    ["Use Sample Data", "Upload CSV"]
)

# Load data
@st.cache_data
def load_data(source="sample"):
    if source == "sample":
        return generate_sample_data(num_customers=100)
    return None

if data_source == "Use Sample Data":
    df = load_data("sample")
elif data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload customer data CSV", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file or use sample data")
        st.stop()

# Initialize calculator
calculator = HealthScoreCalculator()

# Calculate health scores
if df is not None:
    df['health_score'] = df.apply(
        lambda row: calculator.calculate_health_score(
            login_frequency=row['login_frequency'],
            feature_usage=row['feature_usage'],
            support_tickets=row['support_tickets'],
            days_since_last_login=row['days_since_last_login'],
            contract_value=row['contract_value']
        ),
        axis=1
    )

    df['risk_category'] = df['health_score'].apply(calculator.categorize_risk)
    df['churn_risk'] = df['health_score'].apply(lambda x: calculator.predict_churn_probability(x))

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        len(df),
        delta=None
    )

with col2:
    high_risk = len(df[df['risk_category'] == 'High Risk'])
    st.metric(
        "High Risk Customers",
        high_risk,
        delta=f"{(high_risk/len(df)*100):.1f}%",
        delta_color="inverse"
    )

with col3:
    avg_score = df['health_score'].mean()
    st.metric(
        "Avg Health Score",
        f"{avg_score:.1f}",
        delta=None
    )

with col4:
    avg_churn = df['churn_risk'].mean()
    st.metric(
        "Avg Churn Risk",
        f"{avg_churn:.1%}",
        delta=None
    )

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "👥 Customer List", "🔍 Individual Analysis", "📊 Trends"])

with tab1:
    st.header("Health Score Distribution")

    # Health score histogram
    fig_hist = px.histogram(
        df,
        x='health_score',
        nbins=30,
        color='risk_category',
        color_discrete_map={
            'Healthy': 'green',
            'At Risk': 'orange',
            'High Risk': 'red'
        },
        title="Customer Health Score Distribution"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Risk category pie chart
    col1, col2 = st.columns(2)

    with col1:
        risk_counts = df['risk_category'].value_counts()
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Customers by Risk Category",
            color=risk_counts.index,
            color_discrete_map={
                'Healthy': 'green',
                'At Risk': 'orange',
                'High Risk': 'red'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Scatter plot: Health Score vs Contract Value
        fig_scatter = px.scatter(
            df,
            x='contract_value',
            y='health_score',
            color='risk_category',
            size='churn_risk',
            hover_data=['customer_id', 'login_frequency', 'support_tickets'],
            title="Health Score vs Contract Value",
            color_discrete_map={
                'Healthy': 'green',
                'At Risk': 'orange',
                'High Risk': 'red'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.header("Customer Health Scores")

    # Filter by risk category
    filter_risk = st.multiselect(
        "Filter by Risk Category",
        options=['Healthy', 'At Risk', 'High Risk'],
        default=['Healthy', 'At Risk', 'High Risk']
    )

    filtered_df = df[df['risk_category'].isin(filter_risk)].copy()

    # Sort by health score
    filtered_df = filtered_df.sort_values('health_score', ascending=True)

    # Display table
    st.dataframe(
        filtered_df[[
            'customer_id', 'health_score', 'churn_risk', 'risk_category',
            'login_frequency', 'feature_usage', 'support_tickets',
            'days_since_last_login', 'contract_value'
        ]].style.background_gradient(subset=['health_score'], cmap='RdYlGn'),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="customer_health_scores.csv",
        mime="text/csv"
    )

with tab3:
    st.header("Individual Customer Analysis")

    # Customer selector
    customer_id = st.selectbox(
        "Select Customer",
        options=df['customer_id'].tolist()
    )

    customer = df[df['customer_id'] == customer_id].iloc[0]

    # Customer metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Health Score", f"{customer['health_score']:.1f}")
        st.metric("Risk Category", customer['risk_category'])

    with col2:
        st.metric("Churn Probability", f"{customer['churn_risk']:.1%}")
        st.metric("Contract Value", f"${customer['contract_value']:,.0f}")

    with col3:
        st.metric("Login Frequency", f"{customer['login_frequency']}/month")
        st.metric("Support Tickets", int(customer['support_tickets']))

    # Gauge chart for health score
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=customer['health_score'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Health Score"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 40
            }
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Recommendations
    st.subheader("Recommendations")
    recommendations = calculator.get_recommendations(
        health_score=customer['health_score'],
        login_frequency=customer['login_frequency'],
        support_tickets=customer['support_tickets'],
        days_since_last_login=customer['days_since_last_login']
    )

    for rec in recommendations:
        st.info(rec)

with tab4:
    st.header("Trend Analysis")
    st.info("This section would show time-series data if available. Add date columns to your data for trend analysis.")

    # Feature importance
    st.subheader("Feature Importance for Health Score")

    feature_importance = pd.DataFrame({
        'Feature': ['Login Frequency', 'Feature Usage', 'Support Tickets', 'Days Since Last Login', 'Contract Value'],
        'Weight': [0.30, 0.25, 0.20, 0.15, 0.10]
    })

    fig_importance = px.bar(
        feature_importance,
        x='Weight',
        y='Feature',
        orientation='h',
        title="Feature Weights in Health Score Calculation",
        color='Weight',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_importance, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Customer Health Score Calculator v1.0")
