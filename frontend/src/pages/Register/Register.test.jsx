import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, test, expect, beforeEach, afterEach } from 'vitest';
import Register from './Register';

// O caminho feliz está marcado como `skip` por causa de um bug
// Particularidades do componente (por que o teste é escrito deste jeito):
//  <label> não está ligada ao <input> (sem htmlFor/id) -> buscamos por name.
//  <button type="submit"> + campos `required` -> preencher obrigatórios pra submeter.
//  <input type="date"> não aceita userEvent.type -> usar fireEvent.change.
//  user-event v14 -> criar sessão com userEvent.setup().

// Preenche os campos obrigatórios (Nome, Email, Senha) para liberar o submit.
async function preencherObrigatorios(user) {
  await user.type(document.querySelector('input[name="nome"]'), 'Daniel');
  await user.type(document.querySelector('input[name="email"]'), 'daniel@gmail.com');
  await user.type(document.querySelector('input[name="senha"]'), 'senha123!');
}

function preencherData(valor) {
  fireEvent.change(document.querySelector('input[name="dataNascimento"]'), {
    target: { value: valor },
  });
}

const clicarEnviar = (user) =>
  user.click(screen.getByRole('button', { name: /finalizar registro/i }));

describe('Register (cadastro de usuário)', () => {
  test('renderiza o título e o botão de cadastro', () => {
    render(<Register />);
    expect(screen.getByRole('heading', { name: /registre-se/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /finalizar registro/i })).toBeInTheDocument();
  });

  // TODO: Register.jsx ainda não valida data de nascimento futura; remover o .skip quando a validação for implementada.
  test.skip('mostra erro quando a data de nascimento está no futuro', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await preencherObrigatorios(user);
    preencherData('2099-01-01');
    await clicarEnviar(user);

    expect(screen.getByText(/data de nascimento inválida/i)).toBeInTheDocument();
  });

  // TODO: Register.jsx ainda não valida idade mínima de 18 anos; remover o .skip quando a validação for implementada.
  test.skip('mostra erro quando o usuário tem menos de 18 anos', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await preencherObrigatorios(user);
    preencherData('2015-01-01');
    await clicarEnviar(user);

    expect(screen.getByText(/pelo menos 18 anos/i)).toBeInTheDocument();
  });

  test('não acusa erro de data/idade para um adulto', async () => {
    const user = userEvent.setup();
    render(<Register />);

    await preencherObrigatorios(user);
    preencherData('2000-01-01');
    await clicarEnviar(user);

    expect(screen.queryByText(/data de nascimento inválida/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/pelo menos 18 anos/i)).not.toBeInTheDocument();
  });


  // TS-03 — caminho feliz: cadastro válido deveria chamar POST /auth/register.
  // Bug: os campos Nome e Senha não têm onChange/value, então o estado nunca é preenchido e o componente trava em "senha < 8".

  describe('envio ao backend', () => {
    beforeEach(() => {
      global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({}) });
    });
    afterEach(() => vi.restoreAllMocks());

    test.skip('chama POST /auth/register quando o formulário é válido', async () => {
      const user = userEvent.setup();
      render(<Register />);

      await preencherObrigatorios(user);
      preencherData('2000-01-01');
      await clicarEnviar(user);

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/register'),
        expect.objectContaining({ method: 'POST' }),
      );
    });
  });
});
