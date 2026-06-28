import { useState, useEffect, useCallback } from 'react';
import { fetchDashboard } from '../services/dashboard.service';
import { useEmpresa } from '../context/EmpresaContext';

const useDashboard = () => {
  const { idEmpresaLogada } = useEmpresa();
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
      const resultado = await fetchDashboard(idEmpresaLogada);
      setDados(resultado);
    } catch (err) {
      const mensagem =
        err?.response?.data?.erro ||
        'Não foi possível carregar os dados do dashboard. Verifique sua conexão e tente novamente.';
      setErro(mensagem);
    } finally {
      setCarregando(false);
    }
  }, [idEmpresaLogada]);

  // Re-fetch quando a empresa ativa muda (via contexto do US15)
  useEffect(() => {
    buscarDados();
  }, [buscarDados]);

  // Escuta mudanças no localStorage para detectar troca de empresa ativa
  // sem o EmpresaProvider na árvore (compatibilidade antes do merge do US15)
  useEffect(() => {
    const handleStorage = (e) => {
      if (e.key === 'idEmpresaSimulado') buscarDados();
    };
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, [buscarDados]);

  return { dados, carregando, erro, recarregar: buscarDados, idEmpresaLogada };
};

export default useDashboard;
