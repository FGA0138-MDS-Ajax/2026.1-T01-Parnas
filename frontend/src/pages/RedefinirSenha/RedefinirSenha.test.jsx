import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, test, expect } from 'vitest';
import { RedefinirSenha } from './RedefinirSenha';

const novaSenha = () => screen.getByPlaceholderText(/digite sua nova senha/i);
const confirmarSenha = () => screen.getByPlaceholderText(/confirme sua nova senha/i);
const botaoRedefinir = () => screen.getByRole('button', { name: /redefinir senha/i });

describe('RedefinirSenha', () => {
  test('renderiza o titulo e os campos de senha', () => {
    render(<RedefinirSenha />);

    expect(screen.getByRole('heading', { name: /redefinir senha/i })).toBeInTheDocument();
    expect(novaSenha()).toBeInTheDocument();
    expect(confirmarSenha()).toBeInTheDocument();
  });

  test('senha menor que 8 caracteres mostra erro', async () => {
    render(<RedefinirSenha />);

    await userEvent.type(novaSenha(), '123');
    await userEvent.type(confirmarSenha(), '123');
    await userEvent.click(botaoRedefinir());

    expect(await screen.findByText(/no mínimo 8 caracteres/i)).toBeInTheDocument();
  });

  test('senhas diferentes mostram erro de divergencia', async () => {
    render(<RedefinirSenha />);

    await userEvent.type(novaSenha(), 'senha12345');
    await userEvent.type(confirmarSenha(), 'outra12345');
    await userEvent.click(botaoRedefinir());

    expect(await screen.findByText(/as senhas não coincidem/i)).toBeInTheDocument();
  });

  test('senhas validas e iguais redefinem com sucesso', async () => {
    render(<RedefinirSenha />);

    await userEvent.type(novaSenha(), 'senha12345');
    await userEvent.type(confirmarSenha(), 'senha12345');
    await userEvent.click(botaoRedefinir());

    expect(
      await screen.findByText(/senha redefinida com sucesso/i, {}, { timeout: 3000 }),
    ).toBeInTheDocument();
  });
});
