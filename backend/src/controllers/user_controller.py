"""
Controller para gerenciar usuários com SQLite
"""
from src.utils.auth_utils import hash_password, check_password, generate_token
from src.blockchain.web3_client import create_account
from src.models.user import User, get_db, SessionLocal
from src.utils.token_utils import auto_distribute_initial_tokens

class UserController:
    def __init__(self):
        pass
    
    def register(self, username, password):
        """
        Registra um novo usuário no banco de dados
        
        Args:
            username (str): Nome de usuário
            password (str): Senha
            
        Returns:
            dict: Dados do usuário criado
        """
        db = SessionLocal()
        
        try:
            # Verifica se usuário já existe
            existing_user = db.query(User).filter_by(username=username).first()
            if existing_user:
                raise Exception('Usuário já existe')
            
            # Cria conta Ethereum
            eth_account = create_account()
            
            # Hash da senha
            password_hash = hash_password(password)
            
            # Cria usuário no banco
            new_user = User(
                username=username,
                password_hash=password_hash,
                ethereum_address=eth_account['address'],
                private_key=eth_account['private_key'],
                balance=10.0
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f'✅ Usuário criado: {username} - {eth_account["address"]}')
            
            # Distribui 10 ESTCOIN automaticamente para o novo usuário
            distribution_result = auto_distribute_initial_tokens(eth_account['address'])
            
            if distribution_result:
                print(f'✅ 10 ESTCOIN distribuídos automaticamente para {username}')
                actual_balance = distribution_result['amount']
            else:
                print(f'⚠️ Tokens não distribuídos automaticamente. Execute distribute_tokens.py manualmente.')
                actual_balance = 0.0
            
            # Gera token JWT
            token = generate_token(
                user_id=new_user.id,
                username=username,
                ethereum_address=eth_account['address']
            )
            
            return {
                'username': username,
                'ethereum_address': eth_account['address'],
                'balance': actual_balance,
                'token': token,
                'distribution': distribution_result
            }
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def login(self, username, password):
        """
        Autentica um usuário
        
        Args:
            username (str): Nome de usuário
            password (str): Senha
            
        Returns:
            str: Token JWT ou None
        """
        db = SessionLocal()
        
        try:
            # Busca usuário no banco
            user = db.query(User).filter_by(username=username).first()
            
            if not user:
                return None
            
            # Verifica senha
            if not check_password(user.password_hash, password):
                return None
            
            print(f'✅ Login bem-sucedido: {username}')
            
            # Gera token JWT
            token = generate_token(
                user_id=user.id,
                username=user.username,
                ethereum_address=user.ethereum_address
            )
            
            return token
            
        finally:
            db.close()
    
    def get_user(self, username):
        """
        Busca um usuário pelo username
        
        Args:
            username (str): Nome de usuário
            
        Returns:
            dict: Dados do usuário
        """
        db = SessionLocal()
        
        try:
            user = db.query(User).filter_by(username=username).first()
            
            if not user:
                return None
            
            return {
                'id': user.id,
                'username': user.username,
                'ethereum_address': user.ethereum_address,
                'balance': user.balance
            }
            
        finally:
            db.close()
    
    def get_user_by_address(self, ethereum_address):
        """
        Busca um usuário pelo endereço Ethereum
        
        Args:
            ethereum_address (str): Endereço Ethereum
            
        Returns:
            dict: Dados do usuário
        """
        db = SessionLocal()
        
        try:
            user = db.query(User).filter_by(ethereum_address=ethereum_address).first()
            
            if not user:
                return None
            
            return user.to_dict()
            
        finally:
            db.close()