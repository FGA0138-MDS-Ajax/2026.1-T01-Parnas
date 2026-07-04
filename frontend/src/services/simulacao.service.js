import api from "./api";
import { obterEmpresaAtiva } from "./empresa.service";

export const listarSimulacoes = async () => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para listar as simulações.");

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/simulations/`,
  );
  return data;
};

export const salvarSimulacao = async (payload) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para salvar a simulação.");

  //traduz os campos do front (PT) para o DTO do backend (EN)
  const dadosFormatados = {
    requested_amount: Number(payload.valor_solicitado),
    deadline_month: Number(payload.prazo_meses),
    interest_rate: Number(payload.taxa_juros),
    modality: payload.modalidade,
  };

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/simulations/`,
    dadosFormatados,
  );
  return data;
};

export const excluirSimulacao = async (id) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) throw new Error("Selecione uma empresa.");

  const { data } = await api.delete(
    `/api/companies/${empresa.company_id}/simulations/${id}`,
  );
  return data;
};
