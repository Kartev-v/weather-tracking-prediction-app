from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from weather_app import (
    get_current_weather,
    save_user_search,
    get_top_5_hottest_cities,
    get_top_5_coldest_cities,
    get_highest_temp_for_city,
    get_lowest_temp_for_city,
    predict_future_weather
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()
    
    if not city:
        return jsonify({"success": False, "message": "City name required"}), 400
    
    try:
        weather = get_current_weather(city)
        
        if not weather:
            return jsonify({"success": False, "message": "City not found"}), 404
        
        save_user_search(
            city,
            weather.get('temperature', 0),
            weather.get('humidity', 0),
            weather.get('wind_speed', 0),
            weather.get('description', '')
        )
        
        highest_temp = get_highest_temp_for_city(city)
        lowest_temp = get_lowest_temp_for_city(city)
        prediction = predict_future_weather(city)
        
        return jsonify({
            "success": True,
            "weather": weather,
            "highest_temp": highest_temp,
            "lowest_temp": lowest_temp,
            "prediction": prediction
        })
    
    except Exception as e:
        print(f"❌ Error in /api/weather: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@app.route('/api/hottest-cities', methods=['GET'])
def get_hottest_cities():
    try:
        cities = get_top_5_hottest_cities()
        return jsonify({"success": True, "cities": cities})
    except Exception as e:
        print(f"❌ Error in /api/hottest-cities: {e}")
        return jsonify({"success": False, "message": "Error fetching hottest cities"}), 500

@app.route('/api/coldest-cities', methods=['GET'])
def get_coldest_cities():
    try:
        cities = get_top_5_coldest_cities()
        return jsonify({"success": True, "cities": cities})
    except Exception as e:
        print(f"❌ Error in /api/coldest-cities: {e}")
        return jsonify({"success": False, "message": "Error fetching coldest cities"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"success": True, "message": "Server is running!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)