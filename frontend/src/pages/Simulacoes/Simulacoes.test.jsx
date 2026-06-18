import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, beforeEach, test, expect } from 'vitest';

// recharts não renderiza em jsdom — stub explícito dos componentes usados
vi.mock('recharts', () => {
  const Fake = ({ children }) => <div>{children}</div>;
  return {
    ResponsiveContainer: Fake,
    ComposedChart: Fake,
    Bar: Fake,
    Line: Fake,
    XAxis: Fake,
    YAxis: Fake,
    CartesianGrid: Fake,
    Tooltip: Fake,
    Legend: Fake,
    ReferenceLine: Fake,
  };
});

// empresa logada fixa
vi.mock('../../context/EmpresaContext', () => ({
  useEmpresa: () => ({ idEmpresaLogada: 1 }),
}));

const listarSimulacoes = vi.fn();
const salvarSimulacao = vi.fn();
const excluirSimulacao = vi.fn();
vi.mock('../../services/simulacao.service', () => ({
  listarSimulacoes: (...a) => listarSimulacoes(...a),
  salvarSimulacao: (...a) => salvarSimulacao(...a),
  excluirSimulacao: (...a) => excluirSimulacao(...a),
}));

import Simulacoes from './Simulacoes';

beforeEach(() => {
  vi.clearAllMocks();
  listarSimulacoes.mockResolvedValue([]);
  salvarSimulacao.mockResolvedValue({});
  excluirSimulacao.mockResolvedValue();
  // fetch do fluxo de caixa: sem dados (evita ruído no jsdom)
  global.fetch = vi.fn().mockResolvedValue({ ok: false, text: async () => '' });
});

async function preencherForm(user, { valor = '10000', prazo = '12', taxa = '2', modalidade } = {}) {
  await user.type(screen.getByLabelText(/valor solicitado/i), valor);
  await user.type(screen.getByLabelText(/prazo/i), prazo);
  await user.type(screen.getByLabelText(/taxa de juros/i), taxa);
  if (modalidade) await user.selectOptions(screen.getByLabelText(/modalidade/i), modalidade);
}

test('exibe parcela, total e juros em tempo real ao preencher o formulario', async () => {
  const user = userEvent.setup();
  render(<Simulacoes />);

  await preencherForm(user, {});

  expect(await screen.findByText(/Total a Pagar/i)).toBeInTheDocument();
  expect(screen.getByText(/Total de Juros/i)).toBeInTheDocument();
  expect(screen.getByText(/Valor da Parcela/i)).toBeInTheDocument();
});

test('modalidade SAC destaca a "1a Parcela"', async () => {
  const user = userEvent.setup();
  render(<Simulacoes />);

  await preencherForm(user, { modalidade: 'SAC' });

  expect(await screen.findByText(/1ª Parcela/i)).toBeInTheDocument();
});

test('formulario incompleto nao exibe o resultado', async () => {
  const user = userEvent.setup();
  render(<Simulacoes />);

  await user.type(screen.getByLabelText(/valor solicitado/i), '10000');

  expect(screen.queryByText(/Total a Pagar/i)).not.toBeInTheDocument();
});

test('salvar chama o servico de persistencia', async () => {
  const user = userEvent.setup();
  render(<Simulacoes />);

  await preencherForm(user, {});
  await user.click(await screen.findByRole('button', { name: /salvar simula/i }));

  await waitFor(() => expect(salvarSimulacao).toHaveBeenCalledTimes(1));
});

test('lista as simulacoes salvas com seus parametros', async () => {
  listarSimulacoes.mockResolvedValue([
    {
      id_simulacao: 1, data_simulacao: '2026-01-01', valor_solicitado: 10000,
      prazo_meses: 12, modalidade: 'PRICE', taxa_juros: 2,
      valor_parcela: 900, valor_total: 10800, total_juros: 800,
    },
  ]);
  render(<Simulacoes />);

  expect(await screen.findByText(/10\.000/)).toBeInTheDocument();
  expect(screen.getByText('PRICE')).toBeInTheDocument();
});

test('exclusao pede confirmacao e o "Cancelar" nao chama o servico', async () => {
  listarSimulacoes.mockResolvedValue([
    {
      id_simulacao: 1, data_simulacao: '2026-01-01', valor_solicitado: 10000,
      prazo_meses: 12, modalidade: 'PRICE', taxa_juros: 2,
      valor_parcela: 900, valor_total: 10800, total_juros: 800,
    },
  ]);
  const user = userEvent.setup();
  render(<Simulacoes />);

  await user.click(await screen.findByTitle(/excluir simula/i));
  expect(screen.getByText(/Excluir simulação\?/i)).toBeInTheDocument();

  await user.click(screen.getByRole('button', { name: /cancelar/i }));
  expect(excluirSimulacao).not.toHaveBeenCalled();
});

test('exclusao confirmada chama o servico com o id da simulacao', async () => {
  listarSimulacoes.mockResolvedValue([
    {
      id_simulacao: 7, data_simulacao: '2026-01-01', valor_solicitado: 10000,
      prazo_meses: 12, modalidade: 'PRICE', taxa_juros: 2,
      valor_parcela: 900, valor_total: 10800, total_juros: 800,
    },
  ]);
  const user = userEvent.setup();
  render(<Simulacoes />);

  await user.click(await screen.findByTitle(/excluir simula/i));
  await user.click(screen.getByRole('button', { name: /sim, excluir/i }));

  await waitFor(() => expect(excluirSimulacao).toHaveBeenCalledWith(7));
});
