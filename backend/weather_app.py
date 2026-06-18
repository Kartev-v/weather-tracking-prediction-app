import os
from datetime import datetime
import pyodbc
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")


def get_db_connection():
    try:
        connection = pyodbc.connect(
            f"Driver={DB_DRIVER};"
            f"Server={DB_SERVER};"
            f"Database={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        return connection
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None


def get_current_weather(city_name):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"], 1),
                "description": data["weather"][0]["description"],
                "pressure": data["main"]["pressure"],
            }
            return weather_info
        else:
            print(f"❌ City not found on OpenWeatherMap: {city_name}")
            return None

    except requests.exceptions.Timeout:
        print(f"❌ API Request Timeout for: {city_name}")
        return None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None


def save_user_search(
    city_name, temperature, humidity, wind_speed, description
):
    connection = get_db_connection()

    if connection is None:
        print("⚠️ Database unavailable - search not saved")
        return False

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO UserSearches (city_name, temperature, humidity, wind_speed, description)
            VALUES (?, ?, ?, ?, ?)
        """,
            (city_name, temperature, humidity, wind_speed, description),
        )

        connection.commit()
        print(f"✅ Search saved: {city_name}")
        return True

    except Exception as e:
        print(f"❌ Error saving search: {e}")
        return False
    finally:
        connection.close()


def get_top_5_hottest_cities():
    connection = get_db_connection()
    
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT TOP 5 station_name, MAX(max_temp) as highest_temp
            FROM HistoricalWeatherData
            WHERE max_temp <= 60 AND max_temp IS NOT NULL
            GROUP BY station_name
            ORDER BY highest_temp DESC
        """)
        
        results = cursor.fetchall()
        
        cities = []
        for row in results:
            cities.append({
                "name": row[0] if row[0] else "Unknown",
                "temp": round(float(row[1]), 1) if row[1] else 0
            })
        
        return cities
        
    except Exception as e:
        print(f"❌ Error fetching hottest cities: {e}")
        return []
    finally:
        connection.close()


def get_top_5_coldest_cities():
    connection = get_db_connection()
    
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT TOP 5 station_name, MIN(min_temp) as lowest_temp
            FROM HistoricalWeatherData
            WHERE min_temp >= -50 AND min_temp IS NOT NULL
            GROUP BY station_name
            ORDER BY lowest_temp ASC
        """)
        
        results = cursor.fetchall()
        
        cities = []
        for row in results:
            cities.append({
                "name": row[0] if row[0] else "Unknown",
                "temp": round(float(row[1]), 1) if row[1] else 0
            })
        
        return cities
        
    except Exception as e:
        print(f"❌ Error fetching coldest cities: {e}")
        return []
    finally:
        connection.close()


def get_highest_temp_for_city(city_name):
    connection = get_db_connection()
    
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT TOP 1 station_name, MAX(max_temp) as highest_temp
            FROM HistoricalWeatherData
            WHERE LOWER(station_name) LIKE LOWER(?)
            AND max_temp <= 60
            AND max_temp IS NOT NULL
            GROUP BY station_name
            ORDER BY highest_temp DESC
        """, (f"%{city_name}%",))
        
        result = cursor.fetchone()
        
        if result:
            return {
                "station": result[0] if result[0] else "Unknown",
                "temp": round(float(result[1]), 1) if result[1] else None
            }
        return None
        
    except Exception as e:
        print(f"❌ Error fetching highest temp: {e}")
        return None
    finally:
        connection.close()


def get_lowest_temp_for_city(city_name):
    connection = get_db_connection()
    
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT TOP 1 station_name, MIN(min_temp) as lowest_temp
            FROM HistoricalWeatherData
            WHERE LOWER(station_name) LIKE LOWER(?)
            AND min_temp >= -50
            AND min_temp IS NOT NULL
            GROUP BY station_name
            ORDER BY lowest_temp ASC
        """, (f"%{city_name}%",))
        
        result = cursor.fetchone()
        
        if result:
            station_name = result[0] if result[0] else "Unknown"
            lowest_temp = result[1]
            
            if lowest_temp is not None:
                return {
                    "station": station_name,
                    "temp": round(float(lowest_temp), 1)
                }
            else:
                print(f"⚠️ Temperature is None for city: {city_name}")
                return None
        else:
            print(f"⚠️ No data found for city: {city_name}")
            return None
        
    except Exception as e:
        print(f"❌ Error fetching lowest temp: {e}")
        return None
    finally:
        connection.close()


def predict_future_weather(city_name, days_ahead=7):
    connection = get_db_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT 
                AVG((max_temp + min_temp) / 2.0) as avg_temp,
                AVG(max_temp) as avg_max,
                AVG(min_temp) as avg_min,
                AVG(wind_speed) as avg_wind
            FROM HistoricalWeatherData
            WHERE LOWER(station_name) LIKE LOWER(?)
            AND max_temp <= 60 AND min_temp >= -50
        """, (f"%{city_name}%",))
        
        row = cursor.fetchone()
        
        if row and row.avg_temp is not None:
            prediction = {
                "city": city_name,
                "days_predicted_ahead": days_ahead,
                "predicted_temp": round(float(row.avg_temp), 1),
                "predicted_max_temp": round(float(row.avg_max), 1) if row.avg_max else 0,
                "predicted_min_temp": round(float(row.avg_min), 1) if row.avg_min else 0,
                "predicted_wind_speed": round(float(row.avg_wind), 1) if row.avg_wind else 0,
                "method": "Historical Moving Average"
            }
            return prediction
        else:
            print(f"⚠️ No historical data available to make a prediction for: {city_name}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating prediction: {e}")
        return None
    finally:
        connection.close()