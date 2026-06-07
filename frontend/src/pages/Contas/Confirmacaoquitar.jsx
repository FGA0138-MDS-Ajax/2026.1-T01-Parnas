import React from 'react';

const formatarMoeda = (valor) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

const formatarData = (dataStr) => {
  if (!dataStr) return '';
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
};

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
            {formatarMoeda(conta?.valor || 0)} com vencimento em {formatarData(conta?.dataVencimento)}.
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
