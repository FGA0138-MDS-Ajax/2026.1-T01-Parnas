import { useState, useEffect, useCallback, useRef } from "react";
import { listarContasCaixa } from "../services/contaCaixa.service";
import { listarCategorias } from "../services/categoria.service";
import {
  listarTransacoes,
  criarTransacao,
  atualizarTransacao,
  excluirTransacao as excluirTransacaoService,
  criarCategoriaTransferencia,
} from "../services/transacao.service";
import { useEmpresa } from "../context/EmpresaContext";

const getCaixaMappingKey = (empresaId) =>
  `credifab_trans_caixa_mapping_${empresaId || "default"}`;

const getCaixaMapping = (empresaId) => {
  const map = localStorage.getItem(getCaixaMappingKey(empresaId));
  return map ? JSON.parse(map) : {};
};

const salvarCaixaMapping = (empresaId, transactionId, caixaId) => {
  if (!transactionId || !caixaId) return;
  const key = getCaixaMappingKey(empresaId);
  const map = getCaixaMapping(empresaId);
  map[transactionId] = caixaId;
  localStorage.setItem(key, JSON.stringify(map));
};

const useTransacoes = () => {
  const { idEmpresaLogada, versaoEmpresa } = useEmpresa();

  const [transacoes, setTransacoes] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [contasCaixa, setContasCaixa] = useState([]);
  const contasCaixaRef = useRef([]);

  const [totais, setTotais] = useState({
    totalReceitas: 0,
    totalDespesas: 0,
    saldo: 0,
  });
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [totalTransacoes, setTotalTransacoes] = useState(0);

  const [filtros, setFiltros] = useState({
    dataInicio: "",
    dataFim: "",
    tipo: "",
    categoria: "",
    contaCaixaId: "",
    valorMin: "",
    valorMax: "",
  });

  const carregarAuxiliares = useCallback(async () => {
    if (!idEmpresaLogada) return;
    try {
      const [categoriasApi, caixasApi] = await Promise.all([
        listarCategorias(),
        listarContasCaixa(),
      ]);
      setCategorias(categoriasApi || []);
      setContasCaixa(caixasApi || []);
      contasCaixaRef.current = caixasApi || [];
    } catch (error) {
      console.error("Erro ao buscar dados auxiliares:", error);
    }
  }, [idEmpresaLogada]);

  const fetchTransacoes = useCallback(
    async (filtrosAplicados, pagina = 1) => {
      if (!idEmpresaLogada) return;
      try {
        const params = {
          page: pagina,
          per_page: 20,
          ...(filtrosAplicados.dataInicio && {
            data_inicio: filtrosAplicados.dataInicio,
          }),
          ...(filtrosAplicados.dataFim && {
            data_fim: filtrosAplicados.dataFim,
          }),
          ...(filtrosAplicados.tipo && { tipo: filtrosAplicados.tipo }),
          ...(filtrosAplicados.categoria && {
            categoria: filtrosAplicados.categoria,
          }),
          ...(filtrosAplicados.valorMin && {
            valor_min: filtrosAplicados.valorMin,
          }),
          ...(filtrosAplicados.valorMax && {
            valor_max: filtrosAplicados.valorMax,
          }),
        };

        const data = await listarTransacoes(params);
        const caixaMapping = getCaixaMapping(idEmpresaLogada);

        const transacoesMapeadas = (data.transacoes || []).map((t) => {
          const caixaId = caixaMapping[t.transaction_id];
          const caixaObj = contasCaixaRef.current.find(
            (c) => String(c.id) === String(caixaId),
          );
          return {
            id: t.transaction_id,
            descricao: t.description,
            tipo: t.type,
            valor: t.amount,
            data: t.date,
            categoriaId: t.category_id,
            contaCaixaId: caixaId || null,
            contaCaixaNome: caixaObj ? caixaObj.nome : "N/A",
          };
        });

        let transacoesFinais = transacoesMapeadas;
        if (filtrosAplicados.contaCaixaId) {
          transacoesFinais = transacoesMapeadas.filter(
            (t) =>
              String(t.contaCaixaId) === String(filtrosAplicados.contaCaixaId),
          );
        }

        setTransacoes(transacoesFinais);
        setTotais({
          totalReceitas: data.resumo?.total_receitas || 0,
          totalDespesas: data.resumo?.total_despesas || 0,
          saldo: data.resumo?.saldo || 0,
        });
        setPaginaAtual(data.paginacao?.pagina_atual || 1);
        setTotalPaginas(data.paginacao?.paginas || 1);
        setTotalTransacoes(data.paginacao?.total_items || 0);
      } catch (error) {
        console.error("Erro ao buscar transações:", error);
      }
    },
    [idEmpresaLogada],
  );

  useEffect(() => {
    setPaginaAtual(1);
    carregarAuxiliares();
    fetchTransacoes(filtros, 1);
  }, [versaoEmpresa]);

  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltros((prev) => ({ ...prev, [name]: value }));
  };

  const aplicarFiltros = () => fetchTransacoes(filtros, 1);

  const limparFiltros = () => {
    const reset = {
      dataInicio: "",
      dataFim: "",
      tipo: "",
      categoria: "",
      contaCaixaId: "",
      valorMin: "",
      valorMax: "",
    };
    setFiltros(reset);
    fetchTransacoes(reset, 1);
  };

  const mudarPagina = (novaPagina) => {
    if (novaPagina >= 1 && novaPagina <= totalPaginas) {
      fetchTransacoes(filtros, novaPagina);
    }
  };

  const salvarTransacao = async (dadosTransacao, id = null) => {
    if (!idEmpresaLogada) return;

    try {
      if (dadosTransacao.modo === "transferencia") {
        let idCatSaida = categorias.find(
          (c) => (c.nome || c.name) === "Transferência (Saída)",
        )?.id;
        if (!idCatSaida) {
          try {
            idCatSaida = await criarCategoriaTransferencia(
              "Transferência (Saída)",
              "despesa",
            );
          } catch (e) {
            console.error(e);
          }
        }

        let idCatEntrada = categorias.find(
          (c) => (c.nome || c.name) === "Transferência (Entrada)",
        )?.id;
        if (!idCatEntrada) {
          try {
            idCatEntrada = await criarCategoriaTransferencia(
              "Transferência (Entrada)",
              "receita",
            );
          } catch (e) {
            console.error(e);
          }
        }

        if (!idCatSaida) {
          const fallback = categorias.find(
            (c) => (c.tipo || c.type) === "despesa",
          );
          idCatSaida = fallback?.id || fallback?.category_id;
        }
        if (!idCatEntrada) {
          const fallback = categorias.find(
            (c) => (c.tipo || c.type) === "receita",
          );
          idCatEntrada = fallback?.id || fallback?.category_id;
        }

        if (!idCatSaida || !idCatEntrada) {
          throw new Error(
            "Cadastre pelo menos uma categoria de receita e uma de despesa para realizar transferências.",
          );
        }

        const descBase = dadosTransacao.descricao || "Transferência";

        const dataSaida = await criarTransacao({
          description: `${descBase} (Saída)`,
          amount: parseFloat(dadosTransacao.valor),
          date: dadosTransacao.data,
          type: "despesa",
          category_id: parseInt(idCatSaida),
        });
        const savedIdSaida =
          dataSaida?.transaction_id || dataSaida?.transaction?.transaction_id;
        if (savedIdSaida && dadosTransacao.contaOrigemId) {
          salvarCaixaMapping(
            idEmpresaLogada,
            savedIdSaida,
            dadosTransacao.contaOrigemId,
          );
        }

        const dataEntrada = await criarTransacao({
          description: `${descBase} (Entrada)`,
          amount: parseFloat(dadosTransacao.valor),
          date: dadosTransacao.data,
          type: "receita",
          category_id: parseInt(idCatEntrada),
        });
        const savedIdEntrada =
          dataEntrada?.transaction_id ||
          dataEntrada?.transaction?.transaction_id;
        if (savedIdEntrada && dadosTransacao.contaDestinoId) {
          salvarCaixaMapping(
            idEmpresaLogada,
            savedIdEntrada,
            dadosTransacao.contaDestinoId,
          );
        }
      } else {
        const payload = {
          description: dadosTransacao.descricao,
          amount: parseFloat(dadosTransacao.valor),
          date: dadosTransacao.data,
          type: dadosTransacao.tipo,
          category_id: parseInt(dadosTransacao.categoriaId),
        };

        let responseData;
        if (id) {
          responseData = await atualizarTransacao(id, payload);
        } else {
          responseData = await criarTransacao(payload);
        }

        const newId =
          responseData?.transaction_id ||
          responseData?.transaction?.transaction_id ||
          id;
        if (newId && dadosTransacao.contaCaixaId) {
          salvarCaixaMapping(
            idEmpresaLogada,
            newId,
            dadosTransacao.contaCaixaId,
          );
        }
      }

      await carregarAuxiliares();
      fetchTransacoes(filtros, paginaAtual);
    } catch (error) {
      const msgErro =
        error.response?.data?.erro ||
        (error.response?.data?.erros_de_validacao &&
          Object.values(error.response.data.erros_de_validacao).join(", ")) ||
        error.message ||
        "Erro ao salvar transação.";
      alert(msgErro);
      throw error;
    }
  };

  const handleExcluirTransacao = async (id) => {
    try {
      await excluirTransacaoService(id);
      fetchTransacoes(filtros, paginaAtual);
    } catch (error) {
      alert("Erro ao excluir transação.");
    }
  };

  return {
    filtros,
    transacoes,
    totais,
    saldoContaSelecionada: null,
    contaCaixaSelecionada: null,
    paginaAtual,
    totalPaginas,
    totalTransacoes,
    categorias,
    contasCaixa,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
    mudarPagina,
    salvarTransacao,
    excluirTransacao: handleExcluirTransacao,
  };
};

export default useTransacoes;
