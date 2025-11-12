import axios from 'axios';

const API_URL = 'http://localhost:5000/api'; // URL base da API

// Configuração do interceptor do axios para adicionar o token em todas as requisições
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para tratar erros de autenticação
axios.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Token inválido ou expirado - faz logout
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// ============ AUTENTICAÇÃO ============

// Função para registrar um novo usuário
export const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${API_URL}/auth/register`, userData);
        
        // Armazena o token e dados do usuário após registro
        if (response.data.token && response.data.user) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            localStorage.setItem('username', response.data.user.username);
            localStorage.setItem('ethereum_address', response.data.user.ethereum_address);
        }
        
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: 'Erro ao registrar usuário' };
    }
};

// Função para fazer login
export const loginUser = async (credentials) => {
    try {
        const response = await axios.post(`${API_URL}/auth/login`, credentials);
        
        // Armazena o token e dados do usuário
        if (response.data.token && response.data.user) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            localStorage.setItem('username', response.data.user.username);
            localStorage.setItem('ethereum_address', response.data.user.ethereum_address);
        }
        
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: 'Erro ao fazer login' };
    }
};

// Função para logout
export const logoutUser = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('username');
    localStorage.removeItem('ethereum_address');
};

// Verifica se o usuário está autenticado
export const isAuthenticated = () => {
    return !!localStorage.getItem('token');
};

// Obtém dados do usuário logado
export const getCurrentUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};

// Obtém o username do usuário logado
export const getUsername = () => {
    return localStorage.getItem('username');
};

// Obtém o endereço Ethereum do usuário logado
export const getEthereumAddress = () => {
    return localStorage.getItem('ethereum_address');
};

// ============ TRANSAÇÕES ============

// Função para transferir fundos
export const transferFunds = async (transferData) => {
    try {
        const response = await axios.post(`${API_URL}/transactions/transfer`, transferData);
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: 'Erro ao transferir fundos' };
    }
};

// Função para obter o saldo do usuário
export const getBalance = async () => {
    try {
        const response = await axios.get(`${API_URL}/transactions/balance`);
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: 'Erro ao obter saldo' };
    }
};

// Função para obter histórico de transações
export const getTransactionHistory = async (limit = 20) => {
    try {
        const response = await axios.get(`${API_URL}/transactions/history?limit=${limit}`);
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: 'Erro ao obter histórico' };
    }
};