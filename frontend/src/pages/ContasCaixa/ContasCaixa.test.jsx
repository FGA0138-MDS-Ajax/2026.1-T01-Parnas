// daniel: a pagina passou a carregar as contas/caixas da API (contaCaixa.service); reescrevi
// os testes para mockar o service e validar a renderizacao/criacao orientada ao backend.
import { describe, test, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ContasCaixa from './ContasCaixa';
import { listarContasCaixa, criarContaCaixa } from '../../services/contaCaixa.service';

vi.mock('../../services/contaCaixa.service', () => ({
  listarContasCaixa: vi.fn(),
  criarContaCaixa: vi.fn(),
  excluirContaCaixa: vi.fn(),
}));

function renderContasCaixa() {
  render(
    <MemoryRouter>
      <ContasCaixa />
    </MemoryRouter>,
  );
}

const campoNome = () => screen.getByPlaceholderText(/inter, caixa vendas/i);

beforeEach(() => {
  vi.clearAllMocks();
  listarContasCaixa.mockResolvedValue([
    { id: 1, nome: 'Inter' },
    { id: 2, nome: 'Caixa Vendas' },
  ]);
});

describe('ContasCaixa', () => {
  test('renderiza o cabecalho e as contas/caixas vindas da API', async () => {
    renderContasCaixa();
    expect(screen.getByRole('heading', { name: /contas\/caixas/i })).toBeInTheDocument();
    expect(await screen.findByText('Inter')).toBeInTheDocument();
    expect(screen.getByText('Caixa Vendas')).toBeInTheDocument();
  });

  test('adiciona uma nova conta/caixa pelo formulario', async () => {
    criarContaCaixa.mockResolvedValue({ id: 3, nome: 'Nubank' });
    renderContasCaixa();
    await screen.findByText('Inter');

    await userEvent.type(campoNome(), 'Nubank');
    await userEvent.click(screen.getByRole('button', { name: /adicionar/i }));

    expect(await screen.findByText('Nubank')).toBeInTheDocument();
    expect(criarContaCaixa).toHaveBeenCalledWith('Nubank');
    expect(campoNome()).toHaveValue('');
  });

  test('nao cria quando o nome esta vazio ou so com espacos', async () => {
    renderContasCaixa();
    await screen.findByText('Inter');

    await userEvent.type(campoNome(), '   ');
    await userEvent.click(screen.getByRole('button', { name: /adicionar/i }));

    expect(criarContaCaixa).not.toHaveBeenCalled();
  });
});
