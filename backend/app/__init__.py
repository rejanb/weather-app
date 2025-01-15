from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    @app.route("/weather", methods=["GET"])
    def get_weather():
        return {"message": "Weather API response"}

    @app.route("/", methods=["GET"])
    def root():
        return {"message": "Welcome"}

    return app
