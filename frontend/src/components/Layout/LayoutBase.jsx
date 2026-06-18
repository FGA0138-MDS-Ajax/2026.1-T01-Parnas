import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import './LayoutBase.css';

const LayoutBase = () => {
  const navigate = useNavigate();

  return (
    <div className="layout-container">

      <header className="layout-header">

        <Link to="/dashboard" className="logo-link">
          <div className="logo-section">
            <div className="logo-icon-wrapper">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="3">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
              </svg>
            </div>
            <div className="logo-text">
              <h1>CREDIFAB</h1>
              <p>Plataforma de Acesso a Crédito</p>
            </div>
          </div>
        </Link>

        <nav className="layout-nav">
          <Link to="/dashboard" className="nav-link">Dashboard</Link>
          <Link to="/transacoes" className="nav-link">Transações</Link>
          <Link to="/contas" className="nav-link">Contas</Link>
          <Link to="/simulacoes" className="nav-link">Simulações</Link>
          <Link to="/comparacoes" className="nav-link">Comparações</Link>
          <Link to="/relatorios" className="nav-link">Relatórios</Link>
        </nav>

        <button
          onClick={() => navigate('/configuracoes')}
          className="btn-settings"
        >
          Configurações
        </button>
      </header>

      <main className="layout-main">
        <Outlet />
      </main>

    </div>
  );
};

export default LayoutBase;
