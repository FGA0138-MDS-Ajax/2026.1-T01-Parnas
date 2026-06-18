import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import ModalTransacao from './ModalTransacao';

// o modal usa useNavigate (botão "Cadastrar" categoria)
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return { ...actual, useNavigate: () => vi.fn() };
});

const CATEGORIAS = [
  { id: 1, nome: 'Vendas', tipo: 'receita' },
  { id: 2, nome: 'Aluguel', tipo: 'despesa' },
];

const hoje = () => new Date().toISOString().split('T')[0];

function renderModal(props = {}) {
  const onSalvar = vi.fn().mockResolvedValue(undefined);
  const onFechar = vi.fn();
  render(
    <MemoryRouter>
      <ModalTransacao
        categorias={CATEGORIAS}
        onSalvar={onSalvar}
        onFechar={onFechar}
        {...props}
      />
    </MemoryRouter>,
  );
  return { onSalvar, onFechar };
}

const campoDescricao = () => screen.getByLabelText(/descrição/i);
const campoValor = () => screen.getByLabelText(/valor/i);
const campoData = () => screen.getByLabelText(/data/i);
const campoCategoria = () => screen.getByLabelText(/categoria/i);
const botaoRegistrar = () => screen.getByRole('button', { name: /registrar transação/i });

test('exibe titulo de nova transacao quando nao ha edicao', () => {
  // Act
  renderModal();

  // Assert
  expect(screen.getByText('Nova Transação')).toBeInTheDocument();
});

test('exibe titulo de edicao quando recebe transacao para editar', () => {
  // Act
  renderModal({
    transacaoParaEditar: { descricao: 'Venda', valor: 100, tipo: 'receita', data: hoje(), categoriaId: 1 },
  });

  // Assert
  expect(screen.getByText('Editar Transação')).toBeInTheDocument();
});

test('submete transacao valida chamando onSalvar com os dados convertidos', async () => {
  const { onSalvar } = renderModal();

  await userEvent.type(campoDescricao(), 'Venda do dia');
  await userEvent.type(campoValor(), '150.50');
  await userEvent.selectOptions(campoCategoria(), '1');

  // Act
  await userEvent.click(botaoRegistrar());

  // Assert: valor vira number e categoriaId vira number
  expect(onSalvar).toHaveBeenCalledTimes(1);
  expect(onSalvar).toHaveBeenCalledWith(
    expect.objectContaining({ descricao: 'Venda do dia', valor: 150.5, categoriaId: 1, tipo: 'receita' }),
  );
});

test('valor negativo bloqueia o envio e mostra erro', async () => {
  const { onSalvar } = renderModal();

  await userEvent.type(campoDescricao(), 'Venda');
  await userEvent.type(campoValor(), '-5');
  await userEvent.selectOptions(campoCategoria(), '1');

  // Act
  await userEvent.click(botaoRegistrar());

  // Assert
  expect(screen.getByText(/o valor deve ser positivo/i)).toBeInTheDocument();
  expect(onSalvar).not.toHaveBeenCalled();
});

test('data futura bloqueia o envio e mostra erro', async () => {
  const { onSalvar } = renderModal();
  const amanha = new Date(Date.now() + 86400000).toISOString().split('T')[0];

  await userEvent.type(campoDescricao(), 'Venda');
  await userEvent.type(campoValor(), '100');
  await userEvent.selectOptions(campoCategoria(), '1');
  // input date tem max=hoje; setamos o valor futuro diretamente
  fireEvent.change(campoData(), { target: { value: amanha } });

  // Act
  await userEvent.click(botaoRegistrar());

  // Assert
  expect(screen.getByText(/a data não pode ser futura/i)).toBeInTheDocument();
  expect(onSalvar).not.toHaveBeenCalled();
});

test('categoria obrigatoria bloqueia o envio', async () => {
  const { onSalvar } = renderModal();

  await userEvent.type(campoDescricao(), 'Venda');
  await userEvent.type(campoValor(), '100');

  // Act: sem selecionar categoria
  await userEvent.click(botaoRegistrar());

  // Assert: a mensagem de erro (não confundir com o placeholder "Selecione uma categoria...")
  expect(screen.getByText('Selecione uma categoria.')).toBeInTheDocument();
  expect(onSalvar).not.toHaveBeenCalled();
});

test('select de categoria mostra apenas as do tipo selecionado', () => {
  // Act: tipo inicial é receita
  renderModal();

  // Assert: só "Vendas" (receita) aparece; "Aluguel" (despesa) não
  expect(screen.getByRole('option', { name: 'Vendas' })).toBeInTheDocument();
  expect(screen.queryByRole('option', { name: 'Aluguel' })).not.toBeInTheDocument();
});

test('botao cancelar chama onFechar', async () => {
  const { onFechar } = renderModal();

  // Act
  await userEvent.click(screen.getByRole('button', { name: /cancelar/i }));

  // Assert
  expect(onFechar).toHaveBeenCalledTimes(1);
});
