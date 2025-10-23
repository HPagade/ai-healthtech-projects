# YC AI Healthtech Startup Tracker

Analyzing 200+ AI and healthcare startups to identify market trends and funding patterns.

## Features

- Web scraping of Y Combinator's startup directory
- Filtering by AI and Healthcare tags
- Data analysis and visualization of trends
- Batch distribution analysis
- Tag/category analysis
- Growth trend visualization

## Tech Stack

- **Python** - Core programming language
- **BeautifulSoup** - Web scraping
- **Pandas** - Data manipulation and analysis
- **Matplotlib/Seaborn** - Data visualization

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create data directories:
```bash
mkdir -p data visualizations
```

## Usage

### Scrape Startup Data

```bash
python scraper.py
```

This will scrape YC's startup directory for AI and healthcare companies and save the data to `data/yc_startups.csv` and `data/yc_startups.json`.

### Analyze Data

```bash
python analyzer.py
```

This will generate:
- Summary statistics
- Batch distribution charts
- Tag frequency analysis
- Growth trend visualizations

All visualizations are saved to the `visualizations/` directory.

## Project Structure

```
01-yc-healthtech-tracker/
├── scraper.py              # Web scraping script
├── analyzer.py             # Data analysis script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/                  # Scraped data (generated)
│   ├── yc_startups.csv
│   └── yc_startups.json
└── visualizations/        # Generated charts (generated)
    ├── batch_distribution.png
    ├── tag_distribution.png
    └── growth_trends.png
```

## Notes

- The YC website structure may change over time. Update the CSS selectors in `scraper.py` as needed.
- Consider implementing rate limiting to be respectful of YC's servers.
- You may need to use YC's official API if available for more reliable data access.

## Future Enhancements

- [ ] Add funding data analysis
- [ ] Implement caching to avoid re-scraping
- [ ] Add company website scraping for additional insights
- [ ] Create interactive dashboard with Plotly/Dash
- [ ] Add company health/traction metrics
