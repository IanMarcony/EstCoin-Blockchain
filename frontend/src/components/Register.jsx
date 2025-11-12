import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../services/api';
import { useToast } from '../contexts/ToastContext';
import '../styles/Auth.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const toast = useToast();

    const validateForm = () => {
        if (username.length < 3) {
            toast.warning('Nome de usuário deve ter no mínimo 3 caracteres');
            return false;
        }

        if (password.length < 6) {
            toast.warning('Senha deve ter no mínimo 6 caracteres');
            return false;
        }

        if (!/[a-zA-Z]/.test(password)) {
            toast.warning('Senha deve conter pelo menos uma letra');
            return false;
        }

        if (!/\d/.test(password)) {
            toast.warning('Senha deve conter pelo menos um número');
            return false;
        }

        if (password !== confirmPassword) {
            toast.warning('As senhas não coincidem');
            return false;
        }

        return true;
    };

    const handleRegister = async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            const response = await registerUser({ username, password });
            
            // Mostra mensagens de sucesso
            toast.success('Conta criada com sucesso!');
            toast.info(`Saldo inicial: 10 EST creditados`);
            toast.info(`Endereço: ${response.user?.ethereum_address?.substring(0, 10)}...`);
            
            // Aguarda um pouco e redireciona
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (err) {
            console.error('Erro no registro:', err);
            toast.error(err.error || 'Erro ao criar conta. Tente novamente.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>📝 Criar Conta</h2>
                    <p>Registre-se e ganhe 10 EST de bônus!</p>
                </div>

                <form onSubmit={handleRegister} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="username">
                            Nome de Usuário
                            <span className="required">*</span>
                        </label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Mínimo 3 caracteres"
                            required
                            disabled={loading}
                            minLength={3}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">
                            Senha
                            <span className="required">*</span>
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Mínimo 6 caracteres (letra + número)"
                            required
                            disabled={loading}
                            minLength={6}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="confirmPassword">
                            Confirmar Senha
                            <span className="required">*</span>
                        </label>
                        <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Digite a senha novamente"
                            required
                            disabled={loading}
                        />
                    </div>

                    <div className="password-requirements">
                        <h4>Requisitos da senha:</h4>
                        <ul>
                            <li className={password.length >= 6 ? 'valid' : ''}>
                                ✓ Mínimo 6 caracteres
                            </li>
                            <li className={/[a-zA-Z]/.test(password) ? 'valid' : ''}>
                                ✓ Pelo menos uma letra
                            </li>
                            <li className={/\d/.test(password) ? 'valid' : ''}>
                                ✓ Pelo menos um número
                            </li>
                            <li className={password && password === confirmPassword ? 'valid' : ''}>
                                ✓ Senhas coincidem
                            </li>
                        </ul>
                    </div>

                    <button 
                        type="submit" 
                        className="btn-primary"
                        disabled={loading}
                    >
                        {loading ? 'Criando conta...' : 'Criar Conta'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        Já tem uma conta? 
                        <Link to="/login"> Faça login aqui</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register;