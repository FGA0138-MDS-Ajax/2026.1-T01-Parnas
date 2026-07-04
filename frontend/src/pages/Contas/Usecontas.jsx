import { useState, useEffect, useCallback } from "react";
import useAppliedFilters from "../../hooks/useAppliedFilters";
import { listarContasCaixa } from "../../services/contaCaixa.service";
import {
  listarContas,
  criarConta,
  atualizarConta,
  excluirConta,
  quitarConta,
} from "../../services/conta.service";
import { listarCategorias } from "../../services/categoria.service";

const FILTROS_INICIAIS = { status: "", tipo: "", dataInicio: "", dataFim: "" };

const aplicarFiltrosMock = (lista, filtros) => {
  return lista.filter((c) => {
    if (filtros.status && c.status !== filtros.status) return false;
    if (filtros.tipo && c.tipo !== filtros.tipo) return false;
    if (filtros.dataInicio && c.dataVencimento < filtros.dataInicio)
      return false;
    if (filtros.dataFim && c.dataVencimento > filtros.dataFim) return false;
    return true;
  });
};

const normalizarConta = (dados) => ({
  descricao: dados.descricao.trim(),
  valor: parseFloat(String(dados.valor).replace(",", ".")),
  tipo: dados.tipo,
  dataVencimento: dados.dataVencimento,
  categoria: dados.categoria || null,
  contaCaixaId: dados.contaCaixaId || null,
});

const normalizarResposta = (conta) => ({
  id: conta.id || conta.bill_id,
  descricao: conta.description || conta.descricao,
  valor: Number(conta.amount || conta.valor || 0),
  tipo: conta.type === "receber" ? "receita" : "despesa",
  dataVencimento: conta.due_date || conta.dataVencimento,
  status: conta.status === "quitado" ? "quitada" : "pendente",
  dataQuitacao: conta.payment_date || conta.dataQuitacao || null,
  categoria: conta.category_id || conta.categoria || null,
  categoriaNome: "",
  contaCaixaId: conta.contaCaixaId || null,
  contaCaixaNome: conta.contaCaixaNome || "",
});

const useContas = () => {
  const [todasContas, setTodasContas] = useState([]);
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
  const [categorias, setCategorias] = useState([]);
  const [contasCaixa, setContasCaixa] = useState([]);

  const exibirFeedback = (tipo, mensagem) => {
    setFeedback({ tipo, mensagem });
    setTimeout(() => setFeedback(null), 4000);
  };

  const carregarDados = useCallback(async () => {
    try {
      setCarregando(true);
      setErro(null);
      const [contasApi, categoriasApi, caixasApi] = await Promise.all([
        listarContas(),
        listarCategorias(),
        listarContasCaixa(),
      ]);

      const contasNormalizadas = (contasApi || []).map((conta) => {
        const norm = normalizarResposta(conta);
        const cat = categoriasApi?.find(
          (c) => String(c.id) === String(norm.categoria),
        );
        if (cat) norm.categoriaNome = cat.nome;
        const caixa = caixasApi?.find(
          (cx) => String(cx.id) === String(norm.contaCaixaId),
        );
        if (caixa) norm.contaCaixaNome = caixa.nome;

        return norm;
      });

      setTodasContas(contasNormalizadas);
      setCategorias(categoriasApi || []);
      setContasCaixa(caixasApi || []);
    } catch (error) {
      setErro(error.message || "Erro ao carregar dados.");
    } finally {
      setCarregando(false);
    }
  }, []);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const salvarConta = async (dados, id = null) => {
    try {
      setErro(null);
      const dadosNormalizados = normalizarConta(dados);
      if (id) {
        await atualizarConta(id, dadosNormalizados);
        exibirFeedback("sucesso", "Conta atualizada com sucesso!");
      } else {
        await criarConta(dadosNormalizados);
        exibirFeedback("sucesso", "Conta cadastrada com sucesso!");
      }
      await carregarDados();
    } catch (error) {
      const mensagem =
        error.response?.data?.erro || error.message || "Erro ao salvar conta.";
      setErro(mensagem);
      exibirFeedback("erro", mensagem);
      throw error;
    }
  };

  const removerConta = async (id) => {
    try {
      setErro(null);
      await excluirConta(id);
      exibirFeedback("sucesso", "Conta excluída com sucesso!");
      await carregarDados();
    } catch (error) {
      const mensagem =
        error.response?.data?.erro || error.message || "Erro ao excluir conta.";
      setErro(mensagem);
      exibirFeedback("erro", mensagem);
      throw error;
    }
  };

  const liquidarConta = async (id) => {
    try {
      setErro(null);
      await quitarConta(id);
      exibirFeedback(
        "sucesso",
        "Conta quitada! A transação foi gerada automaticamente.",
      );
      await carregarDados();
    } catch (error) {
      const mensagem =
        error.response?.data?.erro || error.message || "Erro ao quitar conta.";
      setErro(mensagem);
      exibirFeedback("erro", mensagem);
      throw error;
    }
  };

  const contas = aplicarFiltrosMock(todasContas, filtrosAplicados);
  const pendentes = contas.filter((c) => c.status === "pendente");
  const quitadas = contas.filter((c) => c.status === "quitada");

  const totalPendentesReceitas = pendentes
    .filter((c) => c.tipo === "receita")
    .reduce((sum, c) => sum + c.valor, 0);
  const totalPendentesDespesas = pendentes
    .filter((c) => c.tipo === "despesa")
    .reduce((sum, c) => sum + c.valor, 0);

  return {
    contas,
    pendentes,
    quitadas,
    filtros,
    categorias,
    contasCaixa,
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
