import api from "./api";
import { obterEmpresaAtiva } from "./empresa.service";

export const listarDocumentos = async (pagina = 1, porPagina = 20) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para listar documentos.");

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/documents/`,
    {
      params: { page: pagina, per_page: porPagina },
    },
  );
  return data;
};

export const uploadDocumento = async (
  nome,
  tipo,
  descricao,
  arquivo,
  onProgress,
) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id)
    throw new Error("Selecione uma empresa para enviar documentos.");

  const formData = new FormData();
  formData.append("name", nome);
  formData.append("type", tipo);
  formData.append("description", descricao || "");
  formData.append("file", arquivo);

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/documents/`,
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total,
          );
          onProgress(percentCompleted);
        }
      },
    },
  );
  return data;
};

export const excluirDocumentoApi = async (id) => {
  const empresa = await obterEmpresaAtiva();
  return api.delete(`/api/companies/${empresa.company_id}/documents/${id}`);
};

export const downloadDocumentoApi = async (id, nomeArquivo) => {
  const empresa = await obterEmpresaAtiva();
  const response = await api.get(
    `/api/companies/${empresa.company_id}/documents/${id}/download`,
    {
      responseType: "blob", //lidar com arquivos binários
    },
  );

  const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", nomeArquivo);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
