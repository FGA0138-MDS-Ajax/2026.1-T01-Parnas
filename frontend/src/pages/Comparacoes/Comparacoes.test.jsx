import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, beforeEach, test, expect } from 'vitest';

vi.mock('recharts', () => {
  const Fake = ({ children }) => <div>{children}</div>;
  return {
    BarChart: Fake, Bar: Fake, XAxis: Fake, YAxis: Fake,
    CartesianGrid: Fake, Tooltip: Fake, ResponsiveContainer: Fake, Cell: Fake,
  };
});

const calcularComparacao = vi.fn();
const salvarComparacao = vi.fn();
const exportarPDF = vi.fn();
vi.mock('../../services/comparacao.service', () => ({
  calcularComparacao: (...a) => calcularComparacao(...a),
  salvarComparacao: (...a) => salvarComparacao(...a),
  exportarPDF: (...a) => exportarPDF(...a),
}));

import Comparacoes from './Comparacoes';

beforeEach(() => {
  vi.clearAllMocks();
  calcularComparacao.mockResolvedValue({
    loan_amount: 10000,
    comparisons: [
      {
        name: 'Banco A', interest_rate: 2, term_months: 12, type: 'PJ',
        monthly_payment: 900, total_amount: 10800, total_interest: 800,
        is_best_option: true, warning_pf: false,
      },
    ],
  });
});

test('começa com uma modalidade e adiciona outra', async () => {
  const user = userEvent.setup();
  render(<Comparacoes />);

  expect(screen.getByText('Modalidade 1')).toBeInTheDocument();

  await user.click(screen.getByRole('button', { name: /adicionar modalidade/i }));

  expect(screen.getByText('Modalidade 2')).toBeInTheDocument();
});

test('calcular sem valor de empréstimo não chama o serviço', async () => {
  const user = userEvent.setup();
  render(<Comparacoes />);

  await user.click(screen.getByRole('button', { name: /calcular compara/i }));

  expect(calcularComparacao).not.toHaveBeenCalled();
});

test('calcular com dados válidos chama o serviço', async () => {
  const user = userEvent.setup();
  render(<Comparacoes />);

  await user.type(screen.getByPlaceholderText('Ex: 50000'), '10000');
  await user.type(screen.getByPlaceholderText(/Caixa Econ/i), 'Banco A');
  await user.type(screen.getByPlaceholderText('Ex: 1.5'), '2');
  await user.type(screen.getByPlaceholderText('Ex: 36'), '12');
  await user.click(screen.getByRole('button', { name: /calcular compara/i }));

  await waitFor(() => expect(calcularComparacao).toHaveBeenCalledTimes(1));
});
