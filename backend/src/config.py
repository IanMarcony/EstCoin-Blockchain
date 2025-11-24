"""
Configurações da aplicação EstCoin Backend
"""
import os

class Config:
    # Flask
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'EST-UEA-2025-BLOCKCHAIN-SECRET')
    
    # Database
    DATABASE_URI = 'sqlite:///users.db'
    
    # Blockchain
    BLOCKCHAIN_URL = os.getenv('BLOCKCHAIN_URL', 'http://127.0.0.1:8545')
    CHAIN_ID = 1337  # Chain ID do genesis.json
    
    # Gas Settings
    GAS_LIMIT = 2000000
    GAS_PRICE = 20000000000  # 20 Gwei
    
    # Token Contract 
    @staticmethod
    def get_token_contract_address():
        """Busca o endereço do contrato do banco de dados"""
        try:
            from src.models.user import SystemConfig
            address = SystemConfig.get_value('TOKEN_CONTRACT_ADDRESS', None)
            return address
        except Exception as e:
            print(f"Erro ao buscar endereço do contrato: {e}")
            return None
    
    # Fallback para compatibilidade com código antigo
    @property
    def TOKEN_CONTRACT_ADDRESS(self):
        return self.get_token_contract_address()
    
    # JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24