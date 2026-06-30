import api from "./api";
import { obterEmpresaAtiva } from "./empresa.service";

export const fetchDashboard = async () => {
  const empresa = obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para carregar o dashboard.");
  }

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/dashboard/`,
  );
  return data;
};

export default fetchDashboard;
