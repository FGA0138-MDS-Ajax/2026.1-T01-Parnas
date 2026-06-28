import { act, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { AuthProvider } from './AuthContext';
import { EmpresaProvider, useEmpresa } from './EmpresaContext';

const empresaA = {
  company_id: 1,
  name: 'Empresa A',
  cnpj: '11222333000181',
};

const empresaB = {
  company_id: 2,
  name: 'Empresa B',
  cnpj: '22333444000192',
};

const resposta = (data, ok = true) => Promise.resolve({
  ok,
  text: async () => JSON.stringify(data),
});

const criarLocalStorageMock = () => {
  let dados = { token: 'jwt-login' };
  return {
    getItem: (chave) => dados[chave] ?? null,
    setItem: (chave, valor) => {
      dados[chave] = String(valor);
    },
    removeItem: (chave) => {
      delete dados[chave];
    },
    clear: () => {
      dados = {};
    },
  };
};

const LeitorContexto = () => {
  const {
    empresas,
    empresaAtiva,
    carregandoEmpresas,
    selecionarEmpresa,
  } = useEmpresa();

  return (
    <div>
      <span data-testid="carregando">{String(carregandoEmpresas)}</span>
      <span data-testid="quantidade">{empresas.length}</span>
      <span data-testid="ativa">{empresaAtiva?.name || 'nenhuma'}</span>
      <button type="button" onClick={() => selecionarEmpresa(2)}>
        Trocar
      </button>
    </div>
  );
};

const renderContexto = () => render(
  <AuthProvider>
    <EmpresaProvider>
      <LeitorContexto />
    </EmpresaProvider>
  </AuthProvider>,
);

describe('EmpresaContext', () => {
  beforeEach(() => {
    vi.stubGlobal('localStorage', criarLocalStorageMock());
    vi.stubGlobal('fetch', vi.fn());
  });

  test('seleciona automaticamente quando o usuário possui uma empresa', async () => {
    fetch
      .mockImplementationOnce(() => resposta([empresaA]))
      .mockImplementationOnce(() => resposta({
        token: 'jwt-empresa-a',
        active_company_id: 1,
      }));

    renderContexto();

    await waitFor(() => {
      expect(screen.getByTestId('ativa')).toHaveTextContent('Empresa A');
    });

    expect(fetch).toHaveBeenNthCalledWith(
      2,
      '/api/sessao/empresa-ativa',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ company_id: 1 }),
      }),
    );
    expect(localStorage.getItem('token')).toBe('jwt-empresa-a');
    expect(JSON.parse(localStorage.getItem('empresaAtiva'))).toEqual(empresaA);
  });

  test('aguarda escolha quando o usuário possui mais de uma empresa', async () => {
    fetch.mockImplementationOnce(() => resposta([empresaA, empresaB]));

    renderContexto();

    await waitFor(() => {
      expect(screen.getByTestId('carregando')).toHaveTextContent('false');
    });

    expect(screen.getByTestId('quantidade')).toHaveTextContent('2');
    expect(screen.getByTestId('ativa')).toHaveTextContent('nenhuma');
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  test('troca a empresa ativa, persiste e substitui o JWT', async () => {
    fetch
      .mockImplementationOnce(() => resposta([empresaA, empresaB]))
      .mockImplementationOnce(() => resposta({
        token: 'jwt-empresa-b',
        active_company_id: 2,
      }));

    renderContexto();
    await waitFor(() => {
      expect(screen.getByTestId('quantidade')).toHaveTextContent('2');
    });

    await act(async () => {
      screen.getByRole('button', { name: 'Trocar' }).click();
    });

    await waitFor(() => {
      expect(screen.getByTestId('ativa')).toHaveTextContent('Empresa B');
    });

    expect(localStorage.getItem('token')).toBe('jwt-empresa-b');
    expect(JSON.parse(localStorage.getItem('empresaAtiva'))).toEqual(empresaB);
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  test('não consulta o backend no acesso de demonstração', async () => {
    localStorage.setItem('token', 'mock_demo_123');

    renderContexto();

    await waitFor(() => {
      expect(screen.getByTestId('ativa')).toHaveTextContent(
        'Empresa Demonstração',
      );
    });

    expect(fetch).not.toHaveBeenCalled();
  });
});
