from flask import Blueprint, request, jsonify
from src.controllers.user_controller import UserController

auth_bp = Blueprint('auth', __name__)
user_controller = UserController()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    user = user_controller.register(username, password)
    return jsonify({'message': 'User registered successfully', 'user': user}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    token = user_controller.login(username, password)
    if token:
        return jsonify({'message': 'Login successful', 'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401