from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.JustADB

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

if __name__ == "__main__":
    app.run(debug=True)