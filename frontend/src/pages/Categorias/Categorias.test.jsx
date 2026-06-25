import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import Categorias from './Categorias';

const novaCategoria = () => screen.getByPlaceholderText(/nome da categoria/i);
const botaoAdicionar = () => screen.getByRole('button', { name: /adicionar categoria/i });
const linhaPorTexto = (texto) => screen.getByText(texto).closest('tr');

test('lista as categorias iniciais', () => {
  render(<Categorias />);

  expect(screen.getByText('Salário')).toBeInTheDocument();
  expect(screen.getByText('Alimentação')).toBeInTheDocument();
});

test('adiciona uma nova categoria pelo formulario', async () => {
  render(<Categorias />);

  await userEvent.type(novaCategoria(), 'Transporte');
  await userEvent.click(botaoAdicionar());

  expect(screen.getByText('Transporte')).toBeInTheDocument();
});

test('formulario limpa o nome apos adicionar', async () => {
  render(<Categorias />);

  await userEvent.type(novaCategoria(), 'Transporte');
  await userEvent.click(botaoAdicionar());

  expect(novaCategoria()).toHaveValue('');
});

test('edita o nome de uma categoria existente inline', async () => {
  render(<Categorias />);

  const linha = linhaPorTexto('Salário');
  await userEvent.click(within(linha).getByRole('button', { name: /editar/i }));
  const input = within(linha).getByRole('textbox');
  await userEvent.clear(input);
  await userEvent.type(input, 'Salário Mensal');
  await userEvent.click(within(linha).getByRole('button', { name: /salvar/i }));

  expect(screen.getByText('Salário Mensal')).toBeInTheDocument();
  expect(screen.queryByText('Salário')).not.toBeInTheDocument();
});

test('cancelar edicao mantem o nome original', async () => {
  render(<Categorias />);

  const linha = linhaPorTexto('Salário');
  await userEvent.click(within(linha).getByRole('button', { name: /editar/i }));
  const input = within(linha).getByRole('textbox');
  await userEvent.clear(input);
  await userEvent.type(input, 'Outro Nome');
  await userEvent.click(within(linha).getByRole('button', { name: /cancelar/i }));

  expect(screen.getByText('Salário')).toBeInTheDocument();
  expect(screen.queryByText('Outro Nome')).not.toBeInTheDocument();
});

test('exclui a categoria quando o usuario confirma', async () => {
  vi.spyOn(window, 'confirm').mockReturnValue(true);
  render(<Categorias />);

  const linha = linhaPorTexto('Alimentação');
  await userEvent.click(within(linha).getByRole('button', { name: /excluir/i }));

  expect(screen.queryByText('Alimentação')).not.toBeInTheDocument();
  window.confirm.mockRestore();
});

test('mantem a categoria quando o usuario cancela a exclusao', async () => {
  vi.spyOn(window, 'confirm').mockReturnValue(false);
  render(<Categorias />);

  const linha = linhaPorTexto('Alimentação');
  await userEvent.click(within(linha).getByRole('button', { name: /excluir/i }));

  expect(screen.getByText('Alimentação')).toBeInTheDocument();
  window.confirm.mockRestore();
});
