import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import { isAuthenticated } from './services/api';
import { ToastProvider } from './contexts/ToastContext';
import './styles/App.css';

// Componente para proteger rotas
const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

const App = () => {
  return (
    <ToastProvider>
      <Router>
        <div className="app">
          <Routes>
            {/* Rota padrão redireciona para login ou dashboard */}
            <Route 
              path="/" 
              element={
                isAuthenticated() ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
              } 
            />
            
            {/* Rotas públicas */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Rotas protegidas */}
            <Route 
              path="/dashboard" 
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } 
            />

            {/* Rota 404 */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </Router>
    </ToastProvider>
  );
};

export default App;