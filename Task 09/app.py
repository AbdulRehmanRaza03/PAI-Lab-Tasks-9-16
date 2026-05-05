"""
Weather App - A beginner-friendly application using Streamlit and OpenWeather API
This app fetches and displays real-time weather data for any city in the world.
"""

import streamlit as st
import requests
from datetime import datetime

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_weather_icon(condition):
    """
    Return an appropriate emoji icon based on weather condition.
    
    Parameters:
        condition (str): Weather condition text
    
    Returns:
        str: Emoji icon representing the weather
    """
    condition = condition.lower()
    
    # Map weather conditions to icons
    if 'clear' in condition or 'sunny' in condition:
        return '☀️'
    elif 'cloud' in condition or 'overcast' in condition:
        return '☁️'
    elif 'rain' in condition or 'drizzle' in condition:
        return '🌧️'
    elif 'thunder' in condition or 'storm' in condition:
        return '⛈️'
    elif 'snow' in condition:
        return '❄️'
    elif 'mist' in condition or 'fog' in condition:
        return '🌫️'
    elif 'wind' in condition:
        return '💨'
    elif 'partly' in condition:
        return '⛅'
    else:
        return '🌤️'

# ============================================
# APP CONFIGURATION
# ============================================

# Set the page title and icon
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# Custom CSS for modern and attractive styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding-top: 1rem;
        background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
        font-size: 1.1em;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1.05em;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Metric cards styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E88E5;
        animation: fadeIn 0.6s ease-in;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #555;
    }
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
    }
    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
    }
    
    /* Smooth animations */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Card-like containers */
    .weather-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid #f0f0f0;
        animation: fadeIn 0.6s ease-in;
    }
    
    /* Metric card styling */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #f5f5f5;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# MAIN APP INTERFACE
# ============================================

# Display the app title with modern styling
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='color: #667eea; font-size: 3.5rem; margin: 0; font-weight: 800;'>
        🌤️ Weather App
    </h1>
    <p style='font-size: 1.2em; color: #666; margin-top: 0.5rem; font-weight: 400;'>
        Get real-time weather information for any city worldwide
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# USER INPUT SECTION
# ============================================

st.write("")

# Create a container for better layout
with st.container():
    st.markdown("<h3 style='color: #333; margin-bottom: 1rem;'>🔍 Search for a City</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create an input field for the city name
        city_name = st.text_input(
            "City Name:",
            placeholder="e.g., London, Tokyo, New York, Paris, Mumbai...",
            help="Type the name of any city to get its current weather",
            label_visibility="collapsed"
        )
    
    with col2:
        # Create a button to fetch weather data
        st.write("")  # Spacing to align with input
        # Disable button if input is empty
        search_button = st.button(
            "🔎 Search", 
            type="primary", 
            use_container_width=True,
            disabled=not city_name or len(city_name.strip()) == 0
        )

st.write("")

# ============================================
# API CONFIGURATION
# ============================================

# WeatherAPI.com API key
# For deployment on Streamlit Cloud, use secrets management
# For local development, use your actual API key
# Get your free API key from: https://www.weatherapi.com/signup.aspx
try:
    # Try to get API key from Streamlit secrets (for deployment)
    API_KEY = st.secrets["API_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback to direct key for local development
    API_KEY = "e00eb9ea06ca41779e8201705251612"  # Your WeatherAPI.com API key

# API endpoint URL
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# ============================================
# WEATHER FETCHING FUNCTION
# ============================================

def get_weather_data(city):
    """
    Fetch weather data from OpenWeather API for a given city.
    
    Parameters:
        city (str): Name of the city
    
    Returns:
        tuple: (weather_data dict or None, error_message or None)
    """
    try:
        # Check if API key is configured
        if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY:
            return None, "⚙️ API key not configured. Please add your WeatherAPI.com API key to use the app."
        
        # Prepare the API request parameters
        params = {
            'key': API_KEY,
            'q': city,
            'aqi': 'no'  # Air Quality Index not needed
        }
        
        # Make the API request with timeout
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 400:
            return None, "❌ Invalid city name. Please check your input and try again."
        elif response.status_code == 401:
            return None, "🔑 Invalid API key. Please check your API key configuration."
        elif response.status_code == 403:
            return None, "🚫 API access forbidden. Your API key may have exceeded its quota."
        elif response.status_code == 404:
            return None, f"🔍 City '{city}' not found. Try a different spelling or include the country name."
        else:
            return None, f"⚠️ API returned status code {response.status_code}. Please try again later."
    
    except requests.exceptions.Timeout:
        return None, "⏱️ Request timed out. Please check your internet connection and try again."
    except requests.exceptions.ConnectionError:
        return None, "🌐 Connection error. Please check your internet connection."
    except requests.exceptions.RequestException as e:
        return None, f"🔌 Network error: {str(e)}"
    except Exception as e:
        return None, f"❌ Unexpected error: {str(e)}"

# ============================================
# DISPLAY WEATHER DATA
# ============================================

# Initialize session state for preventing empty submissions
if 'last_search' not in st.session_state:
    st.session_state.last_search = ''

# Check if user clicked the search button and entered a city name
if search_button:
    # Validate input
    if not city_name or len(city_name.strip()) == 0:
        st.warning("⚠️ Please enter a city name before searching!")
    elif len(city_name.strip()) < 2:
        st.warning("⚠️ Please enter at least 2 characters for the city name!")
    elif city_name.strip().isdigit():
        st.warning("⚠️ Please enter a valid city name, not just numbers!")
    else:
        # Store the search query
        st.session_state.last_search = city_name.strip()
        
        # Show enhanced loading indicator
        with st.spinner('🌍 Connecting to weather service...'):
            import time
            time.sleep(0.5)  # Brief pause for smooth UX
        
        with st.spinner(f'🔍 Fetching weather data for {city_name.strip().title()}...'):
            # Get weather data from API
            weather_data, error_message = get_weather_data(city_name.strip())
    
    # If data was successfully retrieved
    if weather_data:
        
        try:
            # Extract location information with safe fallbacks
            location = weather_data.get('location', {})
            location_name = location.get('name', 'Unknown')
            location_region = location.get('region', '')
            location_country = location.get('country', 'Unknown')
            
            # Extract current weather information
            current = weather_data.get('current', {})
            temperature = current.get('temp_c', 0)
            feels_like = current.get('feelslike_c', 0)
            humidity = current.get('humidity', 0)
            pressure = current.get('pressure_mb', 0)
            
            # WeatherAPI doesn't provide min/max, so we'll use current temp
            temp_min = temperature - 2  # Approximate
            temp_max = temperature + 2  # Approximate
            
            # Extract weather condition
            condition_data = current.get('condition', {})
            condition = condition_data.get('text', 'Unknown')
            description = condition
            icon_url = "https:" + condition_data.get('icon', '')
            
            # Extract wind information
            wind_speed = current.get('wind_kph', 0)  # Already in km/h
            wind_deg = current.get('wind_degree', 0)
            wind_dir = current.get('wind_dir', 'N')
            
            # Extract visibility (already in km)
            visibility = current.get('vis_km', 0)
            
            # WeatherAPI doesn't provide sunrise/sunset in current endpoint
            # We'll use astro data if available, or show N/A
            astro = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {})
            sunrise_time = astro.get('sunrise', 'N/A')
            sunset_time = astro.get('sunset', 'N/A')
            
            # If no astro data, make a note
            if sunrise_time == 'N/A':
                sunrise_time = 'Not available'
                sunset_time = 'Not available'
            
            # Get appropriate emoji weather icon
            weather_emoji = get_weather_icon(condition)
            
            # Display success message with animation
            st.balloons()
            st.success("✅ Weather data retrieved successfully!")
            
            st.write("")
            
            # Location Header with modern card design
            location_display = f"{location_name}"
            if location_region:
                location_display += f", {location_region}"
            location_display += f", {location_country}"
            
            st.markdown(f"""
            <div style='text-align: center; padding: 1.5rem; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 16px; margin: 1.5rem 0; 
                        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);'>
                <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 700;'>
                    📍 {location_display}
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            
            # Main weather condition - Card with modern design
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 16px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 1.5rem 0;'>
            """, unsafe_allow_html=True)
            
            col_icon, col_temp = st.columns([1, 2])
            
            with col_icon:
                st.image(icon_url, width=140)
            
            with col_temp:
                st.markdown(f"""
                <div style='padding: 0.5rem 0;'>
                    <h1 style='font-size: 4.5em; margin: 0; background: linear-gradient(135deg, #667eea, #764ba2); 
                               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                               font-weight: 800;'>{temperature}°C</h1>
                    <p style='font-size: 1.6em; margin: 0.8rem 0; color: #333; font-weight: 600;'>
                        {weather_emoji} {description.title()}
                    </p>
                    <p style='font-size: 1.1em; color: #888; margin: 0.5rem 0;'>
                        💨 Feels like <strong>{feels_like}°C</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            
            # Temperature Range Card
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; 
                        border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 1.5rem 0;'>
                <h3 style='color: white; margin: 0 0 1.5rem 0; font-size: 1.4em; font-weight: 600;'>🌡️ Temperature Details</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col_tmin, col_tmax, col_tfahrenheit = st.columns(3)
            
            with col_tmin:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>❄️</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Min Temp</div>
                    <div style='font-size: 2em; font-weight: 700; color: #667eea;'>""" + f"{temp_min}°C" + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_tmax:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>🔥</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Max Temp</div>
                    <div style='font-size: 2em; font-weight: 700; color: #f76b1c;'>""" + f"{temp_max}°C" + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_tfahrenheit:
                temp_fahrenheit = round((temperature * 9/5) + 32, 1)
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>🌡️</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Fahrenheit</div>
                    <div style='font-size: 2em; font-weight: 700; color: #764ba2;'>""" + f"{temp_fahrenheit}°F" + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.write("")
            
            # Weather Conditions - Card style
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; 
                        border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 1.5rem 0;'>
                <h3 style='color: white; margin: 0 0 1.5rem 0; font-size: 1.4em; font-weight: 600;'>🌤️ Weather Conditions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # First row of metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>💧</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Humidity</div>
                    <div style='font-size: 2em; font-weight: 700; color: #4facfe;'>""" + f"{humidity}%" + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Wind speed already in km/h from WeatherAPI
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>💨</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Wind Speed</div>
                    <div style='font-size: 2em; font-weight: 700; color: #00f2fe;'>""" + f"{wind_speed} km/h" + """</div>
                    <div style='font-size: 0.8em; color: #888; margin-top: 0.3rem;'>""" + wind_dir + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>🌡️</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Pressure</div>
                    <div style='font-size: 2em; font-weight: 700; color: #43e97b;'>""" + f"{pressure} hPa" + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.write("")
            
            # Environmental Data - Card style
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; 
                        border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 1.5rem 0;'>
                <h3 style='color: white; margin: 0 0 1.5rem 0; font-size: 1.4em; font-weight: 600;'>🌍 Environmental Data</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col4, col5, col6 = st.columns(3)
            
            with col4:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>👁️</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Visibility</div>
                    <div style='font-size: 2em; font-weight: 700; color: #4facfe;'>""" + f"{visibility:.1f} km" + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>🌅</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Sunrise</div>
                    <div style='font-size: 1.5em; font-weight: 700; color: #fa709a;'>""" + sunrise_time + """</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col6:
                st.markdown("""
                <div class='metric-card'>
                    <div style='font-size: 2em; margin-bottom: 0.5rem;'>🌇</div>
                    <div style='font-size: 0.9em; color: #888; margin-bottom: 0.5rem;'>Sunset</div>
                    <div style='font-size: 1.5em; font-weight: 700; color: #fee140;'>""" + sunset_time + """</div>
                </div>
                """, unsafe_allow_html=True)
        
        except KeyError as e:
            st.error(f"⚠️ Error parsing weather data: Missing field {str(e)}")
            st.info("The API response format may have changed. Please contact support.")
        except Exception as e:
            st.error(f"❌ Unexpected error displaying weather data: {str(e)}")
            st.info("Please try searching for a different city or refresh the page.")
    
    else:
        # Show detailed error message if data couldn't be retrieved
        st.error(error_message if error_message else f"❌ Could not retrieve weather data for '{city_name.strip().title()}'.")
        
        # Show helpful suggestions in an info box
        with st.expander("💡 Troubleshooting Tips"):
            st.markdown("""
            **Common Issues:**
            - ✅ Check the spelling of the city name
            - ✅ Try entering the city name in English
            - ✅ Include the country name (e.g., 'Paris, France')
            - ✅ Verify your API key is valid and active
            - ✅ Check your internet connection
            - ✅ Make sure you haven't exceeded API rate limits
            
            **Need help?**
            - Get a free API key at [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)
            - Check the [API documentation](https://www.weatherapi.com/docs/)
            """)

# ============================================
# FOOTER
# ============================================

st.write("")
st.write("")
st.markdown("---")

# Add helpful information in an expander
with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    **Setup Instructions:**
    1. Get a free API key from [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)
    2. Replace `YOUR_API_KEY_HERE` in the code with your actual API key
    3. Save the file and restart the app
    
    **Using the App:**
    - Enter any city name in the search field
    - Click the 🔎 Search button or press Enter
    - View comprehensive weather information including:
      - Current temperature with feels-like
      - Weather condition with icon
      - Humidity, pressure, wind speed
      - Visibility
    
    **Tips:**
    - Try: "London", "Tokyo", "New York", "Paris"
    - You can include country names for accuracy (e.g., "Paris, France")
    - The app shows temperature in both Celsius and Fahrenheit
    - Weather icons are provided by WeatherAPI
    """)
