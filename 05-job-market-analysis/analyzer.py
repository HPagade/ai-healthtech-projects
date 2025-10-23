"""
Startup Job Market Analysis - Analyzer
Analyzes job market trends from scraped data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import ast


class JobMarketAnalyzer:
    """Analyzer for startup job market data"""

    def __init__(self, data_file='data/jobs.csv'):
        self.data_file = data_file
        self.df = None
        self.load_data()

    def load_data(self):
        """Load job data"""
        try:
            self.df = pd.read_csv(self.data_file)
            # Parse tags if they're stored as strings
            if 'tags' in self.df.columns and isinstance(self.df['tags'].iloc[0], str):
                self.df['tags'] = self.df['tags'].apply(ast.literal_eval)
            print(f"Loaded {len(self.df)} jobs from {self.data_file}")
        except FileNotFoundError:
            print(f"Data file not found: {self.data_file}")
            self.df = pd.DataFrame()

    def analyze_top_roles(self, top_n=10):
        """Analyze most common job roles"""
        if self.df.empty:
            return

        role_counts = self.df['title'].value_counts().head(top_n)

        print(f"\n=== Top {top_n} Most Common Roles ===")
        for role, count in role_counts.items():
            print(f"{role}: {count} ({count/len(self.df)*100:.1f}%)")

        # Visualization
        plt.figure(figsize=(12, 6))
        role_counts.plot(kind='barh', color='skyblue')
        plt.title(f'Top {top_n} Most In-Demand Roles in Healthtech Startups', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Job Postings')
        plt.ylabel('Job Title')
        plt.tight_layout()
        plt.savefig('visualizations/top_roles.png', dpi=300)
        print("Saved visualization: visualizations/top_roles.png")

    def analyze_salary_ranges(self):
        """Analyze salary distributions"""
        if self.df.empty or 'salary_min' not in self.df.columns:
            return

        print("\n=== Salary Analysis ===")
        print(f"Median Min Salary: ${self.df['salary_min'].median():,.0f}")
        print(f"Median Max Salary: ${self.df['salary_max'].median():,.0f}")
        print(f"Average Salary Range: ${self.df['salary_min'].mean():,.0f} - ${self.df['salary_max'].mean():,.0f}")

        # Salary by role
        salary_by_role = self.df.groupby('title').agg({
            'salary_min': 'median',
            'salary_max': 'median'
        }).sort_values('salary_max', ascending=False).head(10)

        print("\nTop 10 Highest Paying Roles:")
        print(salary_by_role)

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Histogram
        axes[0].hist(self.df['salary_min'], bins=30, alpha=0.7, label='Min Salary', color='blue')
        axes[0].hist(self.df['salary_max'], bins=30, alpha=0.7, label='Max Salary', color='green')
        axes[0].set_xlabel('Salary ($)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Salary Distribution')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Top paying roles
        salary_by_role['salary_max'].plot(kind='barh', ax=axes[1], color='coral')
        axes[1].set_xlabel('Median Max Salary ($)')
        axes[1].set_title('Top 10 Highest Paying Roles')

        plt.tight_layout()
        plt.savefig('visualizations/salary_analysis.png', dpi=300)
        print("Saved visualization: visualizations/salary_analysis.png")

    def analyze_skills_demand(self, top_n=15):
        """Analyze most in-demand skills/tags"""
        if self.df.empty or 'tags' not in self.df.columns:
            return

        # Flatten all tags
        all_tags = []
        for tags in self.df['tags'].dropna():
            if isinstance(tags, list):
                all_tags.extend(tags)

        tag_counts = Counter(all_tags)
        top_tags = dict(tag_counts.most_common(top_n))

        print(f"\n=== Top {top_n} Most Demanded Skills ===")
        for tag, count in top_tags.items():
            print(f"{tag}: {count} ({count/len(self.df)*100:.1f}%)")

        # Visualization
        plt.figure(figsize=(12, 8))
        plt.barh(list(top_tags.keys()), list(top_tags.values()), color='teal')
        plt.xlabel('Number of Job Postings')
        plt.ylabel('Skill/Technology')
        plt.title(f'Top {top_n} Most In-Demand Skills in Healthtech', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('visualizations/skills_demand.png', dpi=300)
        print("Saved visualization: visualizations/skills_demand.png")

    def analyze_locations(self):
        """Analyze job distribution by location"""
        if self.df.empty:
            return

        location_counts = self.df['location'].value_counts().head(10)

        print("\n=== Top 10 Locations ===")
        print(location_counts)

        # Visualization
        plt.figure(figsize=(10, 6))
        location_counts.plot(kind='bar', color='orange')
        plt.title('Job Distribution by Location', fontsize=14, fontweight='bold')
        plt.xlabel('Location')
        plt.ylabel('Number of Jobs')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('visualizations/location_distribution.png', dpi=300)
        print("Saved visualization: visualizations/location_distribution.png")

    def analyze_experience_levels(self):
        """Analyze distribution by experience level"""
        if self.df.empty:
            return

        exp_counts = self.df['experience_level'].value_counts()

        print("\n=== Experience Level Distribution ===")
        print(exp_counts)

        # Visualization
        plt.figure(figsize=(10, 6))
        exp_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        plt.title('Jobs by Experience Level', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('visualizations/experience_distribution.png', dpi=300)
        print("Saved visualization: visualizations/experience_distribution.png")

    def generate_insights_report(self):
        """Generate comprehensive insights report"""
        if self.df.empty:
            print("No data available for analysis")
            return

        report = []
        report.append("=" * 80)
        report.append(" " * 20 + "HEALTHTECH JOB MARKET INSIGHTS REPORT")
        report.append("=" * 80)

        report.append(f"\n📊 Dataset: {len(self.df)} job postings analyzed\n")

        # Top insights
        report.append("🔍 KEY FINDINGS:\n")

        # Most common role
        top_role = self.df['title'].value_counts().index[0]
        top_role_count = self.df['title'].value_counts().values[0]
        report.append(f"1. Most In-Demand Role: {top_role} ({top_role_count} postings)")

        # Salary insights
        if 'salary_max' in self.df.columns:
            avg_salary = self.df['salary_max'].mean()
            report.append(f"2. Average Maximum Salary: ${avg_salary:,.0f}")

        # Remote work
        remote_jobs = len(self.df[self.df['location'].str.contains('Remote', case=False, na=False)])
        remote_pct = (remote_jobs / len(self.df)) * 100
        report.append(f"3. Remote Opportunities: {remote_jobs} ({remote_pct:.1f}%)")

        # Top skill
        all_tags = []
        for tags in self.df['tags'].dropna():
            if isinstance(tags, list):
                all_tags.extend(tags)
        if all_tags:
            top_skill = Counter(all_tags).most_common(1)[0][0]
            report.append(f"4. Most Demanded Skill: {top_skill}")

        report.append("\n" + "=" * 80)

        report_text = "\n".join(report)
        print(report_text)

        # Save report
        with open('reports/insights_report.txt', 'w') as f:
            f.write(report_text)
        print("\nReport saved to: reports/insights_report.txt")

    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        if self.df.empty:
            print("No data available")
            return

        import os
        os.makedirs('visualizations', exist_ok=True)
        os.makedirs('reports', exist_ok=True)

        print("Running full job market analysis...")
        self.analyze_top_roles()
        self.analyze_salary_ranges()
        self.analyze_skills_demand()
        self.analyze_locations()
        self.analyze_experience_levels()
        self.generate_insights_report()

        print("\n✅ Analysis complete! Check visualizations/ and reports/ folders.")


def main():
    """Main execution"""
    analyzer = JobMarketAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
