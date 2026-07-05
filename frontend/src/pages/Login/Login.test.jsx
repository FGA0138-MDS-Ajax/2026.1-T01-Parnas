import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '../../context/AuthContext';
import Login from './Login';

// Espiona o redirecionamento sem perder Link/MemoryRouter reais
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => mockNavigate };
});

function renderLogin() {
  return render(
    <MemoryRouter>
      <AuthProvider>
        <Login />
      </AuthProvider>
    </MemoryRouter>,
  );
}

// Labels não estão associados aos inputs -> buscamos pelos placeholders
const campoEmail = () => screen.getByPlaceholderText('seu@email.com.br');
const campoSenha = () => screen.getByPlaceholderText('••••••••');
const botaoEntrar = () => screen.getByRole('button', { name: /^entrar$/i });

// localStorage de verdade aqui é um stub do Node (quebrado); usamos um em memória
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
  global.fetch = vi.fn();
});

test('renderiza os campos de e-mail, senha e o botao Entrar', () => {
  renderLogin();

  expect(campoEmail()).toBeInTheDocument();
  expect(campoSenha()).toBeInTheDocument();
  expect(botaoEntrar()).toBeInTheDocument();
});

test('login com sucesso salva o token e redireciona para a seleção de empresa', async () => {
  global.fetch.mockResolvedValue({
    ok: true,
    json: async () => ({ token: 'jwt-abc' }),
  });
  renderLogin();

  await userEvent.type(campoEmail(), 'teste@email.com');
  await userEvent.type(campoSenha(), 'Senha@123');
  await userEvent.click(botaoEntrar());

  await waitFor(() => {
    expect(global.fetch).toHaveBeenCalledWith(
      '/auth/login',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'teste@email.com', password: 'Senha@123' }),
      }),
    );
  });
  expect(localStorage.getItem('token')).toBe('jwt-abc');
  expect(mockNavigate).toHaveBeenCalledWith('/selecao-empresa');
});

test('credenciais invalidas exibem a mensagem de erro vinda da API', async () => {
  global.fetch.mockResolvedValue({
    ok: false,
    json: async () => ({ erro: 'E-mail ou senha inválidos' }),
  });
  renderLogin();

  await userEvent.type(campoEmail(), 'teste@email.com');
  await userEvent.type(campoSenha(), 'senha-errada');
  await userEvent.click(botaoEntrar());

  expect(await screen.findByText('E-mail ou senha inválidos')).toBeInTheDocument();
  expect(localStorage.getItem('token')).toBeNull();
  expect(mockNavigate).not.toHaveBeenCalled();
});

test('senha com menos de 8 caracteres barra antes de chamar a API', async () => {
  renderLogin();

  await userEvent.type(campoEmail(), 'teste@email.com');
  await userEvent.type(campoSenha(), '123');
  await userEvent.click(botaoEntrar());

  expect(await screen.findByText(/credenciais inválidas/i)).toBeInTheDocument();
  expect(global.fetch).not.toHaveBeenCalled();
});
