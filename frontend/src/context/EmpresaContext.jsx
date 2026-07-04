import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import useAuth from '../hooks/useAuth';
import { API_BASE_URL } from '../services/api';
import {
  lerEmpresaAtivaPersistida,
  salvarEmpresaAtiva,
  limparEmpresaAtiva,
} from '../services/empresa.service';

const EMPRESA_DEMO = {
  company_id: 'demo',
  name: 'Empresa Demonstração',
  cnpj: '00000000000000',
};

const EmpresaContext = createContext(null);

const requisicaoAutenticada = async (url, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers: {
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    const text = await response.text();
    let data = null;

    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = null;
      }
    }

    if (!response.ok) {
      const mensagem =
        data?.erro ||
        data?.msg ||
        (response.status >= 500
          ? 'O servidor está indisponível. Verifique se o backend está em execução.'
          : 'Não foi possível carregar as empresas.');
      const error = new Error(mensagem);
      error.status = response.status;
      throw error;
    }

    return data;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        'Não foi possível conectar ao servidor. Verifique se o backend está em execução.',
      );
    }
    throw error;
  }
};

export const EmpresaProvider = ({ children }) => {
  const { token, login, logout, isAuthenticated } = useAuth();
  const [empresas, setEmpresas] = useState([]);
  const [empresaAtiva, setEmpresaAtiva] = useState(lerEmpresaAtivaPersistida);
  const [carregandoEmpresas, setCarregandoEmpresas] = useState(Boolean(token));
  const [erroEmpresas, setErroEmpresas] = useState('');
  const [versaoEmpresa, setVersaoEmpresa] = useState(0);
  const tokenRef = useRef(null);
  const ignorarProximaTrocaDeToken = useRef(false);

  const definirEmpresaAtiva = useCallback(async (empresa) => {
    if (!empresa?.company_id) return;

    const data = await requisicaoAutenticada('/api/sessao/empresa-ativa', {
      method: 'POST',
      body: JSON.stringify({ company_id: empresa.company_id }),
    });

    const empresaSelecionada = salvarEmpresaAtiva(empresa);
    setEmpresaAtiva(empresaSelecionada);
    setVersaoEmpresa((versao) => versao + 1);
    ignorarProximaTrocaDeToken.current = true;
    login(data.token, { preservarEmpresa: true });
    return empresaSelecionada;
  }, [login]);

  const carregarEmpresas = useCallback(async () => {
    if (!isAuthenticated) {
      setEmpresas([]);
      setEmpresaAtiva(null);
      setCarregandoEmpresas(false);
      setErroEmpresas('');
      return [];
    }

    if (token?.startsWith('mock_demo_')) {
      salvarEmpresaAtiva(EMPRESA_DEMO);
      setEmpresas([EMPRESA_DEMO]);
      setEmpresaAtiva(EMPRESA_DEMO);
      setCarregandoEmpresas(false);
      setErroEmpresas('');
      return [EMPRESA_DEMO];
    }

    setCarregandoEmpresas(true);
    setErroEmpresas('');

    try {
      const lista = await requisicaoAutenticada('/api/usuarios/me/empresas');
      const empresasNormalizadas = Array.isArray(lista) ? lista : [];
      setEmpresas(empresasNormalizadas);

      const persistida = lerEmpresaAtivaPersistida();
      const empresaPersistidaValida = empresasNormalizadas.find(
        (empresa) =>
          Number(empresa.company_id) === Number(persistida?.company_id),
      );

      if (empresaPersistidaValida) {
        setEmpresaAtiva(empresaPersistidaValida);
      } else {
        limparEmpresaAtiva();
        setEmpresaAtiva(null);

        if (empresasNormalizadas.length === 1) {
          await definirEmpresaAtiva(empresasNormalizadas[0]);
        }
      }

      return empresasNormalizadas;
    } catch (error) {
      if (error.status === 401 || error.status === 422) {
        logout();
        setErroEmpresas('Sua sessão é inválida ou expirou. Entre novamente.');
        return [];
      }
      setErroEmpresas(error.message);
      return [];
    } finally {
      setCarregandoEmpresas(false);
    }
  }, [definirEmpresaAtiva, isAuthenticated, logout, token]);

  useEffect(() => {
    const tokenMudou = tokenRef.current !== token;
    tokenRef.current = token;

    if (tokenMudou && ignorarProximaTrocaDeToken.current) {
      ignorarProximaTrocaDeToken.current = false;
      return;
    }

    if (!tokenMudou && empresaAtiva) return;
    carregarEmpresas();
  }, [token, carregarEmpresas, empresaAtiva]);

  useEffect(() => {
    if (!isAuthenticated) {
      limparEmpresaAtiva();
      setEmpresaAtiva(null);
    }
  }, [isAuthenticated]);

  const selecionarEmpresa = useCallback(async (empresaOuId) => {
    const id = Number(
      typeof empresaOuId === 'object'
        ? empresaOuId.company_id
        : empresaOuId,
    );
    const empresaDaLista = empresas.find(
      (item) => Number(item.company_id) === id,
    );
    const empresaRecebida =
      typeof empresaOuId === 'object' ? empresaOuId : null;
    const empresa = empresaDaLista || empresaRecebida;

    if (!empresa?.company_id) {
      throw new Error('Empresa selecionada não pertence ao usuário.');
    }

    return definirEmpresaAtiva(empresa);
  }, [definirEmpresaAtiva, empresas]);

  const value = useMemo(() => ({
    empresas,
    empresaAtiva,
    idEmpresaLogada: empresaAtiva?.company_id ?? null,
    carregandoEmpresas,
    erroEmpresas,
    versaoEmpresa,
    selecionarEmpresa,
    setIdEmpresaLogada: selecionarEmpresa,
    recarregarEmpresas: carregarEmpresas,
  }), [
    carregarEmpresas,
    carregandoEmpresas,
    empresaAtiva,
    empresas,
    erroEmpresas,
    selecionarEmpresa,
    versaoEmpresa,
  ]);

  return (
    <EmpresaContext.Provider value={value}>
      {children}
    </EmpresaContext.Provider>
  );
};

export const useEmpresa = () => {
  const contexto = useContext(EmpresaContext);

  if (!contexto) {
    throw new Error('useEmpresa deve ser usado dentro de EmpresaProvider.');
  }

  return contexto;
};
