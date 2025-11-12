"""
Cliente Web3 para interagir com a blockchain Ethereum local
"""
from web3 import Web3
from src.config import Config

# Inicializa a conexão com a blockchain local
web3 = Web3(Web3.HTTPProvider(Config.BLOCKCHAIN_URL))

def is_connected():
    """Verifica se está conectado à blockchain"""
    return web3.is_connected()

def get_balance(address):
    """Retorna o saldo em Wei de um endereço"""
    try:
        return web3.eth.get_balance(address)
    except Exception as e:
        print(f"Erro ao obter saldo: {e}")
        return 0

def wei_to_ether(wei_amount):
    """Converte Wei para Ether"""
    return web3.from_wei(wei_amount, 'ether')

def ether_to_wei(ether_amount):
    """Converte Ether para Wei"""
    return web3.to_wei(ether_amount, 'ether')

def get_transaction_count(address):
    """Retorna o número de transações de um endereço"""
    try:
        return web3.eth.get_transaction_count(address)
    except Exception as e:
        print(f"Erro ao obter transaction count: {e}")
        return 0

def get_transaction(tx_hash):
    """Retorna os detalhes de uma transação"""
    try:
        return web3.eth.get_transaction(tx_hash)
    except Exception as e:
        print(f"Erro ao obter transação: {e}")
        return None

def create_account():
    """Cria uma nova conta Ethereum"""
    account = web3.eth.account.create()
    return {
        'address': account.address,
        'private_key': account.key.hex()
    }