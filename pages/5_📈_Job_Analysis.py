"""
Startup Job Market Analysis
Analyze job postings to identify hiring trends, skills demand, and salary ranges
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_css, add_page_header, add_footer
from utils.helpers import format_currency, create_download_button

st.set_page_config(page_title="Job Market Analysis", page_icon="📈", layout="wide")
apply_custom_css()

add_page_header("Startup Job Market Analysis", "Analyze hiring trends in AI and healthtech startups", "📈")

# Generate sample data
@st.cache_data
def generate_job_data(n_jobs=200):
    np.random.seed(42)

    roles = ['Product Manager', 'Software Engineer', 'Data Scientist', 'ML Engineer',
             'Backend Engineer', 'Frontend Engineer', 'Designer', 'Sales',
             'Marketing Manager', 'Customer Success']

    locations = ['San Francisco', 'New York', 'Remote', 'Boston', 'Seattle',
                 'Austin', 'Los Angeles', 'Chicago']

    experience_levels = ['Entry Level', 'Mid Level', 'Senior', 'Lead/Staff']

    skills = ['Python', 'JavaScript', 'React', 'SQL', 'Machine Learning',
              'AWS', 'Docker', 'Kubernetes', 'TensorFlow', 'PyTorch',
              'Product Management', 'Agile', 'Healthcare', 'HIPAA', 'FHIR']

    data = []
    for i in range(n_jobs):
        role = np.random.choice(roles)

        # Salary based on role and experience
        base_salaries = {
            'Software Engineer': 120000, 'Product Manager': 140000, 'Data Scientist': 130000,
            'ML Engineer': 145000, 'Backend Engineer': 115000, 'Frontend Engineer': 110000,
            'Designer': 100000, 'Sales': 90000, 'Marketing Manager': 105000,
            'Customer Success': 85000
        }

        experience = np.random.choice(experience_levels)
        exp_multiplier = {'Entry Level': 0.7, 'Mid Level': 1.0, 'Senior': 1.3, 'Lead/Staff': 1.6}

        base = base_salaries.get(role, 100000)
        salary = int(base * exp_multiplier[experience] * np.random.uniform(0.9, 1.1))

        # Random skills
        num_skills = np.random.randint(3, 8)
        job_skills = np.random.choice(skills, size=num_skills, replace=False).tolist()

        data.append({
            'job_id': f'JOB-{i+1:04d}',
            'title': role,
            'company': f'Company {np.random.randint(1, 50)}',
            'location': np.random.choice(locations),
            'experience_level': experience,
            'salary_min': int(salary * 0.9),
            'salary_max': int(salary * 1.1),
            'salary_avg': salary,
            'skills': ', '.join(job_skills),
            'remote_friendly': np.random.choice([True, False], p=[0.4, 0.6]),
            'healthcare_focus': 'Healthcare' in job_skills or 'HIPAA' in job_skills or 'FHIR' in job_skills,
            'ai_focus': any(s in job_skills for s in ['Machine Learning', 'TensorFlow', 'PyTorch'])
        })

    return pd.DataFrame(data)

df = generate_job_data()

# Sidebar
with st.sidebar:
    st.markdown("### Filters")

    # Role filter
    roles = ['All'] + sorted(df['title'].unique().tolist())
    selected_role = st.selectbox("Job Role", roles)

    # Location filter
    locations = ['All'] + sorted(df['location'].unique().tolist())
    selected_location = st.selectbox("Location", locations)

    # Experience level
    exp_levels = ['All'] + sorted(df['experience_level'].unique().tolist())
    selected_exp = st.selectbox("Experience Level", exp_levels)

    # Salary range
    min_salary = int(df['salary_avg'].min())
    max_salary = int(df['salary_avg'].max())
    salary_range = st.slider(
        "Salary Range ($K)",
        min_salary // 1000,
        max_salary // 1000,
        (min_salary // 1000, max_salary // 1000)
    )

    # Apply filters
    filtered_df = df.copy()
    if selected_role != 'All':
        filtered_df = filtered_df[filtered_df['title'] == selected_role]
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    if selected_exp != 'All':
        filtered_df = filtered_df[filtered_df['experience_level'] == selected_exp]

    filtered_df = filtered_df[
        (filtered_df['salary_avg'] >= salary_range[0] * 1000) &
        (filtered_df['salary_avg'] <= salary_range[1] * 1000)
    ]

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Jobs", len(filtered_df))
with col2:
    avg_salary = filtered_df['salary_avg'].mean()
    st.metric("Avg Salary", format_currency(avg_salary))
with col3:
    remote_pct = (filtered_df['remote_friendly'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("Remote Jobs", f"{remote_pct:.1f}%")
with col4:
    ai_pct = (filtered_df['ai_focus'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("AI-Focused", f"{ai_pct:.1f}%")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💰 Salary Analysis", "🔧 Skills Demand", "📍 Location & Remote"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top Hiring Roles")
        role_counts = filtered_df['title'].value_counts().head(10)
        fig = px.bar(x=role_counts.values, y=role_counts.index, orientation='h',
                     labels={'x': 'Number of Jobs', 'y': 'Role'},
                     color=role_counts.values, color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Experience Level Distribution")
        exp_counts = filtered_df['experience_level'].value_counts()
        fig = px.pie(values=exp_counts.values, names=exp_counts.index, hole=0.4)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Recent Job Postings")
    display_df = filtered_df[['title', 'company', 'location', 'experience_level', 'salary_avg']].head(20)
    display_df['salary_avg'] = display_df['salary_avg'].apply(lambda x: format_currency(x))
    st.dataframe(display_df, use_container_width=True, height=400)

with tab2:
    st.markdown("### Salary Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Salary by role
        salary_by_role = filtered_df.groupby('title')['salary_avg'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(x=salary_by_role.values, y=salary_by_role.index, orientation='h',
                     labels={'x': 'Average Salary ($)', 'y': 'Role'},
                     color=salary_by_role.values, color_continuous_scale='Greens')
        fig.update_layout(title="Average Salary by Role", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Salary by experience
        salary_by_exp = filtered_df.groupby('experience_level')['salary_avg'].mean()
        order = ['Entry Level', 'Mid Level', 'Senior', 'Lead/Staff']
        salary_by_exp = salary_by_exp.reindex([x for x in order if x in salary_by_exp.index])

        fig = px.bar(x=salary_by_exp.index, y=salary_by_exp.values,
                     labels={'x': 'Experience Level', 'y': 'Average Salary ($)'},
                     color=salary_by_exp.values, color_continuous_scale='Reds')
        fig.update_layout(title="Salary by Experience Level", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Salary distribution
    st.markdown("### Salary Distribution")
    fig = px.histogram(filtered_df, x='salary_avg', nbins=30,
                       labels={'salary_avg': 'Salary ($)', 'count': 'Number of Jobs'},
                       color_discrete_sequence=['#1f77b4'])
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Skills in Demand")

    # Extract and count skills
    all_skills = []
    for skills_str in filtered_df['skills'].dropna():
        all_skills.extend([s.strip() for s in skills_str.split(',')])

    skill_counts = Counter(all_skills)
    top_skills = dict(skill_counts.most_common(15))

    if top_skills:
        skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Count'])

        fig = px.bar(skills_df, x='Count', y='Skill', orientation='h',
                     labels={'Count': 'Number of Job Postings', 'Skill': 'Skill'},
                     color='Count', color_continuous_scale='Oranges')
        fig.update_layout(title="Top 15 Most Demanded Skills", showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Skill combinations
        st.markdown("### Common Skill Combinations")
        col1, col2, col3 = st.columns(3)
        skills_list = list(top_skills.keys())

        with col1:
            if len(skills_list) > 0:
                st.metric("Most Common Skill", skills_list[0], f"{top_skills[skills_list[0]]} jobs")
        with col2:
            if len(skills_list) > 1:
                st.metric("2nd Most Common", skills_list[1], f"{top_skills[skills_list[1]]} jobs")
        with col3:
            if len(skills_list) > 2:
                st.metric("3rd Most Common", skills_list[2], f"{top_skills[skills_list[2]]} jobs")

with tab4:
    st.markdown("### Location Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Jobs by location
        location_counts = filtered_df['location'].value_counts().head(10)
        fig = px.bar(x=location_counts.values, y=location_counts.index, orientation='h',
                     labels={'x': 'Number of Jobs', 'y': 'Location'},
                     color=location_counts.values, color_continuous_scale='Purples')
        fig.update_layout(title="Top Locations", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Remote vs On-site
        remote_data = filtered_df['remote_friendly'].value_counts()
        fig = px.pie(values=remote_data.values,
                     names=['Remote-Friendly' if x else 'On-Site' for x in remote_data.index],
                     title="Remote Work Distribution", hole=0.4)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Salary by location
    st.markdown("### Average Salary by Location")
    salary_by_location = filtered_df.groupby('location')['salary_avg'].mean().sort_values(ascending=False)
    fig = px.bar(x=salary_by_location.index, y=salary_by_location.values,
                 labels={'x': 'Location', 'y': 'Average Salary ($)'},
                 color=salary_by_location.values, color_continuous_scale='Viridis')
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

# Download section
st.markdown("---")
st.markdown("### 📥 Export Data")
col1, col2 = st.columns(2)
with col1:
    create_download_button(filtered_df, 'job_market_data.csv', '📄 Download Filtered Data (CSV)', 'csv')
with col2:
    create_download_button(filtered_df, 'job_market_data.json', '📄 Download Filtered Data (JSON)', 'json')

add_footer()
