from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Get the OpenWeather API key from the environment
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_URL = os.getenv('OPENWEATHER_URL')

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Function to fetch weather data
    def get_weather_data(endpoint, params):
        params['appid'] = OPENWEATHER_API_KEY
        response = requests.get(OPENWEATHER_URL + endpoint, params=params)
        return response.json()

    # Weather API endpoint
    @app.route("/weathers", methods=["GET"])
    def get_weather():
        return {"message": "Weather API response"}

    # Root endpoint
    @app.route("/", methods=["GET"])
    def root():
        return {"message": "Welcome"}

    # Current weather endpoint
    @app.route('/weather', methods=['GET'])
    def current_weather():
        city = request.args.get('city', 'London')  # Default to 'London' if no city is provided
        country = request.args.get('country', 'GB')  # Default to 'GB' (United Kingdom) if no country is provided
        params = {'q': f'{city},{country}', 'units': 'metric'}  # City and country in the format 'city,country'
        
        data = get_weather_data('weather', params)
        
        if data.get('cod') != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch weather data')}), 400

        weather_info = {
            'city': city,
            'country': country,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
        }
        return jsonify(weather_info)

    # Hourly forecast endpoint
    @app.route('/forecast/hourly', methods=['GET'])
    def hourly_forecast():
        city = request.args.get('city', 'London')
        country = request.args.get('country', 'GB')
        params = {'q': f'{city},{country}', 'units': 'metric'}
        data = get_weather_data('forecast', params)
        
        if data.get('cod') != '200':
            return jsonify({'error': data.get('message', 'Failed to fetch forecast data')}), 400

        hourly_data = []
        for item in data['list'][:8]:  # Get the next 8 hours
            hourly_data.append({
                'time': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
            })

        return jsonify(hourly_data)

    # Daily forecast endpoint
    @app.route('/forecast/daily', methods=['GET'])
    def daily_forecast():
        city = request.args.get('city', 'London')
        country = request.args.get('country', 'GB')
        params = {'q': f'{city},{country}', 'units': 'metric', 'cnt': 7}  # Get a 7-day forecast
        data = get_weather_data('forecast/daily', params)
        
        if data.get('cod') != '200':
            return jsonify({'error': data.get('message', 'Failed to fetch forecast data')}), 400

        daily_data = []
        for item in data['list']:
            daily_data.append({
                'date': item['dt'],
                'temperature_max': item['temp']['max'],
                'temperature_min': item['temp']['min'],
                'description': item['weather'][0]['description'],
            })

        return jsonify(daily_data)

    return app


# Current Weather:

# http://127.0.0.1:5000/weather?city=Paris&country=FR (for Paris, France)
# http://127.0.0.1:5000/weather?city=New York&country=US (for New York, USA)
# Hourly Forecast:

# http://127.0.0.1:5000/forecast/hourly?city=Paris&country=FR
# Daily Forecast:

# http://127.0.0.1:5000/forecast/daily?city=Paris&country=FR
