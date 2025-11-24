#!/usr/bin/env python3
"""
Script para distribuir ETH (gás) para usuários registrados
"""
import sys
import os
import importlib
from pathlib import Path
from web3 import Web3

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(__file__))

# Recarrega o módulo config para pegar o endereço atualizado
if 'src.config' in sys.modules:
    importlib.reload(sys.modules['src.config'])

from src.models.user import SessionLocal, User
from src.config import Config
from src.blockchain.web3_client import web3

ETH_PER_USER = 1.0  # Quantidade de ETH para cada usuário (para pagar gás)

def get_users():
    """Obtém todos os usuários do banco de dados"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()

def distribute_eth():
    """Distribui ETH para todos os usuários registrados"""
    print("=" * 70)
    print("  DISTRIBUIÇÃO DE ETH (GÁS) PARA USUÁRIOS")
    print("=" * 70)
    print()
    
    # Verifica conexão
    if not web3.is_connected():
        print("❌ Erro: Não conectado ao Ethereum")
        return False
    
    print(f"✅ Conectado ao Ethereum")
    print(f"   Chain ID: {web3.eth.chain_id}")
    print()
    
    # Obtém a conta faucet (primeira conta disponível)
    accounts = web3.eth.accounts
    if not accounts:
        print("❌ Erro: Nenhuma conta disponível")
        return False
    
    faucet = accounts[0]
    print(f"📝 Conta distribuidora (faucet): {faucet}")
    
    # Verifica saldo do faucet
    faucet_balance_wei = web3.eth.get_balance(faucet)
    faucet_balance_eth = web3.from_wei(faucet_balance_wei, 'ether')
    print(f"💰 Saldo disponível: {faucet_balance_eth:,.2f} ETH")
    print()
    
    # Obtém usuários
    users = get_users()
    
    if not users:
        print("⚠️ Nenhum usuário encontrado no banco de dados")
        return False
    
    print(f"👥 Encontrados {len(users)} usuário(s)")
    print()
    
    # Calcula total necessário
    total_needed = len(users) * ETH_PER_USER
    
    if faucet_balance_eth < total_needed:
        print(f"⚠️ Aviso: Saldo insuficiente!")
        print(f"   Necessário: {total_needed} ETH")
        print(f"   Disponível: {faucet_balance_eth:,.2f} ETH")
        print(f"   Distribuindo o máximo possível...")
        eth_amount = max(0.1, (faucet_balance_eth - 0.1) / len(users))
        print(f"   Cada usuário receberá: {eth_amount:.4f} ETH")
    else:
        eth_amount = ETH_PER_USER
        print(f"🎁 Distribuindo {eth_amount} ETH para cada usuário...")
    
    print("-" * 70)
    
    success_count = 0
    error_count = 0
    
    for user in users:
        try:
            address = user.ethereum_address
            
            # Verifica saldo atual
            current_balance = web3.eth.get_balance(address)
            current_balance_eth = web3.from_wei(current_balance, 'ether')
            
            print(f"\n👤 {user.username} ({address})")
            print(f"   Saldo atual: {current_balance_eth:.4f} ETH")
            
            # Se já tem ETH suficiente, pula
            if current_balance_eth >= eth_amount:
                print(f"   ✅ Já tem ETH suficiente, pulando...")
                success_count += 1
                continue
            
            # Calcula quanto enviar
            amount_to_send = eth_amount - current_balance_eth
            amount_wei = web3.to_wei(amount_to_send, 'ether')
            
            # Envia ETH
            tx_hash = web3.eth.send_transaction({
                'from': faucet,
                'to': address,
                'value': amount_wei,
                'gas': 21000
            })
            
            # Aguarda confirmação
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            
            if receipt['status'] == 1:
                new_balance = web3.eth.get_balance(address)
                new_balance_eth = web3.from_wei(new_balance, 'ether')
                
                print(f"   ✅ {amount_to_send:.4f} ETH enviados")
                print(f"   💰 Novo saldo: {new_balance_eth:.4f} ETH")
                print(f"   📝 TX: {tx_hash.hex()}")
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
    
    # Saldo final do faucet
    final_balance = web3.eth.get_balance(faucet)
    final_balance_eth = web3.from_wei(final_balance, 'ether')
    print(f"\n💰 Saldo final do faucet: {final_balance_eth:,.2f} ETH")
    print()
    
    return success_count > 0

def main():
    try:
        success = distribute_eth()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
