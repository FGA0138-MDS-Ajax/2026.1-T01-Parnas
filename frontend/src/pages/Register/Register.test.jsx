import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, test, expect, beforeEach, afterEach } from 'vitest';
import Register from './Register';

// Particularidades do componente:
//  <label> não está ligada ao <input> (sem htmlFor/id) -> buscamos pelo placeholder/name.
//  <button type="submit"> + campos `required` -> preencher obrigatórios pra submeter.
//  <input type="date"> não aceita userEvent.type -> usar fireEvent.change.

// Todos os campos (inclusive CPF) são `required`; sem preencher, o jsdom
// bloqueia o submit por validação nativa e o handler nem roda.
async function preencherObrigatorios(user) {
  await user.type(screen.getByPlaceholderText(/seu nome completo/i), 'Daniel');
  await user.type(screen.getByPlaceholderText(/nome@email\.com/i), 'daniel@gmail.com');
  await user.type(screen.getByPlaceholderText(/000\.000\.000-00/), '123.456.789-00');
  await user.type(screen.getByPlaceholderText(/no mínimo 8 caracteres/i), 'senha123!');
}

function preencherData(valor) {
  fireEvent.change(document.querySelector('input[name="dataNascimento"]'), {
    target: { value: valor },
  });
}

const clicarEnviar = (user) =>
  user.click(screen.getByRole('button', { name: /finalizar registro/i }));

describe('Register (cadastro de usuário)', () => {
  test('renderiza o titulo e o botao de cadastro', () => {
    render(<Register />);
    expect(screen.getByRole('heading', { name: /registre-se/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /finalizar registro/i })).toBeInTheDocument();
  });

  test('mostra erro quando a data de nascimento esta no futuro', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await preencherObrigatorios(user);
    preencherData('2099-01-01');
    await clicarEnviar(user);

    expect(await screen.findByText(/data de nascimento inválida/i)).toBeInTheDocument();
  });

  test('mostra erro quando o usuario tem menos de 16 anos', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await preencherObrigatorios(user);
    preencherData('2015-01-01');
    await clicarEnviar(user);

    expect(await screen.findByText(/pelo menos 16 anos/i)).toBeInTheDocument();
  });

  test('mostra erro quando a senha tem menos de 8 caracteres', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await user.type(screen.getByPlaceholderText(/seu nome completo/i), 'Daniel');
    await user.type(screen.getByPlaceholderText(/nome@email\.com/i), 'daniel@gmail.com');
    await user.type(screen.getByPlaceholderText(/000\.000\.000-00/), '123.456.789-00');
    await user.type(screen.getByPlaceholderText(/no mínimo 8 caracteres/i), '123');
    preencherData('2000-01-01');
    await clicarEnviar(user);

    expect(await screen.findByText(/sua senha deve ter no mínimo 8 caracteres/i)).toBeInTheDocument();
  });

  test('nao acusa erro de data/idade para um adulto', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await preencherObrigatorios(user);
    preencherData('2000-01-01');
    await clicarEnviar(user);

    expect(screen.queryByText(/data de nascimento inválida/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/pelo menos 16 anos/i)).not.toBeInTheDocument();
  });

  describe('envio ao backend', () => {
    beforeEach(() => {
      global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) });
    });
    afterEach(() => vi.restoreAllMocks());

    test('chama POST /api/register com o CPF limpo quando o formulario e valido', async () => {
      const user = userEvent.setup();
      render(<Register />);

      await preencherObrigatorios(user);
      preencherData('2000-01-01');
      await clicarEnviar(user);

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/register'),
        expect.objectContaining({
          method: 'POST',
          body: expect.stringContaining('"cpf":"12345678900"'),
        }),
      );
    });
  });
});
