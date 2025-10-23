"""
Sample Data Generator
Generates realistic sample customer data for testing
"""

import pandas as pd
import numpy as np


def generate_sample_data(num_customers=100, seed=42):
    """
    Generate sample customer data

    Args:
        num_customers: Number of customers to generate
        seed: Random seed for reproducibility

    Returns:
        DataFrame with customer data
    """
    np.random.seed(seed)

    data = {
        'customer_id': [f'CUST-{str(i).zfill(4)}' for i in range(1, num_customers + 1)],
        'login_frequency': np.random.exponential(scale=10, size=num_customers).clip(0, 30),
        'feature_usage': np.random.beta(2, 5, size=num_customers) * 100,
        'support_tickets': np.random.poisson(lam=3, size=num_customers).clip(0, 20),
        'days_since_last_login': np.random.exponential(scale=20, size=num_customers).clip(0, 90),
        'contract_value': np.random.lognormal(mean=10, sigma=0.8, size=num_customers).clip(1000, 100000)
    }

    df = pd.DataFrame(data)

    # Round numeric values
    df['login_frequency'] = df['login_frequency'].round(1)
    df['feature_usage'] = df['feature_usage'].round(1)
    df['days_since_last_login'] = df['days_since_last_login'].round(0).astype(int)
    df['contract_value'] = df['contract_value'].round(0).astype(int)

    return df


if __name__ == "__main__":
    # Generate and save sample data
    df = generate_sample_data(150)
    df.to_csv('sample_customer_data.csv', index=False)
    print(f"Generated {len(df)} sample customers")
    print("\nSample data:")
    print(df.head())
