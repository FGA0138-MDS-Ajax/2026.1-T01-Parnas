import { describe, test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ContasCaixa from './ContasCaixa';

function renderContasCaixa() {
  render(
    <MemoryRouter>
      <ContasCaixa />
    </MemoryRouter>,
  );
}

const campoNome = () => screen.getByPlaceholderText(/inter, caixa vendas/i);

describe('ContasCaixa', () => {
  test('renderiza o cabecalho e as contas/caixas iniciais', () => {
    renderContasCaixa();
    expect(screen.getByRole('heading', { name: /contas\/caixas/i })).toBeInTheDocument();
    expect(screen.getByText('Inter')).toBeInTheDocument();
    expect(screen.getByText('Caixa Vendas')).toBeInTheDocument();
  });

  test('adiciona uma nova conta/caixa pelo formulario', async () => {
    renderContasCaixa();

    await userEvent.type(campoNome(), 'Nubank');
    await userEvent.click(screen.getByRole('button', { name: /adicionar/i }));

    expect(screen.getByText('Nubank')).toBeInTheDocument();
    expect(campoNome()).toHaveValue('');
  });

  test('nao adiciona quando o nome esta vazio ou so com espacos', async () => {
    renderContasCaixa();
    const linhasAntes = screen.getAllByRole('row').length;

    await userEvent.type(campoNome(), '   ');
    await userEvent.click(screen.getByRole('button', { name: /adicionar/i }));

    expect(screen.getAllByRole('row')).toHaveLength(linhasAntes);
  });
});
