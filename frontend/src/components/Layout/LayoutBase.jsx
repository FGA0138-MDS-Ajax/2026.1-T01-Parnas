import React, { useState } from "react";
import { Outlet, Link, useNavigate } from "react-router-dom";
import { Building2 } from "lucide-react";
import logoImg from "../../assets/CredifabLogo.png";
import { useEmpresa } from "../../context/EmpresaContext";
import "./LayoutBase.css";

const LayoutBase = () => {
  const navigate = useNavigate();
  const { empresas, empresaAtiva, selecionarEmpresa, versaoEmpresa } =
    useEmpresa();
  const [trocandoEmpresa, setTrocandoEmpresa] = useState(false);
  const [erroTroca, setErroTroca] = useState("");

  const handleTrocarEmpresa = async (event) => {
    const valor = event.target.value;

    if (valor === "nova_empresa") {
      navigate("/cadastro-empresa");
      return;
    }

    const companyId = Number(valor);
    if (!companyId || companyId === Number(empresaAtiva?.company_id)) return;

    setTrocandoEmpresa(true);
    setErroTroca("");
    try {
      await selecionarEmpresa(companyId);
    } catch (error) {
      setErroTroca(error.message);
    } finally {
      setTrocandoEmpresa(false);
    }
  };

  return (
    <div className="layout-container">
      <header className="layout-header">
        <Link to="/dashboard" className="logo-link">
          <div className="logo-section">
            <img
              src={logoImg}
              alt="Logo CREDIFAB"
              className="layout-logo-img"
            />
            <div className="logo-text">
              <h1>CREDIFAB</h1>
              <p>Plataforma de Acesso a Crédito</p>
            </div>
          </div>
        </Link>

        <nav className="layout-nav">
          <Link to="/dashboard" className="nav-link">
            Dashboard
          </Link>
          <Link to="/documentos" className="nav-link">
            Documentos
          </Link>
          <Link to="/transacoes" className="nav-link">
            Transações
          </Link>
          <Link to="/contas" className="nav-link">
            Contas
          </Link>
          <Link to="/simulacoes" className="nav-link">
            Simulações
          </Link>
          <Link to="/comparacoes" className="nav-link">
            Comparações
          </Link>
          <Link to="/relatorios" className="nav-link">
            Relatórios
          </Link>
          <Link to="/categorias" className="nav-link">
            Categorias
          </Link>
        </nav>

        <div className="layout-actions">
          {empresaAtiva && (
            <div className="empresa-switcher">
              <Building2 size={17} aria-hidden="true" />
              <select
                id="empresa-ativa"
                value={empresaAtiva.company_id}
                onChange={handleTrocarEmpresa}
                disabled={trocandoEmpresa}
              >
                {empresas.map((empresa) => (
                  <option key={empresa.company_id} value={empresa.company_id}>
                    {empresa.name}
                  </option>
                ))}
                <option value="nova_empresa"> + Cadastrar nova empresa </option>
              </select>
            </div>
          )}
          <button
            onClick={() => navigate("/configuracoes")}
            className="btn-settings"
          >
            Configurações
          </button>
        </div>
      </header>

      {erroTroca && (
        <div className="layout-company-error" role="alert">
          {erroTroca}
        </div>
      )}

      <main className="layout-main">
        <div key={versaoEmpresa}>
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default LayoutBase;
