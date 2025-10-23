"""
YC AI Healthtech Startup Tracker - Data Analyzer
Analyzes scraped startup data to identify trends and patterns
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os


class StartupAnalyzer:
    """Analyzer for YC startup data"""

    def __init__(self, data_file='data/yc_startups.csv'):
        """Initialize analyzer with data file"""
        self.data_file = data_file
        self.df = None
        self.load_data()

    def load_data(self):
        """Load startup data from CSV"""
        try:
            self.df = pd.read_csv(self.data_file)
            print(f"Loaded {len(self.df)} startups from {self.data_file}")
        except FileNotFoundError:
            print(f"Data file {self.data_file} not found. Run scraper.py first.")
            self.df = pd.DataFrame()

    def analyze_batch_distribution(self):
        """Analyze distribution of startups by batch"""
        if self.df.empty:
            return

        batch_counts = self.df['batch'].value_counts()
        print("\n=== Batch Distribution ===")
        print(batch_counts)

        plt.figure(figsize=(12, 6))
        batch_counts.plot(kind='bar', color='skyblue')
        plt.title('YC AI Healthtech Startups by Batch', fontsize=14, fontweight='bold')
        plt.xlabel('YC Batch')
        plt.ylabel('Number of Startups')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/batch_distribution.png', dpi=300)
        print("Saved visualization: visualizations/batch_distribution.png")

    def analyze_tags(self):
        """Analyze most common tags/categories"""
        if self.df.empty:
            return

        # Flatten all tags
        all_tags = []
        for tags in self.df['tags'].dropna():
            if isinstance(tags, str):
                all_tags.extend(eval(tags))  # Convert string list to actual list

        tag_counts = Counter(all_tags)
        top_tags = dict(tag_counts.most_common(15))

        print("\n=== Top 15 Tags ===")
        for tag, count in top_tags.items():
            print(f"{tag}: {count}")

        plt.figure(figsize=(12, 8))
        plt.barh(list(top_tags.keys()), list(top_tags.values()), color='coral')
        plt.title('Most Common Tags in AI Healthtech Startups', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Startups')
        plt.ylabel('Tag')
        plt.tight_layout()
        plt.savefig('visualizations/tag_distribution.png', dpi=300)
        print("Saved visualization: visualizations/tag_distribution.png")

    def analyze_growth_trends(self):
        """Analyze growth trends over time"""
        if self.df.empty:
            return

        # Extract year and season from batch
        self.df['year'] = self.df['batch'].str.extract(r'(\d+)').astype(int) + 2000
        self.df['season'] = self.df['batch'].str[0]

        yearly_counts = self.df.groupby('year').size()

        print("\n=== Yearly Growth ===")
        print(yearly_counts)

        plt.figure(figsize=(12, 6))
        yearly_counts.plot(kind='line', marker='o', color='green', linewidth=2)
        plt.title('AI Healthtech Startup Growth Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Year')
        plt.ylabel('Number of Startups')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/growth_trends.png', dpi=300)
        print("Saved visualization: visualizations/growth_trends.png")

    def generate_summary_stats(self):
        """Generate summary statistics"""
        if self.df.empty:
            return

        print("\n=== Summary Statistics ===")
        print(f"Total Startups: {len(self.df)}")
        print(f"Earliest Batch: {self.df['batch'].min()}")
        print(f"Latest Batch: {self.df['batch'].max()}")
        print(f"\nSample Startups:")
        print(self.df[['name', 'batch', 'description']].head(10))

    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        if self.df.empty:
            print("No data available for analysis")
            return

        # Create visualizations directory
        os.makedirs('visualizations', exist_ok=True)

        print("Running full analysis...")
        self.generate_summary_stats()
        self.analyze_batch_distribution()
        self.analyze_tags()
        self.analyze_growth_trends()
        print("\nAnalysis complete! Check the visualizations folder.")


def main():
    """Main execution function"""
    analyzer = StartupAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
