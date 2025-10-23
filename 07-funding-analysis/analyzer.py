"""
Healthcare Startup Funding Analysis - Python Analyzer
Analyzes funding data and creates visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path


class FundingAnalyzer:
    """Analyzer for healthcare startup funding data"""

    def __init__(self, data_file='data/funding_data.csv'):
        self.data_file = data_file
        self.df = None
        self.load_data()

    def load_data(self):
        """Load funding data"""
        try:
            self.df = pd.read_csv(self.data_file)
            self.df['funding_date'] = pd.to_datetime(self.df['funding_date'])
            self.df['funding_millions'] = self.df['funding_amount'] / 1_000_000
            print(f"Loaded {len(self.df)} funding records")
        except FileNotFoundError:
            print(f"Data file not found: {self.data_file}")

    def create_sql_database(self, db_file='data/funding.db'):
        """Create SQLite database from CSV data"""
        conn = sqlite3.connect(db_file)
        self.df.to_sql('funding_data', conn, if_exists='replace', index=False)
        print(f"Created SQLite database: {db_file}")
        conn.close()

    def analyze_yearly_trends(self):
        """Analyze funding trends by year"""
        yearly = self.df.groupby('year').agg({
            'funding_amount': ['count', 'sum', 'mean'],
            'company_id': 'count'
        }).reset_index()

        yearly.columns = ['year', 'num_deals', 'total_funding', 'avg_deal_size', 'companies']
        yearly['total_millions'] = yearly['total_funding'] / 1_000_000
        yearly['avg_millions'] = yearly['avg_deal_size'] / 1_000_000

        print("\n=== Yearly Funding Trends ===")
        print(yearly[['year', 'num_deals', 'total_millions', 'avg_millions']])

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Total funding by year
        axes[0].bar(yearly['year'], yearly['total_millions'], color='steelblue')
        axes[0].set_title('Total Funding by Year', fontweight='bold')
        axes[0].set_xlabel('Year')
        axes[0].set_ylabel('Total Funding ($M)')
        axes[0].grid(axis='y', alpha=0.3)

        # Number of deals by year
        axes[1].bar(yearly['year'], yearly['num_deals'], color='coral')
        axes[1].set_title('Number of Deals by Year', fontweight='bold')
        axes[1].set_xlabel('Year')
        axes[1].set_ylabel('Number of Deals')
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('visualizations/yearly_trends.png', dpi=300)
        print("Saved: visualizations/yearly_trends.png")

    def analyze_categories(self):
        """Analyze funding by category"""
        category_stats = self.df.groupby('category').agg({
            'funding_amount': ['count', 'sum', 'mean']
        }).reset_index()

        category_stats.columns = ['category', 'num_deals', 'total_funding', 'avg_deal']
        category_stats['total_millions'] = category_stats['total_funding'] / 1_000_000
        category_stats = category_stats.sort_values('total_millions', ascending=False)

        print("\n=== Top Categories by Funding ===")
        print(category_stats[['category', 'num_deals', 'total_millions']].head(10))

        # Visualization
        plt.figure(figsize=(12, 6))
        plt.barh(category_stats['category'], category_stats['total_millions'], color='teal')
        plt.xlabel('Total Funding ($M)')
        plt.title('Total Funding by Category', fontweight='bold', fontsize=14)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('visualizations/category_funding.png', dpi=300)
        print("Saved: visualizations/category_funding.png")

    def analyze_stages(self):
        """Analyze funding by stage"""
        stage_order = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D+']

        stage_stats = self.df.groupby('funding_stage').agg({
            'funding_amount': ['count', 'sum', 'mean', 'median']
        }).reset_index()

        stage_stats.columns = ['stage', 'num_deals', 'total', 'mean', 'median']
        stage_stats['mean_millions'] = stage_stats['mean'] / 1_000_000
        stage_stats['median_millions'] = stage_stats['median'] / 1_000_000

        # Reorder by stage
        stage_stats['stage'] = pd.Categorical(stage_stats['stage'], categories=stage_order, ordered=True)
        stage_stats = stage_stats.sort_values('stage')

        print("\n=== Funding by Stage ===")
        print(stage_stats[['stage', 'num_deals', 'mean_millions', 'median_millions']])

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Deal count by stage
        axes[0].bar(stage_stats['stage'], stage_stats['num_deals'], color='skyblue')
        axes[0].set_title('Deal Count by Stage', fontweight='bold')
        axes[0].set_xlabel('Stage')
        axes[0].set_ylabel('Number of Deals')
        axes[0].tick_params(axis='x', rotation=45)

        # Average deal size by stage
        axes[1].bar(stage_stats['stage'], stage_stats['mean_millions'], color='orange')
        axes[1].set_title('Average Deal Size by Stage', fontweight='bold')
        axes[1].set_xlabel('Stage')
        axes[1].set_ylabel('Average Deal Size ($M)')
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('visualizations/stage_analysis.png', dpi=300)
        print("Saved: visualizations/stage_analysis.png")

    def analyze_geography(self):
        """Analyze funding by location"""
        geo_stats = self.df.groupby('location').agg({
            'funding_amount': ['count', 'sum']
        }).reset_index()

        geo_stats.columns = ['location', 'num_deals', 'total_funding']
        geo_stats['total_millions'] = geo_stats['total_funding'] / 1_000_000
        geo_stats = geo_stats.sort_values('total_millions', ascending=False).head(10)

        print("\n=== Top 10 Locations ===")
        print(geo_stats[['location', 'num_deals', 'total_millions']])

        # Visualization
        plt.figure(figsize=(12, 6))
        plt.barh(geo_stats['location'], geo_stats['total_millions'], color='purple')
        plt.xlabel('Total Funding ($M)')
        plt.title('Top 10 Locations by Funding', fontweight='bold', fontsize=14)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('visualizations/geography.png', dpi=300)
        print("Saved: visualizations/geography.png")

    def create_dashboard_summary(self):
        """Create summary statistics for dashboard"""
        summary = {
            'total_companies': len(self.df),
            'total_funding_billions': self.df['funding_amount'].sum() / 1_000_000_000,
            'avg_deal_size_millions': self.df['funding_amount'].mean() / 1_000_000,
            'median_deal_size_millions': self.df['funding_amount'].median() / 1_000_000,
            'top_category': self.df['category'].value_counts().index[0],
            'most_active_year': self.df['year'].value_counts().index[0]
        }

        print("\n=== Dashboard Summary ===")
        for key, value in summary.items():
            print(f"{key}: {value}")

        return summary

    def run_full_analysis(self):
        """Run complete analysis"""
        Path('visualizations').mkdir(exist_ok=True)

        print("Running full funding analysis...")
        self.analyze_yearly_trends()
        self.analyze_categories()
        self.analyze_stages()
        self.analyze_geography()
        self.create_dashboard_summary()
        self.create_sql_database()

        print("\n✅ Analysis complete! Check visualizations/ folder and funding.db")


def main():
    """Main execution"""
    analyzer = FundingAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
