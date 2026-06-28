import React from "react";
import { useNavigate } from "react-router-dom";
import { useEmpresa } from "../../context/EmpresaContext";
import "./Dashboard.css";

const Dashboard = () => {
  const navigate = useNavigate();
  const { empresas } = useEmpresa();

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Painel de Controle</h2>
        <p>Bem-vindo ao CREDIFAB.</p>
      </div>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <div>
            <h3 className="dashboard-card-title title-empresa">
              Gerenciamento de Empresas
            </h3>
            <p className="dashboard-card-text">
              Cadastre sua empresa para liberar as funções do CREDIFAB.
            </p>
          </div>
          <button
            onClick={() => navigate("/cadastro-empresa")}
            className="dashboard-card-button btn-empresa"
          >
            Acessar Cadastro
          </button>
        </div>
      </div>
      {empresas.length > 0 && (
        <div className="dashboard-empresas-section">
          <h3 className="dashboard-empresas-title">Empresas Cadastradas</h3>
          <div className="dashboard-empresas-list">
            {empresas.map((empresa, index) => (
              <div
                className="dashboard-empresa-row"
                key={empresa.company_id || index}
              >
                <div className="empresa-row-info">
                  <h4>{empresa.name}</h4>
                  <div className="empresa-row-details">
                    <span>
                      <strong>CNPJ:</strong> {empresa.cnpj}
                    </span>
                  </div>
                </div>
                <span className="badge-id-banco">
                  ID Banco: {empresa.company_id}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;