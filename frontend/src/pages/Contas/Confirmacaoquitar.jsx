import React from 'react';
import formatCurrency from '../../utils/formatCurrency';
import formatDate from '../../utils/formatDate';

const ConfirmacaoQuitar = ({ conta, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--sm">
        <div className="modal-cabecalho">
          <h3 className="modal-titulo">Quitar conta?</h3>
          <button className="modal-fechar" onClick={onCancelar} aria-label="Fechar modal">
            ✕
          </button>
        </div>

        <div className="modal-corpo">
          <div className="confirmacao-icone confirmacao-icone--quitar">✓</div>
          <p className="confirmacao-texto">
            Confirme a quitação de <strong>{conta?.descricao}</strong>.
          </p>
          <p className="confirmacao-texto">
            {formatCurrency(conta?.valor)} com vencimento em {formatDate(conta?.dataVencimento)}.
          </p>
          <p className="confirmacao-aviso">
            Uma transação será gerada automaticamente quando o backend estiver integrado.
          </p>
        </div>

        <div className="modal-rodape">
          <button type="button" className="btn-cancelar" onClick={onCancelar}>
            Cancelar
          </button>
          <button type="button" className="btn-submit btn-submit--quitar" onClick={onConfirmar}>
            Confirmar quitação
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmacaoQuitar;
