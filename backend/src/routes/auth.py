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
    
    try:
        result = user_controller.register(username, password)
        return jsonify({
            'message': 'User registered successfully',
            'token': result.get('token'),
            'user': {
                'username': result.get('username'),
                'ethereum_address': result.get('ethereum_address'),
                'balance': result.get('balance', 10.0)
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    token = user_controller.login(username, password)
    if token:
        # Busca dados completos do usuário
        user = user_controller.get_user(username)
        
        response_data = {
            'message': 'Login successful',
            'token': token,
            'user': {
                'username': username,
                'ethereum_address': user.get('ethereum_address'),
                'balance': user.get('balance', 10.0)
            }
        }
        
        print(f'✅ Login successful for user: {username}')
        print(f'✅ Response data: {response_data}')
        
        return jsonify(response_data), 200
    return jsonify({'error': 'Invalid credentials'}), 401