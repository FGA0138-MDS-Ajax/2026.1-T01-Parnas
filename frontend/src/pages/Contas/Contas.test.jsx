import { describe, test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Contas from './Contas';

function renderContas() {
  render(
    <MemoryRouter>
      <Contas />
    </MemoryRouter>,
  );
}

describe('Contas (pagina)', () => {
  test('renderiza o cabecalho da pagina', () => {
    renderContas();
    expect(
      screen.getByRole('heading', { name: /contas a pagar e a receber/i }),
    ).toBeInTheDocument();
  });

  test('apos carregar, lista as secoes e uma conta conhecida', async () => {
    renderContas();

    // o hook simula 400ms de carregamento antes de exibir as tabelas
    expect(
      await screen.findByText('Aluguel do escritório', {}, { timeout: 2000 }),
    ).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /pendentes/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /quitadas/i })).toBeInTheDocument();
  });
});
