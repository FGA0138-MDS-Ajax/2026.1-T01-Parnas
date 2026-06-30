import { useState, useEffect, useCallback } from "react";
import { fetchDashboard } from "../services/dashboard.service";
import { useEmpresa } from "../context/EmpresaContext";

const useDashboard = () => {
  const { idEmpresaLogada, versaoEmpresa } = useEmpresa();
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);

  const buscarDados = useCallback(async () => {
    if (!idEmpresaLogada) {
      setDados(null);
      setErro(null);
      return;
    }
    setCarregando(true);
    setErro(null);
    try {
      const resultado = await fetchDashboard();
      setDados(resultado);
    } catch (err) {
      const mensagem =
        err?.response?.data?.erro ||
        "Não foi possível carregar os dados do dashboard. Verifique sua conexão e tente novamente.";
      setErro(mensagem);
    } finally {
      setCarregando(false);
    }
  }, [idEmpresaLogada]);

  useEffect(() => {
    buscarDados();
  }, [buscarDados, versaoEmpresa]);
  return { dados, carregando, erro, recarregar: buscarDados, idEmpresaLogada };
};

export default useDashboard;
