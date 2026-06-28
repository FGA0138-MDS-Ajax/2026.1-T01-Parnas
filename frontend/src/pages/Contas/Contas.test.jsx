import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, beforeEach, test, expect } from 'vitest';

// estado e spies do hook, via vi.hoisted (acessível dentro do vi.mock)
const mocks = vi.hoisted(() => ({
  state: null,
  liquidarConta: vi.fn(),
  removerConta: vi.fn(),
  salvarConta: vi.fn(),
}));

vi.mock('./Usecontas', () => ({ default: () => mocks.state }));

import Contas from './Contas';

const baseHook = () => ({
  pendentes: [],
  quitadas: [],
  filtros: { tipo: '', status: '', dataInicio: '', dataFim: '' },
  carregando: false,
  erro: null,
  feedback: null,
  categorias: [],
  totalPendentesReceitas: 0,
  totalPendentesDespesas: 0,
  handleFiltroChange: vi.fn(),
  aplicarFiltros: vi.fn(),
  limparFiltros: vi.fn(),
  salvarConta: mocks.salvarConta,
  removerConta: mocks.removerConta,
  liquidarConta: mocks.liquidarConta,
});

const PENDENTE = {
  id: 1, descricao: 'Aluguel', categoriaNome: 'Despesas', tipo: 'despesa',
  dataVencimento: '2026-07-01', valor: 1000, status: 'pendente',
};
const QUITADA = {
  id: 2, descricao: 'Venda', categoriaNome: 'Vendas', tipo: 'receita',
  dataVencimento: '2026-06-01', dataQuitacao: '2026-06-02', valor: 500, status: 'quitada',
};

beforeEach(() => {
  vi.clearAllMocks();
  mocks.state = baseHook();
});

test('lista contas separadas em Pendentes e Quitadas', () => {
  mocks.state = { ...baseHook(), pendentes: [PENDENTE], quitadas: [QUITADA] };
  render(<Contas />);

  expect(screen.getByRole('heading', { name: /Pendentes/ })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: /Quitadas/ })).toBeInTheDocument();
  expect(screen.getByText('Aluguel')).toBeInTheDocument();
  expect(screen.getByText('Venda')).toBeInTheDocument();
});

test('conta quitada nao exibe acoes de quitar/editar/excluir', () => {
  mocks.state = { ...baseHook(), quitadas: [QUITADA] };
  render(<Contas />);

  const linha = screen.getByText('Venda').closest('tr');
  expect(within(linha).queryByTitle('Quitar conta')).not.toBeInTheDocument();
  expect(within(linha).queryByTitle('Editar conta')).not.toBeInTheDocument();
  expect(within(linha).queryByTitle('Excluir conta')).not.toBeInTheDocument();
  expect(within(linha).getByText(/Quitada/)).toBeInTheDocument();
});

test('quitar conta pendente pede confirmacao e chama liquidarConta', async () => {
  mocks.state = { ...baseHook(), pendentes: [PENDENTE] };
  const user = userEvent.setup();
  render(<Contas />);

  await user.click(screen.getByTitle('Quitar conta'));
  expect(screen.getByText('Quitar conta?')).toBeInTheDocument();

  await user.click(screen.getByRole('button', { name: /confirmar quita/i }));
  await waitFor(() => expect(mocks.liquidarConta).toHaveBeenCalledWith(1));
});

test('excluir conta pendente: cancelar nao chama removerConta', async () => {
  mocks.state = { ...baseHook(), pendentes: [PENDENTE] };
  const user = userEvent.setup();
  render(<Contas />);

  await user.click(screen.getByTitle('Excluir conta'));
  expect(screen.getByText('Excluir conta?')).toBeInTheDocument();

  await user.click(screen.getByRole('button', { name: /^cancelar$/i }));
  expect(mocks.removerConta).not.toHaveBeenCalled();
});
