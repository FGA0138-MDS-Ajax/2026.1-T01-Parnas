import React from 'react';

const ConfirmacaoExclusaoComparacao = ({ comparacao, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  const formatarMoeda = (valor) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0);

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--confirmacao">
        <div className="confirmacao-icone">⚠</div>

        <h3 className="confirmacao-titulo">Excluir comparação?</h3>
        <p className="confirmacao-descricao">Você está prestes a excluir permanentemente esta comparação do histórico.</p>

        <div className="confirmacao-detalhe">
          <strong>{comparacao?.modalidade || 'Comparação salva'}</strong>
          <span className="confirmacao-valor-sim">
            {formatarMoeda(comparacao?.valor_solicitado || 0)}
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

export default ConfirmacaoExclusaoComparacao;