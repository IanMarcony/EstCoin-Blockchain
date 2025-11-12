"""
Módulo para interagir com o smart contract Token.sol
"""
import json
import os
from src.blockchain.web3_client import web3
from src.config import Config

# Caminho para o arquivo ABI do contrato compilado
CONTRACT_ABI_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    '..',
    'blockchain',
    'build',
    'contracts',
    'Token.json'
)

def load_contract_abi():
    """Carrega o ABI do contrato Token"""
    try:
        if os.path.exists(CONTRACT_ABI_PATH):
            with open(CONTRACT_ABI_PATH, 'r') as f:
                contract_json = json.load(f)
                return contract_json['abi']
        return None
    except Exception as e:
        print(f"Erro ao carregar ABI: {e}")
        return None

def get_contract():
    """Retorna a instância do contrato Token"""
    try:
        if not Config.TOKEN_CONTRACT_ADDRESS:
            return None
        
        abi = load_contract_abi()
        if not abi:
            return None
        
        contract = web3.eth.contract(
            address=Config.TOKEN_CONTRACT_ADDRESS,
            abi=abi
        )
        return contract
    except Exception as e:
        print(f"Erro ao obter contrato: {e}")
        return None

def get_token_balance(address):
    """
    Retorna o saldo de tokens de um endereço
    
    Args:
        address (str): Endereço Ethereum
        
    Returns:
        float: Saldo em tokens
    """
    try:
        contract = get_contract()
        if not contract:
            return 0.0
        
        balance = contract.functions.balanceOf(address).call()
        # Converte de unidades mínimas (18 decimais) para tokens
        return balance / (10 ** 18)
    except Exception as e:
        print(f"Erro ao obter saldo de tokens: {e}")
        return 0.0

def transfer_tokens(from_address, to_address, amount, private_key):
    """
    Transfere tokens de um endereço para outro
    
    Args:
        from_address (str): Endereço do remetente
        to_address (str): Endereço do destinatário
        amount (float): Quantidade de tokens
        private_key (str): Chave privada do remetente
        
    Returns:
        str: Hash da transação
    """
    try:
        contract = get_contract()
        if not contract:
            raise Exception("Contrato não disponível")
        
        # Converte tokens para unidades mínimas (18 decimais)
        amount_in_units = int(amount * (10 ** 18))
        
        # Prepara a transação
        nonce = web3.eth.get_transaction_count(from_address)
        
        transaction = contract.functions.transfer(
            to_address,
            amount_in_units
        ).build_transaction({
            'chainId': Config.CHAIN_ID,
            'gas': Config.GAS_LIMIT,
            'gasPrice': Config.GAS_PRICE,
            'nonce': nonce,
        })
        
        # Assina a transação
        signed_txn = web3.eth.account.sign_transaction(
            transaction,
            private_key=private_key
        )
        
        # Envia a transação
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return tx_hash.hex()
    except Exception as e:
        raise Exception(f"Erro ao transferir tokens: {str(e)}")