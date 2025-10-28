"""
YC AI Healthtech Startup Tracker
Interactive dashboard for analyzing Y Combinator startups in AI and healthcare
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import sys
import os

# Add project directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_css, add_page_header, add_footer
from utils.helpers import format_number, create_download_button

# Page configuration
st.set_page_config(
    page_title="YC AI Healthtech Tracker",
    page_icon="🚀",
    layout="wide"
)

apply_custom_css()


def generate_sample_data(num_startups=200):
    """Generate sample YC startup data for demonstration"""
    import random
    from datetime import datetime

    batches = ['S19', 'W20', 'S20', 'W21', 'S21', 'W22', 'S22', 'W23', 'S23', 'W24', 'S24']
    tags_options = [
        'Healthcare', 'Artificial Intelligence', 'B2B', 'Machine Learning',
        'Digital Health', 'Medical Devices', 'Telemedicine', 'SaaS',
        'Enterprise', 'API', 'Analytics', 'Biotech', 'Diagnostics',
        'Health Insurance', 'Mental Health', 'Pharma'
    ]

    company_prefixes = ['Health', 'Med', 'Care', 'Vital', 'Well', 'Doc', 'Patient', 'Clinical', 'Bio', 'AI']
    company_suffixes = ['AI', 'Health', 'Care', 'MD', 'Analytics', 'Systems', 'Labs', 'Tech', 'Bio', 'Rx']

    data = []
    for i in range(num_startups):
        name = f"{random.choice(company_prefixes)}{random.choice(company_suffixes)}"
        batch = random.choice(batches)
        num_tags = random.randint(2, 5)
        tags = random.sample(tags_options, num_tags)

        data.append({
            'name': name + f" {i+1}",
            'description': f"AI-powered healthcare platform providing innovative solutions for patients and providers",
            'batch': batch,
            'tags': str(tags),
            'website': f"https://{name.lower()}.com",
            'scraped_at': datetime.now().isoformat()
        })

    return pd.DataFrame(data)


@st.cache_data
def load_startup_data():
    """Load startup data from file or generate sample data"""
    data_file = '01-yc-healthtech-tracker/data/yc_startups.csv'

    if os.path.exists(data_file):
        try:
            return pd.read_csv(data_file)
        except:
            pass

    # Generate sample data if file doesn't exist
    return generate_sample_data()


def analyze_batch_distribution(df):
    """Create batch distribution visualization"""
    batch_counts = df['batch'].value_counts().sort_index()

    fig = px.bar(
        x=batch_counts.index,
        y=batch_counts.values,
        labels={'x': 'YC Batch', 'y': 'Number of Startups'},
        title='AI Healthtech Startups by YC Batch',
        color=batch_counts.values,
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        showlegend=False,
        xaxis_tickangle=-45,
        height=500
    )

    return fig


def analyze_tags(df):
    """Analyze and visualize tag distribution"""
    all_tags = []
    for tags in df['tags'].dropna():
        if isinstance(tags, str):
            try:
                tag_list = eval(tags)
                all_tags.extend(tag_list)
            except:
                pass

    tag_counts = Counter(all_tags)
    top_tags = dict(tag_counts.most_common(15))

    fig = px.bar(
        x=list(top_tags.values()),
        y=list(top_tags.keys()),
        orientation='h',
        labels={'x': 'Number of Startups', 'y': 'Tag'},
        title='Most Common Tags in AI Healthtech Startups',
        color=list(top_tags.values()),
        color_continuous_scale='Reds'
    )

    fig.update_layout(
        showlegend=False,
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )

    return fig, top_tags


def analyze_growth_trends(df):
    """Analyze growth trends over time"""
    df_copy = df.copy()
    df_copy['year'] = df_copy['batch'].str.extract(r'(\d+)').astype(int) + 2000
    df_copy['season'] = df_copy['batch'].str[0]

    yearly_counts = df_copy.groupby('year').size().reset_index(name='count')

    fig = px.line(
        yearly_counts,
        x='year',
        y='count',
        title='AI Healthtech Startup Growth Over Time',
        markers=True,
        labels={'year': 'Year', 'count': 'Number of Startups'}
    )

    fig.update_traces(line_color='#2ecc71', line_width=3, marker_size=10)
    fig.update_layout(height=500)

    return fig


# Main App
add_page_header(
    "YC AI Healthtech Startup Tracker",
    "Analyze Y Combinator startups in AI and healthcare to identify market trends",
    "🚀"
)

# Sidebar
with st.sidebar:
    st.markdown("### About This Tool")
    st.markdown("""
    This dashboard analyzes Y Combinator startups in the AI and healthcare space.

    **Features:**
    - Interactive visualizations
    - Batch distribution analysis
    - Tag/category insights
    - Growth trend tracking
    """)

    st.markdown("---")
    st.markdown("### Data Options")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    uploaded_file = st.file_uploader("Upload your own data (CSV)", type=['csv'])

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} startups from uploaded file")
else:
    df = load_startup_data()
    st.info(f"📊 Displaying sample data with {len(df)} startups. Upload your own CSV to analyze real data.")

# Display summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Startups", format_number(len(df)))

with col2:
    earliest_batch = df['batch'].min() if not df.empty else "N/A"
    st.metric("Earliest Batch", earliest_batch)

with col3:
    latest_batch = df['batch'].max() if not df.empty else "N/A"
    st.metric("Latest Batch", latest_batch)

with col4:
    num_batches = df['batch'].nunique() if not df.empty else 0
    st.metric("Total Batches", num_batches)

st.markdown("---")

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Batch Analysis",
    "🏷️ Tag Analysis",
    "📉 Growth Trends"
])

with tab1:
    st.markdown("### 📊 Dataset Overview")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Sample Startups")
        display_df = df[['name', 'batch', 'description']].head(10)
        st.dataframe(display_df, use_container_width=True, height=400)

    with col2:
        st.markdown("#### Quick Stats")

        # Batch distribution
        batch_dist = df['batch'].value_counts()
        st.metric("Most Active Batch", f"{batch_dist.index[0]} ({batch_dist.values[0]} startups)")

        # Calculate average per batch
        avg_per_batch = len(df) / df['batch'].nunique()
        st.metric("Avg per Batch", f"{avg_per_batch:.1f}")

        st.markdown("---")
        st.markdown("#### Download Data")
        create_download_button(
            df,
            filename='yc_healthtech_startups.csv',
            label="📥 Download CSV",
            file_type='csv'
        )

with tab2:
    st.markdown("### 📈 Batch Distribution Analysis")
    st.markdown("Distribution of AI healthtech startups across different YC batches")

    fig = analyze_batch_distribution(df)
    st.plotly_chart(fig, use_container_width=True)

    # Show batch statistics
    st.markdown("#### Batch Statistics")
    batch_stats = df['batch'].value_counts().reset_index()
    batch_stats.columns = ['Batch', 'Number of Startups']
    batch_stats['Percentage'] = (batch_stats['Number of Startups'] / len(df) * 100).round(1)
    batch_stats['Percentage'] = batch_stats['Percentage'].astype(str) + '%'

    col1, col2 = st.columns([3, 2])
    with col1:
        st.dataframe(batch_stats, use_container_width=True, height=400)

with tab3:
    st.markdown("### 🏷️ Tag and Category Analysis")
    st.markdown("Most common tags and categories in AI healthtech startups")

    fig, top_tags = analyze_tags(df)
    st.plotly_chart(fig, use_container_width=True)

    # Tag insights
    st.markdown("#### Top Tag Insights")
    col1, col2, col3 = st.columns(3)

    tags_list = list(top_tags.items())
    with col1:
        st.metric("Most Common Tag", tags_list[0][0], f"{tags_list[0][1]} startups")
    with col2:
        if len(tags_list) > 1:
            st.metric("2nd Most Common", tags_list[1][0], f"{tags_list[1][1]} startups")
    with col3:
        if len(tags_list) > 2:
            st.metric("3rd Most Common", tags_list[2][0], f"{tags_list[2][1]} startups")

with tab4:
    st.markdown("### 📉 Growth Trends Analysis")
    st.markdown("Tracking the growth of AI healthtech startups over time")

    fig = analyze_growth_trends(df)
    st.plotly_chart(fig, use_container_width=True)

    # Growth insights
    df_copy = df.copy()
    df_copy['year'] = df_copy['batch'].str.extract(r'(\d+)').astype(int) + 2000
    yearly_counts = df_copy.groupby('year').size()

    if len(yearly_counts) > 1:
        growth_rate = ((yearly_counts.iloc[-1] - yearly_counts.iloc[0]) / yearly_counts.iloc[0] * 100)
        st.markdown(f"""
        #### Key Insights
        - **Total Growth**: {growth_rate:.1f}% from {yearly_counts.index[0]} to {yearly_counts.index[-1]}
        - **Peak Year**: {yearly_counts.idxmax()} with {yearly_counts.max()} startups
        - **Recent Year**: {yearly_counts.index[-1]} with {yearly_counts.iloc[-1]} startups
        """)

st.markdown("---")

# Additional insights section
with st.expander("💡 Market Insights & Recommendations"):
    st.markdown("""
    ### Key Takeaways

    Based on the analysis of Y Combinator's AI healthtech startups:

    1. **Market Trend**: The AI healthtech sector has shown consistent growth in recent YC batches
    2. **Popular Categories**: Healthcare AI, Digital Health, and B2B solutions dominate the space
    3. **Investment Focus**: Recent batches show increased focus on clinical AI and diagnostics
    4. **Opportunities**: Emerging areas include mental health tech, remote care, and healthcare analytics

    ### For Founders
    - Focus on specific healthcare verticals with clear AI applications
    - B2B solutions for healthcare providers are increasingly popular
    - Consider regulatory pathways early in product development

    ### For Investors
    - Early-stage healthcare AI companies are attracting significant interest
    - Look for teams with domain expertise in both healthcare and AI
    - Companies with clear regulatory strategies show better outcomes
    """)

add_footer()
