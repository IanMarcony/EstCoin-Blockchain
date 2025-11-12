from flask import Blueprint, request, jsonify
from src.controllers.transaction_controller import TransactionController
from src.utils.auth_utils import token_required

transactions_bp = Blueprint('transactions', __name__)
transaction_controller = TransactionController()

@transactions_bp.route('/transfer', methods=['POST'])
@token_required
def transfer(current_user):
    """
    Rota para transferir tokens entre usuários
    Requer autenticação via token JWT
    
    Body JSON:
        - recipient (str): Endereço Ethereum do destinatário
        - amount (float): Quantidade de tokens a transferir
    
    Returns:
        JSON com dados da transação ou erro
    """
    data = request.json
    
    # O sender agora vem do token autenticado (current_user)
    sender = current_user.get('ethereum_address')
    recipient = data.get('recipient')
    amount = data.get('amount')

    # Validações
    if not recipient:
        return jsonify({'error': 'Endereço do destinatário é obrigatório'}), 400
    
    if not amount:
        return jsonify({'error': 'Quantidade é obrigatória'}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'error': 'A quantidade deve ser maior que zero'}), 400
    except ValueError:
        return jsonify({'error': 'Quantidade inválida'}), 400
    
    # Validação de endereço Ethereum (básica)
    if not recipient.startswith('0x') or len(recipient) != 42:
        return jsonify({'error': 'Endereço Ethereum inválido'}), 400

    try:
        transaction = transaction_controller.transfer_funds(sender, recipient, amount)
        return jsonify({
            'message': 'Transferência realizada com sucesso',
            'transaction': transaction,
            'from': sender,
            'to': recipient,
            'amount': amount,
            'user': current_user.get('username')
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao realizar transferência: {str(e)}'}), 500


@transactions_bp.route('/balance', methods=['GET'])
@token_required
def get_balance(current_user):
    """
    Rota para consultar o saldo do usuário autenticado
    Requer autenticação via token JWT
    
    Returns:
        JSON com o saldo do usuário
    """
    try:
        ethereum_address = current_user.get('ethereum_address')
        balance = transaction_controller.get_balance(ethereum_address)
        
        return jsonify({
            'username': current_user.get('username'),
            'ethereum_address': ethereum_address,
            'balance': balance
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao consultar saldo: {str(e)}'}), 500


@transactions_bp.route('/history', methods=['GET'])
@token_required
def get_transaction_history(current_user):
    """
    Rota para consultar histórico de transações do usuário
    Requer autenticação via token JWT
    
    Query params opcionais:
        - limit (int): Número máximo de transações (padrão: 10)
    
    Returns:
        JSON com lista de transações
    """
    try:
        ethereum_address = current_user.get('ethereum_address')
        limit = request.args.get('limit', 10, type=int)
        
        transactions = transaction_controller.get_transaction_history(
            ethereum_address, 
            limit
        )
        
        return jsonify({
            'username': current_user.get('username'),
            'ethereum_address': ethereum_address,
            'transactions': transactions,
            'count': len(transactions)
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao consultar histórico: {str(e)}'}), 500