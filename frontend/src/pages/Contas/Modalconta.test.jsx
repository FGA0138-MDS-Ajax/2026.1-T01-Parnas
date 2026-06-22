import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ModalConta from './Modalconta';

const categorias = [
  { id: 1, nome: 'Vendas', tipo: 'receita' },
  { id: 3, nome: 'Infraestrutura', tipo: 'despesa' },
];
const contasCaixa = [
  { id: 1, nome: 'Inter' },
  { id: 2, nome: 'Caixa Vendas' },
];

function renderModal(props = {}) {
  const onSalvar = vi.fn().mockResolvedValue(undefined);
  const onFechar = vi.fn();
  render(
    <MemoryRouter>
      <ModalConta
        contaParaEditar={null}
        categorias={categorias}
        contasCaixa={contasCaixa}
        onSalvar={onSalvar}
        onFechar={onFechar}
        {...props}
      />
    </MemoryRouter>,
  );
  return { onSalvar, onFechar };
}

describe('ModalConta', () => {
  test('renderiza o titulo de nova conta', () => {
    renderModal();
    expect(screen.getByRole('heading', { name: /nova conta/i })).toBeInTheDocument();
  });

  test('submeter vazio mostra erros e nao chama onSalvar', async () => {
    const { onSalvar } = renderModal();

    await userEvent.click(screen.getByRole('button', { name: /cadastrar conta/i }));

    expect(await screen.findByText(/descrição é obrigatória/i)).toBeInTheDocument();
    expect(screen.getByText(/informe um valor válido/i)).toBeInTheDocument();
    // texto exato: a opção do select é "Selecione uma Conta/Caixa..." (com reticências)
    expect(screen.getByText('Selecione uma Conta/Caixa.')).toBeInTheDocument();
    expect(onSalvar).not.toHaveBeenCalled();
  });

  test('preenchido corretamente chama onSalvar com os dados', async () => {
    const { onSalvar } = renderModal();

    await userEvent.type(screen.getByLabelText('Descrição'), 'Aluguel');
    await userEvent.type(screen.getByLabelText(/valor/i), '1500');
    fireEvent.change(screen.getByLabelText(/data de vencimento/i), {
      target: { value: '2026-07-10' },
    });
    await userEvent.selectOptions(screen.getByLabelText('Conta/Caixa'), '1');

    await userEvent.click(screen.getByRole('button', { name: /cadastrar conta/i }));

    expect(onSalvar).toHaveBeenCalledWith(
      expect.objectContaining({
        descricao: 'Aluguel',
        valor: '1500',
        contaCaixaId: '1',
        dataVencimento: '2026-07-10',
      }),
    );
  });

  test('clicar em fechar dispara onFechar', async () => {
    const { onFechar } = renderModal();
    await userEvent.click(screen.getByRole('button', { name: /fechar modal/i }));
    expect(onFechar).toHaveBeenCalled();
  });
});
