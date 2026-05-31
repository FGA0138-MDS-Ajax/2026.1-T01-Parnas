import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '', rememberMe: false });
  const [error, setError] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Preencha todos os campos.');
      return;
    }

    if (formData.password.length < 6) {
      setError('Credenciais inválidas. Tente novamente.');
      return;
    }

    const mockToken = `mock_${formData.email.split('@')[0]}_${Date.now()}`;
    login(mockToken);
    navigate('/dashboard');
  };

  const handleDemoAccess = () => {
    login(`mock_demo_${Date.now()}`);
    navigate('/dashboard');
  };

  return (
    <div className="login-card">

      <div className="login-header">
        <div className="login-logo-icon">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#0F4C81" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
            <polyline points="17 6 23 6 23 12" />
          </svg>
        </div>
        <h1 className="login-brand">CREDIFAB</h1>
        <p className="login-brand-sub">Plataforma de Acesso a Crédito</p>
      </div>

      <div className="login-body">
        <h2 className="login-title">Bem-vindo de volta</h2>
        <p className="login-subtitle">Entre com suas credenciais para continuar</p>

        {error && <p className="msg-error">{error}</p>}

        <form onSubmit={handleSubmit} className="login-form">

          <div className="input-group">
            <label>E-mail</label>
            <div className="input-icon-wrapper">
              <svg className="input-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                <polyline points="22,6 12,13 2,6" />
              </svg>
              <input
                type="email"
                name="email"
                placeholder="seu@email.com.br"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="input-group">
            <label>Senha</label>
            <div className="input-icon-wrapper">
              <svg className="input-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="login-options">
            <label className="remember-label">
              <input
                type="checkbox"
                name="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
              />
              <span>Lembrar-me</span>
            </label>
            <Link to="/esqueci-senha" className="forgot-link">Esqueceu a senha?</Link>
          </div>

          <button type="submit" className="btn-submit">Entrar</button>

        </form>

        <div className="divider"><span>ou</span></div>

        <button type="button" className="btn-demo" onClick={handleDemoAccess}>
          Acessar Conta Demo
        </button>

        <p className="login-register">
          Não tem uma conta?{' '}
          <Link to="/Register" className="register-link">Cadastre-se gratuitamente</Link>
        </p>

        <p className="login-footer-text">
          Contribuindo para o ODS 9.3 - Democratizando o acesso ao crédito
        </p>
      </div>

    </div>
  );
};

export default Login;
