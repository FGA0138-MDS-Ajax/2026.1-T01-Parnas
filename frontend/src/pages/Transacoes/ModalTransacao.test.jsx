import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ModalTransacao from './ModalTransacao';

// categorias sem tipo aparecem para qualquer tipo (como o Transacoes.jsx as monta)
const categorias = [
  { id: 1, nome: 'Vendas', tipo: '' },
  { id: 2, nome: 'Servicos', tipo: '' },
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
      <ModalTransacao
        transacaoParaEditar={null}
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

describe('ModalTransacao', () => {
  test('renderiza o titulo de nova transacao', () => {
    renderModal();
    expect(screen.getByRole('heading', { name: /nova transação/i })).toBeInTheDocument();
  });

  test('movimentacao vazia mostra erros e nao salva', async () => {
    const { onSalvar } = renderModal();

    await userEvent.click(screen.getByRole('button', { name: /registrar transação/i }));

    expect(await screen.findByText(/a descrição é obrigatória/i)).toBeInTheDocument();
    expect(screen.getByText(/informe um valor válido/i)).toBeInTheDocument();
    expect(onSalvar).not.toHaveBeenCalled();
  });

  test('movimentacao valida chama onSalvar convertendo valor e categoria', async () => {
    const { onSalvar } = renderModal();

    await userEvent.type(screen.getByLabelText('Descrição'), 'Venda do dia');
    await userEvent.type(screen.getByLabelText(/valor/i), '250.5');
    await userEvent.selectOptions(screen.getByLabelText('Conta/Caixa'), '1');
    await userEvent.selectOptions(screen.getByLabelText('Categoria'), '1');

    await userEvent.click(screen.getByRole('button', { name: /registrar transação/i }));

    expect(onSalvar).toHaveBeenCalledWith(
      expect.objectContaining({ descricao: 'Venda do dia', valor: 250.5, categoriaId: 1 }),
    );
  });

  test('data futura é barrada', async () => {
    const { onSalvar } = renderModal();

    await userEvent.type(screen.getByLabelText('Descrição'), 'Venda');
    await userEvent.type(screen.getByLabelText(/valor/i), '100');
    await userEvent.selectOptions(screen.getByLabelText('Conta/Caixa'), '1');
    await userEvent.selectOptions(screen.getByLabelText('Categoria'), '1');
    fireEvent.change(screen.getByLabelText('Data'), { target: { value: '2099-01-01' } });

    await userEvent.click(screen.getByRole('button', { name: /registrar transação/i }));

    expect(await screen.findByText(/a data não pode ser futura/i)).toBeInTheDocument();
    expect(onSalvar).not.toHaveBeenCalled();
  });

  test('transferencia com origem igual a destino acusa erro', async () => {
    const { onSalvar } = renderModal();

    await userEvent.click(screen.getByRole('button', { name: /transferência/i }));

    await userEvent.type(screen.getByLabelText(/valor/i), '300');
    await userEvent.selectOptions(screen.getByLabelText(/conta\/caixa de origem/i), '1');
    await userEvent.selectOptions(screen.getByLabelText(/conta\/caixa de destino/i), '1');

    await userEvent.click(screen.getByRole('button', { name: /registrar transferência/i }));

    expect(await screen.findByText(/origem e destino devem ser diferentes/i)).toBeInTheDocument();
    expect(onSalvar).not.toHaveBeenCalled();
  });
});
