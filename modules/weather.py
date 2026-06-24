import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("❌ WEATHER_API_KEY not found in .env file")


# =========================
# CURRENT WEATHER
# =========================
def get_weather(city: str):

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return None

        return {
            "City": city,
            "Temperature (°C)": data["main"]["temp"],
            "Feels Like (°C)": data["main"]["feels_like"],
            "Humidity (%)": data["main"]["humidity"],
            "Condition": data["weather"][0]["description"],
            "Wind Speed (m/s)": data["wind"]["speed"]
        }

    except Exception:
        return None


# =========================
# FORECAST
# =========================
def get_weather_for_travel_date(city: str, travel_date: str):

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return []

        result = []

        for item in data.get("list", []):
            if travel_date in item.get("dt_txt", ""):
                result.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "weather": item["weather"][0]["description"]
                })

        return result

    except Exception:
        return []