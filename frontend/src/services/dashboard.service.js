import api from "./api";

export const fetchDashboard = async () => {
  const deLocalStorage = localStorage.getItem("empresaAtiva");
  const empresa = deLocalStorage ? JSON.parse(deLocalStorage) : null;

  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para carregar o dashboard.");
  }

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/dashboard/`,
  );
  return data;
};

export default fetchDashboard;
