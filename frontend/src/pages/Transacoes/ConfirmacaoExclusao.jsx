import React from 'react';
import formatCurrency from '../../utils/formatCurrency';
import './Transacoes.css';

const ConfirmacaoExclusao = ({ transacao, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--confirmacao">
        <div className="modal-cabecalho">
          <h3 className="modal-titulo">Excluir transação?</h3>
          <button className="modal-fechar" onClick={onCancelar} aria-label="Fechar modal">
            ✕
          </button>
        </div>

        <div className="modal-corpo">
          <div className="confirmacao-icone confirmacao-icone--excluir">!</div>
          <p className="confirmacao-texto">
            Você está prestes a excluir permanentemente <strong>{transacao?.descricao}</strong>.
          </p>

          <span className={`confirmacao-valor valor--${transacao?.tipo}`}>
            {transacao?.tipo === 'despesa' ? '- ' : '+ '}
            {formatCurrency(transacao?.valor)}
          </span>

          <p className="confirmacao-aviso confirmacao-aviso--erro">
            Esta ação não pode ser desfeita.
          </p>
        </div>

        <div className="modal-rodape">
          <button type="button" className="btn-cancelar" onClick={onCancelar}>
            Cancelar
          </button>
          <button type="button" className="btn-submit btn-submit--excluir" onClick={onConfirmar}>
            Sim, excluir
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmacaoExclusao;
