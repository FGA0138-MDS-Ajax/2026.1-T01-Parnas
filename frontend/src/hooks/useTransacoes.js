import { useState } from 'react';

const TRANSACOES_MOCK = [
  { id: 1, descricao: 'Venda de produtos', valor: 3500.00, tipo: 'receita', categoria: 'Vendas', data: '2025-05-10' },
  { id: 2, descricao: 'Aluguel do escritório', valor: 1200.00, tipo: 'despesa', categoria: 'Infraestrutura', data: '2025-05-05' },
  { id: 3, descricao: 'Consultoria prestada', valor: 2000.00, tipo: 'receita', categoria: 'Serviços', data: '2025-05-15' },
  { id: 4, descricao: 'Conta de energia', valor: 350.00, tipo: 'despesa', categoria: 'Infraestrutura', data: '2025-05-08' },
  { id: 5, descricao: 'Venda online', valor: 800.00, tipo: 'receita', categoria: 'Vendas', data: '2025-05-20' },
  { id: 6, descricao: 'Folha de pagamento', valor: 5000.00, tipo: 'despesa', categoria: 'Pessoal', data: '2025-05-30' },
  { id: 7, descricao: 'Serviço de manutenção', valor: 400.00, tipo: 'despesa', categoria: 'Manutenção', data: '2025-04-18' },
  { id: 8, descricao: 'Recebimento de cliente', valor: 1500.00, tipo: 'receita', categoria: 'Serviços', data: '2025-04-22' },
  { id: 9, descricao: 'Compra de equipamentos', valor: 2300.00, tipo: 'despesa', categoria: 'Equipamentos', data: '2025-04-10' },
  { id: 10, descricao: 'Treinamento de equipe', valor: 600.00, tipo: 'despesa', categoria: 'Pessoal', data: '2025-04-05' },
  { id: 11, descricao: 'Contrato anual renovado', valor: 8000.00, tipo: 'receita', categoria: 'Serviços', data: '2025-03-01' },
  { id: 12, descricao: 'Material de escritório', valor: 250.00, tipo: 'despesa', categoria: 'Infraestrutura', data: '2025-03-15' },
];

const CATEGORIAS_MOCK = ['Vendas', 'Serviços', 'Infraestrutura', 'Pessoal', 'Manutenção', 'Equipamentos'];

const POR_PAGINA = 5;

const FILTROS_INICIAIS = {
  dataInicio: '',
  dataFim: '',
  tipo: '',
  categoria: '',
  valorMin: '',
  valorMax: '',
};

const useTransacoes = () => {
  const [filtros, setFiltros] = useState(FILTROS_INICIAIS);
  const [filtrosAtivos, setFiltrosAtivos] = useState(FILTROS_INICIAIS);
  const [paginaAtual, setPaginaAtual] = useState(1);

  const transacoesFiltradas = TRANSACOES_MOCK.filter((t) => {
    if (filtrosAtivos.tipo && t.tipo !== filtrosAtivos.tipo) return false;
    if (filtrosAtivos.categoria && t.categoria !== filtrosAtivos.categoria) return false;
    if (filtrosAtivos.dataInicio && t.data < filtrosAtivos.dataInicio) return false;
    if (filtrosAtivos.dataFim && t.data > filtrosAtivos.dataFim) return false;
    if (filtrosAtivos.valorMin && t.valor < parseFloat(filtrosAtivos.valorMin)) return false;
    if (filtrosAtivos.valorMax && t.valor > parseFloat(filtrosAtivos.valorMax)) return false;
    return true;
  });

  const totalReceitas = transacoesFiltradas
    .filter((t) => t.tipo === 'receita')
    .reduce((acc, t) => acc + t.valor, 0);

  const totalDespesas = transacoesFiltradas
    .filter((t) => t.tipo === 'despesa')
    .reduce((acc, t) => acc + t.valor, 0);

  const saldo = totalReceitas - totalDespesas;

  const totalPaginas = Math.ceil(transacoesFiltradas.length / POR_PAGINA);

  const transacoesPaginadas = transacoesFiltradas.slice(
    (paginaAtual - 1) * POR_PAGINA,
    paginaAtual * POR_PAGINA
  );

  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltros((prev) => ({ ...prev, [name]: value }));
  };

  const aplicarFiltros = () => {
    setFiltrosAtivos(filtros);
    setPaginaAtual(1);
  };

  const limparFiltros = () => {
    setFiltros(FILTROS_INICIAIS);
    setFiltrosAtivos(FILTROS_INICIAIS);
    setPaginaAtual(1);
  };

  const mudarPagina = (pagina) => {
    if (pagina >= 1 && pagina <= totalPaginas) {
      setPaginaAtual(pagina);
    }
  };

  return {
    filtros,
    transacoes: transacoesPaginadas,
    totais: { totalReceitas, totalDespesas, saldo },
    paginaAtual,
    totalPaginas,
    totalTransacoes: transacoesFiltradas.length,
    categorias: CATEGORIAS_MOCK,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
    mudarPagina,
  };
};

export default useTransacoes;
