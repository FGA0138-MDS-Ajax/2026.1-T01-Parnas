import React from 'react';

const ConfirmacaoExclusaoCategoria = ({ categoria, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--confirmacao">
        <div className="confirmacao-icone">⚠</div>

        <h3 className="confirmacao-titulo">Excluir categoria?</h3>
        <p className="confirmacao-descricao">Você está prestes a excluir permanentemente:</p>

        <div className="confirmacao-detalhe">
          <strong>{categoria?.nome || 'Categoria'}</strong>
          <span className="confirmacao-valor-sim">
            Tipo: {categoria?.tipoExibicao || categoria?.tipo || '—'}
          </span>
        </div>

        <p className="confirmacao-aviso">Esta ação não pode ser desfeita.</p>

        <div className="confirmacao-acoes">
          <button className="btn-cancelar" onClick={onCancelar}>
            Cancelar
          </button>
          <button className="btn-excluir-confirmar" onClick={onConfirmar}>
            Sim, excluir
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmacaoExclusaoCategoria;