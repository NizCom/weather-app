from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

load_dotenv()
api_key = os.getenv('API_KEY')


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        weather = {
            'city': data['location']['name'],
            'country': data['location']['country'],
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'icon': data['current']['condition']['icon']
        }
        return jsonify(weather), 200
    else:
        return jsonify({'error': 'City not found or an error occurred'}), 404


if __name__ == '__main__':
    app.run(debug=True)
