#!/usr/bin/env python3
"""
Script para testar transferência de tokens após a correção
"""
import sys
import os

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.blockchain.web3_client import web3
from src.blockchain.contract import get_contract, transfer_tokens, get_token_balance
from src.config import Config

def test_transfer():
    """Testa a função de transferência"""
    print("=" * 70)
    print("  TESTE DE TRANSFERÊNCIA DE TOKENS")
    print("=" * 70)
    print()
    
    # Verifica conexão
    if not web3.is_connected():
        print("❌ Erro: Não conectado ao Ethereum")
        return False
    
    print(f"✅ Conectado ao Ethereum (Chain ID: {web3.eth.chain_id})")
    
    # Verifica contrato
    contract = get_contract()
    if not contract:
        print(f"❌ Erro: Contrato não deployado")
        print(f"   TOKEN_CONTRACT_ADDRESS = {Config.TOKEN_CONTRACT_ADDRESS}")
        return False
    
    print(f"✅ Contrato carregado: {Config.TOKEN_CONTRACT_ADDRESS}")
    print()
    
    # Pega contas disponíveis
    accounts = web3.eth.accounts
    if len(accounts) < 2:
        print("❌ Erro: Precisa de pelo menos 2 contas")
        return False
    
    from_account = accounts[0]
    to_account = accounts[1]
    
    print(f"📤 De: {from_account}")
    print(f"📥 Para: {to_account}")
    print()
    
    # Verifica saldos iniciais
    from_balance_before = get_token_balance(from_account)
    to_balance_before = get_token_balance(to_account)
    
    print(f"💰 Saldo inicial:")
    print(f"   De: {from_balance_before:,.2f} EST")
    print(f"   Para: {to_balance_before:,.2f} EST")
    print()
    
    if from_balance_before < 1:
        print("❌ Erro: Conta origem não tem tokens suficientes")
        return False
    
    # Prepara transferência
    amount = 0.5
    print(f"🔄 Transferindo {amount} EST...")
    print()
    
    # Simula private_key (pega da primeira conta do Ganache)
    # NOTA: Em produção, pegaria do banco de dados
    try:
        # Para Ganache, as contas são conhecidas
        # Vamos criar uma transação de teste
        print("⚠️  NOTA: Este é um teste simplificado")
        print("   Em produção, a private_key vem do banco de dados")
        print()
        
        # Verifica se podemos fazer transação direta (sem private key)
        # usando as contas desbloqueadas do Ganache
        tx_hash_simple = contract.functions.transfer(
            to_account,
            int(amount * 10**18)
        ).transact({'from': from_account})
        
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash_simple)
        
        if receipt['status'] == 1:
            print(f"✅ Transferência bem-sucedida!")
            print(f"   TX Hash: {tx_hash_simple.hex()}")
            print(f"   Block: {receipt['blockNumber']}")
            print(f"   Gas usado: {receipt['gasUsed']:,}")
            print()
            
            # Verifica saldos finais
            from_balance_after = get_token_balance(from_account)
            to_balance_after = get_token_balance(to_account)
            
            print(f"💰 Saldo final:")
            print(f"   De: {from_balance_after:,.2f} EST (diff: {from_balance_after - from_balance_before:+.2f})")
            print(f"   Para: {to_balance_after:,.2f} EST (diff: {to_balance_after - to_balance_before:+.2f})")
            print()
            
            if abs((from_balance_after - from_balance_before) + amount) < 0.001 and \
               abs((to_balance_after - to_balance_before) - amount) < 0.001:
                print("✅ Saldos corretos!")
                return True
            else:
                print("⚠️  Saldos não batem com o esperado")
                return False
        else:
            print("❌ Transação falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao transferir: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_transfer()
        print()
        print("=" * 70)
        if success:
            print("  ✅ TESTE PASSOU!")
        else:
            print("  ❌ TESTE FALHOU")
        print("=" * 70)
        print()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
