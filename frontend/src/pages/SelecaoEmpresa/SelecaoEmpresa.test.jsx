import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, expect, test, vi } from 'vitest';
import SelecaoEmpresa from './SelecaoEmpresa';

const mockNavigate = vi.fn();

vi.mock('react-router-dom', async (importOriginal) => {
  const original = await importOriginal();
  return {
    ...original,
    useNavigate: () => mockNavigate,
  };
});

vi.mock('../../context/EmpresaContext', () => ({
  useEmpresa: () => ({
    empresas: [],
    empresaAtiva: null,
    carregandoEmpresas: false,
    erroEmpresas: '',
    selecionarEmpresa: vi.fn(),
    recarregarEmpresas: vi.fn(),
  }),
}));

beforeEach(() => {
  mockNavigate.mockReset();
});

test('encaminha para o cadastro quando não existem empresas vinculadas', async () => {
  render(
    <MemoryRouter>
      <SelecaoEmpresa />
    </MemoryRouter>,
  );

  expect(screen.getByText('Nenhuma empresa vinculada')).toBeInTheDocument();

  await userEvent.click(
    screen.getByRole('button', { name: 'Cadastrar empresa' }),
  );

  expect(mockNavigate).toHaveBeenCalledWith('/cadastro-empresa');
});
