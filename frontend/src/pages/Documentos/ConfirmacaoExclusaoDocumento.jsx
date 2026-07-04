import React from 'react';

const ConfirmacaoExclusaoDocumento = ({ documento, onConfirmar, onCancelar }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onCancelar();
  };

  const formatarTamanho = (bytes) => {
    if (!bytes) return '—';
    return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
  };

  const formatarData = (dataStr) => {
    if (!dataStr) return '—';
    const [ano, mes, dia] = dataStr.split('-');
    return `${dia}/${mes}/${ano}`;
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container modal-container--confirmacao">
        <div className="confirmacao-icone">⚠</div>

        <h3 className="confirmacao-titulo">Excluir documento?</h3>
        <p className="confirmacao-descricao">Você está prestes a excluir permanentemente:</p>

        <div className="confirmacao-detalhe">
          <strong>{documento?.name || 'Documento'}</strong>
          <span className="confirmacao-valor-sim">
            {documento?.type || '—'} • {formatarData(documento?.created_at)} • {formatarTamanho(documento?.size)}
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

export default ConfirmacaoExclusaoDocumento;