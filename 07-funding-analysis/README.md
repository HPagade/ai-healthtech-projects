# Healthcare Startup Funding Analysis

Interactive dashboard analyzing AI healthtech funding trends using SQL, Python, and Tableau.

## Features

- Comprehensive funding data collection
- SQL-based analysis queries
- Python data analysis and visualization
- Tableau dashboard templates
- Trend analysis by year, category, stage, and geography
- Investor activity tracking
- Market insights and reporting

## Tech Stack

- **SQL** - Data querying and analysis
- **Python** - Data processing and visualization
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Visualizations
- **SQLite** - Local database
- **Tableau Public** - Interactive dashboards

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create directories:
```bash
mkdir -p data visualizations
```

## Usage

### Step 1: Collect Data

```bash
python data_collector.py
```

This generates sample funding data. In production, integrate with:
- Crunchbase API
- PitchBook data exports
- Public funding announcements

### Step 2: Analyze with Python

```bash
python analyzer.py
```

This creates:
- SQLite database (`data/funding.db`)
- Visualizations in `visualizations/`
- Summary statistics

### Step 3: SQL Analysis

Use the provided SQL queries in `sql_queries.sql`:

```bash
sqlite3 data/funding.db < sql_queries.sql
```

Or connect with your favorite SQL client:
- DBeaver
- DataGrip
- VS Code SQLite extension

### Step 4: Tableau Dashboard

1. Open Tableau Public
2. Connect to `data/tableau_export.csv` or `data/funding.db`
3. Create visualizations:
   - Funding trends over time
   - Category breakdown
   - Geographic heatmap
   - Stage progression
   - Investor network graph

## Sample Analyses

### Yearly Trends
- Total funding by year
- Number of deals by year
- Average deal sizes
- Year-over-year growth

### Category Analysis
- Top funded categories
- Emerging categories
- Category trends over time

### Stage Analysis
- Deal distribution by stage
- Average deal sizes per stage
- Stage progression patterns

### Geographic Analysis
- Top cities for healthtech funding
- Regional trends
- Remote-first companies

### Investor Analysis
- Most active investors
- Investment patterns
- YC-backed companies performance

## SQL Query Examples

```sql
-- Top 10 largest funding rounds
SELECT
    company_name,
    category,
    funding_amount / 1000000 as funding_millions,
    funding_stage,
    funding_date
FROM funding_data
ORDER BY funding_amount DESC
LIMIT 10;

-- Funding by category and stage
SELECT
    category,
    funding_stage,
    COUNT(*) as deals,
    SUM(funding_amount) / 1000000 as total_millions
FROM funding_data
GROUP BY category, funding_stage
ORDER BY total_millions DESC;
```

## Project Structure

```
07-funding-analysis/
├── data_collector.py          # Data collection script
├── analyzer.py                # Python analysis
├── sql_queries.sql            # SQL analysis queries
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── data/                      # Data files (generated)
│   ├── funding_data.csv
│   ├── funding_data.json
│   ├── tableau_export.csv
│   └── funding.db
└── visualizations/            # Charts (generated)
    ├── yearly_trends.png
    ├── category_funding.png
    ├── stage_analysis.png
    └── geography.png
```

## Tableau Dashboard Ideas

### Dashboard 1: Market Overview
- Total funding over time (line chart)
- Funding by category (treemap)
- Deal count by quarter (bar chart)
- Key metrics (scorecards)

### Dashboard 2: Deep Dive
- Category breakdown with drill-down
- Stage progression flow diagram
- Geographic heatmap
- Investor network

### Dashboard 3: Trends
- YoY growth analysis
- Emerging categories
- Deal size evolution
- Market concentration

## Data Sources

For real-world analysis, consider:

**Public Data:**
- Crunchbase (API or export)
- CB Insights reports
- PitchBook (subscription)
- Company press releases
- SEC filings (for public companies)

**Scraping:**
- TechCrunch funding announcements
- VentureBeat news
- Company blogs
- LinkedIn updates

## Key Metrics to Track

- **Total Capital Raised** - Overall market size
- **Deal Count** - Market activity level
- **Average Deal Size** - Capital efficiency
- **Median Deal Size** - Typical deal
- **Mega Rounds** - $50M+ deals
- **YoY Growth** - Market trajectory
- **Category Share** - Market distribution
- **Geographic Concentration** - Location trends

## Future Enhancements

- [ ] Real-time data ingestion
- [ ] Machine learning predictions
- [ ] Automated Tableau dashboard publishing
- [ ] Investor scoring model
- [ ] Company success prediction
- [ ] Market saturation analysis
- [ ] Competitive intelligence
- [ ] Email reports and alerts

## Resources

- [Tableau Public Gallery](https://public.tableau.com/app/discover)
- [Crunchbase API Docs](https://data.crunchbase.com/docs)
- [SQL for Data Analysis Tutorial](https://mode.com/sql-tutorial/)

---

**Note:** Sample data is for demonstration. Use real funding data for actual analysis.
