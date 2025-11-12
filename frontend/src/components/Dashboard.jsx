import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getBalance, getTransactionHistory, isAuthenticated, getCurrentUser } from '../services/api';
import { logout, formatAddress, formatTokenAmount } from '../utils/auth';
import { useToast } from '../contexts/ToastContext';
import Transfer from './Transfer';
import '../styles/Dashboard.css';

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [balance, setBalance] = useState(null);
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showTransfer, setShowTransfer] = useState(false);
    const navigate = useNavigate();
    const toast = useToast();

    useEffect(() => {
        // Verifica autenticação
        if (!isAuthenticated()) {
            navigate('/login');
            return;
        }

        fetchDashboardData();
    }, [navigate]);

    const fetchDashboardData = async () => {
        setLoading(true);

        try {
            // Obtém dados do usuário do localStorage
            const userData = getCurrentUser();
            setUser(userData);

            // Busca saldo
            const balanceData = await getBalance();
            setBalance(balanceData.balance);

            // Busca histórico de transações
            const historyData = await getTransactionHistory(10);
            setTransactions(historyData.transactions || []);
        } catch (err) {
            console.error('Erro ao carregar dados:', err);
            toast.error('Erro ao carregar dados do dashboard');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        toast.info('Até logo! Você foi desconectado.');
        setTimeout(() => {
            logout();
            navigate('/login');
        }, 500);
    };

    const handleTransferSuccess = () => {
        setShowTransfer(false);
        toast.info('Atualizando saldo e histórico...');
        fetchDashboardData(); // Recarrega os dados
    };

    if (loading) {
        return (
            <div className="dashboard-container">
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Carregando dados...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            {/* Header */}
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🪙 EstCoin Dashboard</h1>
                    <button onClick={handleLogout} className="btn-logout">
                        Sair
                    </button>
                </div>
            </header>

            {/* User Info Card */}
            {user && (
                <div className="user-card">
                    <div className="user-info">
                        <h2>👤 {user.username}</h2>
                        <div className="user-address">
                            <span className="label">Endereço Ethereum:</span>
                            <code>{user.ethereum_address}</code>
                            <button 
                                onClick={() => {
                                    navigator.clipboard.writeText(user.ethereum_address);
                                    toast.success('Endereço copiado para a área de transferência!');
                                }}
                                className="btn-copy"
                                title="Copiar endereço"
                            >
                                📋
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Balance Card */}
            <div className="balance-card">
                <div className="balance-content">
                    <h3>Saldo Disponível</h3>
                    <div className="balance-amount">
                        {balance !== null ? (
                            <>
                                <span className="amount">{formatTokenAmount(balance)}</span>
                                <span className="currency">EST</span>
                            </>
                        ) : (
                            <span className="loading-text">Carregando...</span>
                        )}
                    </div>
                    <button 
                        onClick={() => setShowTransfer(!showTransfer)} 
                        className="btn-primary"
                    >
                        {showTransfer ? 'Cancelar' : '💸 Fazer Transferência'}
                    </button>
                </div>
            </div>

            {/* Transfer Component */}
            {showTransfer && (
                <Transfer 
                    onSuccess={handleTransferSuccess}
                    onCancel={() => setShowTransfer(false)}
                />
            )}

            {/* Transaction History */}
            <div className="transactions-card">
                <div className="transactions-header">
                    <h3>📜 Histórico de Transações</h3>
                    <button 
                        onClick={fetchDashboardData} 
                        className="btn-refresh"
                        title="Atualizar"
                    >
                        🔄
                    </button>
                </div>

                {transactions.length === 0 ? (
                    <div className="no-transactions">
                        <p>📭 Nenhuma transação registrada ainda.</p>
                        <p className="hint">Faça sua primeira transferência!</p>
                    </div>
                ) : (
                    <div className="transactions-list">
                        {transactions.map((tx, index) => (
                            <div key={index} className="transaction-item">
                                <div className="tx-icon">
                                    {tx.from === user?.ethereum_address ? '📤' : '📥'}
                                </div>
                                <div className="tx-details">
                                    <div className="tx-addresses">
                                        <span className="tx-label">De:</span>
                                        <code>{formatAddress(tx.from)}</code>
                                        <span className="tx-arrow">→</span>
                                        <span className="tx-label">Para:</span>
                                        <code>{formatAddress(tx.to)}</code>
                                    </div>
                                    {tx.timestamp && (
                                        <div className="tx-timestamp">
                                            {new Date(tx.timestamp).toLocaleString('pt-BR')}
                                        </div>
                                    )}
                                </div>
                                <div className={`tx-amount ${tx.from === user?.ethereum_address ? 'sent' : 'received'}`}>
                                    {tx.from === user?.ethereum_address ? '-' : '+'}
                                    {formatTokenAmount(tx.value)} EST
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;