import { obterEmpresaAtiva } from "./empresa.service";

export const CONTAS_CAIXA_MOCK = [{ id: 1, nome: "Dinheiro em Espécie" }];

const getStorageKey = async () => {
  const empresa = await obterEmpresaAtiva();
  const empresaId = empresa?.company_id || "default";
  return `credifab_contas_caixa_${empresaId}`;
};

export const listarContasCaixa = async () => {
  const key = await getStorageKey();
  const salvas = localStorage.getItem(key);

  if (salvas) {
    return JSON.parse(salvas);
  }

  //se for o primeiro acesso, salva o mock inicial
  localStorage.setItem(key, JSON.stringify(CONTAS_CAIXA_MOCK));
  return CONTAS_CAIXA_MOCK;
};

export const criarContaCaixa = async (nome) => {
  const key = await getStorageKey();
  const lista = await listarContasCaixa();
  const novaConta = { id: Date.now(), nome: nome.trim() };

  const novaLista = [...lista, novaConta];
  localStorage.setItem(key, JSON.stringify(novaLista));
  return novaConta;
};

export const excluirContaCaixa = async (id) => {
  const key = await getStorageKey();
  const lista = await listarContasCaixa();

  const novaLista = lista.filter((c) => c.id !== id);
  localStorage.setItem(key, JSON.stringify(novaLista));
};
