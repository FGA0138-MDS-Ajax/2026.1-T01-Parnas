import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Transacoes from './Transacoes';

// a pagina usa useNavigate; espiona sem perder o resto do react-router
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

function renderPagina() {
  return render(
    <MemoryRouter>
      <Transacoes />
    </MemoryRouter>,
  );
}

const seletorTipo = () => screen.getAllByRole('combobox')[0];
const botaoAplicar = () => screen.getByRole('button', { name: /aplicar filtros/i });
const botaoLimpar = () => screen.getByRole('button', { name: /limpar filtros/i });

test('exibe os cartoes de totais no topo', () => {
  // Act
  renderPagina();

  // Assert
  expect(screen.getByText(/total de receitas/i)).toBeInTheDocument();
  expect(screen.getByText(/total de despesas/i)).toBeInTheDocument();
  expect(screen.getByText('Saldo')).toBeInTheDocument();
});

test('lista a primeira pagina com no maximo o tamanho de pagina', () => {
  // Act
  renderPagina();

  // Assert: 12 transacoes no mock, paginadas (1 cabecalho + 5 linhas de dados)
  expect(screen.getByText(/12 transação\(ões\) encontrada/i)).toBeInTheDocument();
  expect(screen.getAllByRole('row')).toHaveLength(6);
});

test('aplicar filtro de tipo atualiza a listagem', async () => {
  // Arrange
  renderPagina();

  // Act
  await userEvent.selectOptions(seletorTipo(), 'receita');
  await userEvent.click(botaoAplicar());

  // Assert
  expect(screen.getByText(/5 transação\(ões\) encontrada/i)).toBeInTheDocument();
});

test('limpar filtros restaura a listagem completa', async () => {
  // Arrange: aplica um filtro que reduz a lista
  renderPagina();
  await userEvent.selectOptions(seletorTipo(), 'receita');
  await userEvent.click(botaoAplicar());
  expect(screen.getByText(/5 transação\(ões\) encontrada/i)).toBeInTheDocument();

  // Act
  await userEvent.click(botaoLimpar());

  // Assert
  expect(screen.getByText(/12 transação\(ões\) encontrada/i)).toBeInTheDocument();
});
