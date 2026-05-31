import React, { useState, useEffect, useCallback } from 'react';
import { useEmpresa } from '../../context/EmpresaContext';
import ModalTransacao from './ModalTransacao';
import ConfirmacaoExclusao from './ConfirmacaoExclusao';
import './Transacoes.css';

const CATEGORIAS_MOCK = [
  { id: 1, nome: 'Vendas', tipo: 'receita' },
  { id: 2, nome: 'Serviços Prestados', tipo: 'receita' },
  { id: 3, nome: 'Investimentos', tipo: 'receita' },
  { id: 4, nome: 'Aluguel', tipo: 'despesa' },
  { id: 5, nome: 'Folha de Pagamento', tipo: 'despesa' },
  { id: 6, nome: 'Fornecedores', tipo: 'despesa' },
  { id: 7, nome: 'Marketing', tipo: 'despesa' },
  { id: 8, nome: 'Utilidades', tipo: 'despesa' },
];

const TRANSACOES_MOCK = [
  {
    id: 1,
    descricao: 'Venda de produtos - Lote #001',
    valor: 4500.0,
    tipo: 'receita',
    data: '2025-05-10',
    categoriaId: 1,
    categoriaNome: 'Vendas',
  },
  {
    id: 2,
    descricao: 'Pagamento de aluguel escritório',
    valor: 2200.0,
    tipo: 'despesa',
    data: '2025-05-05',
    categoriaId: 4,
    categoriaNome: 'Aluguel',
  },
  {
    id: 3,
    descricao: 'Consultoria técnica - Cliente B',
    valor: 1800.0,
    tipo: 'receita',
    data: '2025-05-12',
    categoriaId: 2,
    categoriaNome: 'Serviços Prestados',
  },
];

const formatarMoeda = (valor) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

const formatarData = (dataISO) => {
  if (!dataISO) return '';
  const [ano, mes, dia] = dataISO.split('-');
  return `${dia}/${mes}/${ano}`;
};

const Transacoes = () => {
  const { idEmpresaLogada } = useEmpresa();

  const [transacoes, setTransacoes] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  const [modalAberto, setModalAberto] = useState(false);
  const [transacaoParaEditar, setTransacaoParaEditar] = useState(null);
  const [confirmacaoAberta, setConfirmacaoAberta] = useState(false);
  const [transacaoParaExcluir, setTransacaoParaExcluir] = useState(null);

  const [filtroTipo, setFiltroTipo] = useState('todos');
  const [filtroCategoria, setFiltroCategoria] = useState('');

  const carregarDados = useCallback(async () => {
    setCarregando(true);
    setErro('');
    try {
      // Simulação de chamada à API:
      // const [resTransacoes, resCategorias] = await Promise.all([
      //   fetch(`/api/transacoes?empresaId=${idEmpresaLogada}`),
      //   fetch(`/api/categorias?empresaId=${idEmpresaLogada}`)
      // ]);
      await new Promise((resolve) => setTimeout(resolve, 600));
      setTransacoes(TRANSACOES_MOCK);
      setCategorias(CATEGORIAS_MOCK);
    } catch {
      setErro('Não foi possível carregar as transações. Tente novamente.');
    } finally {
      setCarregando(false);
    }
  }, [idEmpresaLogada]);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const abrirModalNova = () => {
    setTransacaoParaEditar(null);
    setModalAberto(true);
  };

  const abrirModalEditar = (transacao) => {
    setTransacaoParaEditar(transacao);
    setModalAberto(true);
  };

  const fecharModal = () => {
    setModalAberto(false);
    setTransacaoParaEditar(null);
  };

  const salvarTransacao = async (dadosFormulario) => {
    // POST /transacoes ou PUT /transacoes/:id
    if (transacaoParaEditar) {
      const atualizada = {
        ...transacaoParaEditar,
        ...dadosFormulario,
        categoriaNome: categorias.find((c) => c.id === Number(dadosFormulario.categoriaId))?.nome || '',
      };
      setTransacoes((prev) => prev.map((t) => (t.id === atualizada.id ? atualizada : t)));
    } else {
      const nova = {
        id: Date.now(),
        ...dadosFormulario,
        categoriaNome: categorias.find((c) => c.id === Number(dadosFormulario.categoriaId))?.nome || '',
      };
      setTransacoes((prev) => [nova, ...prev]);
    }
    fecharModal();
  };

  const abrirConfirmacaoExclusao = (transacao) => {
    setTransacaoParaExcluir(transacao);
    setConfirmacaoAberta(true);
  };

  const confirmarExclusao = async () => {
    // DELETE /transacoes/:id
    setTransacoes((prev) => prev.filter((t) => t.id !== transacaoParaExcluir.id));
    setConfirmacaoAberta(false);
    setTransacaoParaExcluir(null);
  };

  const cancelarExclusao = () => {
    setConfirmacaoAberta(false);
    setTransacaoParaExcluir(null);
  };

  const transacoesFiltradas = transacoes.filter((t) => {
    const passaTipo = filtroTipo === 'todos' || t.tipo === filtroTipo;
    const passaCategoria = !filtroCategoria || t.categoriaId === Number(filtroCategoria);
    return passaTipo && passaCategoria;
  });

  const totalReceitas = transacoesFiltradas
    .filter((t) => t.tipo === 'receita')
    .reduce((acc, t) => acc + t.valor, 0);

  const totalDespesas = transacoesFiltradas
    .filter((t) => t.tipo === 'despesa')
    .reduce((acc, t) => acc + t.valor, 0);

  const saldo = totalReceitas - totalDespesas;

  return (
    <div className="transacoes-pagina">
      <div className="transacoes-cabecalho">
        <div>
          <h2 className="transacoes-titulo">Transações Financeiras</h2>
          <p className="transacoes-subtitulo">Gerencie entradas e saídas da sua empresa</p>
        </div>
        <button className="btn-nova-transacao" onClick={abrirModalNova}>
          <span className="btn-icon">+</span>
          Nova Transação
        </button>
      </div>

      <div className="resumo-cards">
        <div className="resumo-card resumo-card--receita">
          <span className="resumo-label">Total de Receitas</span>
          <span className="resumo-valor">{formatarMoeda(totalReceitas)}</span>
        </div>
        <div className="resumo-card resumo-card--despesa">
          <span className="resumo-label">Total de Despesas</span>
          <span className="resumo-valor">{formatarMoeda(totalDespesas)}</span>
        </div>
        <div className={`resumo-card resumo-card--saldo ${saldo >= 0 ? 'positivo' : 'negativo'}`}>
          <span className="resumo-label">Saldo do Período</span>
          <span className="resumo-valor">{formatarMoeda(saldo)}</span>
        </div>
      </div>

      <div className="filtros-barra">
        <div className="filtros-grupo">
          <label className="filtro-label">Tipo</label>
          <div className="filtro-tabs">
            {['todos', 'receita', 'despesa'].map((tipo) => (
              <button
                key={tipo}
                className={`filtro-tab ${filtroTipo === tipo ? 'ativo' : ''}`}
                onClick={() => setFiltroTipo(tipo)}
              >
                {tipo === 'todos' ? 'Todos' : tipo === 'receita' ? 'Receitas' : 'Despesas'}
              </button>
            ))}
          </div>
        </div>

        <div className="filtros-grupo">
          <label className="filtro-label" htmlFor="filtro-categoria">
            Categoria
          </label>
          <select
            id="filtro-categoria"
            className="filtro-select"
            value={filtroCategoria}
            onChange={(e) => setFiltroCategoria(e.target.value)}
          >
            <option value="">Todas as categorias</option>
            {categorias.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.nome}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="transacoes-lista-container">
        {carregando ? (
          <div className="estado-carregando">
            <div className="spinner" />
            <p>Carregando transações...</p>
          </div>
        ) : erro ? (
          <div className="estado-erro">
            <p>{erro}</p>
            <button className="btn-tentar-novamente" onClick={carregarDados}>
              Tentar novamente
            </button>
          </div>
        ) : transacoesFiltradas.length === 0 ? (
          <div className="estado-vazio">
            <div className="vazio-icone">💼</div>
            <p className="vazio-titulo">Nenhuma transação encontrada</p>
            <p className="vazio-descricao">
              {filtroTipo !== 'todos' || filtroCategoria
                ? 'Nenhuma transação corresponde aos filtros selecionados.'
                : 'Comece registrando sua primeira transação financeira.'}
            </p>
            {filtroTipo === 'todos' && !filtroCategoria && (
              <button className="btn-nova-transacao-vazio" onClick={abrirModalNova}>
                Registrar primeira transação
              </button>
            )}
          </div>
        ) : (
          <table className="transacoes-tabela">
            <thead>
              <tr>
                <th>Descrição</th>
                <th>Categoria</th>
                <th>Data</th>
                <th>Tipo</th>
                <th className="col-valor">Valor</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>
            <tbody>
              {transacoesFiltradas.map((transacao) => (
                <tr key={transacao.id} className="transacao-linha">
                  <td className="col-descricao">
                    <span className="descricao-texto">{transacao.descricao}</span>
                  </td>
                  <td>
                    <span className="badge-categoria">{transacao.categoriaNome}</span>
                  </td>
                  <td className="col-data">{formatarData(transacao.data)}</td>
                  <td>
                    <span className={`badge-tipo badge-tipo--${transacao.tipo}`}>
                      {transacao.tipo === 'receita' ? '↑ Receita' : '↓ Despesa'}
                    </span>
                  </td>
                  <td className={`col-valor valor--${transacao.tipo}`}>
                    {transacao.tipo === 'despesa' ? '- ' : '+ '}
                    {formatarMoeda(transacao.valor)}
                  </td>
                  <td className="col-acoes">
                    <button
                      className="btn-acao btn-editar"
                      onClick={() => abrirModalEditar(transacao)}
                      title="Editar transação"
                    >
                      ✎
                    </button>
                    <button
                      className="btn-acao btn-excluir"
                      onClick={() => abrirConfirmacaoExclusao(transacao)}
                      title="Excluir transação"
                    >
                      ✕
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modalAberto && (
        <ModalTransacao
          transacaoParaEditar={transacaoParaEditar}
          categorias={categorias}
          onSalvar={salvarTransacao}
          onFechar={fecharModal}
        />
      )}

      {confirmacaoAberta && (
        <ConfirmacaoExclusao
          transacao={transacaoParaExcluir}
          onConfirmar={confirmarExclusao}
          onCancelar={cancelarExclusao}
        />
      )}
    </div>
  );
};

export default Transacoes;