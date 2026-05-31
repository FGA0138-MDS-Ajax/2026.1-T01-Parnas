import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Configuracoes.css';

const Configuracoes = () => {
  const navigate = useNavigate();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalType, setModalType] = useState(null);

  const handleOpenModal = (type) => {
    setModalType(type);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setModalType(null);
  };

  const handleConfirmAction = () => {
    if (modalType === 'company') {
      console.log("Executando integração para: Excluir Empresa");

      handleCloseModal();
    } else if (modalType === 'user') {
      console.log("Executando integração para: Excluir Conta");

      handleCloseModal();

      navigate('/login', { replace: true });
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
              <h4>Excluir Empresa</h4>
              <p>Deleta a Empresa, históricos e remove os registros e dados vinculados à plataforma.</p>
            </div>
            <button onClick={() => handleOpenModal('company')} className="btn-action-danger">
              Excluir Empresa
            </button>
          </div>

          <div className="admin-row">
            <div className="admin-info">
              <h4>Excluir minha conta</h4>
              <p>Desativa seu acesso à plataforma CREDIFAB e encerra suas credenciais de usuário.</p>
            </div>
            <button onClick={() => handleOpenModal('user')} className="btn-action-danger">
              Excluir Conta
            </button>
          </div>
        </div>
      </div>

      {/* Modal de Confirmação Irreversível */}
      {isModalOpen && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Confirmar Exclusão</h3>
            </div>

            <div className="modal-body">
              <p>
                Você tem certeza que deseja prosseguir?
                Esta ação é <strong>definitiva e totalmente irreversível</strong>.
              </p>
              <p className="modal-warning-text">
                {modalType === 'company'
                  ? "Aviso: A empresa, os históricos de crédito e todos os dados associados serão apagados permanentemente."
                  : "Aviso: Sua conta será excluída e você perderá o acesso à plataforma CREDIFAB imediatamente."}
              </p>
            </div>

            <div className="modal-footer">
              <button className="btn-modal-cancel" onClick={handleCloseModal}>
                Cancelar
              </button>
              <button className="btn-modal-confirm" onClick={handleConfirmAction}>
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