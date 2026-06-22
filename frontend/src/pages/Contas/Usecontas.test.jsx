import { describe, test, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import useContas from './Usecontas';

describe('useContas', () => {
  test('separa as contas iniciais em pendentes e quitadas', () => {
    const { result } = renderHook(() => useContas());
    expect(result.current.pendentes).toHaveLength(5);
    expect(result.current.quitadas).toHaveLength(2);
  });

  test('soma os totais pendentes por tipo', () => {
    const { result } = renderHook(() => useContas());
    expect(result.current.totalPendentesReceitas).toBeCloseTo(13250, 2);
    expect(result.current.totalPendentesDespesas).toBeCloseTo(4119.9, 2);
  });

  test('quitar uma conta move ela de pendentes para quitadas', async () => {
    const { result } = renderHook(() => useContas());

    await act(async () => {
      await result.current.liquidarConta(2);
    });

    expect(result.current.pendentes).toHaveLength(4);
    expect(result.current.quitadas).toHaveLength(3);
  });

  test('excluir uma conta pendente remove ela da lista', async () => {
    const { result } = renderHook(() => useContas());

    await act(async () => {
      await result.current.removerConta(1);
    });

    expect(result.current.pendentes).toHaveLength(4);
  });

  test('excluir uma conta quitada falha e registra o erro', async () => {
    const { result } = renderHook(() => useContas());

    await act(async () => {
      await expect(result.current.removerConta(6)).rejects.toThrow(
        /quitadas não podem ser excluídas/i,
      );
    });

    expect(result.current.erro).toMatch(/quitadas não podem ser excluídas/i);
    expect(result.current.quitadas).toHaveLength(2);
  });

  test('cadastrar uma nova conta entra como pendente', async () => {
    const { result } = renderHook(() => useContas());

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

    expect(result.current.pendentes).toHaveLength(6);
    expect(result.current.pendentes[0].descricao).toBe('Internet');
    expect(result.current.pendentes[0].valor).toBeCloseTo(199.9, 2);
  });
});
