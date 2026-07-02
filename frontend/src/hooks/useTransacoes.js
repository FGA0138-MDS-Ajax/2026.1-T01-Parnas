import { useState, useEffect, useCallback, useMemo } from "react";
import api from "../services/api";
import { listarContasCaixa } from "../services/contaCaixa.service";
import { listarCategorias } from "../services/categoria.service";
import { obterEmpresaAtiva } from "../services/empresa.service";

const useTransacoes = () => {
  const [transacoesRaw, setTransacoesRaw] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [contasCaixa, setContasCaixa] = useState([]);

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

  const carregarAuxiliares = useCallback(async () => {
    try {
      const [categoriasApi, caixasApi] = await Promise.all([
        listarCategorias(),
        listarContasCaixa(),
      ]);
      setCategorias(categoriasApi || []);
      setContasCaixa(caixasApi || []);
    } catch (error) {
      console.error("Erro ao buscar dados auxiliares:", error);
    }
  }, []);

  const fetchTransacoes = useCallback(
    async (filtrosAplicados, pagina = 1) => {
      if (!companyId) return;
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

        const { data } = await api.get(
          `/api/companies/${companyId}/transactions/`,
          { params },
        );

        setTransacoesRaw(data.transacoes || []);

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

  // CORREÇÃO: useMemo importado corretamente e chamado de forma direta
  const transacoes = useMemo(() => {
    const mapeadas = transacoesRaw.map((t) => {
      const caixaId = t.payment_id;
      const caixaObj = contasCaixa.find(
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

    if (filtros.contaCaixaId) {
      return mapeadas.filter(
        (t) => String(t.contaCaixaId) === String(filtros.contaCaixaId),
      );
    }
    return mapeadas;
  }, [transacoesRaw, contasCaixa, filtros.contaCaixaId]);

  useEffect(() => {
    carregarAuxiliares();
    fetchTransacoes(filtros, 1);
  }, [carregarAuxiliares, fetchTransacoes]);

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

    try {
      const payload = {
        description: dadosTransacao.descricao,
        amount: parseFloat(dadosTransacao.valor),
        date: dadosTransacao.data,
        type: dadosTransacao.tipo,
        category_id: parseInt(dadosTransacao.categoriaId),
        payment_id: dadosTransacao.contaCaixaId
          ? parseInt(dadosTransacao.contaCaixaId)
          : null,
      };

      if (id) {
        await api.put(
          `/api/companies/${companyId}/transactions/${id}`,
          payload,
        );
      } else {
        await api.post(`/api/companies/${companyId}/transactions/`, payload);
      }

      await carregarAuxiliares();
      fetchTransacoes(filtros, paginaAtual);
    } catch (error) {
      alert(error.response?.data?.erro || "Erro ao salvar transação.");
    }
  };

  const excluirTransacao = async (id) => {
    try {
      await api.delete(`/api/companies/${companyId}/transactions/${id}`);
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
    excluirTransacao,
  };
};

export default useTransacoes;
