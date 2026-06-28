import { describe, test, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import useAppliedFilters from './useAppliedFilters';

const INICIAIS = { tipo: '', status: '' };

describe('useAppliedFilters', () => {
  test('comeca com os filtros iniciais nos dois estados', () => {
    const { result } = renderHook(() => useAppliedFilters(INICIAIS));
    expect(result.current.filtros).toEqual(INICIAIS);
    expect(result.current.filtrosAplicados).toEqual(INICIAIS);
  });

  test('handleFiltroChange muda o rascunho mas nao o aplicado', () => {
    const { result } = renderHook(() => useAppliedFilters(INICIAIS));

    act(() => {
      result.current.handleFiltroChange({ target: { name: 'tipo', value: 'receita' } });
    });

    expect(result.current.filtros.tipo).toBe('receita');
    expect(result.current.filtrosAplicados.tipo).toBe('');
  });

  test('aplicarFiltros promove o rascunho para o aplicado', () => {
    const { result } = renderHook(() => useAppliedFilters(INICIAIS));

    act(() => {
      result.current.handleFiltroChange({ target: { name: 'tipo', value: 'despesa' } });
    });
    act(() => {
      result.current.aplicarFiltros();
    });

    expect(result.current.filtrosAplicados.tipo).toBe('despesa');
  });

  test('limparFiltros volta os dois estados ao inicial', () => {
    const { result } = renderHook(() => useAppliedFilters(INICIAIS));

    act(() => {
      result.current.handleFiltroChange({ target: { name: 'tipo', value: 'receita' } });
      result.current.aplicarFiltros();
    });
    act(() => {
      result.current.limparFiltros();
    });

    expect(result.current.filtros).toEqual(INICIAIS);
    expect(result.current.filtrosAplicados).toEqual(INICIAIS);
  });
});
