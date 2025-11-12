import React, { createContext, useContext, useState, useCallback } from 'react';
import '../styles/Toast.css';

const ToastContext = createContext();

export const useToast = () => {
    const context = useContext(ToastContext);
    if (!context) {
        throw new Error('useToast deve ser usado dentro de ToastProvider');
    }
    return context;
};

export const ToastProvider = ({ children }) => {
    const [toasts, setToasts] = useState([]);

    const addToast = useCallback((message, type = 'info') => {
        const id = Date.now();
        const newToast = {
            id,
            message,
            type, // 'success', 'error', 'warning', 'info'
        };

        setToasts((prev) => [...prev, newToast]);

        // Remove o toast após 5 segundos
        setTimeout(() => {
            removeToast(id);
        }, 5000);

        return id;
    }, []);

    const removeToast = useCallback((id) => {
        setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, []);

    // Atalhos para tipos específicos
    const success = useCallback((message) => addToast(message, 'success'), [addToast]);
    const error = useCallback((message) => addToast(message, 'error'), [addToast]);
    const warning = useCallback((message) => addToast(message, 'warning'), [addToast]);
    const info = useCallback((message) => addToast(message, 'info'), [addToast]);

    return (
        <ToastContext.Provider value={{ addToast, success, error, warning, info, removeToast }}>
            {children}
            <ToastContainer toasts={toasts} removeToast={removeToast} />
        </ToastContext.Provider>
    );
};

const ToastContainer = ({ toasts, removeToast }) => {
    return (
        <div className="toast-container">
            {toasts.map((toast) => (
                <Toast
                    key={toast.id}
                    toast={toast}
                    onClose={() => removeToast(toast.id)}
                />
            ))}
        </div>
    );
};

const Toast = ({ toast, onClose }) => {
    const getIcon = () => {
        switch (toast.type) {
            case 'success':
                return '✓';
            case 'error':
                return '✕';
            case 'warning':
                return '⚠';
            case 'info':
                return 'ℹ';
            default:
                return 'ℹ';
        }
    };

    const getTitle = () => {
        switch (toast.type) {
            case 'success':
                return 'Sucesso';
            case 'error':
                return 'Erro';
            case 'warning':
                return 'Atenção';
            case 'info':
                return 'Informação';
            default:
                return 'Notificação';
        }
    };

    return (
        <div className={`toast toast-${toast.type}`}>
            <div className="toast-icon">{getIcon()}</div>
            <div className="toast-content">
                <div className="toast-title">{getTitle()}</div>
                <div className="toast-message">{toast.message}</div>
            </div>
            <button className="toast-close" onClick={onClose}>
                ✕
            </button>
        </div>
    );
};
