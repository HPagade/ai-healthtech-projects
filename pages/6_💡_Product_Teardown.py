"""
AI Healthtech Product Teardown
Deep strategic analysis framework for leading AI healthtech products
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_css, add_page_header, add_footer

st.set_page_config(page_title="Product Teardown", page_icon="💡", layout="wide")
apply_custom_css()

add_page_header("AI Healthtech Product Teardown", "Strategic analysis framework for healthcare products", "💡")

# Sidebar - Product selector
with st.sidebar:
    st.markdown("### Featured Products")

    product_examples = [
        "Custom Analysis",
        "OpenAI Health (Example)",
        "Epic Systems MyChart",
        "Tempus AI",
        "Livongo/Teladoc",
        "K Health"
    ]

    selected_product = st.selectbox("Select Product to Analyze", product_examples)

    st.markdown("---")
    st.markdown("### Analysis Framework")
    st.markdown("""
    **Components:**
    - Problem & Market
    - Product Strategy
    - User Experience
    - Technology Stack
    - Business Model
    - Competitive Analysis
    - Future Opportunities
    """)

# Main interface
tab1, tab2, tab3 = st.tabs(["📝 Create Analysis", "📚 Templates", "🎯 Examples"])

with tab1:
    if selected_product == "Custom Analysis":
        st.markdown("### Create Your Product Teardown")

        with st.form("teardown_form"):
            st.markdown("#### 1️⃣ Product Overview")
            product_name = st.text_input("Product Name")
            company_name = st.text_input("Company Name")
            product_category = st.selectbox(
                "Category",
                ["Digital Health", "Clinical AI", "Medical Devices", "Telemedicine",
                 "Health Insurance Tech", "Healthcare Analytics", "Diagnostics", "Other"]
            )

            col1, col2 = st.columns(2)
            with col1:
                founding_year = st.number_input("Founding Year", min_value=2000, max_value=2024, value=2020)
            with col2:
                funding_stage = st.selectbox(
                    "Funding Stage",
                    ["Seed", "Series A", "Series B", "Series C+", "Public", "Unknown"]
                )

            st.markdown("#### 2️⃣ Problem & Market")
            problem_statement = st.text_area(
                "What problem does this solve?",
                placeholder="Describe the core problem this product addresses...",
                height=100
            )

            target_market = st.text_area(
                "Target Market & Users",
                placeholder="Who are the primary users? Market size? Geography?",
                height=100
            )

            st.markdown("#### 3️⃣ Product Analysis")
            key_features = st.text_area(
                "Key Features",
                placeholder="List the main features and capabilities...",
                height=100
            )

            value_proposition = st.text_area(
                "Value Proposition",
                placeholder="What unique value does this provide to users?",
                height=100
            )

            st.markdown("#### 4️⃣ Technology")
            tech_stack = st.multiselect(
                "Technology Stack (select all that apply)",
                ["AI/ML", "NLP", "Computer Vision", "Cloud (AWS/GCP/Azure)",
                 "Mobile Apps", "Web Platform", "API Integration", "Blockchain",
                 "IoT/Wearables", "FHIR/HL7", "Other"]
            )

            regulatory = st.multiselect(
                "Regulatory/Compliance",
                ["FDA Approved", "HIPAA Compliant", "CE Mark", "GDPR Compliant", "SOC 2", "None"]
            )

            st.markdown("#### 5️⃣ Business Model")
            revenue_model = st.multiselect(
                "Revenue Model",
                ["B2B SaaS Subscription", "B2C Subscription", "Per-Transaction", "Per-User",
                 "Marketplace", "Advertising", "Insurance Reimbursement", "One-time Purchase"]
            )

            st.markdown("#### 6️⃣ Competitive Analysis")
            competitors = st.text_area(
                "Main Competitors",
                placeholder="List key competitors and how they compare...",
                height=100
            )

            competitive_advantage = st.text_area(
                "Competitive Advantages",
                placeholder="What makes this product stand out?",
                height=100
            )

            st.markdown("#### 7️⃣ Assessment")
            col1, col2 = st.columns(2)
            with col1:
                strengths = st.text_area("Strengths", height=100)
            with col2:
                weaknesses = st.text_area("Weaknesses", height=100)

            col1, col2 = st.columns(2)
            with col1:
                opportunities = st.text_area("Opportunities", height=100)
            with col2:
                threats = st.text_area("Threats", height=100)

            # Submit
            submit = st.form_submit_button("📊 Generate Analysis Report", type="primary", use_container_width=True)

        if submit and product_name:
            st.markdown("---")
            st.markdown("## 📄 Product Teardown Report")

            # Generate formatted report
            report = f"""
# {product_name} - Product Teardown Analysis

**Company:** {company_name}
**Category:** {product_category}
**Founded:** {founding_year}
**Funding Stage:** {funding_stage}

---

## 1. Problem & Market Opportunity

**Problem Statement:**
{problem_statement}

**Target Market:**
{target_market}

---

## 2. Product Strategy

**Key Features:**
{key_features}

**Value Proposition:**
{value_proposition}

---

## 3. Technology & Innovation

**Technology Stack:**
{', '.join(tech_stack) if tech_stack else 'Not specified'}

**Regulatory/Compliance:**
{', '.join(regulatory) if regulatory else 'Not specified'}

---

## 4. Business Model

**Revenue Model:**
{', '.join(revenue_model) if revenue_model else 'Not specified'}

---

## 5. Competitive Landscape

**Main Competitors:**
{competitors}

**Competitive Advantages:**
{competitive_advantage}

---

## 6. SWOT Analysis

**Strengths:**
{strengths}

**Weaknesses:**
{weaknesses}

**Opportunities:**
{opportunities}

**Threats:**
{threats}

---

## 7. Overall Assessment

This product operates in the {product_category} space and appears to be at the {funding_stage} stage.
The company is addressing {problem_statement.split('.')[0] if problem_statement else 'a healthcare challenge'}.

---

*Analysis generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}*
"""

            st.markdown(report)

            # Download button
            st.download_button(
                "📥 Download Report (Markdown)",
                data=report,
                file_name=f"{product_name.replace(' ', '_')}_teardown.md",
                mime="text/markdown"
            )

    else:
        # Show example analysis
        st.info(f"Viewing example analysis for: **{selected_product}**")
        st.markdown("""
        ### OpenAI Health - Product Teardown Example

        **Company:** OpenAI
        **Category:** Healthcare AI / Clinical Decision Support
        **Status:** Research/Early Development

        ---

        #### Problem & Market
        Healthcare providers face information overload and need better tools to synthesize
        medical literature, patient data, and clinical guidelines to make informed decisions.

        #### Product Strategy
        - AI-powered medical information synthesis
        - Natural language interface for clinicians
        - Integration with EHR systems
        - Evidence-based recommendations

        #### Technology Stack
        - GPT-4 and specialized medical models
        - HIPAA-compliant infrastructure
        - FHIR API integration
        - Real-time medical literature access

        #### Business Model
        - B2B SaaS for healthcare organizations
        - Per-clinician licensing
        - Enterprise contracts

        #### Competitive Landscape
        **Competitors:** Epic, IBM Watson Health, Google Health, Nuance DAX

        **Advantages:**
        - State-of-the-art AI technology
        - Strong brand recognition
        - Extensive research capabilities

        #### SWOT Analysis

        **Strengths:**
        - Leading AI technology
        - Strong engineering team
        - Significant funding

        **Weaknesses:**
        - Limited healthcare industry experience
        - Regulatory uncertainties
        - High operational costs

        **Opportunities:**
        - Massive healthcare market
        - Clinical workflow integration
        - Global expansion

        **Threats:**
        - Regulatory approval challenges
        - Liability concerns
        - Established competitors

        ---

        *This is a hypothetical analysis for educational purposes.*
        """)

with tab2:
    st.markdown("### 📋 Analysis Templates")

    templates = {
        "Full Product Teardown": """
# [Product Name] - Comprehensive Teardown

## Executive Summary
[Brief overview of the product and key findings]

## 1. Company & Product Overview
- Company name and background
- Product name and launch date
- Funding and valuation
- Team size and key personnel

## 2. Problem & Market Opportunity
- Problem statement
- Market size (TAM/SAM/SOM)
- Target customers
- Current solutions and gaps

## 3. Product Analysis
- Core features
- User experience
- Technology architecture
- Integration capabilities
- Data & privacy approach

## 4. Business Model
- Revenue streams
- Pricing strategy
- Customer acquisition
- Unit economics

## 5. Go-to-Market Strategy
- Marketing channels
- Sales approach
- Partnerships
- Distribution

## 6. Competitive Analysis
- Direct competitors
- Indirect competitors
- Competitive advantages
- Positioning

## 7. Regulatory & Compliance
- Relevant regulations
- Approval status
- Compliance measures

## 8. Traction & Metrics
- User/customer count
- Revenue (if public)
- Growth rate
- Key partnerships

## 9. SWOT Analysis
- Strengths
- Weaknesses
- Opportunities
- Threats

## 10. Future Outlook
- Product roadmap
- Market trends
- Potential pivots
- Investment perspective

---
""",
        "Quick Competitive Analysis": """
# Quick Competitive Analysis Template

## Product: [Name]

### 1. Core Offering
- What it does:
- Target users:
- Key value prop:

### 2. Competitive Position
| Competitor | Strengths | Weaknesses | Market Share |
|------------|-----------|------------|--------------|
| [Name 1]   |           |            |              |
| [Name 2]   |           |            |              |
| [Name 3]   |           |            |              |

### 3. Differentiation
- Unique features:
- Technology advantages:
- Market positioning:

### 4. Assessment
- Market opportunity: [High/Medium/Low]
- Execution quality: [High/Medium/Low]
- Competitive moat: [Strong/Moderate/Weak]

---
""",
        "UX Analysis": """
# UX/Product Analysis Template

## Product: [Name]

### 1. First Impressions
- Initial user experience:
- Onboarding flow:
- Time to value:

### 2. Core User Flows
[Map out 2-3 main user journeys]

### 3. Interface Design
- Visual design:
- Information architecture:
- Mobile experience:

### 4. Feature Analysis
| Feature | Purpose | Effectiveness | Notes |
|---------|---------|---------------|-------|
|         |         |               |       |

### 5. Pain Points
- Usability issues:
- Missing features:
- Performance problems:

### 6. Recommendations
- Quick wins:
- Strategic improvements:
- Innovation opportunities:

---
"""
    }

    selected_template = st.selectbox("Select a template", list(templates.keys()))
    st.markdown("### Template Preview")
    st.code(templates[selected_template], language="markdown")

    st.download_button(
        "📥 Download Template",
        data=templates[selected_template],
        file_name=f"{selected_template.replace(' ', '_')}_template.md",
        mime="text/markdown"
    )

with tab3:
    st.markdown("### 🎯 Real-World Examples")

    st.markdown("""
    ### Example 1: Tempus AI

    **Category:** Precision Medicine / Clinical AI
    **Funding:** $1B+ raised
    **Status:** Public (IPO 2024)

    **Key Insights:**
    - **Problem:** Oncologists lack personalized treatment insights
    - **Solution:** AI-powered genomic analysis and treatment recommendations
    - **Technology:** Proprietary genomic database + ML models
    - **Business Model:** B2B SaaS for healthcare systems
    - **Success Factors:**
      - Large proprietary dataset (moat)
      - Clinical validation and partnerships
      - Strong physician network effects

    ---

    ### Example 2: K Health

    **Category:** Telemedicine / Symptom Checker
    **Funding:** $271M raised
    **Status:** Private (Series E)

    **Key Insights:**
    - **Problem:** Primary care is expensive and inaccessible
    - **Solution:** AI-powered symptom checker + virtual care
    - **Technology:** Proprietary medical AI trained on millions of cases
    - **Business Model:** B2C subscription + insurance partnerships
    - **Success Factors:**
      - Low-cost primary care alternative
      - Strong AI accuracy (clinical validation)
      - Insurance partnerships for scale

    ---

    ### Example 3: Livongo (acquired by Teladoc)

    **Category:** Chronic Disease Management
    **Funding:** $380M before IPO
    **Exit:** $18.5B acquisition

    **Key Insights:**
    - **Problem:** Chronic disease management is fragmented
    - **Solution:** Connected devices + coaching + data analytics
    - **Technology:** IoT devices + AI-powered insights
    - **Business Model:** B2B through employers
    - **Success Factors:**
      - Clear ROI for employers
      - Behavioral science integration
      - Multiple chronic condition expansion

    ---

    ### What These Successful Products Have in Common:

    1. **Clear Problem:** Well-defined pain point with measurable impact
    2. **Defensible Technology:** AI/data moats that are hard to replicate
    3. **Clinical Validation:** Evidence of effectiveness
    4. **Scalable Model:** Can grow without linear cost increases
    5. **Regulatory Path:** Clear strategy for compliance and approval
    6. **Strong Team:** Healthcare + technical expertise
    """)

add_footer()
