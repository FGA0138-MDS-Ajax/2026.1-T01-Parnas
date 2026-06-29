import { Building2, ChevronRight, LoaderCircle } from "lucide-react";
import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import logoImg from "../../assets/LogoFundoBranco.png";
import { useEmpresa } from "../../context/EmpresaContext";
import "./SelecaoEmpresa.css";

const formatarCnpj = (cnpj = "") => {
  const numeros = cnpj.replace(/\D/g, "");
  if (numeros.length !== 14) return cnpj;
  return numeros.replace(
    /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
    "$1.$2.$3/$4-$5",
  );
};

const SelecaoEmpresa = () => {
  const {
    empresas,
    empresaAtiva,
    carregandoEmpresas,
    erroEmpresas,
    selecionarEmpresa,
    recarregarEmpresas,
  } = useEmpresa();
  const [selecionandoId, setSelecionandoId] = useState(null);
  const [erroSelecao, setErroSelecao] = useState("");
  const navigate = useNavigate();

  if (empresaAtiva && !carregandoEmpresas) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSelecionar = async (empresa) => {
    setSelecionandoId(empresa.company_id);
    setErroSelecao("");

    try {
      await selecionarEmpresa(empresa);
      navigate("/dashboard", { replace: true });
    } catch (error) {
      setErroSelecao(error.message);
      setSelecionandoId(null);
    }
  };

  return (
    <main className="selecao-empresa-page">
      <section className="selecao-empresa-card">
        <div className="selecao-empresa-brand">
          <img src={logoImg} alt="CREDIFAB" />
          <span>CREDIFAB</span>
        </div>

        <div className="selecao-empresa-heading">
          <div className="selecao-empresa-icon">
            <Building2 size={28} aria-hidden="true" />
          </div>
          <h1>Escolha a empresa ativa</h1>
          <p>
            Os dados exibidos e cadastrados serão vinculados à empresa
            selecionada.
          </p>
        </div>

        {carregandoEmpresas ? (
          <div className="selecao-empresa-status" role="status">
            <LoaderCircle className="selecao-empresa-spinner" />
            Carregando suas empresas...
          </div>
        ) : (
          <>
            {(erroEmpresas || erroSelecao) && (
              <div className="selecao-empresa-erro" role="alert">
                <p>{erroSelecao || erroEmpresas}</p>
                {erroEmpresas && (
                  <button type="button" onClick={recarregarEmpresas}>
                    Tentar novamente
                  </button>
                )}
              </div>
            )}

            {!erroEmpresas && empresas.length === 0 && (
              <div className="selecao-empresa-vazio">
                <h2>Nenhuma empresa vinculada</h2>
                <p>Cadastre sua primeira empresa para continuar.</p>
                <button
                  type="button"
                  onClick={() => navigate("/cadastro-empresa")}
                >
                  Cadastrar empresa
                </button>
              </div>
            )}

            <div className="selecao-empresa-lista">
              {empresas.map((empresa) => {
                const selecionando =
                  Number(selecionandoId) === Number(empresa.company_id);

                return (
                  <button
                    type="button"
                    className="selecao-empresa-item"
                    key={empresa.company_id}
                    onClick={() => handleSelecionar(empresa)}
                    disabled={selecionandoId !== null}
                  >
                    <span className="selecao-empresa-avatar">
                      {empresa.name?.charAt(0).toUpperCase() || "E"}
                    </span>
                    <span className="selecao-empresa-dados">
                      <strong>{empresa.name}</strong>
                      <small>CNPJ {formatarCnpj(empresa.cnpj)}</small>
                    </span>
                    {selecionando ? (
                      <LoaderCircle className="selecao-empresa-spinner" />
                    ) : (
                      <ChevronRight aria-hidden="true" />
                    )}
                  </button>
                );
              })}
            </div>
            <div className="selecao-empresa-acoes">
              <button
                type="button"
                className="selecao-empresa-btn-novo"
                onClick={() => navigate("/cadastro-empresa")}
              >
                + Cadastrar nova empresa
              </button>
            </div>
          </>
        )}
      </section>
    </main>
  );
};

export default SelecaoEmpresa;
