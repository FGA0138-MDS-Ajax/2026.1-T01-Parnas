import api from "./api";
import { obterEmpresaAtiva } from "./empresa.service";

export const calcularComparacao = async (payload) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) throw new Error("Selecione uma empresa ativa.");

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/comparisons/calcular`,
    payload,
  );
  return data;
};

export const salvarComparacao = async (payload) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) throw new Error("Selecione uma empresa ativa.");

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/comparisons/`,
    payload,
  );
  return data;
};

export const listarComparacoes = async () => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) throw new Error("Selecione uma empresa ativa.");

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/comparisons/`,
  );
  return data;
};

export const deletarComparacao = async (id) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) throw new Error("Selecione uma empresa ativa.");

  const { data } = await api.delete(
    `/api/companies/${empresa.company_id}/comparisons/${id}`,
  );
  return data;
};

export const exportarPDF = async (id) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) throw new Error("Selecione uma empresa ativa.");

  const response = await api.get(
    `/api/companies/${empresa.company_id}/comparisons/${id}/exportar`,
    {
      responseType: "blob",
    },
  );

  const url = window.URL.createObjectURL(
    new Blob([response.data], { type: "application/pdf" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = `comparativo_credito_${id}.pdf`;
  link.click();
  window.URL.revokeObjectURL(url);
};
