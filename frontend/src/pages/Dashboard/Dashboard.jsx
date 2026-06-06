import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const empresasCadastradas = JSON.parse(localStorage.getItem('credifab_empresas_reais') || '[]');

  return (
    <div className="dashboard-container">

      <div className="dashboard-header">
        <h2>Painel de Controle</h2>
        <p>Bem-vindo ao CREDIFAB.</p>
      </div>

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <div>
            <h3 className="dashboard-card-title title-empresa">Gerenciamento de Empresas</h3>
            <p className="dashboard-card-text">
              Cadastre sua empresa para liberar as funções do CREDIFAB.
            </p>
          </div>
          <button
            onClick={() => navigate('/cadastro-empresa')}
            className="dashboard-card-button btn-empresa"
          >
            Acessar Cadastro
          </button>
        </div>

        {/* Transações Financeiras */}
        <div className="dashboard-card">
          <div>
            <h3 className="dashboard-card-title title-transacoes">Transações Financeiras</h3>
            <p className="dashboard-card-text">
              Registre e gerencie entradas e saídas financeiras da sua empresa.
            </p>
          </div>
          <button
            onClick={() => navigate('/transacoes')}
            className="dashboard-card-button btn-transacoes"
          >
            Acessar Transações
          </button>
        </div>

      </div>

      {empresasCadastradas.length > 0 && (
        <div className="dashboard-empresas-section">
          <h3 className="dashboard-empresas-title">Empresas Cadastradas</h3>
          <div className="dashboard-empresas-list">
            {empresasCadastradas.map((empresa, index) => (
              <div className="dashboard-empresa-row" key={empresa.company_id || index}>
                <div className="empresa-row-info">
                  <h4>{empresa.name}</h4>
                  <div className="empresa-row-details">
                    <span><strong>CNPJ:</strong> {empresa.cnpj}</span>
                    <span><strong>E-mail:</strong> {empresa.email}</span>
                    <span><strong>Tel:</strong> {empresa.phone}</span>
                  </div>
                </div>
                <span className="badge-id-banco">ID Banco: {empresa.company_id}</span>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};

export default Dashboard;