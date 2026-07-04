const EMPRESA_ATIVA_KEY = "empresaAtiva";

const normalizarCompanyId = (companyId) => {
  const numero = Number(companyId);
  return companyId !== "" && Number.isFinite(numero) ? numero : companyId;
};

/**
 * Fonte única de verdade para "qual empresa está ativa agora".
 *
 * Usa a MESMA chave de localStorage que o EmpresaContext.jsx. Isso é
 * proposital: o que o usuário seleciona na interface através do
 * EmpresaContext (selecionarEmpresa -> definirEmpresaAtiva) precisa ser
 * exatamente o que os services de dados enxergam, ou a troca de empresa
 * não tem efeito real nas chamadas à API.
 */
export const lerEmpresaAtivaPersistida = () => {
  try {
    const valor = localStorage.getItem(EMPRESA_ATIVA_KEY);
    return valor ? JSON.parse(valor) : null;
  } catch {
    localStorage.removeItem(EMPRESA_ATIVA_KEY);
    return null;
  }
};

export const salvarEmpresaAtiva = (empresa) => {
  if (!empresa?.company_id) return null;

  const empresaNormalizada = {
    ...empresa,
    company_id: normalizarCompanyId(empresa.company_id),
  };

  localStorage.setItem(EMPRESA_ATIVA_KEY, JSON.stringify(empresaNormalizada));
  return empresaNormalizada;
};

export const limparEmpresaAtiva = () => {
  localStorage.removeItem(EMPRESA_ATIVA_KEY);
};

/**
 * Usado por todos os services de dados (conta, categoria, documento,
 * comparacao, simulacao, contaCaixa) para descobrir o company_id a usar
 * nas chamadas à API.
 *
 * IMPORTANTE — mudança de comportamento intencional: esta função NÃO
 * faz mais fallback de "pegar a primeira empresa salva" nem chama a API
 * sozinha para escolher uma empresa por conta própria. Ela só reflete o
 * que foi explicitamente selecionado pelo usuário via EmpresaContext.
 * Se nada foi selecionado ainda, retorna null — e cada service lança o
 * erro "Selecione uma empresa para..." (esse é o comportamento correto:
 * força o usuário a escolher antes de ver dados de qualquer empresa).
 */
export const obterEmpresaAtiva = async () => {
  return lerEmpresaAtivaPersistida();
};
