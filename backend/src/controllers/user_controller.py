"""
Controller para gerenciar usuários
"""
from src.utils.auth_utils import hash_password, check_password, generate_token
from src.blockchain.web3_client import create_account

# Simulação de banco de dados em memória (será substituído por SQLite)
users_db = {}

class UserController:
    def __init__(self):
        self.users = users_db
    
    def register(self, username, password):
        """
        Registra um novo usuário
        
        Args:
            username (str): Nome de usuário
            password (str): Senha
            
        Returns:
            dict: Dados do usuário criado
        """
        # Verifica se usuário já existe
        if username in self.users:
            raise Exception('Usuário já existe')
        
        # Cria conta Ethereum
        eth_account = create_account()
        
        # Hash da senha
        password_hash = hash_password(password)
        
        # Cria usuário
        user = {
            'username': username,
            'password_hash': password_hash,
            'ethereum_address': eth_account['address'],
            'private_key': eth_account['private_key'],  # Em produção, deve ser criptografado
            'balance': 10.0  # Saldo inicial
        }
        
        self.users[username] = user
        
        # Gera token JWT
        token = generate_token(
            user_id=username,
            username=username,
            ethereum_address=eth_account['address']
        )
        
        return {
            'username': username,
            'ethereum_address': eth_account['address'],
            'balance': 10.0,
            'token': token
        }
    
    def login(self, username, password):
        """
        Autentica um usuário
        
        Args:
            username (str): Nome de usuário
            password (str): Senha
            
        Returns:
            str: Token JWT
        """
        # Busca usuário
        user = self.users.get(username)
        
        if not user:
            return None
        
        # Verifica senha
        if not check_password(user['password_hash'], password):
            return None
        
        # Gera token JWT
        token = generate_token(
            user_id=username,
            username=username,
            ethereum_address=user['ethereum_address']
        )
        
        return token
    
    def get_user(self, username):
        """
        Busca um usuário pelo username
        
        Args:
            username (str): Nome de usuário
            
        Returns:
            dict: Dados do usuário
        """
        return self.users.get(username)