import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import Categorias from './Categorias';

const novaCategoria = () => screen.getByPlaceholderText(/nome da categoria/i);
const botaoAdicionar = () => screen.getByRole('button', { name: /adicionar categoria/i });
const linhaPorTexto = (texto) => screen.getByText(texto).closest('tr');

test('lista as categorias iniciais', () => {
  // Act
  render(<Categorias />);

  // Assert: as duas categorias do estado inicial aparecem
  expect(screen.getByText('Salário')).toBeInTheDocument();
  expect(screen.getByText('Alimentação')).toBeInTheDocument();
});

test('adiciona uma nova categoria pelo formulario', async () => {
  render(<Categorias />);

  // Act
  await userEvent.type(novaCategoria(), 'Transporte');
  await userEvent.click(botaoAdicionar());

  // Assert
  expect(screen.getByText('Transporte')).toBeInTheDocument();
});

test('formulario limpa o nome apos adicionar', async () => {
  render(<Categorias />);

  // Act
  await userEvent.type(novaCategoria(), 'Transporte');
  await userEvent.click(botaoAdicionar());

  // Assert
  expect(novaCategoria()).toHaveValue('');
});

test('edita o nome de uma categoria existente inline', async () => {
  render(<Categorias />);

  // Act: abre a edição da linha 'Salário' e troca o nome
  const linha = linhaPorTexto('Salário');
  await userEvent.click(within(linha).getByRole('button', { name: /editar/i }));
  const input = within(linha).getByRole('textbox');
  await userEvent.clear(input);
  await userEvent.type(input, 'Salário Mensal');
  await userEvent.click(within(linha).getByRole('button', { name: /salvar/i }));

  // Assert
  expect(screen.getByText('Salário Mensal')).toBeInTheDocument();
  expect(screen.queryByText('Salário')).not.toBeInTheDocument();
});

test('cancelar edicao mantem o nome original', async () => {
  render(<Categorias />);

  // Act
  const linha = linhaPorTexto('Salário');
  await userEvent.click(within(linha).getByRole('button', { name: /editar/i }));
  await userEvent.type(within(linha).getByRole('textbox'), 'XYZ');
  await userEvent.click(within(linha).getByRole('button', { name: /cancelar/i }));

  // Assert
  expect(screen.getByText('Salário')).toBeInTheDocument();
});

test('exclui uma categoria apos confirmacao', async () => {
  vi.spyOn(window, 'confirm').mockReturnValue(true);
  render(<Categorias />);

  // Act
  const linha = linhaPorTexto('Alimentação');
  await userEvent.click(within(linha).getByRole('button', { name: /excluir/i }));

  // Assert
  expect(screen.queryByText('Alimentação')).not.toBeInTheDocument();
  window.confirm.mockRestore();
});

test('nao exclui quando a confirmacao e cancelada', async () => {
  vi.spyOn(window, 'confirm').mockReturnValue(false);
  render(<Categorias />);

  // Act
  const linha = linhaPorTexto('Alimentação');
  await userEvent.click(within(linha).getByRole('button', { name: /excluir/i }));

  // Assert
  expect(screen.getByText('Alimentação')).toBeInTheDocument();
  window.confirm.mockRestore();
});
