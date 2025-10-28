# 🚀 Deploy Your AI Healthtech Portfolio to Streamlit Cloud

## ✅ Your App is Ready!

All 8 projects are built and ready to deploy. Follow these exact steps:

---

## Step-by-Step Deployment

### 1️⃣ Go to Streamlit Cloud

Open: **[share.streamlit.io](https://share.streamlit.io)**

- Sign in with your GitHub account
- Authorize Streamlit to access your repositories

### 2️⃣ Create New App

Click the **"New app"** button (big blue button in top right)

### 3️⃣ Fill in Deployment Settings

**IMPORTANT - Use these exact values:**

```
Repository: HPagade/ai-healthtech-projects
Branch: main
Main file path: Home.py
App URL: (choose your custom name)
```

**Screenshot guide:**
- Repository dropdown → select "HPagade/ai-healthtech-projects"
- Branch → type "main"
- Main file path → type "Home.py" (case sensitive!)
- Advanced settings → leave as default (Python 3.9)

### 4️⃣ Click "Deploy"

Streamlit will now:
- Install dependencies from requirements.txt
- Start your app
- Give you a live URL

**This takes 2-5 minutes** - you'll see a progress indicator

---

## 🔧 Common Deployment Errors & Fixes

### Error: "Repository not found"
**Fix:** Make sure you've authorized Streamlit to access your GitHub repos
- Go to Settings → Connected accounts → Reconnect GitHub

### Error: "ModuleNotFoundError"
**Fix:** This means requirements.txt wasn't found
- Double-check Branch is set to "main"
- Verify requirements.txt exists in root directory

### Error: "File Home.py not found"
**Fix:** Check the exact spelling and case
- Must be: `Home.py` (capital H)
- Not: `home.py` or `HOME.py`

### Error: "App failed to load - Python version"
**Fix:** Set Python version in Advanced settings
- Click "Advanced settings"
- Python version: 3.9

### Error: "Import error in pages"
**Fix:** This is usually okay - refresh after 30 seconds
- Streamlit takes time to set up multi-page apps
- If persists, check that pages/ directory exists on GitHub

---

## ⚙️ Optional: Add API Keys for AI Features

**Projects 3 & 8 need OpenAI API key** (Projects 1,2,4,5,6,7 work without it)

### To Add API Key:

1. After deployment, click your app
2. Click **"⋮ Menu"** (three dots) → **"Settings"**
3. Go to **"Secrets"** tab
4. Paste this:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

5. Click **"Save"**
6. App will automatically restart

**Get OpenAI API key:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## 🎯 What You'll See After Deployment

### Home Page
- Overview of all 8 projects
- Professional navigation
- Metrics dashboard

### 8 Interactive Pages
1. YC Tracker - Startup analysis
2. Health Score - Churn prediction
3. Cover Letter - AI writing (needs API key)
4. Clinical Support - Symptom checker
5. Job Analysis - Market insights
6. Product Teardown - Analysis framework
7. Funding Analysis - Investment trends
8. Patient Triage - AI chatbot (needs API key)

---

## 🐛 Still Having Issues?

### Check Deployment Logs

In Streamlit Cloud:
1. Click your app
2. Click **"Manage app"** (bottom right)
3. View **"Logs"** tab
4. Look for error messages

### Common Log Errors:

**"No module named 'streamlit'"**
→ requirements.txt not found - verify branch is "main"

**"FileNotFoundError: pages/"**
→ pages/ directory not on GitHub - verify commit was pushed

**"Import error from utils"**
→ utils/ directory not on GitHub - verify commit was pushed

### Force Refresh

If app seems stuck:
1. Go to **"Manage app"**
2. Click **"Reboot app"**
3. Wait 1-2 minutes

---

## ✅ Verification Checklist

Before deploying, verify on GitHub:

- [ ] Repository: `HPagade/ai-healthtech-projects` exists
- [ ] Branch `main` exists
- [ ] File `Home.py` exists in root
- [ ] Folder `pages/` exists with 8 .py files
- [ ] Folder `utils/` exists with helpers
- [ ] File `requirements.txt` exists in root
- [ ] File `.streamlit/config.toml` exists

**Check on GitHub:** https://github.com/HPagade/ai-healthtech-projects

---

## 🎉 After Successful Deployment

Your app URL will be: `https://[your-custom-name].streamlit.app`

### Share Your Portfolio:
- Add to LinkedIn
- Add to resume
- Share with clients/employers
- Use in demos

### Customize (Optional):
1. **Custom Domain:**
   - Settings → General → Set up custom domain

2. **Make App Public/Private:**
   - Settings → Sharing → Set visibility

3. **Update Your App:**
   - Just push to GitHub main branch
   - Streamlit auto-deploys changes

---

## 📞 Need Help?

**Streamlit Documentation:**
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Troubleshooting](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/troubleshoot-deployment)

**Your Repository:**
- [GitHub Repo](https://github.com/HPagade/ai-healthtech-projects)
- [Issues](https://github.com/HPagade/ai-healthtech-projects/issues)

**Streamlit Community:**
- [Forum](https://discuss.streamlit.io)

---

## 🚀 Ready to Deploy!

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Fill in:
   - Repository: HPagade/ai-healthtech-projects
   - Branch: main
   - Main file: Home.py
4. Click "Deploy"
5. Wait 2-5 minutes
6. Your app is live!

**Good luck! 🎉**
