# Customer Health Score Calculator

Interactive dashboard for predicting customer churn risk using usage metrics and engagement data.

## Features

- Real-time health score calculation
- Interactive Plotly visualizations
- Customer risk categorization (Healthy / At Risk / High Risk)
- Churn probability prediction
- Individual customer analysis
- Actionable recommendations
- CSV data upload/download
- Sample data generation

## Tech Stack

- **Python** - Core programming language
- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Using Sample Data

1. Select "Use Sample Data" in the sidebar
2. Explore the dashboard tabs:
   - **Overview**: Distribution charts and summary statistics
   - **Customer List**: Sortable table of all customers
   - **Individual Analysis**: Deep dive into specific customers
   - **Trends**: Feature importance and trend analysis

### Uploading Your Own Data

1. Select "Upload CSV" in the sidebar
2. Upload a CSV file with the following columns:
   - `customer_id`: Unique customer identifier
   - `login_frequency`: Number of logins per month
   - `feature_usage`: Percentage of features used (0-100)
   - `support_tickets`: Number of support tickets opened
   - `days_since_last_login`: Days since last login
   - `contract_value`: Annual contract value in dollars

## Health Score Calculation

The health score (0-100) is calculated using weighted metrics:

| Metric | Weight | Description |
|--------|--------|-------------|
| Login Frequency | 30% | Higher is better |
| Feature Usage | 25% | Higher is better |
| Support Tickets | 20% | Lower is better |
| Days Since Last Login | 15% | Lower is better |
| Contract Value | 10% | Higher is better |

### Risk Categories

- **Healthy** (70-100): Low churn risk
- **At Risk** (40-69): Medium churn risk, needs attention
- **High Risk** (0-39): High churn risk, immediate action required

## Project Structure

```
02-customer-health-score/
├── app.py                      # Main Streamlit application
├── health_score.py             # Health score calculation logic
├── data_generator.py           # Sample data generator
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── sample_customer_data.csv    # Generated sample data (optional)
```

## Customization

### Adjusting Weights

Modify the weights in `health_score.py`:

```python
self.weights = {
    'login_frequency': 0.30,
    'feature_usage': 0.25,
    'support_tickets': 0.20,
    'days_since_last_login': 0.15,
    'contract_value': 0.10
}
```

### Adding New Metrics

1. Add the metric to the health score calculation in `health_score.py`
2. Update the normalization logic
3. Add the metric to the dashboard in `app.py`

## Future Enhancements

- [ ] Time-series tracking of health scores
- [ ] Machine learning model for churn prediction
- [ ] Automated alert system for at-risk customers
- [ ] Integration with CRM systems
- [ ] Cohort analysis
- [ ] Predictive analytics for contract renewals
