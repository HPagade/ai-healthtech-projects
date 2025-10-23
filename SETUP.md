# Setup Guide - AI Healthtech Projects Portfolio

Complete setup instructions for all 8 projects in this portfolio.

## Prerequisites

### Required Software

1. **Python 3.9+**
   ```bash
   python --version  # Should be 3.9 or higher
   ```

2. **pip** (Python package manager)
   ```bash
   pip --version
   ```

3. **Git** (already installed if you cloned this repo)
   ```bash
   git --version
   ```

### Optional Software

- **Tableau Public** (for Project 7 - Funding Analysis dashboards)
- **SQLite Browser** (for viewing database files)
- **VS Code** or your preferred IDE

## Global Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-healthtech-projects.git
cd ai-healthtech-projects
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install All Dependencies

To install dependencies for ALL projects at once:

```bash
pip install -r requirements-all.txt
```

Or install dependencies for individual projects as needed (see below).

## Project-Specific Setup

### Project 1: YC AI Healthtech Startup Tracker

```bash
cd 01-yc-healthtech-tracker
pip install -r requirements.txt
mkdir -p data visualizations

# Run the scraper
python scraper.py

# Run analysis
python analyzer.py
```

### Project 2: Customer Health Score Calculator

```bash
cd 02-customer-health-score
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

Access at: http://localhost:8501

### Project 3: AI Cover Letter Generator

```bash
cd 03-ai-cover-letter
pip install -r requirements.txt

# Set up API key
export OPENAI_API_KEY='your-api-key-here'

# Run interactive mode
python interactive.py

# Or use command-line mode
python generator.py --company "HealthTech AI" --position "Product Manager" \
  --company-desc "AI healthcare platform" \
  --job-desc "PM with healthcare experience" \
  --background "5 years in healthtech"
```

### Project 4: AI Clinical Decision Support Tool

```bash
cd 04-clinical-decision-support
pip install -r requirements.txt
mkdir -p data models

# Train the model
python symptom_checker.py

# Run interactive checker
python interactive_checker.py
```

### Project 5: Startup Job Market Analysis

```bash
cd 05-job-market-analysis
pip install -r requirements.txt
mkdir -p data visualizations reports

# Scrape job data (generates sample data)
python job_scraper.py

# Run analysis
python analyzer.py
```

### Project 6: AI Healthtech Product Teardown

```bash
cd 06-product-teardown

# No installation needed - this is a research framework
# Use the templates to analyze products
# See README.md for detailed instructions
```

### Project 7: Healthcare Startup Funding Analysis

```bash
cd 07-funding-analysis
pip install -r requirements.txt
mkdir -p data visualizations

# Generate sample data
python data_collector.py

# Run Python analysis
python analyzer.py

# Run SQL queries
sqlite3 data/funding.db < sql_queries.sql

# For Tableau: Import data/tableau_export.csv into Tableau Public
```

### Project 8: AI Patient Triage Chatbot

```bash
cd 08-patient-triage-chatbot
pip install -r requirements.txt

# Set up API key
export OPENAI_API_KEY='your-api-key-here'

# Run Streamlit app
streamlit run app.py

# Or run CLI version
python chatbot.py
```

Access at: http://localhost:8501

## API Keys Setup

Several projects require API keys:

### OpenAI API Key (Projects 3, 8)

1. Get API key from: https://platform.openai.com/api-keys
2. Set environment variable:
   ```bash
   export OPENAI_API_KEY='sk-...'
   ```
3. Or create `.env` file in project directory:
   ```
   OPENAI_API_KEY=sk-...
   ```

**Cost estimates:**
- Project 3 (Cover Letter): ~$0.03-0.06 per letter
- Project 8 (Triage Chatbot): ~$0.03-0.10 per conversation

### Optional API Keys

For production use, you might want:
- **Crunchbase API** (Project 1, 7) - For real funding data
- **Indeed/LinkedIn API** (Project 5) - For real job data

## Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: `OPENAI_API_KEY not found`**
```bash
# Solution: Set the environment variable
export OPENAI_API_KEY='your-key-here'
```

**Issue: Port already in use (Streamlit)**
```bash
# Solution: Use a different port
streamlit run app.py --server.port 8502
```

**Issue: SQLite database locked**
```bash
# Solution: Close all database connections
# Then delete and regenerate the database
rm data/funding.db
python data_collector.py
python analyzer.py
```

### Python Version Issues

If you have multiple Python versions:
```bash
# Use specific version
python3.9 -m venv venv
# or
python3.10 -m venv venv
```

## Running Multiple Projects

To run multiple Streamlit apps simultaneously:

```bash
# Terminal 1
cd 02-customer-health-score
streamlit run app.py --server.port 8501

# Terminal 2
cd 08-patient-triage-chatbot
streamlit run app.py --server.port 8502
```

## Development Tips

### Use Virtual Environments

Always use virtual environments to avoid dependency conflicts:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### Update Dependencies

To update all packages:
```bash
pip install --upgrade -r requirements.txt
```

### IDE Setup

**VS Code:**
1. Install Python extension
2. Select interpreter: `Cmd+Shift+P` → "Python: Select Interpreter"
3. Choose the venv interpreter

**PyCharm:**
1. Open project
2. Settings → Project → Python Interpreter
3. Add interpreter from venv

## Testing Projects

### Quick Test Commands

```bash
# Test Project 1
cd 01-yc-healthtech-tracker && python scraper.py

# Test Project 2
cd 02-customer-health-score && streamlit run app.py

# Test Project 4
cd 04-clinical-decision-support && python symptom_checker.py

# Test Project 7
cd 07-funding-analysis && python data_collector.py && python analyzer.py
```

## Data Privacy & Security

### Important Notes

1. **API Keys**: Never commit API keys to git
2. **.env files**: Add to `.gitignore`
3. **Sample Data**: All projects use synthetic data by default
4. **Medical Data**: Projects 4 and 8 use educational data only

### Production Checklist

If deploying any project:
- [ ] Use environment variables for secrets
- [ ] Implement authentication
- [ ] Add HTTPS
- [ ] Set up logging
- [ ] Enable error tracking
- [ ] Configure CORS appropriately
- [ ] Review HIPAA compliance (for healthcare projects)

## Next Steps

After setup:

1. **Explore Each Project** - Review individual README files
2. **Customize** - Adapt projects to your needs
3. **Extend** - Add new features
4. **Share** - Deploy to Streamlit Cloud, Heroku, etc.

## Getting Help

- **Project Documentation**: Each project has a detailed README.md
- **Issues**: Check GitHub issues for common problems
- **Python Docs**: https://docs.python.org/3/
- **Streamlit Docs**: https://docs.streamlit.io/
- **LangChain Docs**: https://python.langchain.com/

## Resources

### Learning Resources

- **Python**: [Real Python](https://realpython.com/)
- **Data Science**: [Kaggle Learn](https://www.kaggle.com/learn)
- **Healthcare AI**: [Stanford AIMI](https://aimi.stanford.edu/)
- **Streamlit**: [Streamlit Gallery](https://streamlit.io/gallery)

### Healthcare Tech Resources

- **FDA AI/ML Guidance**: https://www.fda.gov/medical-devices/software-medical-device-samd
- **HIPAA**: https://www.hhs.gov/hipaa/
- **HL7 FHIR**: https://www.hl7.org/fhir/

## Contributing

To contribute to any project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy coding! 🚀**

Questions? Open an issue or reach out on [LinkedIn](https://linkedin.com/in/hannah-pagade)
