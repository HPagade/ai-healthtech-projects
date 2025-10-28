"""
Healthcare Startup Funding Analysis
Interactive dashboard analyzing AI healthtech funding trends
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_css, add_page_header, add_footer
from utils.helpers import format_currency, create_download_button

st.set_page_config(page_title="Funding Analysis", page_icon="💰", layout="wide")
apply_custom_css()

add_page_header("Healthcare Startup Funding Analysis", "Analyze AI healthtech funding trends and patterns", "💰")

# Generate sample funding data
@st.cache_data
def generate_funding_data(n_rounds=300):
    np.random.seed(42)

    categories = ['Digital Health', 'Clinical AI', 'Medical Devices', 'Telemedicine',
                  'Health Insurance Tech', 'Diagnostics', 'Mental Health', 'Biotech']

    stages = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D+']

    # Generate data over past 5 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)

    data = []
    for i in range(n_rounds):
        stage = np.random.choice(stages)

        # Funding amounts by stage (in millions)
        stage_amounts = {
            'Seed': (0.5, 5),
            'Series A': (5, 20),
            'Series B': (15, 50),
            'Series C': (30, 100),
            'Series D+': (50, 300)
        }

        min_amt, max_amt = stage_amounts[stage]
        amount = np.random.uniform(min_amt, max_amt) * 1_000_000

        # Random date
        days_ago = np.random.randint(0, 1825)  # 5 years
        funding_date = end_date - timedelta(days=days_ago)

        data.append({
            'company_name': f'Company {i+1}',
            'category': np.random.choice(categories),
            'funding_stage': stage,
            'funding_amount': amount,
            'funding_date': funding_date,
            'year': funding_date.year,
            'quarter': f"Q{(funding_date.month-1)//3 + 1} {funding_date.year}",
            'investors': np.random.randint(1, 8),
            'location': np.random.choice(['San Francisco', 'New York', 'Boston', 'London', 'Singapore']),
            'yc_backed': np.random.choice([True, False], p=[0.15, 0.85])
        })

    return pd.DataFrame(data).sort_values('funding_date', ascending=False)

df = generate_funding_data()

# Sidebar - Filters
with st.sidebar:
    st.markdown("### Filters")

    # Year range
    years = sorted(df['year'].unique())
    year_range = st.slider("Year Range", min(years), max(years), (min(years), max(years)))

    # Categories
    categories = st.multiselect(
        "Categories",
        options=sorted(df['category'].unique()),
        default=sorted(df['category'].unique())
    )

    # Funding stage
    stages = st.multiselect(
        "Funding Stages",
        options=['Seed', 'Series A', 'Series B', 'Series C', 'Series D+'],
        default=['Seed', 'Series A', 'Series B', 'Series C', 'Series D+']
    )

    # Apply filters
    filtered_df = df[
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1]) &
        (df['category'].isin(categories)) &
        (df['funding_stage'].isin(stages))
    ]

    st.markdown("---")
    st.markdown(f"**{len(filtered_df)}** deals match filters")

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_funding = filtered_df['funding_amount'].sum()
    st.metric("Total Funding", format_currency(total_funding))

with col2:
    avg_deal = filtered_df['funding_amount'].mean()
    st.metric("Avg Deal Size", format_currency(avg_deal))

with col3:
    st.metric("Total Deals", len(filtered_df))

with col4:
    yoy_growth = ((filtered_df[filtered_df['year'] == year_range[1]]['funding_amount'].sum() /
                   filtered_df[filtered_df['year'] == year_range[0]]['funding_amount'].sum() - 1) * 100
                  if filtered_df[filtered_df['year'] == year_range[0]]['funding_amount'].sum() > 0 else 0)
    st.metric("YoY Growth", f"{yoy_growth:.1f}%")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏷️ Categories", "🎯 Stages", "📍 Geography"])

with tab1:
    st.markdown("### Funding Trends Over Time")

    # Yearly funding
    yearly_funding = filtered_df.groupby('year').agg({
        'funding_amount': 'sum',
        'company_name': 'count'
    }).reset_index()
    yearly_funding.columns = ['Year', 'Total Funding', 'Number of Deals']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly_funding['Year'],
        y=yearly_funding['Total Funding'],
        name='Total Funding',
        yaxis='y',
        marker_color='lightblue'
    ))
    fig.add_trace(go.Scatter(
        x=yearly_funding['Year'],
        y=yearly_funding['Number of Deals'],
        name='Number of Deals',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(size=10, color='red'),
        line=dict(width=3)
    ))

    fig.update_layout(
        title='Annual Funding Volume and Deal Count',
        yaxis=dict(title='Total Funding ($)', side='left'),
        yaxis2=dict(title='Number of Deals', overlaying='y', side='right'),
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Quarterly trends
    st.markdown("### Quarterly Trends")
    quarterly = filtered_df.groupby('quarter')['funding_amount'].sum().reset_index()
    quarterly = quarterly.sort_values('quarter')

    fig = px.line(quarterly, x='quarter', y='funding_amount',
                  labels={'quarter': 'Quarter', 'funding_amount': 'Total Funding ($)'},
                  markers=True)
    fig.update_layout(height=300, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Funding by Category")

    col1, col2 = st.columns(2)

    with col1:
        # Total funding by category
        category_funding = filtered_df.groupby('category')['funding_amount'].sum().sort_values(ascending=False)

        fig = px.bar(
            x=category_funding.values,
            y=category_funding.index,
            orientation='h',
            labels={'x': 'Total Funding ($)', 'y': 'Category'},
            color=category_funding.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(title="Total Funding by Category", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Deal count by category
        category_deals = filtered_df.groupby('category').size().sort_values(ascending=False)

        fig = px.pie(
            values=category_deals.values,
            names=category_deals.index,
            title="Deal Distribution by Category",
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Category trends over time
    st.markdown("### Category Trends Over Time")
    category_yearly = filtered_df.groupby(['year', 'category'])['funding_amount'].sum().reset_index()

    fig = px.line(
        category_yearly,
        x='year',
        y='funding_amount',
        color='category',
        labels={'year': 'Year', 'funding_amount': 'Funding Amount ($)', 'category': 'Category'},
        markers=True
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Analysis by Funding Stage")

    col1, col2 = st.columns(2)

    with col1:
        # Funding by stage
        stage_funding = filtered_df.groupby('funding_stage')['funding_amount'].sum()
        stage_order = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D+']
        stage_funding = stage_funding.reindex([s for s in stage_order if s in stage_funding.index])

        fig = px.bar(
            x=stage_funding.index,
            y=stage_funding.values,
            labels={'x': 'Funding Stage', 'y': 'Total Funding ($)'},
            color=stage_funding.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(title="Total Funding by Stage", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Average deal size by stage
        stage_avg = filtered_df.groupby('funding_stage')['funding_amount'].mean()
        stage_avg = stage_avg.reindex([s for s in stage_order if s in stage_avg.index])

        fig = px.bar(
            x=stage_avg.index,
            y=stage_avg.values,
            labels={'x': 'Funding Stage', 'y': 'Average Deal Size ($)'},
            color=stage_avg.values,
            color_continuous_scale='Oranges'
        )
        fig.update_layout(title="Average Deal Size by Stage", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Deal count by stage
    st.markdown("### Deal Distribution")
    stage_counts = filtered_df['funding_stage'].value_counts()
    stage_counts = stage_counts.reindex([s for s in stage_order if s in stage_counts.index])

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, (stage, count) in enumerate(stage_counts.items()):
        with cols[i]:
            pct = (count / len(filtered_df)) * 100
            st.metric(stage, f"{count} deals", f"{pct:.1f}%")

with tab4:
    st.markdown("### Geographic Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Funding by location
        location_funding = filtered_df.groupby('location')['funding_amount'].sum().sort_values(ascending=False)

        fig = px.bar(
            x=location_funding.values,
            y=location_funding.index,
            orientation='h',
            labels={'x': 'Total Funding ($)', 'y': 'Location'},
            color=location_funding.values,
            color_continuous_scale='Purples'
        )
        fig.update_layout(title="Funding by Location", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Deal count by location
        location_deals = filtered_df.groupby('location').size().sort_values(ascending=False)

        fig = px.pie(
            values=location_deals.values,
            names=location_deals.index,
            title="Deal Distribution by Location",
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Top deals
    st.markdown("### Largest Deals")
    top_deals = filtered_df.nlargest(10, 'funding_amount')[
        ['company_name', 'category', 'funding_stage', 'funding_amount', 'funding_date', 'location']
    ].copy()
    top_deals['funding_amount'] = top_deals['funding_amount'].apply(lambda x: format_currency(x))
    top_deals['funding_date'] = top_deals['funding_date'].dt.strftime('%Y-%m-%d')

    st.dataframe(top_deals, use_container_width=True, height=400)

# Insights
st.markdown("---")
with st.expander("📊 Key Insights & Market Trends"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Market Observations

        - **Growth Trend:** Healthcare tech funding has shown strong growth over the past 5 years
        - **Hot Categories:** Digital Health and Clinical AI attract the most capital
        - **Deal Sizes:** Average deal sizes are increasing across all stages
        - **Geographic Concentration:** San Francisco and New York dominate funding activity

        ### Investment Patterns

        - Seed rounds: $0.5M - $5M range
        - Series A: $5M - $20M typical
        - Series B+: Significant jump in deal sizes
        - Late-stage mega-rounds ($100M+) becoming more common
        """)

    with col2:
        st.markdown("""
        ### For Founders

        **Fundraising Strategy:**
        - Target appropriate stage investors
        - Highlight differentiation in crowded categories
        - Consider geographic advantages
        - Build strategic investor relationships

        **Market Timing:**
        - Monitor category trends
        - Understand investor appetite by stage
        - Track competitive funding rounds
        - Plan 12-18 months runway

        ### For Investors

        **Opportunities:**
        - Emerging categories showing growth
        - Geographic expansion beyond SF/NY
        - Earlier stage opportunities (Seed/A)
        - Platform plays across healthcare verticals
        """)

# Download
st.markdown("---")
st.markdown("### 📥 Export Data")
create_download_button(filtered_df, 'funding_analysis.csv', '📄 Download Funding Data', 'csv')

add_footer()
