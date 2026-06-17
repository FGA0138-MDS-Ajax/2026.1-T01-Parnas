import { renderHook, act } from '@testing-library/react';
import useTransacoes from './useTransacoes';

// dispara o onChange de um filtro como o input/select faria
function mudarFiltro(result, name, value) {
  act(() => result.current.handleFiltroChange({ target: { name, value } }));
}

function aplicar(result) {
  act(() => result.current.aplicarFiltros());
}

test('estado inicial lista a primeira pagina com todas as transacoes', () => {
  // Act
  const { result } = renderHook(() => useTransacoes());

  // Assert
  expect(result.current.totalTransacoes).toBe(12);
  expect(result.current.transacoes).toHaveLength(5); // 5 por pagina
  expect(result.current.totalPaginas).toBe(3);
});

test('totais somam receitas, despesas e saldo de tudo', () => {
  // Act
  const { result } = renderHook(() => useTransacoes());

  // Assert
  expect(result.current.totais.totalReceitas).toBe(15800);
  expect(result.current.totais.totalDespesas).toBe(10100);
  expect(result.current.totais.saldo).toBe(5700);
});

test('filtro por tipo receita mantem apenas receitas', () => {
  // Arrange
  const { result } = renderHook(() => useTransacoes());

  // Act
  mudarFiltro(result, 'tipo', 'receita');
  aplicar(result);

  // Assert
  expect(result.current.totalTransacoes).toBe(5);
  expect(result.current.totais.totalDespesas).toBe(0);
  expect(result.current.totais.totalReceitas).toBe(15800);
});

test('filtro por categoria mantem apenas a categoria escolhida', () => {
  // Arrange
  const { result } = renderHook(() => useTransacoes());

  // Act
  mudarFiltro(result, 'categoria', 'Pessoal');
  aplicar(result);

  // Assert
  expect(result.current.totalTransacoes).toBe(2);
  expect(result.current.transacoes.every((t) => t.categoria === 'Pessoal')).toBe(true);
});

test('filtro por periodo recorta pelo intervalo de datas', () => {
  // Arrange
  const { result } = renderHook(() => useTransacoes());

  // Act
  mudarFiltro(result, 'dataInicio', '2025-05-01');
  mudarFiltro(result, 'dataFim', '2025-05-31');
  aplicar(result);

  // Assert
  expect(result.current.totalTransacoes).toBe(6);
  expect(result.current.transacoes.every((t) => t.data >= '2025-05-01' && t.data <= '2025-05-31')).toBe(true);
});

test('filtro por valor minimo e maximo recorta pela faixa', () => {
  // Arrange
  const { result } = renderHook(() => useTransacoes());

  // Act
  mudarFiltro(result, 'valorMin', '1000');
  mudarFiltro(result, 'valorMax', '3000');
  aplicar(result);

  // Assert
  expect(result.current.transacoes.every((t) => t.valor >= 1000 && t.valor <= 3000)).toBe(true);
  expect(result.current.totalTransacoes).toBe(4);
});

test('aplicar filtros volta para a primeira pagina', () => {
  // Arrange: vai para a ultima pagina antes de filtrar
  const { result } = renderHook(() => useTransacoes());
  act(() => result.current.mudarPagina(3));
  expect(result.current.paginaAtual).toBe(3);

  // Act
  mudarFiltro(result, 'tipo', 'despesa');
  aplicar(result);

  // Assert
  expect(result.current.paginaAtual).toBe(1);
});

test('limpar filtros restaura a listagem completa', () => {
  // Arrange: aplica um filtro que reduz a lista
  const { result } = renderHook(() => useTransacoes());
  mudarFiltro(result, 'tipo', 'receita');
  aplicar(result);
  expect(result.current.totalTransacoes).toBe(5);

  // Act
  act(() => result.current.limparFiltros());

  // Assert
  expect(result.current.totalTransacoes).toBe(12);
  expect(result.current.filtros.tipo).toBe('');
  expect(result.current.paginaAtual).toBe(1);
});

test('mudar pagina avanca dentro dos limites', () => {
  // Arrange
  const { result } = renderHook(() => useTransacoes());

  // Act
  act(() => result.current.mudarPagina(2));

  // Assert
  expect(result.current.paginaAtual).toBe(2);
  expect(result.current.transacoes).toHaveLength(5);
});

test('mudar pagina ignora valores fora do intervalo', () => {
  // Arrange
  const { result } = renderHook(() => useTransacoes());

  // Act + Assert: abaixo do minimo nao muda
  act(() => result.current.mudarPagina(0));
  expect(result.current.paginaAtual).toBe(1);

  // Act + Assert: acima do maximo tambem nao muda
  act(() => result.current.mudarPagina(99));
  expect(result.current.paginaAtual).toBe(1);
});
