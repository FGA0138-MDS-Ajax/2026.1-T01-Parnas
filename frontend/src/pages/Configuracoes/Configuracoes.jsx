import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Configuracoes.css";
import useAuth from "../../hooks/useAuth.js";
import { useEmpresa } from "../../context/EmpresaContext";
import api from "../../services/api";

const Configuracoes = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { idEmpresaLogada, recarregarEmpresas, selecionarEmpresa } =
    useEmpresa();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalType, setModalType] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");

  const handleOpenModal = (type) => {
    setErro("");
    setModalType(type);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    if (carregando) return;
    setIsModalOpen(false);
    setModalType(null);
    setErro("");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    if (logout) logout();
    window.location.href = "/";
  };

  const handleConfirmAction = async () => {
    setErro("");
    setCarregando(true);

    try {
      if (modalType === "company") {
        if (!idEmpresaLogada) {
          setErro("Nenhuma empresa ativa selecionada.");
          return;
        }

        await api.delete(`/api/companies/${idEmpresaLogada}`);

        handleCloseModal();

        const empresasRestantes = await recarregarEmpresas();
        if (empresasRestantes?.length > 0) {
          await selecionarEmpresa(empresasRestantes[0]);
        }

        navigate("/dashboard");
      } else if (modalType === "user") {
        await api.delete("/api/usuarios/profile");

        handleCloseModal();
        localStorage.removeItem("token");
        localStorage.removeItem("empresaAtiva");
        if (logout) logout();
        navigate("/login", { replace: true });
      }
    } catch (error) {
      const mensagem =
        error.response?.data?.erro ||
        error.response?.data?.mensagem ||
        "Ocorreu um erro ao processar a solicitação. Tente novamente.";
      setErro(mensagem);
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="config-container">
      <div className="config-header">
        <h2>Configurações</h2>
        <p>Gerencie as preferências da sua conta.</p>
      </div>

      <div className="config-card">
        <div className="admin-actions">
          <div className="admin-row">
            <div className="admin-info">
              <h4>Dados do Perfil</h4>
              <p>Atualize suas informações pessoais.</p>
            </div>
            <button
              onClick={() => navigate("/editar-perfil")}
              className="btn-action-primary"
            >
              Editar Perfil
            </button>
          </div>

          <div className="admin-row">
            <div className="admin-info">
              <h4>Sair do Sistema</h4>
              <p>
                Encerra sua sessão atual com segurança e remove suas credenciais
                temporárias do navegador.
              </p>
            </div>
            <button onClick={handleLogout} className="btn-action-danger">
              Sair da Conta
            </button>
          </div>

          <div className="admin-row">
            <div className="admin-info">
              <h4>Excluir Empresa</h4>
              <p>
                Deleta a Empresa, históricos e remove os registros e dados
                vinculados à plataforma.
              </p>
            </div>
            <button
              onClick={() => handleOpenModal("company")}
              className="btn-action-danger"
              disabled={!idEmpresaLogada}
              title={!idEmpresaLogada ? "Selecione uma empresa primeiro" : ""}
            >
              Excluir Empresa
            </button>
          </div>

          <div className="admin-row">
            <div className="admin-info">
              <h4>Excluir minha conta</h4>
              <p>
                Desativa seu acesso à plataforma CREDIFAB e encerra suas
                credenciais de usuário.
              </p>
            </div>
            <button
              onClick={() => handleOpenModal("user")}
              className="btn-action-danger"
            >
              Excluir Conta
            </button>
          </div>
        </div>
      </div>

      {isModalOpen && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Confirmar Exclusão</h3>
            </div>

            <div className="modal-body">
              <p>
                Você tem certeza que deseja prosseguir? Esta ação é{" "}
                <strong>definitiva e totalmente irreversível</strong>.
              </p>
              <p className="modal-warning-text">
                {modalType === "company"
                  ? "Aviso: A empresa, os históricos de crédito e todos os dados associados serão apagados permanentemente."
                  : "Aviso: Sua conta será excluída e você perderá o acesso à plataforma CREDIFAB imediatamente."}
              </p>

              {erro && (
                <p
                  style={{
                    color: "red",
                    marginTop: "0.5rem",
                    fontSize: "0.9rem",
                  }}
                >
                  {erro}
                </p>
              )}
            </div>

            <div className="modal-footer">
              <button
                className="btn-modal-cancel"
                onClick={handleCloseModal}
                disabled={carregando}
              >
                Cancelar
              </button>
              <button
                className="btn-modal-confirm"
                onClick={handleConfirmAction}
                disabled={carregando}
              >
                {carregando ? "Processando..." : "Confirmar e Excluir"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Configuracoes;
