import api from "./api";
import { obterEmpresaAtiva as obterEmpresaAtivaService } from "./empresa.service";

const obterEmpresaAtiva = async () => {
  const empresa = await obterEmpresaAtivaService();
  return empresa;
};

// fazendo com que a parte de contas caixa funcione independente do bd 
const getCaixaMappingKey = async () => {
  const empresa = await obterEmpresaAtiva();
  return `credifab_bill_caixa_mapping_${empresa?.company_id || "default"}`;
};

const getCaixaMapping = async () => {
  const key = await getCaixaMappingKey();
  const map = localStorage.getItem(key);
  return map ? JSON.parse(map) : {};
};

const saveCaixaMapping = async (billId, caixaId) => {
  if (!billId || !caixaId) return;
  const key = await getCaixaMappingKey();
  const map = await getCaixaMapping();
  map[billId] = caixaId;
  localStorage.setItem(key, JSON.stringify(map));
};

export const listarContas = async (status = "") => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para carregar as contas.");
  }

  const params = {};
  if (status) params.status = status;

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/bills/`,
    { params },
  );

  const contas = Array.isArray(data) ? data : data?.contas || [];

  const caixaMapping = await getCaixaMapping();
  return contas.map((conta) => ({
    ...conta,
    contaCaixaId: caixaMapping[conta.id || conta.bill_id] || null,
  }));
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

  const response = await api.post(
    `/api/companies/${empresa.company_id}/bills/`,
    payload,
  );

  const novoId = response.data?.id || response.data?.bill_id;
  if (novoId && dados.contaCaixaId) {
    await saveCaixaMapping(novoId, dados.contaCaixaId);
  }

  return response;
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

  const response = await api.put(
    `/api/companies/${empresa.company_id}/bills/${id}`,
    payload,
  );

  if (dados.contaCaixaId) {
    await saveCaixaMapping(id, dados.contaCaixaId);
  }

  return response;
};

export const excluirConta = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.delete(`/api/companies/${empresa.company_id}/bills/${id}`);
};

export const quitarConta = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.patch(`/api/companies/${empresa.company_id}/bills/${id}/quitar`);
};
