import api from "./api";
import { obterEmpresaAtiva } from "./empresa.service";

const normalizarPagamento = (pagamento) => ({
  id: pagamento.payment_id ?? pagamento.id,
  nome: pagamento.name ?? pagamento.nome,
});

export const listarContasCaixa = async () => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para carregar as contas caixa.");
  }

  const { data } = await api.get(
    `/api/companies/${empresa.company_id}/payments/`,
  );

  const pagamentos = Array.isArray(data?.payments) ? data.payments : [];
  return pagamentos.map(normalizarPagamento);
};

export const criarContaCaixa = async (nome) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para criar a conta caixa.");
  }

  const { data } = await api.post(
    `/api/companies/${empresa.company_id}/payments/`,
    { name: nome.trim() },
  );

  return normalizarPagamento(data?.payment || {});
};

export const atualizarContaCaixa = async (id, nome) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para atualizar a conta caixa.");
  }

  const { data } = await api.put(
    `/api/companies/${empresa.company_id}/payments/${id}`,
    { name: nome.trim() },
  );

  return normalizarPagamento(data?.payment || {});
};

export const excluirContaCaixa = async (id) => {
  const empresa = await obterEmpresaAtiva();
  if (!empresa?.company_id) {
    throw new Error("Selecione uma empresa para excluir a conta caixa.");
  }

  return api.delete(`/api/companies/${empresa.company_id}/payments/${id}`);
};
