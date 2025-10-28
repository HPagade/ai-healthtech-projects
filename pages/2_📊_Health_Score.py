"""
Customer Health Score Calculator
Interactive dashboard for predicting customer churn using usage metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add project directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '02-customer-health-score'))

from utils.styling import apply_custom_css, add_page_header, add_footer
from utils.helpers import create_download_button

# Import from project directory
try:
    import sys
    project_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '02-customer-health-score')
    if project_path not in sys.path:
        sys.path.insert(0, project_path)

    from health_score import HealthScoreCalculator
    from data_generator import generate_sample_data
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Customer Health Score Calculator",
    page_icon="📊",
    layout="wide"
)

apply_custom_css()

# Main header
add_page_header(
    "Customer Health Score Calculator",
    "Predict customer churn risk using usage metrics and engagement data",
    "📊"
)

# Sidebar
with st.sidebar:
    st.markdown("### About This Tool")
    st.markdown("""
    Predict customer churn using a sophisticated health scoring system.

    **Key Metrics:**
    - Login Frequency
    - Feature Usage
    - Support Tickets
    - Last Login Date
    - Contract Value

    **Risk Categories:**
    - 🟢 Healthy (70-100)
    - 🟡 At Risk (40-69)
    - 🔴 High Risk (0-39)
    """)

    st.markdown("---")
    st.markdown("### Data Source")

    # Data source selection
    data_source = st.radio(
        "Select Data Source",
        ["Use Sample Data", "Upload CSV"],
        label_visibility="collapsed"
    )

# Load data
@st.cache_data
def load_sample_data():
    return generate_sample_data(num_customers=100)

if data_source == "Use Sample Data":
    df = load_sample_data()
    st.info("📊 Displaying 100 sample customers. Upload your own CSV to analyze real data.")
else:
    uploaded_file = st.sidebar.file_uploader("Upload customer data CSV", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} customers from uploaded file")
    else:
        st.warning("⚠️ Please upload a CSV file or use sample data")
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

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(df))

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
    st.metric("Avg Health Score", f"{avg_score:.1f}")

with col4:
    avg_churn = df['churn_risk'].mean()
    st.metric("Avg Churn Risk", f"{avg_churn:.1%}")

st.markdown("---")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "👥 Customer List",
    "🔍 Individual Analysis",
    "📊 Analytics"
])

with tab1:
    st.markdown("### Health Score Distribution")

    # Health score histogram
    fig_hist = px.histogram(
        df,
        x='health_score',
        nbins=30,
        color='risk_category',
        color_discrete_map={
            'Healthy': '#28a745',
            'At Risk': '#ffc107',
            'High Risk': '#dc3545'
        },
        title="Customer Health Score Distribution",
        labels={'health_score': 'Health Score', 'count': 'Number of Customers'}
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        # Risk category pie chart
        risk_counts = df['risk_category'].value_counts()
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Customers by Risk Category",
            color=risk_counts.index,
            color_discrete_map={
                'Healthy': '#28a745',
                'At Risk': '#ffc107',
                'High Risk': '#dc3545'
            },
            hole=0.4
        )
        fig_pie.update_layout(height=400)
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
                'Healthy': '#28a745',
                'At Risk': '#ffc107',
                'High Risk': '#dc3545'
            },
            labels={'contract_value': 'Contract Value ($)', 'health_score': 'Health Score'}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Key insights
    st.markdown("### 📊 Key Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        healthy_pct = (risk_counts.get('Healthy', 0) / len(df) * 100)
        st.metric("Healthy Customers", f"{healthy_pct:.1f}%")

    with col2:
        at_risk_revenue = df[df['risk_category'] != 'Healthy']['contract_value'].sum()
        st.metric("At-Risk Revenue", f"${at_risk_revenue:,.0f}")

    with col3:
        high_risk_high_value = len(df[(df['risk_category'] == 'High Risk') & (df['contract_value'] > 50000)])
        st.metric("High-Risk High-Value", high_risk_high_value)

with tab2:
    st.markdown("### Customer Health Scores")

    # Filter controls
    col1, col2 = st.columns([3, 1])

    with col1:
        filter_risk = st.multiselect(
            "Filter by Risk Category",
            options=['Healthy', 'At Risk', 'High Risk'],
            default=['Healthy', 'At Risk', 'High Risk']
        )

    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=['health_score', 'churn_risk', 'contract_value'],
            format_func=lambda x: {'health_score': 'Health Score', 'churn_risk': 'Churn Risk', 'contract_value': 'Contract Value'}[x]
        )

    filtered_df = df[df['risk_category'].isin(filter_risk)].copy()
    filtered_df = filtered_df.sort_values(sort_by, ascending=(sort_by != 'health_score'))

    # Display table with styling
    st.dataframe(
        filtered_df[[
            'customer_id', 'health_score', 'churn_risk', 'risk_category',
            'login_frequency', 'feature_usage', 'support_tickets',
            'days_since_last_login', 'contract_value'
        ]].style.background_gradient(subset=['health_score'], cmap='RdYlGn'),
        use_container_width=True,
        height=400
    )

    # Download options
    st.markdown("### 📥 Export Data")
    col1, col2 = st.columns(2)

    with col1:
        create_download_button(
            filtered_df,
            filename='customer_health_scores.csv',
            label="Download Filtered Data (CSV)",
            file_type='csv'
        )

    with col2:
        create_download_button(
            filtered_df,
            filename='customer_health_scores.json',
            label="Download Filtered Data (JSON)",
            file_type='json'
        )

with tab3:
    st.markdown("### Individual Customer Analysis")

    # Customer selector
    col1, col2 = st.columns([3, 1])

    with col1:
        customer_id = st.selectbox(
            "Select Customer ID",
            options=df['customer_id'].tolist(),
            format_func=lambda x: f"{x} ({df[df['customer_id']==x].iloc[0]['risk_category']})"
        )

    with col2:
        # Quick filter buttons
        if st.button("🔴 Show High Risk", use_container_width=True):
            high_risk_customers = df[df['risk_category'] == 'High Risk']['customer_id'].tolist()
            if high_risk_customers:
                customer_id = high_risk_customers[0]

    customer = df[df['customer_id'] == customer_id].iloc[0]

    # Customer overview
    st.markdown(f"#### Customer: `{customer_id}`")

    # Three column metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Health Score", f"{customer['health_score']:.1f}")
        risk_emoji = {'Healthy': '🟢', 'At Risk': '🟡', 'High Risk': '🔴'}
        st.metric("Risk Category", f"{risk_emoji[customer['risk_category']]} {customer['risk_category']}")

    with col2:
        st.metric("Churn Probability", f"{customer['churn_risk']:.1%}")
        st.metric("Contract Value", f"${customer['contract_value']:,.0f}")

    with col3:
        st.metric("Login Frequency", f"{customer['login_frequency']}/month")
        st.metric("Support Tickets", int(customer['support_tickets']))
        st.metric("Days Since Login", int(customer['days_since_last_login']))

    st.markdown("---")

    # Two columns for gauge and details
    col1, col2 = st.columns([1, 1])

    with col1:
        # Gauge chart for health score
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=customer['health_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Health Score", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'steps': [
                    {'range': [0, 40], 'color': '#ffcccc'},
                    {'range': [40, 70], 'color': '#fff4cc'},
                    {'range': [70, 100], 'color': '#ccffcc'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 40
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Feature breakdown
        st.markdown("#### Metric Breakdown")
        metrics_df = pd.DataFrame({
            'Metric': ['Login Frequency', 'Feature Usage', 'Support Tickets', 'Days Since Login', 'Contract Value'],
            'Score': [
                calculator.normalize_score(customer['login_frequency'], 0, 30, False),
                calculator.normalize_score(customer['feature_usage'], 0, 100, False),
                calculator.normalize_score(customer['support_tickets'], 0, 20, True),
                calculator.normalize_score(customer['days_since_last_login'], 0, 90, True),
                calculator.normalize_score(customer['contract_value'], 0, 100000, False)
            ]
        })

        fig_bar = px.bar(
            metrics_df,
            x='Score',
            y='Metric',
            orientation='h',
            title="Individual Metric Scores",
            color='Score',
            color_continuous_scale='RdYlGn',
            range_color=[0, 100]
        )
        fig_bar.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Recommendations
    st.markdown("### 💡 Recommendations")
    recommendations = calculator.get_recommendations(
        health_score=customer['health_score'],
        login_frequency=customer['login_frequency'],
        support_tickets=customer['support_tickets'],
        days_since_last_login=customer['days_since_last_login']
    )

    for i, rec in enumerate(recommendations, 1):
        if '🚨' in rec:
            st.error(rec)
        elif '✅' in rec or '✓' in rec:
            st.success(rec)
        else:
            st.info(rec)

with tab4:
    st.markdown("### 📊 Advanced Analytics")

    # Feature importance
    st.markdown("#### Feature Importance in Health Score")

    feature_importance = pd.DataFrame({
        'Feature': ['Login Frequency', 'Feature Usage', 'Support Tickets', 'Days Since Last Login', 'Contract Value'],
        'Weight': [0.30, 0.25, 0.20, 0.15, 0.10],
        'Description': [
            'Monthly login activity',
            'Number of features actively used',
            'Support ticket volume (inverted)',
            'Recency of engagement (inverted)',
            'Account value indicator'
        ]
    })

    fig_importance = px.bar(
        feature_importance,
        x='Weight',
        y='Feature',
        orientation='h',
        title="Feature Weights in Health Score Calculation",
        color='Weight',
        color_continuous_scale='Blues',
        hover_data=['Description']
    )
    fig_importance.update_layout(height=400)
    st.plotly_chart(fig_importance, use_container_width=True)

    st.markdown("---")

    # Correlation analysis
    st.markdown("#### Metric Correlations")

    correlation_data = df[['health_score', 'login_frequency', 'feature_usage', 'support_tickets', 'days_since_last_login', 'contract_value']].corr()

    fig_heatmap = px.imshow(
        correlation_data,
        labels=dict(color="Correlation"),
        x=correlation_data.columns,
        y=correlation_data.columns,
        color_continuous_scale='RdBu_r',
        title="Correlation Matrix of Customer Metrics",
        zmin=-1, zmax=1
    )
    fig_heatmap.update_layout(height=500)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Distribution by risk
    st.markdown("#### Metric Distributions by Risk Category")

    metric_to_plot = st.selectbox(
        "Select metric to analyze",
        options=['login_frequency', 'feature_usage', 'support_tickets', 'contract_value'],
        format_func=lambda x: x.replace('_', ' ').title()
    )

    fig_box = px.box(
        df,
        x='risk_category',
        y=metric_to_plot,
        color='risk_category',
        color_discrete_map={
            'Healthy': '#28a745',
            'At Risk': '#ffc107',
            'High Risk': '#dc3545'
        },
        title=f"{metric_to_plot.replace('_', ' ').title()} Distribution by Risk Category",
        labels={metric_to_plot: metric_to_plot.replace('_', ' ').title(), 'risk_category': 'Risk Category'}
    )
    fig_box.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")

# Actionable insights
with st.expander("💡 Business Insights & Action Items"):
    high_risk_count = len(df[df['risk_category'] == 'High Risk'])
    at_risk_count = len(df[df['risk_category'] == 'At Risk'])
    high_value_at_risk = df[(df['risk_category'] != 'Healthy') & (df['contract_value'] > 50000)]

    st.markdown(f"""
    ### Current Status

    - **High Risk Customers**: {high_risk_count} customers require immediate attention
    - **At Risk Customers**: {at_risk_count} customers need proactive engagement
    - **High-Value At-Risk**: {len(high_value_at_risk)} customers with contracts > $50K

    ### Recommended Actions

    1. **Immediate (This Week)**
       - Schedule calls with all {high_risk_count} high-risk customers
       - Review support tickets for common issues
       - Send personalized re-engagement campaigns

    2. **Short-term (This Month)**
       - Create onboarding improvements for low-engagement segments
       - Develop feature adoption campaigns
       - Implement early warning system for declining metrics

    3. **Long-term (This Quarter)**
       - Build customer success playbooks by segment
       - Create automated health score monitoring
       - Develop upsell strategies for healthy customers
    """)

add_footer()
