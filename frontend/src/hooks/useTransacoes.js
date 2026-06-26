import { useState, useEffect, useCallback } from "react";
import api from "../services/api";
import { CONTAS_CAIXA_MOCK } from "../services/contaCaixa.service";
import { listarCategorias } from "../services/categoria.service";
import { obterEmpresaAtiva } from "../services/empresa.service";

const useTransacoes = () => {
  const [transacoes, setTransacoes] = useState([]);
  const [categorias, setCategorias] = useState([]);

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

  const [companyId, setCompanyId] = useState(null);

  useEffect(() => {
    const carregarEmpresa = async () => {
      const empresa = await obterEmpresaAtiva();
      setCompanyId(empresa?.company_id || null);
    };
    carregarEmpresa();
  }, []);

  const fetchCategorias = useCallback(async () => {
    try {
      const categoriasApi = await listarCategorias();
      setCategorias(categoriasApi);
    } catch (error) {
      console.error("Erro ao buscar categorias:", error);
    }
  }, []);

  const fetchTransacoes = useCallback(
    async (filtrosAplicados, pagina = 1) => {
      if (!companyId) return;

      try {
        const params = {
          company_id: companyId,
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

        const { data } = await api.get("/api/transactions/", { params });

        const transacoesMapeadas = (data.transacoes || []).map((t) => ({
          id: t.transaction_id,
          descricao: t.description,
          tipo: t.tipo,
          valor: t.valor,
          data: t.data,
          categoriaId: t.categoria_id,
          contaCaixaNome: "N/A",
        }));

        setTransacoes(transacoesMapeadas);
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
    [companyId],
  );

  useEffect(() => {
    fetchCategorias();
    fetchTransacoes(filtros, 1);
  }, [fetchCategorias, fetchTransacoes]);

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
    if (!companyId) return;
    if (dadosTransacao.modo === "transferencia") {
      const catTransferencia =
        categorias.find((c) => c.nome.toLowerCase().includes("transfer")) ||
        categorias[0];

      if (!catTransferencia) {
        alert(
          "Por favor, cadastre pelo menos uma categoria (ex: 'Transferências') para realizar transferências.",
        );
        return;
      }

      const descricaoBase =
        dadosTransacao.descricao || "Transferência entre contas";

      const payloadOrigem = {
        description: `${descricaoBase} (Saída)`,
        amount: parseFloat(dadosTransacao.valor),
        date: dadosTransacao.data,
        type: "despesa",
        category_id: parseInt(catTransferencia.id),
        company_id: parseInt(companyId),
      };

      const payloadDestino = {
        description: `${descricaoBase} (Entrada)`,
        amount: parseFloat(dadosTransacao.valor),
        date: dadosTransacao.data,
        type: "receita",
        category_id: parseInt(catTransferencia.id),
        company_id: parseInt(companyId),
      };

      try {
        await api.post("/api/transactions/", payloadOrigem);
        await api.post("/api/transactions/", payloadDestino);
        fetchTransacoes(filtros, paginaAtual);
        return;
      } catch (error) {
        alert("Erro ao registrar a transferência.");
        throw error;
      }
    }

    const payload = {
      description: dadosTransacao.descricao,
      amount: parseFloat(dadosTransacao.valor),
      date: dadosTransacao.data,
      type: dadosTransacao.tipo,
      category_id: parseInt(dadosTransacao.categoriaId),
      company_id: parseInt(companyId),
    };

    try {
      if (id) {
        await api.put(`/api/transactions/${id}`, payload);
      } else {
        await api.post("/api/transactions/", payload);
      }
      fetchTransacoes(filtros, paginaAtual);
    } catch (error) {
      const msgErro =
        error.response?.data?.erro ||
        Object.values(error.response?.data?.erros_de_validacao || {}).join(
          ", ",
        ) ||
        "Erro ao salvar transação.";
      alert(msgErro);
      throw error;
    }
  };

  const excluirTransacao = async (id) => {
    try {
      await api.delete(`/api/transactions/${id}?company_id=${companyId}`);
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
