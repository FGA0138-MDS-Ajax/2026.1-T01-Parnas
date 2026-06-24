import { describe, test, expect } from 'vitest';
import formatCurrency from './formatCurrency';

describe('formatCurrency', () => {
  test('formata um valor positivo como moeda BRL', () => {
    expect(formatCurrency(1234.56)).toMatch(/R\$\s*1\.234,56/);
  });

  test('formata zero', () => {
    expect(formatCurrency(0)).toMatch(/R\$\s*0,00/);
  });

  test('trata valor ausente como zero', () => {
    expect(formatCurrency(undefined)).toMatch(/R\$\s*0,00/);
  });

  test('formata valor negativo', () => {
    expect(formatCurrency(-50)).toMatch(/-\s*R\$\s*50,00/);
  });
});
