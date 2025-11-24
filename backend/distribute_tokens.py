#!/usr/bin/env python3
"""
Script para distribuir tokens iniciais para usuários registrados
"""
import json
import sys
import os
from pathlib import Path
from web3 import Web3
from src.models.user import SessionLocal, User, SystemConfig

# Lê as configurações necessárias
BLOCKCHAIN_URL = 'http://127.0.0.1:8545'

# Função para ler o endereço do contrato do banco de dados
def get_contract_address():
    """Lê o endereço do contrato do banco de dados"""
    try:
        address = SystemConfig.get_value('TOKEN_CONTRACT_ADDRESS', None)
        return address
    except Exception as e:
        print(f"Erro ao buscar endereço do contrato: {e}")
        return None

# Caminhos
BACKEND_DIR = Path(__file__).parent
PROJECT_DIR = BACKEND_DIR.parent
CONTRACT_BUILD_PATH = PROJECT_DIR / "blockchain" / "build" / "contracts" / "Token.json"

TOKENS_PER_USER = 10  # Quantidade de tokens para cada usuário (saldo inicial)

def load_contract():
    """Carrega o contrato Token"""
    with open(CONTRACT_BUILD_PATH, 'r') as f:
        contract_json = json.load(f)
    
    web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
    
    if not web3.is_connected():
        print(f"❌ Erro: Não foi possível conectar ao Ethereum em {BLOCKCHAIN_URL}")
        return None, None
    
    # Busca o endereço do contrato do banco
    contract_address = get_contract_address()
    
    if not contract_address:
        print("❌ Erro: TOKEN_CONTRACT_ADDRESS não está configurado no banco de dados")
        print("   Execute deploy_contract.py primeiro")
        return None, None
    
    contract = web3.eth.contract(
        address=contract_address,
        abi=contract_json['abi']
    )
    
    return web3, contract

def get_users():
    """Obtém todos os usuários do banco de dados"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()

def distribute_tokens():
    """Distribui tokens para todos os usuários registrados"""
    print("=" * 70)
    print("  DISTRIBUIÇÃO DE TOKENS ESTCOIN")
    print("=" * 70)
    print()
    
    # Carrega o contrato
    web3, contract = load_contract()
    if not web3 or not contract:
        return
    
    # Busca o endereço do contrato
    contract_address = get_contract_address()
    
    print(f"✅ Conectado ao Ethereum")
    print(f"   Chain ID: {web3.eth.chain_id}")
    print(f"   Contrato: {contract_address}")
    print()
    
    # Obtém a conta do deployer (primeira conta disponível)
    accounts = web3.eth.accounts
    if not accounts:
        print("❌ Erro: Nenhuma conta encontrada")
        return
    
    deployer = accounts[0]
    print(f"📝 Conta distribuidora: {deployer}")
    
    # Verifica saldo do deployer
    deployer_balance = contract.functions.balanceOf(deployer).call()
    deployer_balance_tokens = deployer_balance / (10 ** 18)
    print(f"💰 Saldo disponível: {deployer_balance_tokens:,.2f} EST")
    print()
    
    # Obtém usuários
    users = get_users()
    
    if not users:
        print("❌ Nenhum usuário encontrado no banco de dados")
        print("   Registre usuários primeiro usando /auth/register")
        return
    
    print(f"👥 Encontrados {len(users)} usuário(s)")
    print()
    
    # Calcula total necessário
    total_needed = len(users) * TOKENS_PER_USER
    
    if deployer_balance_tokens < total_needed:
        print(f"⚠️  Aviso: Saldo insuficiente!")
        print(f"   Necessário: {total_needed:,.2f} EST")
        print(f"   Disponível: {deployer_balance_tokens:,.2f} EST")
        print()
        
        # Ajusta a quantidade por usuário
        TOKENS_PER_USER_ADJUSTED = int(deployer_balance_tokens / len(users))
        if TOKENS_PER_USER_ADJUSTED == 0:
            print("❌ Erro: Saldo insuficiente para distribuir")
            return
        
        print(f"🔄 Ajustando para {TOKENS_PER_USER_ADJUSTED} EST por usuário")
        print()
        tokens_amount = TOKENS_PER_USER_ADJUSTED
    else:
        tokens_amount = TOKENS_PER_USER
    
    # Converte para unidades (18 decimais)
    amount_units = int(tokens_amount * (10 ** 18))
    
    print(f"🎁 Distribuindo {tokens_amount} EST para cada usuário (saldo inicial)...")
    print(f"   Cada usuário receberá até 10 ESTCOIN no total...")
    print("-" * 70)
    
    success_count = 0
    error_count = 0
    
    for user in users:
        try:
            # Verifica saldo atual do usuário
            current_balance = contract.functions.balanceOf(user.ethereum_address).call()
            current_balance_tokens = current_balance / (10 ** 18)
            
            print(f"\n👤 {user.username} ({user.ethereum_address})")
            print(f"   Saldo atual: {current_balance_tokens:.2f} EST")
            
            # Se já tem 10 ou mais tokens, pula
            if current_balance_tokens >= 10:
                print(f"   ✅ Já possui saldo inicial (10 EST), pulando...")
                success_count += 1
                continue
            
            # Se tem menos de 10, completa até 10
            if current_balance_tokens > 0 and current_balance_tokens < 10:
                tokens_to_send = 10 - current_balance_tokens
                amount_units = int(tokens_to_send * (10 ** 18))
                print(f"   🔄 Completando saldo para 10 EST (enviando {tokens_to_send:.2f} EST)...")
            else:
                tokens_to_send = tokens_amount
            
            # Transfere tokens
            if 'tokens_to_send' not in locals():
                tokens_to_send = tokens_amount
                
            print(f"   📤 Transferindo {tokens_to_send} EST...")
            
            tx_hash = contract.functions.transfer(
                user.ethereum_address,
                amount_units
            ).transact({
                'from': deployer,
                'gas': 100000
            })
            
            # Aguarda confirmação
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if tx_receipt.status == 1:
                print(f"   ✅ Transferência concluída!")
                print(f"   TX: {tx_hash.hex()}")
                
                # Verifica novo saldo
                new_balance = contract.functions.balanceOf(user.ethereum_address).call()
                new_balance_tokens = new_balance / (10 ** 18)
                print(f"   💰 Novo saldo: {new_balance_tokens:.2f} EST")
                success_count += 1
            else:
                print(f"   ❌ Transação falhou")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            error_count += 1
    
    print()
    print("=" * 70)
    print("  RESUMO DA DISTRIBUIÇÃO")
    print("=" * 70)
    print(f"✅ Sucesso: {success_count}")
    print(f"❌ Erros: {error_count}")
    print(f"📊 Total: {len(users)}")
    
    # Saldo final do deployer
    final_balance = contract.functions.balanceOf(deployer).call()
    final_balance_tokens = final_balance / (10 ** 18)
    print(f"💰 Saldo restante do distribuidor: {final_balance_tokens:,.2f} EST")
    print()

def main():
    try:
        distribute_tokens()
    except KeyboardInterrupt:
        print("\n\n⚠️  Distribuição cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
