"""
Healthcare Startup Funding Analysis - Data Collector
Collects and structures funding data from various sources
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json


class FundingDataCollector:
    """Collector for startup funding data"""

    def __init__(self):
        self.funding_data = []

    def generate_sample_data(self, n_companies=150):
        """
        Generate sample funding data for demonstration

        Args:
            n_companies: Number of companies to generate
        """
        np.random.seed(42)

        # Define categories
        categories = [
            'AI Diagnostics', 'Telemedicine', 'Digital Therapeutics',
            'Clinical Decision Support', 'Healthcare Analytics',
            'Remote Patient Monitoring', 'Medical Devices',
            'Genomics', 'Drug Discovery', 'Care Coordination'
        ]

        stages = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D+']

        investors = [
            'Andreessen Horowitz', 'General Catalyst', 'Khosla Ventures',
            'GV (Google Ventures)', 'First Round Capital', 'Sequoia Capital',
            'a16z Bio', 'Lux Capital', 'NFX', 'Y Combinator'
        ]

        locations = [
            'San Francisco, CA', 'New York, NY', 'Boston, MA',
            'Palo Alto, CA', 'Austin, TX', 'Seattle, WA',
            'Los Angeles, CA', 'Chicago, IL', 'Cambridge, MA'
        ]

        # Generate companies
        for i in range(n_companies):
            company_name = f"HealthTech{i+1:03d}"

            # Determine funding stage
            stage = np.random.choice(stages, p=[0.35, 0.30, 0.20, 0.10, 0.05])

            # Funding amount based on stage
            if stage == 'Seed':
                amount = np.random.uniform(0.5, 5) * 1_000_000
            elif stage == 'Series A':
                amount = np.random.uniform(5, 20) * 1_000_000
            elif stage == 'Series B':
                amount = np.random.uniform(15, 50) * 1_000_000
            elif stage == 'Series C':
                amount = np.random.uniform(40, 100) * 1_000_000
            else:  # Series D+
                amount = np.random.uniform(80, 300) * 1_000_000

            # Random date in last 3 years
            days_ago = np.random.randint(0, 1095)
            funding_date = datetime.now() - timedelta(days=days_ago)

            # Number of investors
            n_investors = np.random.randint(1, 5)
            company_investors = np.random.choice(investors, size=n_investors, replace=False).tolist()

            # Generate data
            data = {
                'company_id': f'C{i+1:04d}',
                'company_name': company_name,
                'category': np.random.choice(categories),
                'funding_stage': stage,
                'funding_amount': round(amount, 0),
                'funding_date': funding_date.strftime('%Y-%m-%d'),
                'year': funding_date.year,
                'quarter': f"Q{(funding_date.month-1)//3 + 1}",
                'location': np.random.choice(locations),
                'investors': ', '.join(company_investors),
                'n_investors': n_investors,
                'has_yc_backing': np.random.choice([True, False], p=[0.3, 0.7]),
                'total_raised': round(amount * np.random.uniform(1.0, 3.0), 0)
            }

            self.funding_data.append(data)

        print(f"Generated {n_companies} funding records")

    def save_to_csv(self, filename='data/funding_data.csv'):
        """Save funding data to CSV"""
        if not self.funding_data:
            print("No data to save")
            return

        df = pd.DataFrame(self.funding_data)
        df.to_csv(filename, index=False)
        print(f"Saved {len(self.funding_data)} records to {filename}")
        return df

    def save_to_json(self, filename='data/funding_data.json'):
        """Save funding data to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.funding_data, f, indent=2)
        print(f"Saved to {filename}")

    def export_for_tableau(self, filename='data/tableau_export.csv'):
        """Export data in Tableau-friendly format"""
        if not self.funding_data:
            print("No data to export")
            return

        df = pd.DataFrame(self.funding_data)

        # Add calculated fields for Tableau
        df['funding_amount_millions'] = df['funding_amount'] / 1_000_000
        df['total_raised_millions'] = df['total_raised'] / 1_000_000

        df.to_csv(filename, index=False)
        print(f"Tableau export saved to {filename}")


def main():
    """Main execution"""
    import os
    os.makedirs('data', exist_ok=True)

    collector = FundingDataCollector()

    # Generate sample data
    collector.generate_sample_data(n_companies=150)

    # Save in multiple formats
    collector.save_to_csv()
    collector.save_to_json()
    collector.export_for_tableau()

    print("\nData collection complete!")


if __name__ == "__main__":
    main()
