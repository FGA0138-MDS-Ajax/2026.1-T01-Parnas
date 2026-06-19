import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '../../context/AuthContext';
import Configuracoes from './Configuracoes';

// Espiona o redirecionamento sem perder o restante do react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

function renderConfiguracoes() {
  return render(
    <MemoryRouter>
      <AuthProvider>
        <Configuracoes />
      </AuthProvider>
    </MemoryRouter>,
  );
}

const botaoExcluirEmpresa = () => screen.getByRole('button', { name: /excluir empresa/i });
const botaoExcluirConta = () => screen.getByRole('button', { name: /excluir conta/i });
const botaoConfirmar = () => screen.getByRole('button', { name: /confirmar e excluir/i });

// localStorage de verdade no Node é um stub quebrado; usamos um em memória
function criarLocalStorageMock() {
  let loja = {};
  return {
    getItem: (k) => (k in loja ? loja[k] : null),
    setItem: (k, v) => { loja[k] = String(v); },
    removeItem: (k) => { delete loja[k]; },
    clear: () => { loja = {}; },
  };
}

beforeEach(() => {
  vi.stubGlobal('localStorage', criarLocalStorageMock());
  mockNavigate.mockReset();
});

test('renderiza as ações de excluir empresa e excluir conta', () => {
  // Arrange / Act
  renderConfiguracoes();

  // Assert
  expect(botaoExcluirEmpresa()).toBeInTheDocument();
  expect(botaoExcluirConta()).toBeInTheDocument();
});

test('abrir exclusão de empresa mostra o aviso específico de empresa', async () => {
  // Arrange
  const user = userEvent.setup();
  renderConfiguracoes();

  // Act
  await user.click(botaoExcluirEmpresa());

  // Assert
  expect(screen.getByText('Confirmar Exclusão')).toBeInTheDocument();
  expect(screen.getByText(/históricos de crédito/i)).toBeInTheDocument();
});

test('abrir exclusão de conta mostra o aviso específico de usuário', async () => {
  // Arrange
  const user = userEvent.setup();
  renderConfiguracoes();

  // Act
  await user.click(botaoExcluirConta());

  // Assert
  expect(screen.getByText(/perderá o acesso à plataforma/i)).toBeInTheDocument();
});

test('cancelar fecha o modal de confirmação', async () => {
  // Arrange
  const user = userEvent.setup();
  renderConfiguracoes();
  await user.click(botaoExcluirEmpresa());

  // Act
  await user.click(screen.getByRole('button', { name: /cancelar/i }));

  // Assert
  expect(screen.queryByText('Confirmar Exclusão')).not.toBeInTheDocument();
});

test('clicar fora do modal (overlay) fecha a confirmação', async () => {
  // Arrange
  const user = userEvent.setup();
  const { container } = renderConfiguracoes();
  await user.click(botaoExcluirConta());

  // Act
  await user.click(container.querySelector('.modal-overlay'));

  // Assert
  expect(screen.queryByText('Confirmar Exclusão')).not.toBeInTheDocument();
});

test('confirmar exclusão de conta redireciona para o login', async () => {
  // Arrange
  const user = userEvent.setup();
  renderConfiguracoes();
  await user.click(botaoExcluirConta());

  // Act
  await user.click(botaoConfirmar());

  // Assert
  expect(mockNavigate).toHaveBeenCalledWith('/login', { replace: true });
  expect(screen.queryByText('Confirmar Exclusão')).not.toBeInTheDocument();
});

test('confirmar exclusão de empresa fecha o modal sem redirecionar', async () => {
  // Arrange
  const user = userEvent.setup();
  renderConfiguracoes();
  await user.click(botaoExcluirEmpresa());

  // Act
  await user.click(botaoConfirmar());

  // Assert
  expect(screen.queryByText('Confirmar Exclusão')).not.toBeInTheDocument();
  expect(mockNavigate).not.toHaveBeenCalled();
});
