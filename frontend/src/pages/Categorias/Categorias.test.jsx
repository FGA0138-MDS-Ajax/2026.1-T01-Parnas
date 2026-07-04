// daniel: a pagina passou a usar a API (categoria.service) e a recarregar a lista apos cada
// acao; reescrevi os testes com um mock em memoria do service para simular o backend e validar
// listagem, cadastro, edicao inline e exclusao.
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, beforeEach, test, expect } from 'vitest';
import Categorias from './Categorias';
import {
  listarCategorias, criarCategoria, atualizarCategoria, excluirCategoria,
} from '../../services/categoria.service';

vi.mock('../../services/categoria.service', () => ({
  listarCategorias: vi.fn(),
  criarCategoria: vi.fn(),
  atualizarCategoria: vi.fn(),
  excluirCategoria: vi.fn(),
}));

let store;

beforeEach(() => {
  vi.clearAllMocks();
  store = [
    { id: 1, nome: 'Salário', tipoExibicao: 'Receita' },
    { id: 2, nome: 'Alimentação', tipoExibicao: 'Despesa' },
  ];
  let nextId = 3;

  listarCategorias.mockImplementation(async () => store.map((c) => ({ ...c })));
  criarCategoria.mockImplementation(async ({ nome, tipo }) => {
    store.push({ id: nextId++, nome, tipoExibicao: tipo === 'receita' ? 'Receita' : 'Despesa' });
  });
  atualizarCategoria.mockImplementation(async (id, { nome, tipo }) => {
    const c = store.find((x) => x.id === id);
    if (c) { c.nome = nome; c.tipoExibicao = tipo === 'receita' ? 'Receita' : 'Despesa'; }
  });
  excluirCategoria.mockImplementation(async (id) => {
    store = store.filter((x) => x.id !== id);
  });
});

const novaCategoria = () => screen.getByPlaceholderText(/nome da categoria/i);
const botaoAdicionar = () => screen.getByRole('button', { name: /adicionar categoria/i });
const linhaPorTexto = (texto) => screen.getByText(texto).closest('tr');

test('lista as categorias vindas da API', async () => {
  render(<Categorias />);

  expect(await screen.findByText('Salário')).toBeInTheDocument();
  expect(screen.getByText('Alimentação')).toBeInTheDocument();
});

test('adiciona uma nova categoria pelo formulario', async () => {
  render(<Categorias />);
  await screen.findByText('Salário');

  await userEvent.type(novaCategoria(), 'Transporte');
  await userEvent.click(botaoAdicionar());

  expect(await screen.findByText('Transporte')).toBeInTheDocument();
  expect(criarCategoria).toHaveBeenCalledWith({ nome: 'Transporte', tipo: 'receita' });
});

test('formulario limpa o nome apos adicionar', async () => {
  render(<Categorias />);
  await screen.findByText('Salário');

  await userEvent.type(novaCategoria(), 'Transporte');
  await userEvent.click(botaoAdicionar());

  await screen.findByText('Transporte');
  expect(novaCategoria()).toHaveValue('');
});

test('edita o nome de uma categoria existente inline', async () => {
  render(<Categorias />);
  await screen.findByText('Salário');

  const linha = linhaPorTexto('Salário');
  await userEvent.click(within(linha).getByRole('button', { name: /editar/i }));
  const input = within(linha).getByRole('textbox');
  await userEvent.clear(input);
  await userEvent.type(input, 'Salário Mensal');
  await userEvent.click(within(linha).getByRole('button', { name: /salvar/i }));

  expect(await screen.findByText('Salário Mensal')).toBeInTheDocument();
  expect(screen.queryByText('Salário')).not.toBeInTheDocument();
});

test('cancelar edicao mantem o nome original', async () => {
  render(<Categorias />);
  await screen.findByText('Salário');

  const linha = linhaPorTexto('Salário');
  await userEvent.click(within(linha).getByRole('button', { name: /editar/i }));
  const input = within(linha).getByRole('textbox');
  await userEvent.clear(input);
  await userEvent.type(input, 'Outro Nome');
  await userEvent.click(within(linha).getByRole('button', { name: /cancelar/i }));

  expect(screen.getByText('Salário')).toBeInTheDocument();
  expect(screen.queryByText('Outro Nome')).not.toBeInTheDocument();
});
