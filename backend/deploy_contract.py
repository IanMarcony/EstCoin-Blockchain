#!/usr/bin/env python3
"""
Script para fazer deploy do contrato Token e atualizar o config.py com o endereço
"""
import json
import os
from web3 import Web3
from pathlib import Path

# Configurações
BLOCKCHAIN_URL = "http://127.0.0.1:8545"
INITIAL_SUPPLY = 1_000_000  # 1 milhão de tokens

# Caminhos
BACKEND_DIR = Path(__file__).parent
PROJECT_DIR = BACKEND_DIR.parent
CONTRACT_BUILD_PATH = PROJECT_DIR / "blockchain" / "build" / "contracts" / "Token.json"
CONFIG_PATH = BACKEND_DIR / "src" / "config.py"

def load_contract_data():
    """Carrega o ABI e bytecode do contrato compilado"""
    with open(CONTRACT_BUILD_PATH, 'r') as f:
        contract_json = json.load(f)
    return contract_json['abi'], contract_json['bytecode']

def deploy_contract():
    """Faz o deploy do contrato Token"""
    print("🚀 Iniciando deploy do contrato Token...")
    
    # Conecta ao Ethereum
    web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
    
    if not web3.is_connected():
        print("❌ Erro: Não foi possível conectar ao Ethereum")
        print(f"   Certifique-se de que o servidor está rodando em {BLOCKCHAIN_URL}")
        return None
    
    print(f"✅ Conectado ao Ethereum em {BLOCKCHAIN_URL}")
    print(f"   Chain ID: {web3.eth.chain_id}")
    
    # Carrega ABI e bytecode
    abi, bytecode = load_contract_data()
    
    # Obtém a conta para fazer o deploy (primeira conta disponível)
    accounts = web3.eth.accounts
    if not accounts:
        print("❌ Erro: Nenhuma conta encontrada")
        print("   Execute o servidor Ethereum com contas desbloqueadas")
        return None
    
    deployer_account = accounts[0]
    print(f"📝 Conta do deployer: {deployer_account}")
    
    # Verifica saldo
    balance = web3.eth.get_balance(deployer_account)
    balance_eth = web3.from_wei(balance, 'ether')
    print(f"💰 Saldo: {balance_eth} ETH")
    
    if balance == 0:
        print("⚠️  Aviso: A conta do deployer não tem saldo")
    
    # Cria o contrato
    Token = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    # IMPORTANTE: O contrato já multiplica por 10^18 internamente
    # Então passamos apenas o valor base (1.000.000)
    initial_supply_base = INITIAL_SUPPLY  # Passa 1000000, não 1000000 * 10^18
    
    print(f"📦 Fazendo deploy com supply inicial de {INITIAL_SUPPLY:,} tokens...")
    print(f"   (O contrato multiplicará automaticamente por 10^18)")
    
    # Constrói a transação de deploy
    try:
        tx_hash = Token.constructor(initial_supply_base).transact({
            'from': deployer_account,
            'gas': 3000000  # Aumentado para segurança
        })
        
        print(f"⏳ Aguardando confirmação da transação...")
        print(f"   TX Hash: {tx_hash.hex()}")
        
        # Aguarda a transação ser minerada
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        contract_address = tx_receipt.contractAddress
        print(f"✅ Contrato deployado com sucesso!")
        print(f"   Endereço: {contract_address}")
        print(f"   Gas usado: {tx_receipt.gasUsed:,}")
        print(f"   Bloco: {tx_receipt.blockNumber}")
        
        # Verifica o saldo inicial
        token_contract = web3.eth.contract(address=contract_address, abi=abi)
        deployer_balance = token_contract.functions.balanceOf(deployer_account).call()
        deployer_balance_tokens = deployer_balance / (10 ** 18)
        
        print(f"🪙 Saldo do deployer: {deployer_balance_tokens:,} EST")
        
        return contract_address
        
    except Exception as e:
        print(f"❌ Erro ao fazer deploy: {e}")
        return None

def update_config(contract_address):
    """Salva o endereço do contrato no banco de dados"""
    print(f"\n📝 Salvando endereço do contrato no banco de dados...")
    
    try:
        from src.models.user import SystemConfig, init_db
        
        # Garante que o banco está inicializado
        init_db()
        
        # Salva o endereço no banco
        success = SystemConfig.set_value('TOKEN_CONTRACT_ADDRESS', contract_address)
        
        if success:
            print(f"✅ Endereço salvo no banco de dados!")
            print(f"   TOKEN_CONTRACT_ADDRESS = '{contract_address}'")
        else:
            print(f"❌ Erro ao salvar endereço no banco de dados")
            
    except Exception as e:
        print(f"❌ Erro ao atualizar configuração: {e}")

def main():
    print("=" * 70)
    print("  DEPLOY DO CONTRATO ESTCOIN TOKEN")
    print("=" * 70)
    print()
    
    # Verifica se o contrato está compilado
    if not CONTRACT_BUILD_PATH.exists():
        print(f"❌ Erro: Contrato não compilado")
        print(f"   Execute 'truffle compile' no diretório blockchain/")
        return
    
    # Faz o deploy
    contract_address = deploy_contract()
    
    if contract_address:
        # Atualiza o config
        update_config(contract_address)
        
        print()
        print("=" * 70)
        print("  ✅ DEPLOY CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print()
        print("Próximos passos:")
        print("1. Reinicie o servidor backend para carregar o novo endereço")
        print("2. Distribua tokens iniciais para os usuários se necessário")
        print()
    else:
        print()
        print("=" * 70)
        print("  ❌ DEPLOY FALHOU")
        print("=" * 70)
        print()

if __name__ == "__main__":
    main()
