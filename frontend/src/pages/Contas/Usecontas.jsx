import { useState, useEffect } from 'react';
import useAppliedFilters from '../../hooks/useAppliedFilters';
import { CONTAS_CAIXA_MOCK } from '../../services/contaCaixa.service';

// ---------------------------------------------------------------------------
// MOCK — remover imports abaixo e descomentar os de produção quando o back
// estiver pronto:
//
// import {
//   listarContas,
//   criarConta,
//   atualizarConta,
//   excluirConta,
//   quitarConta,
// } from '../services/contasService';
// ---------------------------------------------------------------------------

let proximoId = 10;

const CATEGORIAS_MOCK = [
  { id: 1, nome: 'Vendas', tipo: 'receita' },
  { id: 2, nome: 'Servicos', tipo: 'receita' },
  { id: 3, nome: 'Infraestrutura', tipo: 'despesa' },
  { id: 4, nome: 'Pessoal', tipo: 'despesa' },
  { id: 5, nome: 'Impostos', tipo: 'despesa' },
  { id: 6, nome: 'Outros', tipo: '' },
];

const CONTAS_MOCK = [
  {
    id: 1,
    descricao: 'Aluguel do escritório',
    valor: 3200.00,
    tipo: 'despesa',
    dataVencimento: '2026-06-10',
    status: 'pendente',
    dataQuitacao: null,
    categoria: 3,
    categoriaNome: 'Infraestrutura',
    contaCaixaId: 1,
    contaCaixaNome: 'Inter',
  },
  {
    id: 2,
    descricao: 'Nota fiscal — Cliente Alfa',
    valor: 8500.00,
    tipo: 'receita',
    dataVencimento: '2026-06-15',
    status: 'pendente',
    dataQuitacao: null,
    categoria: 1,
    categoriaNome: 'Vendas',
    contaCaixaId: 2,
    contaCaixaNome: 'Caixa Vendas',
  },
  {
    id: 3,
    descricao: 'Assinatura de software',
    valor: 299.90,
    tipo: 'despesa',
    dataVencimento: '2026-05-30',  // vencida
    status: 'pendente',
    dataQuitacao: null,
    categoria: 3,
    categoriaNome: 'Infraestrutura',
    contaCaixaId: 3,
    contaCaixaNome: 'Banco do Brasil',
  },
  {
    id: 4,
    descricao: 'Serviço de consultoria — Cliente Beta',
    valor: 4750.00,
    tipo: 'receita',
    dataVencimento: '2026-06-20',
    status: 'pendente',
    dataQuitacao: null,
    categoria: 2,
    categoriaNome: 'Servicos',
    contaCaixaId: 1,
    contaCaixaNome: 'Inter',
  },
  {
    id: 5,
    descricao: 'Conta de energia',
    valor: 620.00,
    tipo: 'despesa',
    dataVencimento: '2026-05-01',  // vencida
    status: 'pendente',
    dataQuitacao: null,
    categoria: 3,
    categoriaNome: 'Infraestrutura',
    contaCaixaId: 4,
    contaCaixaNome: 'Dinheiro em Especie',
  },
  {
    id: 6,
    descricao: 'Mensalidade contabilidade',
    valor: 1100.00,
    tipo: 'despesa',
    dataVencimento: '2026-05-05',
    status: 'quitada',
    dataQuitacao: '2026-05-04',
    categoria: 4,
    categoriaNome: 'Pessoal',
    contaCaixaId: 3,
    contaCaixaNome: 'Banco do Brasil',
  },
  {
    id: 7,
    descricao: 'Pagamento projeto web — Cliente Gama',
    valor: 12000.00,
    tipo: 'receita',
    dataVencimento: '2026-05-20',
    status: 'quitada',
    dataQuitacao: '2026-05-19',
    categoria: 2,
    categoriaNome: 'Servicos',
    contaCaixaId: 2,
    contaCaixaNome: 'Caixa Vendas',
  },
];

// Simula delay de rede
const delay = (ms = 300) => new Promise((res) => setTimeout(res, ms));

// ---------------------------------------------------------------------------

const FILTROS_INICIAIS = {
  status: '',
  tipo: '',
  dataInicio: '',
  dataFim: '',
};

const aplicarFiltrosMock = (lista, filtros) => {
  return lista.filter((c) => {
    if (filtros.status && c.status !== filtros.status) return false;
    if (filtros.tipo && c.tipo !== filtros.tipo) return false;
    if (filtros.dataInicio && c.dataVencimento < filtros.dataInicio) return false;
    if (filtros.dataFim && c.dataVencimento > filtros.dataFim) return false;
    return true;
  });
};

const buscarCategoria = (id) =>
  CATEGORIAS_MOCK.find((categoria) => String(categoria.id) === String(id));

const buscarContaCaixa = (id) =>
  CONTAS_CAIXA_MOCK.find((contaCaixa) => String(contaCaixa.id) === String(id));

const normalizarConta = (dados) => {
  const categoria = dados.categoria ? buscarCategoria(dados.categoria) : null;
  const contaCaixa = buscarContaCaixa(dados.contaCaixaId);

  return {
    descricao: dados.descricao.trim(),
    valor: parseFloat(String(dados.valor).replace(',', '.')),
    tipo: dados.tipo,
    dataVencimento: dados.dataVencimento,
    categoria: categoria?.id || null,
    categoriaNome: categoria?.nome || '',
    contaCaixaId: contaCaixa?.id || null,
    contaCaixaNome: contaCaixa?.nome || '',
  };
};

const useContas = () => {
  const [todasContas, setTodasContas] = useState(CONTAS_MOCK);
  const {
    filtros,
    filtrosAplicados,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
  } = useAppliedFilters(FILTROS_INICIAIS);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const exibirFeedback = (tipo, mensagem) => {
    setFeedback({ tipo, mensagem });
    setTimeout(() => setFeedback(null), 4000);
  };

  const falharOperacao = (mensagem) => {
    setErro(mensagem);
    exibirFeedback('erro', mensagem);
    throw new Error(mensagem);
  };

  // Simula carregamento inicial
  useEffect(() => {
    setCarregando(true);
    delay(400).then(() => setCarregando(false));
  }, []);

  // CRUD mock — substitua o corpo de cada função pela chamada real ao service

  const salvarConta = async (dados, id = null) => {
    await delay();
    setErro(null);
    const dadosNormalizados = normalizarConta(dados);

    if (id) {
      const contaAtual = todasContas.find((conta) => conta.id === id);
      if (!contaAtual) {
        falharOperacao('Conta não encontrada.');
      }
      if (contaAtual.status === 'quitada') {
        falharOperacao('Contas quitadas não podem ser editadas.');
      }

      // TODO: const atualizada = await atualizarConta(id, dados);
      setTodasContas((prev) =>
        prev.map((c) =>
          c.id === id
            ? { ...c, ...dadosNormalizados }
            : c
        )
      );
      exibirFeedback('sucesso', 'Conta atualizada com sucesso!');
    } else {
      // TODO: const nova = await criarConta(dados);
      const nova = {
        id: proximoId++,
        ...dadosNormalizados,
        status: 'pendente',
        dataQuitacao: null,
      };
      setTodasContas((prev) => [nova, ...prev]);
      exibirFeedback('sucesso', 'Conta cadastrada com sucesso!');
    }
  };

  const removerConta = async (id) => {
    await delay();
    setErro(null);
    const contaAtual = todasContas.find((conta) => conta.id === id);
    if (!contaAtual) {
      falharOperacao('Conta não encontrada.');
    }
    if (contaAtual.status === 'quitada') {
      falharOperacao('Contas quitadas não podem ser excluídas.');
    }

    // TODO: await excluirConta(id);
    setTodasContas((prev) => prev.filter((c) => c.id !== id));
    exibirFeedback('sucesso', 'Conta excluída com sucesso!');
  };

  const liquidarConta = async (id) => {
    await delay();
    setErro(null);
    const contaAtual = todasContas.find((conta) => conta.id === id);
    if (!contaAtual) {
      falharOperacao('Conta não encontrada.');
    }
    if (contaAtual.status === 'quitada') {
      falharOperacao('Esta conta já está quitada.');
    }

    // TODO: const quitada = await quitarConta(id);
    const hoje = new Date().toISOString().split('T')[0];
    setTodasContas((prev) =>
      prev.map((c) =>
        c.id === id ? { ...c, status: 'quitada', dataQuitacao: hoje } : c
      )
    );
    exibirFeedback('sucesso', 'Conta quitada! A transação foi gerada automaticamente.');
  };

  // Aplica filtros na lista em memória
  const contas = aplicarFiltrosMock(todasContas, filtrosAplicados);
  const pendentes = contas.filter((c) => c.status === 'pendente');
  const quitadas = contas.filter((c) => c.status === 'quitada');

  const totalPendentesReceitas = pendentes
    .filter((c) => c.tipo === 'receita')
    .reduce((sum, c) => sum + c.valor, 0);

  const totalPendentesDespesas = pendentes
    .filter((c) => c.tipo === 'despesa')
    .reduce((sum, c) => sum + c.valor, 0);

  return {
    contas,
    pendentes,
    quitadas,
    filtros,
    categorias: CATEGORIAS_MOCK,
    contasCaixa: CONTAS_CAIXA_MOCK,
    carregando,
    erro,
    feedback,
    totalPendentesReceitas,
    totalPendentesDespesas,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
    salvarConta,
    removerConta,
    liquidarConta,
  };
};

export default useContas;
