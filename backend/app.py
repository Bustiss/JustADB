from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
bqrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") # secret key for JWT( JSON Web Token)
jwt = JWTManager(app)


# Load environment variables from .env file
load_dotenv()

# MongoDB connection string
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.JustADB
users = db.users

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check if user already exists
    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists!"}), 400
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    users.insert_one({"email": email, "password": hashed_password})
    return jsonify({"message": "User created successfully!"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check if user exists
    user = users.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401
    
    # Create access token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)