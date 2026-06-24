import { useState } from 'react';
import useAppliedFilters from './useAppliedFilters';
import { CONTAS_CAIXA_MOCK } from '../services/contaCaixa.service';

const TRANSACOES_MOCK = [
  { id: 1, descricao: 'Venda de produtos', valor: 3500.00, tipo: 'receita', categoria: 'Vendas', categoriaId: 1, data: '2025-05-10', contaCaixaId: 2, contaCaixaNome: 'Caixa Vendas' },
  { id: 2, descricao: 'Aluguel do escritório', valor: 1200.00, tipo: 'despesa', categoria: 'Infraestrutura', categoriaId: 3, data: '2025-05-05', contaCaixaId: 3, contaCaixaNome: 'Banco do Brasil' },
  { id: 3, descricao: 'Consultoria prestada', valor: 2000.00, tipo: 'receita', categoria: 'Serviços', categoriaId: 2, data: '2025-05-15', contaCaixaId: 1, contaCaixaNome: 'Inter' },
  { id: 4, descricao: 'Conta de energia', valor: 350.00, tipo: 'despesa', categoria: 'Infraestrutura', categoriaId: 3, data: '2025-05-08', contaCaixaId: 4, contaCaixaNome: 'Dinheiro em Especie' },
  { id: 5, descricao: 'Venda online', valor: 800.00, tipo: 'receita', categoria: 'Vendas', categoriaId: 1, data: '2025-05-20', contaCaixaId: 2, contaCaixaNome: 'Caixa Vendas' },
  { id: 6, descricao: 'Folha de pagamento', valor: 5000.00, tipo: 'despesa', categoria: 'Pessoal', categoriaId: 4, data: '2025-05-30', contaCaixaId: 3, contaCaixaNome: 'Banco do Brasil' },
  { id: 7, descricao: 'Serviço de manutenção', valor: 400.00, tipo: 'despesa', categoria: 'Manutenção', categoriaId: 5, data: '2025-04-18', contaCaixaId: 1, contaCaixaNome: 'Inter' },
  { id: 8, descricao: 'Recebimento de cliente', valor: 1500.00, tipo: 'receita', categoria: 'Serviços', categoriaId: 2, data: '2025-04-22', contaCaixaId: 1, contaCaixaNome: 'Inter' },
  { id: 9, descricao: 'Compra de equipamentos', valor: 2300.00, tipo: 'despesa', categoria: 'Equipamentos', categoriaId: 6, data: '2025-04-10', contaCaixaId: 3, contaCaixaNome: 'Banco do Brasil' },
  { id: 10, descricao: 'Treinamento de equipe', valor: 600.00, tipo: 'despesa', categoria: 'Pessoal', categoriaId: 4, data: '2025-04-05', contaCaixaId: 3, contaCaixaNome: 'Banco do Brasil' },
  { id: 11, descricao: 'Contrato anual renovado', valor: 8000.00, tipo: 'receita', categoria: 'Serviços', categoriaId: 2, data: '2025-03-01', contaCaixaId: 1, contaCaixaNome: 'Inter' },
  { id: 12, descricao: 'Material de escritório', valor: 250.00, tipo: 'despesa', categoria: 'Infraestrutura', categoriaId: 3, data: '2025-03-15', contaCaixaId: 4, contaCaixaNome: 'Dinheiro em Especie' },
];

const CATEGORIAS_MOCK = ['Vendas', 'Serviços', 'Infraestrutura', 'Pessoal', 'Manutenção', 'Equipamentos'];

const POR_PAGINA = 5;

const FILTROS_INICIAIS = {
  dataInicio: '',
  dataFim: '',
  tipo: '',
  categoria: '',
  contaCaixaId: '',
  valorMin: '',
  valorMax: '',
};

const buscarContaCaixa = (id) =>
  CONTAS_CAIXA_MOCK.find((contaCaixa) => String(contaCaixa.id) === String(id));

const buscarCategoria = (id) =>
  CATEGORIAS_MOCK.find((categoria, index) => String(index + 1) === String(id));

const calcularSaldoConta = (transacoes, contaCaixaId) =>
  transacoes
    .filter((transacao) => String(transacao.contaCaixaId) === String(contaCaixaId))
    .reduce((saldo, transacao) => {
      if (transacao.tipo === 'receita') return saldo + transacao.valor;
      if (transacao.tipo === 'despesa') return saldo - transacao.valor;
      return saldo;
    }, 0);

const useTransacoes = () => {
  const [todasTransacoes, setTodasTransacoes] = useState(TRANSACOES_MOCK);
  const {
    filtros,
    filtrosAplicados,
    handleFiltroChange,
    aplicarFiltros: aplicarFiltrosBase,
    limparFiltros: limparFiltrosBase,
  } = useAppliedFilters(FILTROS_INICIAIS);
  const [paginaAtual, setPaginaAtual] = useState(1);

  const transacoesFiltradas = todasTransacoes.filter((t) => {
    if (filtrosAplicados.tipo && t.tipo !== filtrosAplicados.tipo) return false;
    if (filtrosAplicados.categoria && t.categoria !== filtrosAplicados.categoria) return false;
    if (filtrosAplicados.contaCaixaId && String(t.contaCaixaId) !== String(filtrosAplicados.contaCaixaId)) return false;
    if (filtrosAplicados.dataInicio && t.data < filtrosAplicados.dataInicio) return false;
    if (filtrosAplicados.dataFim && t.data > filtrosAplicados.dataFim) return false;
    if (filtrosAplicados.valorMin && t.valor < parseFloat(filtrosAplicados.valorMin)) return false;
    if (filtrosAplicados.valorMax && t.valor > parseFloat(filtrosAplicados.valorMax)) return false;
    return true;
  });

  const totalReceitas = transacoesFiltradas
    .filter((t) => t.tipo === 'receita')
    .reduce((acc, t) => acc + t.valor, 0);

  const totalDespesas = transacoesFiltradas
    .filter((t) => t.tipo === 'despesa')
    .reduce((acc, t) => acc + t.valor, 0);

  const saldo = totalReceitas - totalDespesas;
  const apenasContaCaixaFiltrada = Boolean(filtrosAplicados.contaCaixaId)
    && !filtrosAplicados.tipo
    && !filtrosAplicados.categoria
    && !filtrosAplicados.dataInicio
    && !filtrosAplicados.dataFim
    && !filtrosAplicados.valorMin
    && !filtrosAplicados.valorMax;

  const contaCaixaSelecionada = filtrosAplicados.contaCaixaId
    ? buscarContaCaixa(filtrosAplicados.contaCaixaId)
    : null;

  const saldoContaSelecionada = apenasContaCaixaFiltrada
    ? calcularSaldoConta(todasTransacoes, filtrosAplicados.contaCaixaId)
    : null;

  const totalPaginas = Math.ceil(transacoesFiltradas.length / POR_PAGINA);

  const transacoesPaginadas = transacoesFiltradas.slice(
    (paginaAtual - 1) * POR_PAGINA,
    paginaAtual * POR_PAGINA
  );

  const aplicarFiltros = () => {
    aplicarFiltrosBase();
    setPaginaAtual(1);
  };

  const limparFiltros = () => {
    limparFiltrosBase();
    setPaginaAtual(1);
  };

  const mudarPagina = (pagina) => {
    if (pagina >= 1 && pagina <= totalPaginas) {
      setPaginaAtual(pagina);
    }
  };

  const salvarTransacao = async (dados, id = null) => {
    if (dados.modo === 'transferencia') {
      const origem = buscarContaCaixa(dados.contaOrigemId);
      const destino = buscarContaCaixa(dados.contaDestinoId);
      if (!origem || !destino || origem.id === destino.id) return;
      const valor = parseFloat(dados.valor);
      const transferenciaId = `transferencia_${Date.now()}`;
      const descricao = dados.descricao?.trim() || `Transferencia de ${origem.nome} para ${destino.nome}`;

      setTodasTransacoes((prev) => [
        {
          id: Date.now(),
          transferenciaId,
          descricao,
          valor,
          tipo: 'despesa',
          categoria: 'Transferencia',
          categoriaId: null,
          data: dados.data,
          contaCaixaId: origem.id,
          contaCaixaNome: origem.nome,
        },
        {
          id: Date.now() + 1,
          transferenciaId,
          descricao,
          valor,
          tipo: 'receita',
          categoria: 'Transferencia',
          categoriaId: null,
          data: dados.data,
          contaCaixaId: destino.id,
          contaCaixaNome: destino.nome,
        },
        ...prev,
      ]);
      return;
    }

    const categoria = buscarCategoria(dados.categoriaId);
    const contaCaixa = buscarContaCaixa(dados.contaCaixaId);
    const transacaoNormalizada = {
      descricao: dados.descricao.trim(),
      valor: parseFloat(dados.valor),
      tipo: dados.tipo,
      categoria: categoria || '',
      categoriaId: dados.categoriaId ? Number(dados.categoriaId) : null,
      data: dados.data,
      contaCaixaId: contaCaixa?.id || null,
      contaCaixaNome: contaCaixa?.nome || '',
    };

    if (id) {
      setTodasTransacoes((prev) =>
        prev.map((transacao) =>
          transacao.id === id ? { ...transacao, ...transacaoNormalizada } : transacao
        )
      );
      return;
    }

    setTodasTransacoes((prev) => [
      { id: Date.now(), ...transacaoNormalizada },
      ...prev,
    ]);
  };

  const excluirTransacao = async (id) => {
    setTodasTransacoes((prev) => {
      const transacao = prev.find((item) => item.id === id);
      if (!transacao?.transferenciaId) {
        return prev.filter((item) => item.id !== id);
      }
      return prev.filter((item) => item.transferenciaId !== transacao.transferenciaId);
    });
  };

  return {
    filtros,
    transacoes: transacoesPaginadas,
    totais: { totalReceitas, totalDespesas, saldo },
    saldoContaSelecionada,
    contaCaixaSelecionada,
    paginaAtual,
    totalPaginas,
    totalTransacoes: transacoesFiltradas.length,
    categorias: CATEGORIAS_MOCK,
    contasCaixa: CONTAS_CAIXA_MOCK,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
    mudarPagina,
    salvarTransacao,
    excluirTransacao,
  };
};

export default useTransacoes;
