import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginUser } from '../services/api';
import { useToast } from '../contexts/ToastContext';
import '../styles/Auth.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const toast = useToast();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await loginUser({ username, password });
            
            // Login bem-sucedido
            toast.success(`Bem-vindo, ${response.user?.username || username}!`);
            
            // Aguarda um pouco para mostrar o toast antes de redirecionar
            setTimeout(() => {
                navigate('/dashboard');
            }, 500);
        } catch (err) {
            console.error('Erro no login:', err);
            toast.error(err.error || 'Erro ao fazer login. Verifique suas credenciais.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>🔐 Login</h2>
                    <p>Acesse sua carteira blockchain</p>
                </div>

                <form onSubmit={handleLogin} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="username">Usuário</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Digite seu nome de usuário"
                            required
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Senha</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Digite sua senha"
                            required
                            disabled={loading}
                        />
                    </div>

                    <button 
                        type="submit" 
                        className="btn-primary"
                        disabled={loading}
                    >
                        {loading ? 'Entrando...' : 'Entrar'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        Não tem uma conta? 
                        <Link to="/register"> Registre-se aqui</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;