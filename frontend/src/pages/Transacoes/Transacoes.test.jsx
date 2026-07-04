// daniel: a pagina passou a depender do hook useTransacoes (orientado a API). Mocko o hook
// com dados controlados e valido a renderizacao (cartoes, contagem) e os handlers de filtro.
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, beforeEach, test, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Transacoes from './Transacoes';
import useTransacoes from '../../hooks/useTransacoes';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

vi.mock('../../hooks/useTransacoes', () => ({ default: vi.fn() }));

const aplicarFiltros = vi.fn();
const limparFiltros = vi.fn();

function hookState(over = {}) {
  return {
    filtros: { dataInicio: '', dataFim: '', tipo: '', categoria: '', contaCaixaId: '', valorMin: '', valorMax: '' },
    transacoes: [],
    totais: { totalReceitas: 15800, totalDespesas: 10100, saldo: 5700 },
    saldoContaSelecionada: null,
    contaCaixaSelecionada: null,
    paginaAtual: 1,
    totalPaginas: 3,
    totalTransacoes: 12,
    categorias: [],
    contasCaixa: [],
    handleFiltroChange: vi.fn(),
    aplicarFiltros,
    limparFiltros,
    mudarPagina: vi.fn(),
    salvarTransacao: vi.fn(),
    excluirTransacao: vi.fn(),
    ...over,
  };
}

beforeEach(() => {
  vi.clearAllMocks();
  useTransacoes.mockReturnValue(hookState());
});

function renderPagina() {
  return render(
    <MemoryRouter>
      <Transacoes />
    </MemoryRouter>,
  );
}

test('exibe os cartoes de totais no topo', () => {
  renderPagina();

  expect(screen.getByText(/total de receitas/i)).toBeInTheDocument();
  expect(screen.getByText(/total de despesas/i)).toBeInTheDocument();
  expect(screen.getByText('Saldo')).toBeInTheDocument();
});

test('mostra a contagem de transacoes vinda do hook', () => {
  renderPagina();

  expect(screen.getByText(/12 transação\(ões\) encontrada/i)).toBeInTheDocument();
});

test('aplicar e limpar filtros chamam os handlers do hook', async () => {
  renderPagina();

  await userEvent.click(screen.getByRole('button', { name: /aplicar filtros/i }));
  expect(aplicarFiltros).toHaveBeenCalled();

  await userEvent.click(screen.getByRole('button', { name: /limpar filtros/i }));
  expect(limparFiltros).toHaveBeenCalled();
});
