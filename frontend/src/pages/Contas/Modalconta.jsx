import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ModalConta = ({ contaParaEditar, categorias, contasCaixa = [], onSalvar, onFechar }) => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    descricao: '',
    valor: '',
    tipo: 'despesa',
    dataVencimento: '',
    categoria: '',
    contaCaixaId: '',
  });
  const [erros, setErros] = useState({});
  const [salvando, setSalvando] = useState(false);

  useEffect(() => {
    if (contaParaEditar) {
      setForm({
        descricao: contaParaEditar.descricao || '',
        valor: contaParaEditar.valor?.toString() || '',
        tipo: contaParaEditar.tipo || 'despesa',
        dataVencimento: contaParaEditar.dataVencimento || '',
        categoria: contaParaEditar.categoria ? String(contaParaEditar.categoria) : '',
        contaCaixaId: contaParaEditar.contaCaixaId ? String(contaParaEditar.contaCaixaId) : '',
      });
    } else {
      setForm({
        descricao: '',
        valor: '',
        tipo: 'despesa',
        dataVencimento: '',
        categoria: '',
        contaCaixaId: '',
      });
    }
    setErros({});
  }, [contaParaEditar]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (erros[name]) setErros((prev) => ({ ...prev, [name]: '' }));
  };

  const setTipo = (tipo) => {
    setForm((prev) => ({ ...prev, tipo, categoria: '' }));
  };

  const validar = () => {
    const novosErros = {};
    if (!form.descricao.trim()) novosErros.descricao = 'Descrição é obrigatória.';
    if (!form.valor || isNaN(form.valor) || parseFloat(form.valor) <= 0)
      novosErros.valor = 'Informe um valor válido maior que zero.';
    if (!form.dataVencimento) novosErros.dataVencimento = 'Data de vencimento é obrigatória.';
    if (!form.contaCaixaId) novosErros.contaCaixaId = 'Selecione uma Conta/Caixa.';
    setErros(novosErros);
    return Object.keys(novosErros).length === 0;
  };

  const handleSubmit = async (e) => {
    e?.preventDefault();
    if (!validar()) return;
    setSalvando(true);
    try {
      await onSalvar(form);
    } finally {
      setSalvando(false);
    }
  };

  const isEdicao = !!contaParaEditar;
  const categoriasFiltradas = categorias.filter(
    (cat) => cat.tipo === form.tipo || !cat.tipo
  );

  return (
    <div className="modal-overlay" onClick={onFechar} role="dialog" aria-modal="true">
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-cabecalho">
          <h3 className="modal-titulo">
            {isEdicao ? 'Editar Conta' : 'Nova Conta'}
          </h3>
          <button className="modal-fechar" onClick={onFechar} aria-label="Fechar modal">✕</button>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <div className="modal-corpo">
            {/* Tipo toggle */}
            <div className="tipo-toggle">
              <button
                type="button"
                className={`tipo-btn tipo-btn--receita ${form.tipo === 'receita' ? 'ativo' : ''}`}
                onClick={() => setTipo('receita')}
              >
                ↑ Conta a Receber
              </button>
              <button
                type="button"
                className={`tipo-btn tipo-btn--despesa ${form.tipo === 'despesa' ? 'ativo' : ''}`}
                onClick={() => setTipo('despesa')}
              >
                ↓ Conta a Pagar
              </button>
            </div>

            {/* Descrição */}
            <div className="input-group">
              <label htmlFor="descricao">Descrição</label>
              <input
                id="descricao"
                name="descricao"
                type="text"
                placeholder="Ex: Aluguel do escritório, Nota fiscal cliente..."
                value={form.descricao}
                onChange={handleChange}
                className={erros.descricao ? 'input-erro' : ''}
              />
              {erros.descricao && <span className="msg-campo-erro">{erros.descricao}</span>}
            </div>

            {/* Valor + Vencimento */}
            <div className="form-row">
              <div className="input-group">
                <label htmlFor="valor">Valor (R$)</label>
                <input
                  id="valor"
                  name="valor"
                  type="number"
                  placeholder="0,00"
                  min="0"
                  step="0.01"
                  value={form.valor}
                  onChange={handleChange}
                  className={erros.valor ? 'input-erro' : ''}
                />
                {erros.valor && <span className="msg-campo-erro">{erros.valor}</span>}
              </div>
              <div className="input-group">
                <label htmlFor="dataVencimento">Data de Vencimento</label>
                <input
                  id="dataVencimento"
                  name="dataVencimento"
                  type="date"
                  value={form.dataVencimento}
                  onChange={handleChange}
                  className={erros.dataVencimento ? 'input-erro' : ''}
                />
                {erros.dataVencimento && <span className="msg-campo-erro">{erros.dataVencimento}</span>}
              </div>
            </div>

            {/* Conta/Caixa */}
            <div className="input-group">
              <div className="campo-label-acoes">
                <label htmlFor="contaCaixaId">Conta/Caixa</label>
                <button
                  type="button"
                  className="btn-link-categoria"
                  onClick={() => navigate('/contas-caixa')}
                >
                  Cadastrar
                </button>
              </div>
              <select
                id="contaCaixaId"
                name="contaCaixaId"
                value={form.contaCaixaId}
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

            {/* Categoria */}
            <div className="input-group">
              <div className="campo-label-acoes">
                <label htmlFor="categoria">
                  Categoria
                  {categoriasFiltradas.length === 0 && (
                    <span className="msg-campo-aviso" style={{ marginLeft: '8px', textTransform: 'none', fontWeight: 400 }}>
                      (Nenhuma categoria disponível para este tipo)
                    </span>
                  )}
                </label>
                <button
                  type="button"
                  className="btn-link-categoria"
                  onClick={() => navigate('/categorias')}
                >
                  Cadastrar
                </button>
              </div>
              <select
                id="categoria"
                name="categoria"
                value={form.categoria}
                onChange={handleChange}
                disabled={categoriasFiltradas.length === 0}
              >
                <option value="">Sem categoria</option>
                {categoriasFiltradas.map((cat) => (
                  <option key={cat.id} value={cat.id}>{cat.nome}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="modal-rodape">
            <button type="button" className="btn-cancelar" onClick={onFechar} disabled={salvando}>
              Cancelar
            </button>
            <button type="submit" className="btn-submit" disabled={salvando}>
              {salvando ? 'Salvando...' : isEdicao ? 'Salvar alterações' : 'Cadastrar conta'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ModalConta;
