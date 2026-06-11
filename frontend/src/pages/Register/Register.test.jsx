// Testes da página de cadastro (Register).
// Roda com: npm test   (modo watch)  ou  npm run test:run  (roda uma vez).
//
// Lembre: o componente real usa `fetch` (não axios) e as <label> NÃO estão
// ligadas aos <input> (sem htmlFor/id), por isso buscamos por placeholder/name.

import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, test, expect, beforeEach, afterEach } from 'vitest';
import Register from './Register';

describe('Register', () => {
  // ---------- Teste 1: renderização simples ----------
  test('renderiza o título e o botão de cadastro', () => {
    // Arrange + Act: monta o componente no DOM falso
    render(<Register />);

    // Assert: o que o usuário vê está na tela.
    // getByRole é a busca preferida (papel do elemento + texto acessível).
    expect(screen.getByRole('heading', { name: /registre-se/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /finalizar registro/i })).toBeInTheDocument();
  });

  // ---------- Teste 2: data de nascimento no futuro ----------
  test('mostra erro quando a data de nascimento está no futuro', async () => {
    // Arrange
    render(<Register />);
    // O input de data tem onChange ligado, então conseguimos preenchê-lo.
    // Como não há label associada, pegamos pelo atributo name.
    const dataInput = document.querySelector('input[name="dataNascimento"]');

    // Act: input type="date" não aceita userEvent.type — usamos fireEvent.change
    // para setar o valor direto (formato ISO yyyy-mm-dd).
    fireEvent.change(dataInput, { target: { value: '2099-01-01' } });
    await userEvent.click(screen.getByRole('button', { name: /finalizar registro/i }));

    // Assert: a mensagem de erro aparece na tela.
    expect(screen.getByText(/data de nascimento inválida/i)).toBeInTheDocument();
  });

  // ---------- Teste 3: menor de 18 anos ----------
  test('mostra erro quando o usuário tem menos de 18 anos', async () => {
    render(<Register />);
    const dataInput = document.querySelector('input[name="dataNascimento"]');

    // Uma criança nascida há poucos anos -> idade < 18
    fireEvent.change(dataInput, { target: { value: '2015-01-01' } });
    await userEvent.click(screen.getByRole('button', { name: /finalizar registro/i }));

    expect(screen.getByText(/pelo menos 18 anos/i)).toBeInTheDocument();
  });

  // ---------- Teste 4: caminho feliz com fetch mockado ----------
  // Este teste MOCKA a rede. O componente usa `fetch`, então substituímos
  // global.fetch por uma versão falsa que devolve uma resposta de sucesso.
  describe('envio ao backend', () => {
    beforeEach(() => {
      // Arrange global: fetch falso que responde 200 OK com json vazio.
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({}),
      });
    });

    afterEach(() => {
      vi.restoreAllMocks(); // limpa o mock entre testes
    });

    // NOTE: este teste DEVE FALHAR hoje — e isso é proposital.
    // Os campos Nome e Senha no Register.jsx não têm onChange/value, então
    // formData.senha fica sempre "" e o componente barra com "senha < 8".
    // Ou seja: fetch nunca é chamado. O teste documenta o bug.
    test('chama o backend quando o formulário é válido', async () => {
      render(<Register />);

      await userEvent.type(document.querySelector('input[name="email"]'), 'daniel@gmail.com');
      await userEvent.type(document.querySelector('input[name="senha"]'), 'senha123!');
      fireEvent.change(document.querySelector('input[name="dataNascimento"]'), {
        target: { value: '2000-01-01' },
      });
      await userEvent.click(screen.getByRole('button', { name: /finalizar registro/i }));

      // Esperado SE o componente estivesse correto: fetch chamado na rota de registro.
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/register'),
        expect.objectContaining({ method: 'POST' }),
      );
    });
  });
});