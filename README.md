# Weather Tracking & Prediction Web Application

## 📋 Project Description

This is a full-stack web application that combines **real-time weather data**, **historical weather analysis**, and **simple weather prediction**. Users can search for any city, view current weather conditions, historical temperature records, and get a 7-day weather prediction based on moving averages.

## ✨ Features

- 🌍 **Real-Time Weather:** Fetch current weather from OpenWeatherMap API
- 📊 **Historical Analysis:** Query database for highest/lowest temperatures recorded
- 🔥 **Top 5 Hottest Cities:** View the 5 hottest cities from historical records
- ❄️ **Top 5 Coldest Cities:** View the 5 coldest cities from historical records
- 📈 **Weather Prediction:** Simple 7-day forecast using moving average algorithm
- 💾 **Auto-Save:** Every search is automatically saved to the database
- 🎨 **Beautiful UI:** Modern, responsive design with gradient backgrounds

## 🛠️ Tech Stack

**Backend:**
- Python 3.x
- Flask (Web framework)
- PyODBC (Database connection)
- Requests (API calls)

**Frontend:**
- HTML5
- CSS3 (with gradients and animations)
- JavaScript (Vanilla, no frameworks)

**Database:**
- SQL Server Express 2019
- SQL Server Management Studio (SSMS)

**API:**
- OpenWeatherMap (Real-time weather)


## 🚀 How to Run

### Prerequisites
- Python 3.x installed
- SQL Server Express installed
- SSMS installed
- OpenWeatherMap API key (free from https://openweathermap.org)

### Installation Steps

1. **Clone the repository:**
   bash
   git clone https://github.com/Kartev-v/weather-tracking-prediction-app.git
   cd WeatherApp

2. Install Python dependencies:
   cd backend
pip install requests pyodbc python-dotenv flask flask-cors

3. Create .env file in the root folder:

OPENWEATHER_API_KEY=your_api_key_here
DB_SERVER=.\SQLEXPRESS
DB_NAME=WeatherAppDB
DB_DRIVER=ODBC Driver 17 for SQL Server

4. Import CSV data into SQL Server:

- Open SSMS
- Create database WeatherAppDB
- Create tables using the SQL scripts in backend/weather_app.py
- Import data/weather_data.csv using SSMS Import/Export Wizard

5. Start the backend server:
    cd backend
    python app.py

6. Open in browser:

Go to http://localhost:5000
Start searching for cities! 