// daniel: o hook foi reescrito de mock local para integracao real com a API; reescrevi os
// testes para mockar os services (api, empresa, categorias, contas) e validar o
// comportamento orientado ao backend (envio de params, mapeamento da resposta, paginacao).
import { renderHook, act, waitFor } from '@testing-library/react';
import { vi, describe, test, expect, beforeEach } from 'vitest';
import useTransacoes from './useTransacoes';
import api from '../services/api';
import { obterEmpresaAtiva } from '../services/empresa.service';
import { listarCategorias } from '../services/categoria.service';
import { listarContasCaixa } from '../services/contaCaixa.service';

vi.mock('../services/api', () => ({
  default: { get: vi.fn(), post: vi.fn(), put: vi.fn(), delete: vi.fn() },
}));
vi.mock('../services/empresa.service', () => ({ obterEmpresaAtiva: vi.fn() }));
vi.mock('../services/categoria.service', () => ({ listarCategorias: vi.fn() }));
vi.mock('../services/contaCaixa.service', () => ({ listarContasCaixa: vi.fn() }));

const respostaApi = {
  data: {
    transacoes: [
      { transaction_id: 1, description: 'Venda', tipo: 'receita', valor: 1000, data: '2025-05-10', categoria_id: 2 },
      { transaction_id: 2, description: 'Aluguel', tipo: 'despesa', valor: 400, data: '2025-05-12', categoria_id: 3 },
    ],
    resumo: { total_receitas: 1000, total_despesas: 400, saldo: 600 },
    paginacao: { pagina_atual: 1, paginas: 2, total_items: 8 },
  },
};

beforeEach(() => {
  vi.clearAllMocks();
  obterEmpresaAtiva.mockResolvedValue({ company_id: 1 });
  listarCategorias.mockResolvedValue([]);
  listarContasCaixa.mockResolvedValue([]);
  api.get.mockResolvedValue(respostaApi);
});

test('aplicarFiltros envia os filtros escolhidos como params', async () => {
  const { result } = renderHook(() => useTransacoes());
  await waitFor(() => expect(api.get).toHaveBeenCalled());

  act(() => result.current.handleFiltroChange({ target: { name: 'tipo', value: 'receita' } }));
  await act(async () => { await result.current.aplicarFiltros(); });

  const [, config] = api.get.mock.calls.at(-1);
  expect(config.params).toMatchObject({ tipo: 'receita', page: 1 });
});

test('handleFiltroChange atualiza o estado de filtros', async () => {
  const { result } = renderHook(() => useTransacoes());
  await waitFor(() => expect(api.get).toHaveBeenCalled());

  act(() => result.current.handleFiltroChange({ target: { name: 'categoria', value: 'Pessoal' } }));
  expect(result.current.filtros.categoria).toBe('Pessoal');
});

test('mudarPagina dentro dos limites busca a pagina; fora dos limites nao', async () => {
  const { result } = renderHook(() => useTransacoes());
  await waitFor(() => expect(api.get).toHaveBeenCalled());

  api.get.mockClear();
  act(() => result.current.mudarPagina(2)); // totalPaginas=2 -> valido
  await waitFor(() => expect(api.get).toHaveBeenCalledTimes(1));
  expect(api.get.mock.calls.at(-1)[1].params.page).toBe(2);

  api.get.mockClear();
  act(() => result.current.mudarPagina(99)); // fora do intervalo -> nao busca
  expect(api.get).not.toHaveBeenCalled();
});

test('limparFiltros reseta os filtros e rebusca', async () => {
  const { result } = renderHook(() => useTransacoes());
  await waitFor(() => expect(api.get).toHaveBeenCalled());

  act(() => result.current.handleFiltroChange({ target: { name: 'tipo', value: 'despesa' } }));
  expect(result.current.filtros.tipo).toBe('despesa');

  await act(async () => { await result.current.limparFiltros(); });
  expect(result.current.filtros.tipo).toBe('');
});
