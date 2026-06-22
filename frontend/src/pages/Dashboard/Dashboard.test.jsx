import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, test, expect, beforeEach } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Dashboard from './Dashboard';

// Espiona o redirecionamento sem perder MemoryRouter real
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

function criarLocalStorageMock() {
  let loja = {};
  return {
    getItem: (k) => (k in loja ? loja[k] : null),
    setItem: (k, v) => { loja[k] = String(v); },
    removeItem: (k) => { delete loja[k]; },
    clear: () => { loja = {}; },
  };
}

function renderDashboard() {
  return render(
    <MemoryRouter>
      <Dashboard />
    </MemoryRouter>,
  );
}

beforeEach(() => {
  vi.stubGlobal('localStorage', criarLocalStorageMock());
  mockNavigate.mockReset();
});

describe('Dashboard', () => {
  test('renderiza o painel e o card de gerenciamento de empresas', () => {
    renderDashboard();

    expect(screen.getByRole('heading', { name: /painel de controle/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /gerenciamento de empresas/i })).toBeInTheDocument();
  });

  test('botao de cadastro leva para a rota de cadastro de empresa', async () => {
    renderDashboard();

    await userEvent.click(screen.getByRole('button', { name: /acessar cadastro/i }));

    expect(mockNavigate).toHaveBeenCalledWith('/cadastro-empresa');
  });

  test('nao mostra a secao de empresas quando nao ha empresas cadastradas', () => {
    renderDashboard();

    expect(screen.queryByText(/empresas cadastradas/i)).not.toBeInTheDocument();
  });

  test('lista as empresas guardadas no localStorage', () => {
    localStorage.setItem(
      'credifab_empresas_reais',
      JSON.stringify([
        { company_id: 7, name: 'Acme LTDA', cnpj: '00.000.000/0001-00', email: 'acme@email.com', phone: '6133334444' },
      ]),
    );
    renderDashboard();

    expect(screen.getByText('Acme LTDA')).toBeInTheDocument();
    expect(screen.getByText('Acme LTDA').closest('.dashboard-empresa-row')).toHaveTextContent('00.000.000/0001-00');
  });
});
