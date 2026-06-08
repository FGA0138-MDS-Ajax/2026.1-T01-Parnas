import React from 'react';

const formatarMoeda = (valor) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

const ConfirmacaoExclusaoConta = ({ conta, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--sm">
        <div className="modal-cabecalho">
          <h3 className="modal-titulo">Excluir conta?</h3>
          <button className="modal-fechar" onClick={onCancelar} aria-label="Fechar modal">
            ✕
          </button>
        </div>

        <div className="modal-corpo">
          <div className="confirmacao-icone confirmacao-icone--excluir">!</div>
          <p className="confirmacao-texto">
            Você está prestes a excluir <strong>{conta?.descricao}</strong>.
          </p>
          <p className="confirmacao-texto">
            {formatarMoeda(conta?.valor || 0)}
          </p>
          <p className="confirmacao-aviso confirmacao-aviso--erro">
            Esta ação não poderá ser desfeita.
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

export default ConfirmacaoExclusaoConta;
