import React from 'react';

const ConfirmacaoExclusaoSimulacao = ({ simulacao, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  const formatarMoeda = (valor) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0);

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--confirmacao">
        <div className="confirmacao-icone">⚠</div>

        <h3 className="confirmacao-titulo">Excluir simulação?</h3>
        <p className="confirmacao-descricao">Você está prestes a excluir permanentemente:</p>

        <div className="confirmacao-detalhe">
          <strong>{simulacao?.modalidade} — {simulacao?.prazo_meses} meses</strong>
          <span className="confirmacao-valor-sim">
            {formatarMoeda(simulacao?.valor_solicitado)} a {simulacao?.taxa_juros}% a.m.
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

export default ConfirmacaoExclusaoSimulacao;
