import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, test, expect } from 'vitest';

// recharts e lucide-react não renderizam util em jsdom — stubs leves
vi.mock('recharts', () => {
  const Fake = ({ children }) => <div>{children}</div>;
  return {
    PieChart: Fake, Pie: Fake, Tooltip: Fake, Cell: Fake,
    ResponsiveContainer: Fake, LineChart: Fake, Line: Fake,
    XAxis: Fake, YAxis: Fake, CartesianGrid: Fake,
    BarChart: Fake, Bar: Fake, Legend: Fake,
  };
});
vi.mock('lucide-react', () => ({ BarChart3: () => null }));

import Relatorios from './Relatorios';

test('exibe os cards de Receitas, Despesas e Saldo', () => {
  render(<Relatorios />);

  expect(screen.getByRole('heading', { name: 'Receitas' })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Despesas' })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Saldo' })).toBeInTheDocument();
});

test('por padrao (mensal) exibe o campo de mes', () => {
  const { container } = render(<Relatorios />);

  expect(container.querySelector('input[type="month"]')).toBeInTheDocument();
});

test('selecionar periodo personalizado exibe dois campos de data', async () => {
  const user = userEvent.setup();
  const { container } = render(<Relatorios />);

  await user.selectOptions(screen.getByRole('combobox'), 'personalizado');

  expect(container.querySelectorAll('input[type="date"]').length).toBe(2);
});

test('selecionar periodo anual exibe campo de ano', async () => {
  const user = userEvent.setup();
  const { container } = render(<Relatorios />);

  await user.selectOptions(screen.getByRole('combobox'), 'anual');

  expect(container.querySelector('input[placeholder="Ano"]')).toBeInTheDocument();
});
