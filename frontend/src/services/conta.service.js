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

  const params = {};
  if (status) params.status = status;

  //atualizando rotas de acordo com o novo padrão do backend
  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/bills/`,
    { params },
  );
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
  };

  return api.post(`/api/companies/${empresa.company_id}/bills/`, payload);
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
  };

  return api.put(`/api/companies/${empresa.company_id}/bills/${id}`, payload);
};

export const excluirConta = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.delete(`/api/companies/${empresa.company_id}/bills/${id}`);
};

export const quitarConta = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.patch(`/api/companies/${empresa.company_id}/bills/${id}/quitar`);
};
