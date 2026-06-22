import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, test, expect, beforeEach, afterEach } from 'vitest';
import { EsqueciSenha } from './EsqueciSenha';

// emailjs faz chamada externa; substituimos por um mock que sempre resolve.
vi.mock('@emailjs/browser', () => ({
  default: { init: vi.fn(), send: vi.fn().mockResolvedValue({}) },
}));

const campoEmail = () => screen.getByPlaceholderText('seu@email.com');
const botaoEnviar = () => screen.getByRole('button', { name: /enviar link/i });

beforeEach(() => {
  // Sem token na URL -> tela de solicitação
  window.history.pushState({}, '', '/esqueci-senha');
  global.fetch = vi.fn();
});

afterEach(() => vi.restoreAllMocks());

describe('EsqueciSenha (solicitar recuperacao)', () => {
  test('renderiza o titulo de recuperacao e o campo de e-mail', () => {
    render(<EsqueciSenha />);

    expect(screen.getByRole('heading', { name: /recuperar senha/i })).toBeInTheDocument();
    expect(campoEmail()).toBeInTheDocument();
  });

  test('erro vindo da API exibe a mensagem de falha', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      json: async () => ({ erro: 'E-mail não cadastrado' }),
    });
    render(<EsqueciSenha />);

    await userEvent.type(campoEmail(), 'teste@email.com');
    await userEvent.click(botaoEnviar());

    expect(await screen.findByText('E-mail não cadastrado')).toBeInTheDocument();
  });

  test('solicitacao bem-sucedida mostra a mensagem de envio', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        email: 'teste@email.com',
        reset_link: 'http://api/reset/token-abc',
      }),
    });
    render(<EsqueciSenha />);

    await userEvent.type(campoEmail(), 'teste@email.com');
    await userEvent.click(botaoEnviar());

    expect(await screen.findByText(/e-mail de recuperação enviado com sucesso/i)).toBeInTheDocument();
  });
});

describe('EsqueciSenha (redefinir com token na URL)', () => {
  beforeEach(() => {
    window.history.pushState({}, '', '/esqueci-senha?token=token-abc');
  });

  test('com token na URL exibe o formulario de nova senha', async () => {
    render(<EsqueciSenha />);

    expect(await screen.findByRole('heading', { name: /nova senha/i })).toBeInTheDocument();
  });

  test('senha menor que 8 caracteres barra antes de chamar a API', async () => {
    render(<EsqueciSenha />);

    const campos = await screen.findAllByPlaceholderText('••••••••');
    await userEvent.type(campos[0], '123');
    await userEvent.type(campos[1], '123');
    await userEvent.click(screen.getByRole('button', { name: /alterar senha/i }));

    expect(await screen.findByText(/no mínimo 8 caracteres/i)).toBeInTheDocument();
    expect(global.fetch).not.toHaveBeenCalled();
  });

  test('senhas diferentes nao chamam a API', async () => {
    render(<EsqueciSenha />);

    const campos = await screen.findAllByPlaceholderText('••••••••');
    await userEvent.type(campos[0], 'senha12345');
    await userEvent.type(campos[1], 'outra12345');
    await userEvent.click(screen.getByRole('button', { name: /alterar senha/i }));

    expect(await screen.findByText(/as senhas não coincidem/i)).toBeInTheDocument();
    expect(global.fetch).not.toHaveBeenCalled();
  });
});
