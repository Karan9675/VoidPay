from fastapi import FastAPI
import joblib
import time
import threading
import pandas as pd
import requests

# 🔥 PUT YOUR API KEY HERE
API_KEY = "f610299e9be04adf5ae892e26403493b"

app = FastAPI()

# Load ML model
model = joblib.load("risk_model.pkl")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow headers=["*"1,
                   )
# Simulated user data
user_data = {
    "city": "delhi",
    "plan": "pro"
}

# Store last payout
last_payout = None

# last_fetch_time = 0
cached_data = {}


# 🔹 Premium Calculation
def calculate_premium(risk, aqi, rain, duration):
    base = 50

    if risk == "High":
        base += 70
    elif risk == "Medium":
        base += 30

    if rain == 1:
        base += 10
    if duration >= 4:
        base += 10
    if aqi > 400:
        base += 20

    return base


# 🔹 REAL API FUNCTION
def get_city_data(city: str):
    global cached_data

    try:
        # ✅ USE CACHE (avoid too many API calls)
        if city in cached_data and time.time() - cached_data[city]["time"] < 30:
            return cached_data[city]["data"]

        # 🌍 Step 1: Get coordinates
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_data = requests.get(geo_url, timeout=5).json()

        print("Geo API Response:", geo_data)

        if not geo_data:
            print("❌ City not found")
            return 200, 30, 0, 1, 1

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # 🌦 Step 2: Get weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_data = requests.get(weather_url, timeout=5).json()

        temp = weather_data["main"]["temp"]
        rain = 1 if "rain" in weather_data else 0

        # 🌫 Step 3: Get pollution
        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        aqi_data = requests.get(aqi_url, timeout=5).json()

        pm25 = aqi_data["list"][0]["components"]["pm2_5"]

        # Convert PM2.5 → AQI approx
        aqi = int(pm25 * 10)

        # Simulated duration & time
        duration = 3 if rain else 1
        time_val = 2

        print(f"[VOIDPAY] {city} → AQI={aqi}, Temp={temp}, Rain={rain}")

        # ✅ SAVE TO CACHE
        cached_data[city] = {
            "data": (aqi, temp, rain, duration, time_val),
            "time": time.time()
}

        return cached_data[city]["data"]

    except Exception as e:
        print("⚠ API FAILED:", e)
        return 200, 30, 0, 1, 1


# 🔹 BACKGROUND AUTO MONITORING
def monitor_user():
    global last_payout

    while True:
        city = user_data["city"]

        aqi, temp, rain, duration, time_val = get_city_data(city)

        data = pd.DataFrame(
            [[aqi, temp, rain, duration, time_val]],
            columns=["AQI", "Temperature", "Rain", "Duration", "TimeOfDay"]
        )

        result = model.predict(data)

        labels = {0: "Low", 1: "Medium", 2: "High"}
        risk = labels[result[0]]

        if risk == "High":
            payout = 400
            last_payout = payout
            print(f"🚨 AUTO PAYOUT TRIGGERED: ₹{payout} due to {risk} risk")

        time.sleep(60)


# 🔹 MANUAL TEST API
@app.get("/predict")
def predict(aqi: int, temp: int, rain: int, duration: int, time: int):

    data = pd.DataFrame(
        [[aqi, temp, rain, duration, time]],
        columns=["AQI", "Temperature", "Rain", "Duration", "TimeOfDay"]
    )

    result = model.predict(data)

    labels = {0: "Low", 1: "Medium", 2: "High"}
    risk = labels[result[0]]

    premium = calculate_premium(risk, aqi, rain, duration)

    payout = 0
    if risk == "High":
        payout = 400
    elif risk == "Medium":
        payout = 200

    return {
        "AQI": aqi,
        "Risk": risk,
        "Premium (weekly)": premium,
        "Payout": payout
    }


# 🔹 DASHBOARD API
@app.get("/dashboard")
def dashboard(city: str = "delhi"):
    city = city.lower()

    aqi, temp, rain, duration, time_val = get_city_data(city)

    data = pd.DataFrame(
        [[aqi, temp, rain, duration, time_val]],
        columns=["AQI", "Temperature", "Rain", "Duration", "TimeOfDay"]
    )

    result = model.predict(data)

    labels = {0: "Low", 1: "Medium", 2: "High"}
    risk = labels[result[0]]

    premium = calculate_premium(risk, aqi, rain, duration)

    return {
        "City": city,
        "AQI": aqi,
        "Risk": risk,
        "Premium": premium,
        "Payout": last_payout,
        "Status": "Monitoring"
    }


# 🔹 START BACKGROUND THREAD
@app.on_event("startup")
def start_monitoring():
    threading.Thread(target=monitor_user, daemon=True).start()
