# Startup Job Market Analysis

Analyzing job postings from YC and healthtech startups to identify hiring trends, in-demand skills, and salary ranges.

## Features

- Web scraping of startup job boards
- Trend analysis of most in-demand roles
- Salary range analysis by role and location
- Skills/technology demand tracking
- Location and remote work analysis
- Experience level distribution
- Comprehensive insights reporting
- Data visualization

## Tech Stack

- **Python** - Core programming language
- **BeautifulSoup** - Web scraping
- **Pandas** - Data analysis
- **Matplotlib/Seaborn** - Visualizations
- **Tableau** - Advanced dashboards (optional)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create directories:
```bash
mkdir -p data visualizations reports
```

## Usage

### Step 1: Scrape Job Data

```bash
python job_scraper.py
```

This generates sample data (200 job postings). In production, update the scraper to target actual job boards.

### Step 2: Analyze Data

```bash
python analyzer.py
```

This runs the full analysis pipeline and generates:
- Visualizations in `visualizations/`
- Insights report in `reports/`

## Analysis Outputs

### Visualizations

1. **top_roles.png** - Most in-demand job titles
2. **salary_analysis.png** - Salary distributions and top-paying roles
3. **skills_demand.png** - Most sought-after skills and technologies
4. **location_distribution.png** - Geographic distribution of jobs
5. **experience_distribution.png** - Jobs by experience level

### Reports

- **insights_report.txt** - Key findings and statistics

## Sample Insights

The analysis can reveal insights such as:

- Product Managers and Engineers are the most hired roles
- Remote work comprises ~30% of opportunities
- AI and Healthcare tags appear in 60%+ of postings
- Average salaries range from $100K-$180K
- San Francisco and Remote are top locations

## Customization

### Adding New Data Sources

Edit `job_scraper.py` to add scrapers for:
- LinkedIn Jobs
- Indeed
- AngelList
- Company career pages
- Wellfound (formerly AngelList Talent)

### Filtering by Tags

Target specific tags:
```python
scraper.scrape_yc_jobs(tags=['Healthcare', 'AI', 'Machine Learning'])
```

## Project Structure

```
05-job-market-analysis/
├── job_scraper.py         # Web scraping script
├── analyzer.py            # Analysis and visualization
├── requirements.txt       # Dependencies
├── README.md             # This file
├── data/                 # Scraped data (generated)
│   ├── jobs.csv
│   └── jobs.json
├── visualizations/       # Charts (generated)
│   ├── top_roles.png
│   ├── salary_analysis.png
│   ├── skills_demand.png
│   ├── location_distribution.png
│   └── experience_distribution.png
└── reports/              # Analysis reports (generated)
    └── insights_report.txt
```

## Tableau Integration

For advanced visualizations:

1. Export data to Tableau-friendly format:
```python
df.to_csv('tableau_export.csv', index=False)
```

2. Import into Tableau Public
3. Create interactive dashboards
4. Publish and share publicly

## Future Enhancements

- [ ] Real-time scraping from multiple job boards
- [ ] Time-series tracking of hiring trends
- [ ] Company-specific analysis
- [ ] Job recommendation engine
- [ ] Email alerts for new matching jobs
- [ ] Skill gap analysis
- [ ] Salary negotiation insights
- [ ] Market demand forecasting
