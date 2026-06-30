import api from "./api";
import { obterEmpresaAtiva } from "./empresa.service";

const getEmpresaOuErro = async () => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para operar as transações.");
  }
  return empresa;
};

export const listarTransacoes = async (params = {}) => {
  const empresa = await getEmpresaOuErro();

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/transactions/`,
    { params },
  );
  return data;
};

export const criarTransacao = async (payload) => {
  const empresa = await getEmpresaOuErro();

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/transactions/`,
    payload,
  );
  return data;
};

export const atualizarTransacao = async (id, payload) => {
  const empresa = await getEmpresaOuErro();

  const { data } = await api.put(
    `/api/companies/${empresa.company_id}/transactions/${id}`,
    payload,
  );
  return data;
};

export const excluirTransacao = async (id) => {
  const empresa = await getEmpresaOuErro();

  const { data } = await api.delete(
    `/api/companies/${empresa.company_id}/transactions/${id}`,
  );
  return data;
};

export const criarCategoriaTransferencia = async (nome, tipo) => {
  const empresa = await getEmpresaOuErro();

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/categories/`,
    { name: nome, type: tipo },
  );
  return data?.category_id || data?.id;
};
