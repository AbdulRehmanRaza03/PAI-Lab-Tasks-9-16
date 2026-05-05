# 🌤️ Weather App - Real-Time Weather Information

A beautiful, beginner-friendly weather application built with **Python** and **Streamlit** that provides real-time weather data for any city worldwide using the WeatherAPI.com API.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🌍 **Global Coverage** - Get weather data for any city in the world
- 🎨 **Beautiful UI** - Clean, modern interface with gradient cards and smooth animations
- 🌡️ **Detailed Weather Info** - Temperature (°C and °F), humidity, wind speed, pressure, visibility, and UV index
- 🎭 **Dynamic Weather Icons** - Context-aware emoji icons based on weather conditions
- ⚡ **Real-Time Data** - Fetches live weather information from WeatherAPI.com
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- 🔍 **Smart Search** - Input validation and helpful error messages
- ⏳ **Loading Indicators** - Smooth loading animations for better UX
- 🛡️ **Error Handling** - Graceful handling of API errors and edge cases

## 🎯 Demo

[Live Demo](https://weather-2025.streamlit.app/)

### Screenshots

**Main Interface:**
- Clean search interface with city input
- Dynamic weather icons
- Large temperature display
- Gradient location header

**Weather Details:**
- 6 metric cards showing comprehensive weather data
- Professional card-like layout
- Color-coded information

## 🛠️ Tech Stack

- **Python 3.8+** - Programming language
- **Streamlit 1.29.0** - Web framework for building the UI
- **Requests 2.31.0** - HTTP library for API calls
- **WeatherAPI.com** - Weather data provider

## 📋 Prerequisites

Before running this app, make sure you have:

1. Python 3.8 or higher installed
2. pip (Python package manager)
3. A free API key from [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```

### 2. Create a Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your API Key

1. Sign up at [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)
2. Navigate to your account dashboard
3. Copy your API key

### 5. Configure the API Key

Open `app.py` and replace the placeholder with your actual API key:

```python
# Line 47
API_KEY = "your_actual_api_key_here"
```

**🔒 Security Note:** For production deployments, use Streamlit secrets management (see Deployment section).

### 6. Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage

1. **Enter a City Name** - Type any city name in the search field
2. **Click Search** - Press the search button or hit Enter
3. **View Weather Data** - See real-time weather information with beautiful visuals

### Example Searches:
- `London`
- `Tokyo`
- `New York`
- `Paris, France`
- `Sydney, Australia`

## 🌐 Deployment on Streamlit Community Cloud

### Step 1: Prepare Your Repository

1. Create a `.gitignore` file (already included)
2. Push your code to GitHub
3. **DO NOT commit your API key** in the code

### Step 2: Create Streamlit Secrets

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. In the app settings, add your secrets:

```toml
# .streamlit/secrets.toml (this file should NOT be committed)
API_KEY = "your_actual_api_key_here"
```

### Step 3: Update Code for Secrets

Modify `app.py` line 47 to use secrets:

```python
# For local development, use the direct key
# For deployment, use Streamlit secrets
try:
    API_KEY = st.secrets["API_KEY"]
except:
    API_KEY = "YOUR_API_KEY_HERE"  # Fallback for local dev
```

### Step 4: Deploy

1. Select your repository, branch, and main file (`app.py`)
2. Click "Deploy"
3. Wait for the app to build and launch

Your app will be live at: `https://your-app-name.streamlit.app`

## 📁 Project Structure

```
weather-app/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
│
└── .streamlit/            # Streamlit configuration (for deployment)
    ├── config.toml        # App theme and settings
    └── secrets.toml       # API keys (DO NOT COMMIT)
```

## 🎨 Features Breakdown

### Input Validation
- Empty input prevention
- Minimum character requirement (2 chars)
- Numeric-only input rejection
- Whitespace trimming

### Error Handling
- API connection errors
- Invalid city names
- API key issues
- Timeout handling
- Network errors
- Rate limit notifications

### Weather Icons
| Condition | Icon |
|-----------|------|
| Clear/Sunny | ☀️ |
| Cloudy | ☁️ |
| Rain | 🌧️ |
| Thunderstorm | ⛈️ |
| Snow | ❄️ |
| Fog/Mist | 🌫️ |
| Partly Cloudy | ⛅ |

### Weather Metrics Displayed
- 🌡️ Temperature (°C)
- 💧 Humidity (%)
- 💨 Wind Speed (km/h) + Direction
- 🌡️ Atmospheric Pressure (mb)
- 👁️ Visibility (km)
- ☀️ UV Index
- 🌡️ Temperature (°F)
- 🤚 Feels Like Temperature

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues & Future Improvements

### Future Enhancements:
- [ ] 7-day weather forecast
- [ ] Weather alerts and warnings
- [ ] Favorite cities list
- [ ] Dark mode toggle
- [ ] Historical weather data
- [ ] Weather maps integration
- [ ] Multiple language support
- [ ] Export weather data as PDF
- [ ] Geolocation auto-detection

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Portfolio: [yourwebsite.com](https://yourwebsite.com)

## 🙏 Acknowledgments

- [WeatherAPI.com](https://www.weatherapi.com/) for providing free weather data API
- [Streamlit](https://streamlit.io/) for the amazing framework
- The open-source community for inspiration and resources

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting section](#troubleshooting) in the app
2. Open an issue on [GitHub](https://github.com/yourusername/weather-app/issues)
3. Contact via email: your.email@example.com

## 🔧 Troubleshooting

### Common Issues:

**"API key not configured"**
- Make sure you've replaced `YOUR_API_KEY_HERE` with your actual API key

**"City not found"**
- Check spelling
- Try including country name
- Use English city names

**"Connection error"**
- Check your internet connection
- Verify firewall settings
- Try again after a few moments

**"API quota exceeded"**
- Free tier has request limits
- Wait for quota reset or upgrade plan

---

⭐ **If you found this project helpful, please give it a star!** ⭐

Made with ❤️ and Python



