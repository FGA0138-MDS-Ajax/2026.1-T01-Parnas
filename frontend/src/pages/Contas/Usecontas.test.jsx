// daniel: o hook passou a buscar as contas da API (conta.service) e a normalizar a resposta;
// reescrevi os testes para mockar os services e validar a separacao/normalizacao e as acoes
// (quitar, excluir, salvar) que agora delegam ao backend.
import { describe, test, expect, vi, beforeEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import useContas from './Usecontas';
import {
  listarContas, criarConta, excluirConta, quitarConta,
} from '../../services/conta.service';
import { listarCategorias } from '../../services/categoria.service';
import { listarContasCaixa } from '../../services/contaCaixa.service';

vi.mock('../../services/conta.service', () => ({
  listarContas: vi.fn(),
  criarConta: vi.fn(),
  atualizarConta: vi.fn(),
  excluirConta: vi.fn(),
  quitarConta: vi.fn(),
}));
vi.mock('../../services/categoria.service', () => ({ listarCategorias: vi.fn() }));
vi.mock('../../services/contaCaixa.service', () => ({ listarContasCaixa: vi.fn() }));

// shape de "bill" como o backend devolve (normalizarResposta converte para o formato do front)
const CONTAS_API = [
  { bill_id: 1, description: 'Aluguel', amount: 1000, type: 'pagar', due_date: '2026-07-01', status: 'pendente', category_id: 1 },
  { bill_id: 2, description: 'Venda', amount: 2000, type: 'receber', due_date: '2026-07-02', status: 'pendente', category_id: 2 },
  { bill_id: 6, description: 'Conta Paga', amount: 500, type: 'pagar', due_date: '2026-06-01', status: 'quitado', category_id: 1 },
];

beforeEach(() => {
  vi.clearAllMocks();
  listarContas.mockResolvedValue(CONTAS_API);
  listarCategorias.mockResolvedValue([]);
  listarContasCaixa.mockResolvedValue([]);
  criarConta.mockResolvedValue({});
  excluirConta.mockResolvedValue({});
  quitarConta.mockResolvedValue({});
});

describe('useContas', () => {
  test('separa as contas da API em pendentes e quitadas', async () => {
    const { result } = renderHook(() => useContas());

    await waitFor(() => expect(result.current.pendentes).toHaveLength(2));
    expect(result.current.quitadas).toHaveLength(1);
  });

  test('soma os totais pendentes por tipo', async () => {
    const { result } = renderHook(() => useContas());

    await waitFor(() => expect(result.current.pendentes).toHaveLength(2));
    expect(result.current.totalPendentesReceitas).toBeCloseTo(2000, 2);
    expect(result.current.totalPendentesDespesas).toBeCloseTo(1000, 2);
  });

  test('quitar uma conta chama quitarConta e recarrega', async () => {
    const { result } = renderHook(() => useContas());
    await waitFor(() => expect(result.current.pendentes).toHaveLength(2));

    await act(async () => { await result.current.liquidarConta(2); });

    expect(quitarConta).toHaveBeenCalledWith(2);
    expect(listarContas).toHaveBeenCalledTimes(2); // carga inicial + recarga
  });

  test('excluir uma conta pendente chama excluirConta', async () => {
    const { result } = renderHook(() => useContas());
    await waitFor(() => expect(result.current.pendentes).toHaveLength(2));

    await act(async () => { await result.current.removerConta(1); });

    expect(excluirConta).toHaveBeenCalledWith(1);
  });

  test('excluir uma conta quitada falha e registra o erro', async () => {
    excluirConta.mockRejectedValue(new Error('Contas quitadas não podem ser excluídas'));
    const { result } = renderHook(() => useContas());
    await waitFor(() => expect(result.current.pendentes).toHaveLength(2));

    await act(async () => {
      await expect(result.current.removerConta(6)).rejects.toThrow(/quitadas não podem ser excluídas/i);
    });

    expect(result.current.erro).toMatch(/quitadas não podem ser excluídas/i);
  });

  test('cadastrar uma nova conta envia os dados normalizados', async () => {
    const { result } = renderHook(() => useContas());
    await waitFor(() => expect(result.current.pendentes).toHaveLength(2));

    await act(async () => {
      await result.current.salvarConta({
        descricao: 'Internet',
        valor: '199,90',
        tipo: 'despesa',
        dataVencimento: '2026-07-01',
        categoria: '3',
        contaCaixaId: '1',
      });
    });

    expect(criarConta).toHaveBeenCalledTimes(1);
    const enviado = criarConta.mock.calls[0][0];
    expect(enviado.descricao).toBe('Internet');
    expect(enviado.valor).toBeCloseTo(199.9, 2);
    expect(enviado.tipo).toBe('despesa');
  });
});
