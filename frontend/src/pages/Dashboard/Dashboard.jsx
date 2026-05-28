import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="dashboard-container">

      <div className="dashboard-header">
        <h2>Painel de Controle</h2>
        <p>Bem-vindo ao ambiente integrado do CREDIFAB.</p>
      </div>

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <div>
            <h3 className="dashboard-card-title title-empresa">Gerenciamento de Empresas</h3>
            <p className="dashboard-card-text">
              Cadastre sua empresa  para liberar as funções do CREDIFAB.
            </p>
          </div>
          <button
            onClick={() => navigate('/cadastro-empresa')}
            className="dashboard-card-button btn-empresa"
          >
            Acessar Cadastro
          </button>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;