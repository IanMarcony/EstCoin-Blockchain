"""
Utilitários para distribuição automática de tokens
"""
from src.blockchain.web3_client import web3
from src.blockchain.contract import get_contract
from src.config import Config

INITIAL_USER_BALANCE = 10  # Saldo inicial para cada novo usuário (10 ESTCOIN)
INITIAL_ETH_BALANCE = 1.0  # ETH inicial para pagar gás (1 ETH)

def distribute_eth_for_gas(user_address):
    """
    Distribui ETH para uma nova conta para pagar taxas de gás
    
    Args:
        user_address (str): Endereço Ethereum do novo usuário
        
    Returns:
        dict: Informações da distribuição ou None se falhar
    """
    try:
        # Obtém a primeira conta disponível (faucet de ETH)
        accounts = web3.eth.accounts
        if not accounts:
            print("⚠️ Aviso: Nenhuma conta disponível para distribuir ETH")
            return None
        
        faucet_account = accounts[0]
        
        # Verifica se o faucet tem ETH suficiente
        faucet_balance_wei = web3.eth.get_balance(faucet_account)
        faucet_balance_eth = web3.from_wei(faucet_balance_wei, 'ether')
        
        if faucet_balance_eth < INITIAL_ETH_BALANCE:
            print(f"⚠️ Aviso: Faucet tem apenas {faucet_balance_eth} ETH disponíveis")
            if faucet_balance_eth < 0.1:
                return None
            # Distribui o que tem disponível (deixa 0.1 ETH no faucet)
            amount_to_send = float(faucet_balance_eth) - 0.1
        else:
            amount_to_send = INITIAL_ETH_BALANCE
        
        # Converte para Wei
        amount_wei = web3.to_wei(amount_to_send, 'ether')
        
        # Envia ETH
        tx_hash = web3.eth.send_transaction({
            'from': faucet_account,
            'to': user_address,
            'value': amount_wei,
            'gas': 21000  # Gas padrão para transferência ETH
        })
        
        # Aguarda confirmação
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        
        if tx_receipt.status == 1:
            print(f"✅ {amount_to_send} ETH distribuídos para {user_address} (para pagar gás)")
            return {
                'success': True,
                'amount': amount_to_send,
                'tx_hash': tx_hash.hex(),
                'message': f'{amount_to_send} ETH distribuídos para pagar taxas de gás'
            }
        else:
            print(f"❌ Falha ao distribuir ETH para {user_address}")
            return None
            
    except Exception as e:
        print(f"⚠️ Erro ao distribuir ETH: {e}")
        return None

def auto_distribute_initial_tokens(user_address):
    """
    Distribui automaticamente 10 ESTCOIN e 1 ETH para um novo usuário
    
    Args:
        user_address (str): Endereço Ethereum do novo usuário
        
    Returns:
        dict: Informações da distribuição ou None se falhar
    """
    try:
        # Primeiro, distribui ETH para pagar gás
        eth_result = distribute_eth_for_gas(user_address)
        
        # Depois, distribui tokens ESTCOIN
        contract = get_contract()
        if not contract:
            print("⚠️ Aviso: Contrato não deployado, tokens não distribuídos")
            return None
        
        # Obtém a primeira conta disponível (deployer/faucet)
        accounts = web3.eth.accounts
        if not accounts:
            print("⚠️ Aviso: Nenhuma conta disponível para distribuir tokens")
            return None
        
        faucet_account = accounts[0]
        
        # Verifica se o faucet tem tokens suficientes
        faucet_balance = contract.functions.balanceOf(faucet_account).call()
        faucet_balance_tokens = faucet_balance / (10 ** 18)
        
        if faucet_balance_tokens < INITIAL_USER_BALANCE:
            print(f"⚠️ Aviso: Faucet tem apenas {faucet_balance_tokens} EST disponíveis")
            if faucet_balance_tokens == 0:
                return None
            # Distribui o que tem disponível
            amount_to_send = faucet_balance_tokens
        else:
            amount_to_send = INITIAL_USER_BALANCE
        
        # Converte para unidades (18 decimais)
        amount_units = int(amount_to_send * (10 ** 18))
        
        # Transfere tokens
        tx_hash = contract.functions.transfer(
            user_address,
            amount_units
        ).transact({
            'from': faucet_account,
            'gas': 100000
        })
        
        # Aguarda confirmação
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        
        if tx_receipt.status == 1:
            print(f"✅ {amount_to_send} ESTCOIN distribuídos para {user_address}")
            
            # Retorna informações combinadas
            result = {
                'success': True,
                'amount': amount_to_send,
                'tx_hash': tx_hash.hex(),
                'message': f'{amount_to_send} ESTCOIN distribuídos automaticamente'
            }
            
            if eth_result:
                result['eth_amount'] = eth_result['amount']
                result['eth_tx_hash'] = eth_result['tx_hash']
                result['message'] += f' + {eth_result["amount"]} ETH para gás'
            
            return result
        else:
            print(f"❌ Falha ao distribuir tokens para {user_address}")
            return None
            
    except Exception as e:
        print(f"⚠️ Erro ao distribuir tokens: {e}")
        return None

def check_faucet_balance():
    """
    Verifica o saldo do faucet (conta que distribui tokens)
    
    Returns:
        float: Saldo em ESTCOIN ou 0 se erro
    """
    try:
        contract = get_contract()
        if not contract:
            return 0
        
        accounts = web3.eth.accounts
        if not accounts:
            return 0
        
        faucet_account = accounts[0]
        balance = contract.functions.balanceOf(faucet_account).call()
        return balance / (10 ** 18)
        
    except Exception as e:
        print(f"Erro ao verificar saldo do faucet: {e}")
        return 0
