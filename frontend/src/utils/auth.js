// Utilitários de autenticação
// Nota: As funções principais estão em services/api.js

export const getToken = () => {
    return localStorage.getItem('token');
};

export const isAuthenticated = () => {
    return !!getToken();
};

export const getCurrentUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
};

// Função para formatar endereços Ethereum (exibe apenas inicio e fim)
export const formatAddress = (address) => {
    if (!address) return '';
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
};

// Função para formatar valores de tokens
export const formatTokenAmount = (amount) => {
    return parseFloat(amount).toFixed(4);
};

// Função para validar endereço Ethereum
export const isValidEthereumAddress = (address) => {
    return /^0x[a-fA-F0-9]{40}$/.test(address);
};