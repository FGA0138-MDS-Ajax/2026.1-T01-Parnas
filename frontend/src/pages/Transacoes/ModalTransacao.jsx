import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Transacoes.css';

const hoje = () => new Date().toISOString().split('T')[0];

const ESTADO_INICIAL = {
  modo: 'movimentacao',
  descricao: '',
  valor: '',
  tipo: 'receita',
  data: hoje(),
  categoriaId: '',
  contaCaixaId: '',
  contaOrigemId: '',
  contaDestinoId: '',
};

const ModalTransacao = ({ transacaoParaEditar, categorias, contasCaixa = [], onSalvar, onFechar }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState(ESTADO_INICIAL);
  const [erros, setErros] = useState({});
  const [salvando, setSalvando] = useState(false);

  const ehEdicao = Boolean(transacaoParaEditar);

  useEffect(() => {
    if (ehEdicao) {
      setFormData({
        modo: 'movimentacao',
        descricao: transacaoParaEditar.descricao,
        valor: String(transacaoParaEditar.valor),
        tipo: transacaoParaEditar.tipo,
        data: transacaoParaEditar.data,
        categoriaId: transacaoParaEditar.categoriaId ? String(transacaoParaEditar.categoriaId) : '',
        contaCaixaId: transacaoParaEditar.contaCaixaId ? String(transacaoParaEditar.contaCaixaId) : '',
        contaOrigemId: '',
        contaDestinoId: '',
      });
    } else {
      setFormData(ESTADO_INICIAL);
    }
    setErros({});
  }, [transacaoParaEditar, ehEdicao]);

  const categoriasFiltradas = categorias.filter(
    (cat) => cat.tipo === formData.tipo || !cat.tipo
  );
  const ehTransferencia = formData.modo === 'transferencia';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
      // Limpa categoria quando muda o tipo para evitar categoria inválida
      ...(name === 'tipo' ? { categoriaId: '' } : {}),
      ...(name === 'modo' ? { categoriaId: '', contaCaixaId: '', contaOrigemId: '', contaDestinoId: '' } : {}),
    }));
    if (erros[name]) {
      setErros((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validar = () => {
    const novosErros = {};

    if (!ehTransferencia && !formData.descricao.trim()) {
      novosErros.descricao = 'A descrição é obrigatória.';
    }

    const valorNum = parseFloat(formData.valor);
    if (!formData.valor || isNaN(valorNum)) {
      novosErros.valor = 'Informe um valor válido.';
    } else if (valorNum <= 0) {
      novosErros.valor = 'O valor deve ser positivo.';
    }

    if (!formData.data) {
      novosErros.data = 'A data é obrigatória.';
    } else if (formData.data > hoje()) {
      novosErros.data = 'A data não pode ser futura.';
    }

    if (ehTransferencia) {
      if (!formData.contaOrigemId) {
        novosErros.contaOrigemId = 'Selecione a Conta/Caixa de origem.';
      }
      if (!formData.contaDestinoId) {
        novosErros.contaDestinoId = 'Selecione a Conta/Caixa de destino.';
      }
      if (
        formData.contaOrigemId
        && formData.contaDestinoId
        && formData.contaOrigemId === formData.contaDestinoId
      ) {
        novosErros.contaDestinoId = 'Origem e destino devem ser diferentes.';
      }
    } else if (!formData.categoriaId) {
      novosErros.categoriaId = 'Selecione uma categoria.';
    }

    if (!ehTransferencia && !formData.contaCaixaId) {
      novosErros.contaCaixaId = 'Selecione uma Conta/Caixa.';
    }

    setErros(novosErros);
    return Object.keys(novosErros).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validar()) return;

    setSalvando(true);
    try {
      await onSalvar({
        ...formData,
        valor: parseFloat(formData.valor),
        categoriaId: formData.categoriaId ? Number(formData.categoriaId) : null,
      });
    } finally {
      setSalvando(false);
    }
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onFechar();
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} role="dialog" aria-modal="true">
      <div className="modal-container">
        <div className="modal-cabecalho">
          <h3 className="modal-titulo">
            {ehEdicao ? 'Editar Transação' : 'Nova Transação'}
          </h3>
          <button className="modal-fechar" onClick={onFechar} aria-label="Fechar modal">
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <div className="modal-corpo">
            {!ehEdicao && (
              <div className="input-group">
                <label>Modo</label>
                <div className="tipo-toggle">
                  <button
                    type="button"
                    className={`tipo-btn ${formData.modo === 'movimentacao' ? 'ativo' : ''}`}
                    onClick={() => handleChange({ target: { name: 'modo', value: 'movimentacao' } })}
                  >
                    Movimentação
                  </button>
                  <button
                    type="button"
                    className={`tipo-btn ${formData.modo === 'transferencia' ? 'ativo' : ''}`}
                    onClick={() => handleChange({ target: { name: 'modo', value: 'transferencia' } })}
                  >
                    Transferência
                  </button>
                </div>
              </div>
            )}

            {!ehTransferencia && (
              <div className="input-group">
                <label>Tipo de transação</label>
                <div className="tipo-toggle">
                  <button
                    type="button"
                    className={`tipo-btn tipo-btn--receita ${formData.tipo === 'receita' ? 'ativo' : ''}`}
                    onClick={() => handleChange({ target: { name: 'tipo', value: 'receita' } })}
                  >
                    ↑ Receita
                  </button>
                  <button
                    type="button"
                    className={`tipo-btn tipo-btn--despesa ${formData.tipo === 'despesa' ? 'ativo' : ''}`}
                    onClick={() => handleChange({ target: { name: 'tipo', value: 'despesa' } })}
                  >
                    ↓ Despesa
                  </button>
                </div>
              </div>
            )}

            {ehTransferencia && (
              <div className="form-row">
                <div className="input-group">
                  <label htmlFor="modal-conta-origem">Conta/Caixa de origem</label>
                  <select
                    id="modal-conta-origem"
                    name="contaOrigemId"
                    value={formData.contaOrigemId}
                    onChange={handleChange}
                    className={erros.contaOrigemId ? 'input-erro' : ''}
                  >
                    <option value="">Selecione...</option>
                    {contasCaixa.map((contaCaixa) => (
                      <option key={contaCaixa.id} value={contaCaixa.id}>
                        {contaCaixa.nome}
                      </option>
                    ))}
                  </select>
                  {erros.contaOrigemId && <span className="msg-campo-erro">{erros.contaOrigemId}</span>}
                </div>

                <div className="input-group">
                  <label htmlFor="modal-conta-destino">Conta/Caixa de destino</label>
                  <select
                    id="modal-conta-destino"
                    name="contaDestinoId"
                    value={formData.contaDestinoId}
                    onChange={handleChange}
                    className={erros.contaDestinoId ? 'input-erro' : ''}
                  >
                    <option value="">Selecione...</option>
                    {contasCaixa.map((contaCaixa) => (
                      <option key={contaCaixa.id} value={contaCaixa.id}>
                        {contaCaixa.nome}
                      </option>
                    ))}
                  </select>
                  {erros.contaDestinoId && <span className="msg-campo-erro">{erros.contaDestinoId}</span>}
                </div>
              </div>
            )}

            {!ehTransferencia && (
              <div className="input-group">
                <label htmlFor="modal-descricao">Descrição</label>
                <input
                  id="modal-descricao"
                  type="text"
                  name="descricao"
                  placeholder="Ex.: Venda de produtos - Lote #001"
                  value={formData.descricao}
                  onChange={handleChange}
                  className={erros.descricao ? 'input-erro' : ''}
                />
                {erros.descricao && <span className="msg-campo-erro">{erros.descricao}</span>}
              </div>
            )}

            {ehTransferencia && (
              <div className="input-group">
                <label htmlFor="modal-descricao-transferencia">Descrição da transferência</label>
                <input
                  id="modal-descricao-transferencia"
                  type="text"
                  name="descricao"
                  placeholder="Ex.: Transferência para reserva"
                  value={formData.descricao}
                  onChange={handleChange}
                />
              </div>
            )}

            <div className="form-row">
              <div className="input-group">
                <label htmlFor="modal-valor">Valor (R$)</label>
                <input
                  id="modal-valor"
                  type="number"
                  name="valor"
                  placeholder="0,00"
                  min="0.01"
                  step="0.01"
                  value={formData.valor}
                  onChange={handleChange}
                  className={erros.valor ? 'input-erro' : ''}
                />
                {erros.valor && <span className="msg-campo-erro">{erros.valor}</span>}
              </div>

              <div className="input-group">
                <label htmlFor="modal-data">Data</label>
                <input
                  id="modal-data"
                  type="date"
                  name="data"
                  max={hoje()}
                  value={formData.data}
                  onChange={handleChange}
                  className={erros.data ? 'input-erro' : ''}
                />
                {erros.data && <span className="msg-campo-erro">{erros.data}</span>}
              </div>
            </div>

            {/* Categoria */}
            {!ehTransferencia && (
              <div className="input-group">
                <div className="campo-label-acoes">
                  <label htmlFor="modal-conta-caixa">Conta/Caixa</label>
                  <button
                    type="button"
                    className="btn-link-categoria"
                    onClick={() => navigate('/contas-caixa')}
                  >
                    Cadastrar
                  </button>
                </div>
                <select
                  id="modal-conta-caixa"
                  name="contaCaixaId"
                  value={formData.contaCaixaId}
                  onChange={handleChange}
                  className={erros.contaCaixaId ? 'input-erro' : ''}
                >
                  <option value="">Selecione uma Conta/Caixa...</option>
                  {contasCaixa.map((contaCaixa) => (
                    <option key={contaCaixa.id} value={contaCaixa.id}>
                      {contaCaixa.nome}
                    </option>
                  ))}
                </select>
                {erros.contaCaixaId && <span className="msg-campo-erro">{erros.contaCaixaId}</span>}
              </div>
            )}

            {!ehTransferencia && (
              <div className="input-group">
              <div className="campo-label-acoes">
                <label htmlFor="modal-categoria">Categoria</label>
                <button
                  type="button"
                  className="btn-link-categoria"
                  onClick={() => navigate('/categorias')}
                >
                  Cadastrar
                </button>
              </div>
              <select
                id="modal-categoria"
                name="categoriaId"
                value={formData.categoriaId}
                onChange={handleChange}
                className={erros.categoriaId ? 'input-erro' : ''}
              >
                <option value="">Selecione uma categoria...</option>
                {categoriasFiltradas.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.nome}
                  </option>
                ))}
              </select>
              {erros.categoriaId && (
                <span className="msg-campo-erro">{erros.categoriaId}</span>
              )}
              {categoriasFiltradas.length === 0 && formData.tipo && (
                <span className="msg-campo-aviso">
                  Nenhuma categoria cadastrada para este tipo.
                </span>
              )}
              </div>
            )}
          </div>

          <div className="modal-rodape">
            <button type="button" className="btn-cancelar" onClick={onFechar} disabled={salvando}>
              Cancelar
            </button>
            <button type="submit" className="btn-submit" disabled={salvando}>
              {salvando ? 'Salvando...' : ehEdicao ? 'Salvar Alterações' : ehTransferencia ? 'Registrar Transferência' : 'Registrar Transação'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ModalTransacao;
