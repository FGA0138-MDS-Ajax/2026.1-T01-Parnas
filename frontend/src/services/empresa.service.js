import api from "./api";

const STORAGE_KEY = "credifab_empresas_reais";
const EMPRESA_ATIVA_KEY = "empresa_ativa";
const EMPRESA_ID_KEY = "idEmpresaSimulado";
const USER_EMAIL_KEY = "auth_user_email";

const getUserKey = () => {
  const email = (localStorage.getItem(USER_EMAIL_KEY) || "default")
    .trim()
    .toLowerCase();
  return `credifab_empresas_${email}`;
};

const getEmpresaAtivaKey = () => {
  const email = (localStorage.getItem(USER_EMAIL_KEY) || "default")
    .trim()
    .toLowerCase();
  return `empresa_ativa_${email}`;
};

const getEmpresaIdKey = () => {
  const email = (localStorage.getItem(USER_EMAIL_KEY) || "default")
    .trim()
    .toLowerCase();
  return `idEmpresaSimulado_${email}`;
};

const normalizarEmpresa = (empresa) => ({
  ...empresa,
  company_id: empresa.company_id || empresa.id || empresa.companyId,
  cnpj: empresa.cnpj || empresa.CNPJ || empresa.cnpjEmpresa || "",
  name: empresa.name || empresa.nome || empresa.company_name || "",
});

export const lerEmpresasSalvas = () => {
  try {
    const valor =
      localStorage.getItem(getUserKey()) || localStorage.getItem(STORAGE_KEY);
    if (!valor) return [];
    const empresas = JSON.parse(valor);
    return Array.isArray(empresas) ? empresas.map(normalizarEmpresa) : [];
  } catch (error) {
    return [];
  }
};

export const salvarEmpresaAtiva = (empresa) => {
  const empresaNormalizada = normalizarEmpresa(empresa);
  if (!empresaNormalizada.company_id && !empresaNormalizada.cnpj) return null;

  localStorage.setItem(
    getEmpresaAtivaKey(),
    JSON.stringify(empresaNormalizada),
  );
  localStorage.setItem(
    getEmpresaIdKey(),
    String(empresaNormalizada.company_id || ""),
  );
  localStorage.setItem(EMPRESA_ATIVA_KEY, JSON.stringify(empresaNormalizada));
  localStorage.setItem(
    EMPRESA_ID_KEY,
    String(empresaNormalizada.company_id || ""),
  );

  const empresasSalvas = lerEmpresasSalvas();
  const jaExiste = empresasSalvas.some(
    (item) =>
      String(item.company_id || "") ===
      String(empresaNormalizada.company_id || ""),
  );

  const listaAtualizada = jaExiste
    ? empresasSalvas.map((item) =>
        String(item.company_id || "") ===
        String(empresaNormalizada.company_id || "")
          ? empresaNormalizada
          : item,
      )
    : [empresaNormalizada, ...empresasSalvas];

  localStorage.setItem(getUserKey(), JSON.stringify(listaAtualizada));
  localStorage.setItem(STORAGE_KEY, JSON.stringify(listaAtualizada));
  return empresaNormalizada;
};

export const obterEmpresaAtiva = async () => {
  const empresasSalvas = lerEmpresasSalvas();
  if (empresasSalvas.length > 0) {
    const empresaSalva = empresasSalvas[0];
    if (empresaSalva.company_id || empresaSalva.cnpj) {
      salvarEmpresaAtiva(empresaSalva);
      return empresaSalva;
    }
  }

  const token =
    localStorage.getItem("token") || localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const { data } = await api.get("/api/companies");
    const empresas = Array.isArray(data?.companies) ? data.companies : [];
    if (empresas.length === 0) return null;

    const empresaAtiva = salvarEmpresaAtiva(empresas[0]);
    return empresaAtiva;
  } catch (error) {
    return null;
  }
};

export const limparEmpresaAtiva = () => {
  localStorage.removeItem(getEmpresaAtivaKey());
  localStorage.removeItem(getEmpresaIdKey());
  localStorage.removeItem(EMPRESA_ATIVA_KEY);
  localStorage.removeItem(EMPRESA_ID_KEY);
};
