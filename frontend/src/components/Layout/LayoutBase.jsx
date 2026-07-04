import React, { useState, useRef, useEffect } from "react";
import { Outlet, Link, useNavigate } from "react-router-dom";
import { Building2, ChevronDown, Plus, Check } from "lucide-react";
import logoImg from "../../assets/CredifabLogo.png";
import { useEmpresa } from "../../context/EmpresaContext";
import "./LayoutBase.css";

const LayoutBase = () => {
  const navigate = useNavigate();
  const { empresas, empresaAtiva, selecionarEmpresa, versaoEmpresa } =
    useEmpresa();
  const [trocandoEmpresa, setTrocandoEmpresa] = useState(false);
  const [erroTroca, setErroTroca] = useState("");
  const [dropdownAberto, setDropdownAberto] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const fecharFora = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownAberto(false);
      }
    };
    document.addEventListener("mousedown", fecharFora);
    return () => document.removeEventListener("mousedown", fecharFora);
  }, []);

  const handleSelecionarEmpresa = async (companyId) => {
    setDropdownAberto(false);
    if (companyId === empresaAtiva?.company_id) return;

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

  const handleCadastrarEmpresa = () => {
    setDropdownAberto(false);
    navigate("/cadastro-empresa");
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
            <div className="empresa-switcher-wrapper" ref={dropdownRef}>
              <button
                className={`empresa-switcher-btn ${dropdownAberto ? "aberto" : ""} ${trocandoEmpresa ? "carregando" : ""}`}
                onClick={() => !trocandoEmpresa && setDropdownAberto((v) => !v)}
                aria-haspopup="listbox"
                aria-expanded={dropdownAberto}
                disabled={trocandoEmpresa}
              >
                <Building2
                  size={15}
                  aria-hidden="true"
                  className="empresa-icon"
                />
                <div className="empresa-btn-texto">
                  <span className="empresa-label">Empresa ativa</span>
                  <span className="empresa-nome">
                    {trocandoEmpresa ? "Alternando..." : empresaAtiva.name}
                  </span>
                </div>
                <ChevronDown
                  size={14}
                  aria-hidden="true"
                  className={`empresa-chevron ${dropdownAberto ? "rotacionado" : ""}`}
                />
              </button>

              {dropdownAberto && (
                <div className="empresa-dropdown" role="listbox">
                  {empresas.length > 0 && (
                    <>
                      <p className="empresa-dropdown-label">Suas empresas</p>
                      <ul className="empresa-lista">
                        {empresas.map((empresa) => {
                          const ativa =
                            Number(empresa.company_id) ===
                            Number(empresaAtiva.company_id);
                          return (
                            <li key={empresa.company_id}>
                              <button
                                role="option"
                                aria-selected={ativa}
                                className={`empresa-item ${ativa ? "empresa-item--ativa" : ""}`}
                                onClick={() =>
                                  handleSelecionarEmpresa(empresa.company_id)
                                }
                              >
                                <span className="empresa-item-nome">
                                  {empresa.name}
                                </span>
                                {ativa && (
                                  <Check
                                    size={14}
                                    aria-hidden="true"
                                    className="empresa-check"
                                  />
                                )}
                              </button>
                            </li>
                          );
                        })}
                      </ul>
                      <div className="empresa-dropdown-divider" />
                    </>
                  )}
                  <button
                    className="empresa-item empresa-item--cadastrar"
                    onClick={handleCadastrarEmpresa}
                  >
                    <Plus size={14} aria-hidden="true" />
                    Cadastrar nova empresa
                  </button>
                </div>
              )}
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
