import api from "./api";
import { obterEmpresaAtiva as obterEmpresaAtivaService } from "./empresa.service";

const obterEmpresaAtiva = async () => {
  const empresa = await obterEmpresaAtivaService();
  return empresa;
};

export const listarContas = async (status = "") => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para carregar as contas.");
  }

  const params = { company_id: empresa.company_id };
  if (status) params.status = status;

  // AQUI: adicionamos a barra no final para evitar o erro 308
  const { data } = await api.get("/api/contas/", { params });
  return Array.isArray(data) ? data : data?.contas || [];
};

export const criarConta = async (dados) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para criar a conta.");
  }

  const payload = {
    description: dados.descricao,
    amount: Number(dados.valor),
    type: dados.tipo === "receita" ? "receber" : "pagar",
    due_date: dados.dataVencimento,
    category_id: Number(dados.categoria),
    company_id: empresa.company_id,
  };

  return api.post("/api/contas/", payload);
};

export const atualizarConta = async (id, dados) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para atualizar a conta.");
  }

  const payload = {
    description: dados.descricao,
    amount: Number(dados.valor),
    type: dados.tipo === "receita" ? "receber" : "pagar",
    due_date: dados.dataVencimento,
    category_id: Number(dados.categoria),
    company_id: empresa.company_id,
  };

  return api.put(`/api/contas/${id}`, payload);
};

export const excluirConta = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.delete(`/api/contas/${id}?company_id=${empresa.company_id}`);
};

export const quitarConta = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.patch(`/api/contas/${id}/quitar?company_id=${empresa.company_id}`);
};
