# 🏥 AI Healthtech Projects - Streamlit Deployment

## Quick Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud
Visit [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub

### Step 2: Deploy New App
1. Click **"New app"**
2. Repository: `HPagade/ai-healthtech-projects`
3. Branch: **main**
4. Main file path: **Home.py**
5. Click **"Deploy"**

### Step 3: Configure Secrets (Optional - for AI features)
In Streamlit Cloud dashboard:
- Go to **App settings → Secrets**
- Add:
```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

## Your App Structure

```
Home.py              ← Main entry point (START HERE)
├── pages/           ← 8 project pages
│   ├── 1_🚀_YC_Tracker.py
│   ├── 2_📊_Health_Score.py
│   ├── 3_🤖_Cover_Letter.py
│   ├── 4_🏥_Clinical_Support.py
│   ├── 5_📈_Job_Analysis.py
│   ├── 6_💡_Product_Teardown.py
│   ├── 7_💰_Funding_Analysis.py
│   └── 8_🤖_Patient_Triage.py
└── utils/           ← Shared functions
```

## What Works Without API Key

✅ Projects 1, 2, 4, 5, 6, 7 - Work immediately
⚠️ Projects 3, 8 - Need OpenAI API key

## Troubleshooting

### "App is having trouble loading"
- Check Streamlit Cloud logs
- Verify all files committed and pushed
- Check requirements.txt is present

### "Module not found"
- Ensure requirements.txt is in root directory
- Check spelling of packages

### "Page not found"
- Verify pages/ directory exists
- Check file names match pattern: `1_emoji_Name.py`

## Testing Locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Support

- Deployment issues: Check DEPLOYMENT.md
- Streamlit docs: https://docs.streamlit.io
- This repo issues: https://github.com/HPagade/ai-healthtech-projects/issues

---

**Your app will be live at:** `https://your-app-name.streamlit.app`
