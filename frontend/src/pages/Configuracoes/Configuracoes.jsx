import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Configuracoes.css";
import useAuth from "../../hooks/useAuth.js";

const Configuracoes = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalType, setModalType] = useState(null);
  const [cnpjInput, setCnpjInput] = useState("");

  const handleOpenModal = (type) => {
    setModalType(type);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setModalType(null);
    setCnpjInput("");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    if (logout) {
      logout();
    }
    window.location.href = "/";
  };

  const handleConfirmAction = async () => {
    if (modalType === "company") {
      if (!cnpjInput.trim()) {
        alert("Por favor, informe o CNPJ da empresa que deseja excluir.");
        return;
      }

      const limparCacheLocal = () => {
        const locaisAtuais = JSON.parse(
          localStorage.getItem("credifab_empresas_reais") || "[]",
        );
        const cnpjDigitadoLimpo = cnpjInput.trim().replace(/\D/g, "");

        const locaisAtualizados = locaisAtuais.filter((emp) => {
          const cnpjBancoLimpo = emp.cnpj.replace(/\D/g, "");
          return cnpjBancoLimpo !== cnpjDigitadoLimpo;
        });

        localStorage.setItem(
          "credifab_empresas_reais",
          JSON.stringify(locaisAtualizados),
        );
        localStorage.removeItem("idEmpresaSimulado");
      };

      try {
        const token = localStorage.getItem("token");

        const response = await axios.delete(
          "http://127.0.0.1:5000/api/companies/delete",
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            data: {
              cnpj: cnpjInput.trim(),
            },
          },
        );

        alert(response.data.mensagem || "Empresa excluída com sucesso.");
        limparCacheLocal();
        handleCloseModal();
        window.location.reload();
      } catch (error) {
        console.error("Erro na integração de exclusão:", error);

        if (error.response?.status === 404) {
          alert(
            "Esta empresa já foi removida do servidor. Atualizando seu painel local...",
          );
          limparCacheLocal();
          handleCloseModal();
          window.location.reload();
          return;
        }

        if (error.response?.data?.erros_de_validacao) {
          alert("O backend recusou: O formato do CNPJ digitado é inválido.");
        } else {
          alert(error.response?.data?.erro || "Erro interno do servidor.");
        }
      }
    } else if (modalType === "user") {
      console.log("Executando integração para: Excluir Conta");
      handleCloseModal();
      navigate("/login", { replace: true });
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

              {modalType === "company" && (
                <div className="company-input-container">
                  <label
                    htmlFor="company-cnpj-field"
                    className="company-input-label"
                  >
                    Confirme o CNPJ da empresa para remoção:
                  </label>
                  <input
                    id="company-cnpj-field"
                    type="text"
                    placeholder="Digite apenas números ou formato padrão"
                    value={cnpjInput}
                    onChange={(e) => setCnpjInput(e.target.value)}
                    className="company-cnpj-input"
                  />
                </div>
              )}

              <p className="modal-warning-text">
                {modalType === "company"
                  ? "Aviso: A empresa correspondente ao CNPJ, os históricos de crédito e todos os dados associados serão apagados permanentemente."
                  : "Aviso: Sua conta será excluída e você perderá o acesso à plataforma CREDIFAB imediatamente."}
              </p>
            </div>

            <div className="modal-footer">
              <button className="btn-modal-cancel" onClick={handleCloseModal}>
                Cancelar
              </button>
              <button
                className="btn-modal-confirm"
                onClick={handleConfirmAction}
              >
                Confirmar e Excluir
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Configuracoes;
