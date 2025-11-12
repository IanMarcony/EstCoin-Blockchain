import React, { useState } from 'react';
import { transferFunds } from '../services/api';
import { isValidEthereumAddress } from '../utils/auth';
import { useToast } from '../contexts/ToastContext';
import '../styles/Transfer.css';

const Transfer = ({ onSuccess, onCancel }) => {
    const [recipient, setRecipient] = useState('');
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const toast = useToast();

    const validateForm = () => {
        if (!recipient.trim()) {
            toast.warning('Endereço do destinatário é obrigatório');
            return false;
        }

        if (!isValidEthereumAddress(recipient)) {
            toast.error('Endereço Ethereum inválido. Deve começar com 0x e ter 42 caracteres');
            return false;
        }

        if (!amount || parseFloat(amount) <= 0) {
            toast.warning('Quantidade deve ser maior que zero');
            return false;
        }

        return true;
    };

    const handleTransfer = async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            const response = await transferFunds({
                recipient: recipient.trim(),
                amount: parseFloat(amount)
            });

            toast.success(`Transferência realizada com sucesso! ${amount} EST enviados`);
            toast.info(`Para: ${recipient.substring(0, 10)}...${recipient.substring(recipient.length - 8)}`);
            
            // Limpa o formulário
            setRecipient('');
            setAmount('');

            // Aguarda um pouco e chama o callback de sucesso
            setTimeout(() => {
                if (onSuccess) {
                    onSuccess();
                }
            }, 1500);
        } catch (err) {
            console.error('Erro na transferência:', err);
            toast.error(err.error || 'Erro ao realizar a transferência');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="transfer-container">
            <div className="transfer-card">
                <div className="transfer-header">
                    <h3>💸 Fazer Transferência</h3>
                    {onCancel && (
                        <button onClick={onCancel} className="btn-close">
                            ✕
                        </button>
                    )}
                </div>

                <form onSubmit={handleTransfer} className="transfer-form">
                    <div className="form-group">
                        <label htmlFor="recipient">
                            Endereço do Destinatário
                            <span className="required">*</span>
                        </label>
                        <input
                            type="text"
                            id="recipient"
                            value={recipient}
                            onChange={(e) => setRecipient(e.target.value)}
                            placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                            disabled={loading}
                        />
                        <small className="hint">
                            Endereço Ethereum (0x...) com 42 caracteres
                        </small>
                    </div>

                    <div className="form-group">
                        <label htmlFor="amount">
                            Quantidade (EST)
                            <span className="required">*</span>
                        </label>
                        <input
                            type="number"
                            id="amount"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            placeholder="0.00"
                            step="0.0001"
                            min="0.0001"
                            disabled={loading}
                        />
                        <small className="hint">
                            Quantidade de tokens EstCoin a transferir
                        </small>
                    </div>

                    <div className="transfer-actions">
                        {onCancel && (
                            <button 
                                type="button"
                                onClick={onCancel}
                                className="btn-secondary"
                                disabled={loading}
                            >
                                Cancelar
                            </button>
                        )}
                        <button 
                            type="submit"
                            className="btn-primary"
                            disabled={loading}
                        >
                            {loading ? '⏳ Processando...' : '💸 Enviar'}
                        </button>
                    </div>
                </form>

                <div className="transfer-info">
                    <h4>ℹ️ Informações Importantes:</h4>
                    <ul>
                        <li>✓ A transação será registrada na blockchain</li>
                        <li>✓ Verifique o endereço antes de enviar</li>
                        <li>✓ Transações não podem ser revertidas</li>
                        <li>✓ Aguarde alguns segundos para confirmação</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Transfer;