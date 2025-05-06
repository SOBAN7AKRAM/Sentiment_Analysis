from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from flask_cors import CORS
import bcrypt
import jwt
import datetime
import random
import re
from werkzeug.exceptions import BadRequest

# Initialize Flask app
app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": ["https://localhost:3000"]}})

# Configure app
app.config['SECRET_KEY'] = 'dkchvsdudshvjsdyuedbuyv'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask_auth'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hasnainali2690@gmail.com'
app.config['MAIL_PASSWORD'] = 'aehn aiah fczl symx'

# Initialize extensions
mail = Mail(app)
mongo = PyMongo(app)
users_collection = mongo.db.users

# ===================== EMAIL VALIDATION =====================
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise BadRequest("Invalid email format.")

# ===================== SIGNUP ROUTE =====================
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('fullName')

    # Validate email format
    validate_email(email)

    # Check if user already exists
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 409

    # Hash password before saving to DB
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user data into database
    users_collection.insert_one({'email': email, 'password': hashed_pw, 'fullName': full_name})
    return jsonify({'message': 'User created successfully'}), 201

# ===================== LOGIN ROUTE =====================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate email format
    validate_email(email)

    # Check if user exists and verify password
    user = users_collection.find_one({'email': email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        users_collection.update_one({'email': email}, {'$set': {
            'otp': otp,
            'otp_expiry': datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
        }})

        # Send OTP via email
        try:
            msg = Message('Your OTP Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f'Your OTP is: {otp}. It expires in 3 minutes.'
            mail.send(msg)
        except Exception as e:
            return jsonify({'error': 'Failed to send OTP'}), 500

        return jsonify({'message': 'OTP sent'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# ===================== VERIFY OTP ROUTE =====================
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    # Find user by email
    user = users_collection.find_one({'email': email})
    if user and user.get('otp') == otp and datetime.datetime.utcnow() < user.get('otp_expiry'):
        # Generate JWT token
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        # Clean up OTP after successful verification
        users_collection.update_one({'email': email}, {'$unset': {'otp': "", 'otp_expiry': ""}})
        return jsonify({'message': 'OTP verified', 'token': token}), 200

    return jsonify({'error': 'Invalid or expired OTP'}), 401
@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Only PDFs allowed.'}), 400

    file.save(f"./uploads/{file.filename}")  # Save to uploads/ folder
    return jsonify({'message': 'Resume uploaded successfully'}), 200


# ===================== RUN THE FLASK APP =====================
if _name_ == '_main_':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)