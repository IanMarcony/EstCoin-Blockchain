import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'UEA-EST-2025')
JWT_ALGORITHM = 'HS256'
TOKEN_EXPIRATION_HOURS = 24


def generate_token(user_id, username, ethereum_address):
    """
    Gera um token JWT para autenticação do usuário
    
    Args:
        user_id (int): ID do usuário no banco de dados
        username (str): Nome de usuário
        ethereum_address (str): Endereço da carteira Ethereum do usuário
    
    Returns:
        str: Token JWT codificado
    """
    try:
        payload = {
            'user_id': user_id,
            'username': username,
            'ethereum_address': ethereum_address,
            'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
            'iat': datetime.utcnow()  # Issued at
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token
    except Exception as e:
        raise Exception(f"Erro ao gerar token: {str(e)}")


def verify_token(token):
    """
    Verifica a validade de um token JWT
    
    Args:
        token (str): Token JWT a ser verificado
    
    Returns:
        dict: Payload decodificado do token se válido
        None: Se o token for inválido ou expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido


def hash_password(password):
    """
    Gera um hash bcrypt da senha fornecida
    
    Args:
        password (str): Senha em texto plano
    
    Returns:
        str: Hash da senha em formato string
    """
    # Converte a senha para bytes e gera o hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds é um bom equilíbrio entre segurança e performance
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Retorna como string para armazenar no banco
    return hashed.decode('utf-8')


def check_password(hashed_password, password):
    """
    Verifica se a senha fornecida corresponde ao hash armazenado
    
    Args:
        hashed_password (str): Hash da senha armazenado no banco
        password (str): Senha em texto plano fornecida pelo usuário
    
    Returns:
        bool: True se a senha corresponde, False caso contrário
    """
    try:
        # Converte ambos para bytes
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Verifica se a senha corresponde ao hash
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Erro ao verificar senha: {str(e)}")
        return False


def token_required(f):
    """
    Decorator para proteger rotas que requerem autenticação
    
    Uso:
        @app.route('/rota-protegida')
        @token_required
        def rota_protegida(current_user):
            return jsonify({'user': current_user})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Procura o token no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Formato esperado: "Bearer <token>"
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Formato de token inválido. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'message': 'Token de autenticação não fornecido'}), 401
        
        # Verifica o token
        current_user = verify_token(token)
        
        if not current_user:
            return jsonify({'message': 'Token inválido ou expirado'}), 401
        
        # Passa os dados do usuário para a função decorada
        return f(current_user, *args, **kwargs)
    
    return decorated


def extract_token_from_request():
    """
    Extrai o token JWT do header da requisição
    
    Returns:
        str: Token extraído ou None
    """
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
            return token
        except IndexError:
            return None
    return None


def validate_password_strength(password):
    """
    Valida a força da senha
    
    Args:
        password (str): Senha a ser validada
    
    Returns:
        tuple: (bool, str) - (é válida, mensagem de erro)
    """
    if len(password) < 6:
        return False, "A senha deve ter no mínimo 6 caracteres"
    
    if len(password) > 128:
        return False, "A senha deve ter no máximo 128 caracteres"
    
    # Verifica se tem pelo menos uma letra
    if not any(char.isalpha() for char in password):
        return False, "A senha deve conter pelo menos uma letra"
    
    # Verifica se tem pelo menos um número
    if not any(char.isdigit() for char in password):
        return False, "A senha deve conter pelo menos um número"
    
    return True, "Senha válida"