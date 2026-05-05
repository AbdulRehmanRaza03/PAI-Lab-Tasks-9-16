# Weather App - Deployment Guide

## 🚀 Quick Deployment to Streamlit Cloud

Follow these steps to deploy your Weather App to Streamlit Community Cloud:

### Prerequisites
- GitHub account
- WeatherAPI.com API key
- Streamlit Cloud account (free)

### Step-by-Step Guide

#### 1. Prepare Your GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit - Weather App"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/yourusername/weather-app.git
git branch -M main
git push -u origin main
```

#### 2. Sign in to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Authorize Streamlit to access your repositories

#### 3. Deploy Your App

1. Click **"New app"** button
2. Select your repository: `yourusername/weather-app`
3. Choose branch: `main`
4. Set main file path: `app.py`
5. Click **"Advanced settings"**

#### 4. Configure Secrets

In the Advanced settings, add your secrets:

```toml
[default]
API_KEY = "your_actual_api_key_here"
```

#### 5. Deploy

1. Click **"Deploy!"**
2. Wait 2-3 minutes for the app to build
3. Your app will be live at: `https://your-app-name.streamlit.app`

## 🔧 Local Testing Before Deployment

Test your app locally to ensure everything works:

```bash
# Activate your virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Run the app
streamlit run app.py
```

## 📝 Environment Variables

### Local Development
Edit `app.py` and replace:
```python
API_KEY = "YOUR_API_KEY_HERE"
```

### Production (Streamlit Cloud)
The app automatically uses `st.secrets["API_KEY"]` when deployed.

## 🔄 Updating Your Deployment

To update your live app:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push

# Streamlit Cloud will automatically redeploy
```

## 🎯 Custom Domain (Optional)

To use a custom domain:

1. Go to your app settings on Streamlit Cloud
2. Navigate to "General" → "Custom domain"
3. Follow the instructions to configure your DNS

## 🐛 Troubleshooting Deployment

### Build Fails
- Check `requirements.txt` has correct versions
- Verify all files are committed to Git
- Check deployment logs for specific errors

### App Crashes
- Verify API key is correctly set in secrets
- Check for syntax errors in `app.py`
- Review error logs in Streamlit Cloud dashboard

### Secrets Not Working
- Ensure secrets are in the correct format (TOML)
- Check for typos in key names
- Secrets are case-sensitive

## 📊 Monitoring Your App

Streamlit Cloud provides:
- Real-time logs
- Usage analytics
- Error tracking
- Resource usage monitoring

Access these in your app dashboard.

## 💰 Pricing & Limits

**Free Tier Includes:**
- 1 app
- Unlimited viewers
- 1 GB RAM
- Community support

**Upgrade for:**
- More apps
- More resources
- Private apps
- Priority support

## 🔒 Security Best Practices

1. ✅ Never commit API keys to Git
2. ✅ Use Streamlit secrets for sensitive data
3. ✅ Keep dependencies updated
4. ✅ Monitor API usage and costs
5. ✅ Use environment-specific configurations

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [WeatherAPI Documentation](https://www.weatherapi.com/docs/)

---

Need help? Open an issue on GitHub or contact support!
