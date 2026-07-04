import api from "./api";
import { obterEmpresaAtiva as obterEmpresaAtivaService } from "./empresa.service";

const obterEmpresaAtiva = async () => {
  const empresa = await obterEmpresaAtivaService();
  return empresa;
};

const normalizarTipo = (tipo) => {
  const valor = String(tipo || "")
    .trim()
    .toLowerCase();
  if (valor === "despesa" || valor === "pagar" || valor === "expense")
    return "despesa";
  return "receita";
};

const formatarTipoParaExibicao = (tipo) => {
  const valor = String(tipo || "")
    .trim()
    .toLowerCase();
  if (valor === "despesa" || valor === "pagar" || valor === "expense")
    return "Despesa";
  return "Receita";
};

export const listarCategorias = async () => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para carregar as categorias.");

  //rota atualizada para o padrão do backend
  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/categories/`,
  );
  const categorias = Array.isArray(data?.categories) ? data.categories : [];
  return categorias.map((categoria) => ({
    id: categoria.category_id || categoria.id,
    nome: categoria.name || categoria.nome,
    tipo: normalizarTipo(categoria.type || categoria.tipo),
    tipoExibicao: formatarTipoParaExibicao(categoria.type || categoria.tipo),
  }));
};

export const criarCategoria = async (dados) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para criar a categoria.");

  return api.post(`/api/companies/${empresa.company_id}/categories/`, {
    name: dados.nome,
    type: normalizarTipo(dados.tipo),
  });
};

export const atualizarCategoria = async (id, dados) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para atualizar a categoria.");

  return api.put(`/api/companies/${empresa.company_id}/categories/${id}`, {
    name: dados.nome,
    type: normalizarTipo(dados.tipo),
  });
};

export const excluirCategoria = async (id) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para excluir a categoria.");

  return api.delete(`/api/companies/${empresa.company_id}/categories/${id}`);
};
