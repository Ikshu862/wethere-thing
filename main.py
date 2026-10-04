import streamlit as st
import time
import json
import requests
import pandas as pd

st.write("Weather DB")
country = st.selectbox("Select your country", ["ambalangoda", "Colombo", "Galle", "Italy", "Germany", "France", "UK", "Australia", "canada"])

st.sidebar.write("Weather DB")
if st.sidebar.button("How to use this app"):
    st.video("vid.mp4")

# Sidebar navigation should be global so it initializes immediately
selectbox_option = st.sidebar.selectbox(
    'Select data to visualize',
    ('Temperature', 'UV Index', 'Precipitation')
)

# Geographic Coordinate mappings
if country == "ambalangoda":
    lat, lon = 6.2355, 80.0525
elif country == "Colombo":
    lat, lon = 6.9271, 79.8612
elif country == "Galle":
    lat, lon = 6.0517, 80.2214
elif country == "Italy":
    lat, lon = 41.8719, 12.5674   
elif country == "Germany":
    lat, lon = 51.1657, 10.4515
elif country =="France":
    lat, lon = 46.6034, 1.8883
elif country == "UK":
    lat, lon = 55.3781, -3.4360 # Fixed negative longitude
elif country == "Australia":
    lat, lon = -25.2744, 133.7751 # Added negative sign for Southern Hemisphere lat
elif country == "canada":
    lat, lon = 56.1304, -106.3468 # Fixed negative longitude
elif country == "China":
    lat, lon = 35.8617, 104.1954
elif country == "USA":
    lat, lon = 37.0902, -95.7129 # Fixed negative longitude
elif country == "Russia":
    lat, lon = 61.5240, 105.3188
elif country == "Japan":
    lat, lon = 36.2048, 138.2529

# Fetching the weather API payload
resp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_max,uv_index_clear_sky_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration,sunrise,sunset,daylight_duration,sunshine_duration,moonrise,moonset,moon_phase,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,visibility,evapotranspiration,et0_fao_evapotranspiration,cloud_cover_high,vapour_pressure_deficit,wind_speed_10m,wind_speed_120m,wind_speed_80m,wind_speed_180m,wind_direction_10m,wind_direction_80m,wind_direction_180m,wind_direction_120m,wind_gusts_10m,temperature_80m,temperature_120m,temperature_180m,soil_temperature_0cm,soil_temperature_18cm,soil_temperature_6cm,soil_temperature_54cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm,soil_moisture_27_to_81cm&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,wind_speed_10m,wind_direction_10m,wind_gusts_10m,rain,precipitation,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure")
data = json.loads(resp.text)
temp = data['current']['temperature_2m']

if st.button("Get Weather Data"):
   st.metric(label="Temperature", value=f"{temp} °C")
   st.metric(label="Humidity", value=f"{data['current']['relative_humidity_2m']} %") 
   
   if data['current']['is_day'] == 1:
         st.write("It is Daytime")
   else:
         st.write("It is Nighttime")    
         
   st.metric(label="Precipitation", value=f"{data['current']['precipitation']} mm")  
   st.metric(label="Time", value=time.ctime())

# ---------- Prepare DataFrames ----------
dates = data["daily"]["time"]
temp_df = pd.DataFrame({
    "Date": dates,
    "Max Temperature (°C)": data["daily"]["temperature_2m_max"]
})
uv_df = pd.DataFrame({
    "Date": dates,
    "UV Index": data["daily"]["uv_index_max"]
})
precip_df = pd.DataFrame({
    "Date": dates,
    "Precipitation (mm)": data["daily"]["precipitation_sum"] # Fixed 'data' addition here
})

# ---------- Line Chart Display ----------
if selectbox_option == "Temperature":
    st.line_chart(temp_df.set_index("Date"))
elif selectbox_option == "UV Index":
    st.line_chart(uv_df.set_index("Date"))
else:
    st.line_chart(precip_df.set_index("Date"))
