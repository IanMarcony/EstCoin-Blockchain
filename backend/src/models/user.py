"""
Modelo de dados do usuário
"""
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Caminho para o banco de dados
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'users.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

# Cria engine e sessão
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    """
    Modelo de usuário com autenticação e carteira Ethereum
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    ethereum_address = Column(String(42), unique=True, nullable=False)
    private_key = Column(String(66), nullable=False)  # Armazenado criptografado em produção
    balance = Column(Float, default=10.0)

    def __repr__(self):
        return f"<User(username='{self.username}', ethereum_address='{self.ethereum_address}', balance={self.balance})>"

    def to_dict(self):
        """Converte o usuário para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'ethereum_address': self.ethereum_address,
            'balance': self.balance
        }

def init_db():
    """Inicializa o banco de dados criando as tabelas"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ Banco de dados criado em: {DB_PATH}")

def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # A sessão será fechada pelo caller