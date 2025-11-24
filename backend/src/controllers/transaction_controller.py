"""
Controller para gerenciar transações de tokens
"""
from src.blockchain.web3_client import web3, get_balance, wei_to_ether
from src.blockchain.contract import get_contract, transfer_tokens, get_token_balance
from src.models.user import User, SessionLocal

class TransactionController:
    def __init__(self):
        self.web3 = web3
        
    def transfer_funds(self, user_id, recipient_address, amount):
        """
        Transfere tokens de um endereço para outro
        
        Args:
            user_id (int): ID do usuário remetente (para buscar private_key)
            recipient_address (str): Endereço do destinatário
            amount (float): Quantidade de tokens
            
        Returns:
            dict: Informações da transação
        """
        db = SessionLocal()
        try:
            # Busca o usuário no banco para obter a private_key
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                raise Exception("Usuário não encontrado")
            
            sender_address = user.ethereum_address
            private_key = user.private_key
            
            # Verifica se o contrato está disponível
            contract = get_contract()
            if not contract:
                raise Exception("Contrato de token não está deployado. Configure TOKEN_CONTRACT_ADDRESS no config.py")
            
            # Verifica saldo antes de transferir
            balance = get_token_balance(sender_address)
            if balance < amount:
                raise Exception(f"Saldo insuficiente. Saldo atual: {balance} EST, necessário: {amount} EST")
            
            # Realiza a transferência
            tx_hash = transfer_tokens(sender_address, recipient_address, amount, private_key)
            
            return {
                'status': 'success',
                'from': sender_address,
                'to': recipient_address,
                'amount': amount,
                'tx_hash': tx_hash,
                'message': 'Transferência realizada com sucesso'
            }
        except Exception as e:
            raise Exception(f"Erro na transferência: {str(e)}")
        finally:
            db.close()
    
    def get_balance(self, address):
        """
        Retorna o saldo de tokens de um endereço
        
        Args:
            address (str): Endereço Ethereum
            
        Returns:
            float: Saldo em tokens
        """
        try:
            if not address:
                return 0.0
            
            # Verifica se o contrato está disponível
            contract = get_contract()
            if not contract:
                raise Exception("Contrato de token não está deployado. Configure TOKEN_CONTRACT_ADDRESS no config.py")
            
            # Obtém saldo real do contrato
            balance = get_token_balance(address)
            return balance
        except Exception as e:
            raise Exception(f"Erro ao consultar saldo: {str(e)}")
    
    def get_transaction_history(self, address, limit=10):
        """
        Retorna o histórico de transações de um endereço
        
        Args:
            address (str): Endereço Ethereum
            limit (int): Número máximo de transações
            
        Returns:
            list: Lista de transações
        """
        try:
            # Verifica se o contrato está disponível
            contract = get_contract()
            if not contract:
                raise Exception("Contrato de token não está deployado. Configure TOKEN_CONTRACT_ADDRESS no config.py")
            
            # Obtém eventos Transfer do contrato
            # Filtra eventos onde o endereço é from ou to
            transfer_filter_sent = contract.events.Transfer.create_filter(
                fromBlock=0,
                argument_filters={'from': address}
            )
            
            transfer_filter_received = contract.events.Transfer.create_filter(
                fromBlock=0,
                argument_filters={'to': address}
            )
            
            # Obtém todos os eventos
            sent_events = transfer_filter_sent.get_all_entries()
            received_events = transfer_filter_received.get_all_entries()
            
            # Combina e processa os eventos
            all_events = []
            
            for event in sent_events:
                all_events.append({
                    'type': 'sent',
                    'from': event['args']['from'],
                    'to': event['args']['to'],
                    'amount': event['args']['value'] / (10 ** 18),  # Converte de wei para tokens
                    'tx_hash': event['transactionHash'].hex(),
                    'block_number': event['blockNumber'],
                    'timestamp': self._get_block_timestamp(event['blockNumber'])
                })
            
            for event in received_events:
                # Evita duplicatas (quando from == to)
                if event['args']['from'] != address:
                    all_events.append({
                        'type': 'received',
                        'from': event['args']['from'],
                        'to': event['args']['to'],
                        'amount': event['args']['value'] / (10 ** 18),
                        'tx_hash': event['transactionHash'].hex(),
                        'block_number': event['blockNumber'],
                        'timestamp': self._get_block_timestamp(event['blockNumber'])
                    })
            
            # Ordena por número de bloco (mais recente primeiro)
            all_events.sort(key=lambda x: x['block_number'], reverse=True)
            
            # Limita a quantidade de resultados
            return all_events[:limit]
            
        except Exception as e:
            raise Exception(f"Erro ao consultar histórico: {str(e)}")
    
    def _get_block_timestamp(self, block_number):
        """
        Obtém o timestamp de um bloco
        
        Args:
            block_number (int): Número do bloco
            
        Returns:
            int: Timestamp Unix do bloco
        """
        try:
            block = self.web3.eth.get_block(block_number)
            return block['timestamp']
        except Exception as e:
            print(f"Erro ao obter timestamp do bloco {block_number}: {e}")
            return 0