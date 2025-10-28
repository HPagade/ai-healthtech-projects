# Deployment Guide - AI Healthtech Projects Portfolio

Complete guide for deploying your multi-page Streamlit application.

## 🚀 Quick Deploy to Streamlit Cloud (Recommended)

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at [streamlit.io/cloud](https://streamlit.io/cloud))
3. OpenAI API key (for Projects 3 & 8)

### Step-by-Step Deployment

#### 1. Push to GitHub
```bash
git add .
git commit -m "Complete AI Healthtech Portfolio deployment"
git push origin main
```

#### 2. Deploy on Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Click** "New app"
3. **Select** your repository: `HPagade/ai-healthtech-projects`
4. **Set** Main file path: `Home.py`
5. **Click** "Deploy"

#### 3. Configure Secrets

In Streamlit Cloud dashboard:
1. Go to **App settings** → **Secrets**
2. Add your secrets:

```toml
# Streamlit Secrets
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

#### 4. Access Your App

Your app will be live at:
```
https://your-app-name.streamlit.app
```

---

## 📦 Local Development

### Setup

```bash
# Clone repository
git clone https://github.com/HPagade/ai-healthtech-projects.git
cd ai-healthtech-projects

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your API keys

# Run the app
streamlit run Home.py
```

### Access Locally
Open browser to: `http://localhost:8501`

---

## 🔑 API Keys Setup

### Required API Keys

#### OpenAI API Key (Projects 3 & 8)
1. Create account at [platform.openai.com](https://platform.openai.com)
2. Go to **API keys** section
3. Click **Create new secret key**
4. Copy key and add to Streamlit secrets

**Cost Estimate:**
- Project 3 (Cover Letter): ~$0.03-0.06 per letter
- Project 8 (Patient Triage): ~$0.03-0.10 per conversation

### Optional API Keys (for production features)

#### Crunchbase API (for real data in Projects 1 & 7)
- [data.crunchbase.com](https://data.crunchbase.com)

#### Job Board APIs (for Project 5)
- LinkedIn API
- Indeed API
- AngelList API

---

## ⚙️ Configuration

### Streamlit Configuration

The app is configured via `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"  # Brand color
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
port = 8501
enableCORS = false
```

### Customize Branding

Edit `Home.py` and `utils/styling.py` to customize:
- Colors
- Logo
- Company name
- Contact information
- Footer text

---

## 🌍 Alternative Deployment Options

### Option 1: Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create setup.sh
cat > setup.sh << EOF
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
EOF

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: AWS EC2

```bash
# On EC2 instance
sudo apt update
sudo apt install python3-pip python3-venv

# Clone and setup
git clone https://github.com/HPagade/ai-healthtech-projects.git
cd ai-healthtech-projects
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with nohup
nohup streamlit run Home.py --server.port 8501 &
```

### Option 3: Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t ai-healthtech-portfolio .
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key ai-healthtech-portfolio
```

---

## 🔒 Security Best Practices

### Production Checklist

- [ ] Use environment variables for all API keys
- [ ] Never commit secrets to Git
- [ ] Add `.streamlit/secrets.toml` to `.gitignore`
- [ ] Enable HTTPS (automatic on Streamlit Cloud)
- [ ] Set up rate limiting for API calls
- [ ] Add user authentication (if collecting data)
- [ ] Review HIPAA compliance for Projects 4 & 8
- [ ] Add Terms of Service and Privacy Policy
- [ ] Enable error tracking (Sentry, etc.)
- [ ] Set up monitoring and alerts

### Environment Variables

For production, use environment variables:

```python
import os
import streamlit as st

# Get API key from secrets or environment
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
```

---

## 📊 Performance Optimization

### Caching

The app uses Streamlit caching:

```python
@st.cache_data  # Cache data that doesn't change often
def load_data():
    return pd.read_csv('data.csv')

@st.cache_resource  # Cache ML models
def load_model():
    return train_model()
```

### Tips for Better Performance

1. **Cache expensive operations:** Data loading, model training
2. **Minimize rerun triggers:** Use session state wisely
3. **Optimize data loading:** Load only what's needed
4. **Use pagination:** For large datasets
5. **Compress images:** Reduce file sizes
6. **Enable CDN:** For static assets

---

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

#### "API key not found"
Check `.streamlit/secrets.toml` or environment variables

#### "Port already in use"
```bash
streamlit run Home.py --server.port 8502
```

#### Pages not showing
- Ensure `pages/` directory exists
- Check file naming: `1_🚀_YC_Tracker.py`
- Verify `st.set_page_config()` in each page

### Debug Mode

```bash
streamlit run Home.py --logger.level=debug
```

### Check Logs

Streamlit Cloud: **Manage app** → **Logs**

---

## 📈 Monitoring & Analytics

### Streamlit Analytics

Built-in analytics in Streamlit Cloud dashboard:
- Page views
- Active users
- Session duration
- Error rates

### Custom Analytics

Add Google Analytics:

```python
# In Home.py
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

---

## 🔄 Updates & Maintenance

### Updating the App

```bash
# Make changes locally
git add .
git commit -m "Update: [description]"
git push origin main

# Streamlit Cloud will auto-deploy
```

### Rollback

In Streamlit Cloud:
1. Go to **Manage app**
2. Click **Reboot app**
3. Or redeploy previous commit

---

## 📱 Custom Domain Setup

### Streamlit Cloud

1. Go to **App settings** → **General**
2. Click **Set up custom domain**
3. Follow DNS configuration instructions
4. Add CNAME record: `your-domain.com` → `your-app.streamlit.app`

---

## 💰 Cost Considerations

### Streamlit Cloud
- **Free tier:** 1 app, community support
- **Pro:** $20/month, multiple apps, custom domains
- **Enterprise:** Custom pricing

### API Costs (OpenAI)
- **Estimated monthly:** $10-50 depending on usage
- **Per request:** ~$0.03-0.10 (GPT-4)
- **Monitor:** Set up billing alerts

### Other Services
- **Domain:** $10-15/year
- **CDN (optional):** $5-20/month
- **Monitoring (optional):** $0-50/month

---

## 📞 Support & Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [OpenAI API Docs](https://platform.openai.com/docs)

### Community
- [Streamlit Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/HPagade/ai-healthtech-projects/issues)

### Contact
- Email: hannah.pagade@gmail.com
- LinkedIn: [Hannah Pagade](https://linkedin.com/in/hannah-pagade)

---

**Ready to deploy? Follow the Quick Deploy section above to get started!** 🚀
