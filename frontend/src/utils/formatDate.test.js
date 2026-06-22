import { describe, test, expect } from 'vitest';
import formatDate from './formatDate';

describe('formatDate', () => {
  test('converte ISO (aaaa-mm-dd) para dd/mm/aaaa', () => {
    expect(formatDate('2026-06-10')).toBe('10/06/2026');
  });

  test('string vazia retorna vazio', () => {
    expect(formatDate('')).toBe('');
  });

  test('valor nulo retorna vazio', () => {
    expect(formatDate(null)).toBe('');
  });
});
