import { render, screen, fireEvent, act } from '@testing-library/react';
import { vi } from 'vitest';
import Documentos from './Documentos';

function arquivo(nome, tipo, tamanho) {
  const file = new File(['conteudo'], nome, { type: tipo });
  if (tamanho != null) Object.defineProperty(file, 'size', { value: tamanho });
  return file;
}

const inputArquivo = () => document.querySelector('input[type="file"]');
const campoNome = () => screen.getByPlaceholderText(/nome do documento/i);
const campoDescricao = () => screen.getByPlaceholderText(/descrição do documento/i);
const botaoEnviar = () => screen.getByRole('button', { name: /enviar documento/i });

function preencheEEnvia(file) {
  fireEvent.change(campoNome(), { target: { value: 'Contrato 2024' } });
  fireEvent.change(campoDescricao(), { target: { value: 'Contrato anual' } });
  fireEvent.change(inputArquivo(), { target: { files: [file] } });
  // Act: o envio simula progresso via setInterval até 100%
  fireEvent.click(botaoEnviar());
  act(() => vi.advanceTimersByTime(1300));
}

test('inicia sem documentos cadastrados', () => {
  // Act
  render(<Documentos />);

  // Assert
  expect(screen.getByText(/nenhum documento cadastrado/i)).toBeInTheDocument();
});

test('arquivo de tipo invalido mostra erro', () => {
  render(<Documentos />);

  // Act: txt não é PDF/PNG/JPG
  fireEvent.change(inputArquivo(), { target: { files: [arquivo('nota.txt', 'text/plain')] } });

  // Assert
  expect(screen.getByText(/apenas arquivos pdf, png ou jpg/i)).toBeInTheDocument();
});

test('arquivo acima de 5MB mostra erro', () => {
  render(<Documentos />);

  // Act: PDF válido, porém com 6MB
  fireEvent.change(inputArquivo(), {
    target: { files: [arquivo('grande.pdf', 'application/pdf', 6 * 1024 * 1024)] },
  });

  // Assert
  expect(screen.getByText(/no máximo 5 mb/i)).toBeInTheDocument();
});

test('submeter sem arquivo mostra erro', () => {
  render(<Documentos />);
  fireEvent.change(campoNome(), { target: { value: 'Sem arquivo' } });
  fireEvent.change(campoDescricao(), { target: { value: 'x' } });

  // Act
  fireEvent.click(botaoEnviar());

  // Assert
  expect(screen.getByText(/selecione um arquivo/i)).toBeInTheDocument();
});

test('upload valido adiciona o documento na tabela', () => {
  vi.useFakeTimers();
  try {
    render(<Documentos />);

    preencheEEnvia(arquivo('contrato.pdf', 'application/pdf', 1024));

    // Assert
    expect(screen.getByText('Contrato 2024')).toBeInTheDocument();
  } finally {
    vi.useRealTimers();
  }
});

test('excluir documento com confirmacao remove da tabela', () => {
  vi.useFakeTimers();
  try {
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    render(<Documentos />);
    preencheEEnvia(arquivo('contrato.pdf', 'application/pdf', 1024));
    expect(screen.getByText('Contrato 2024')).toBeInTheDocument();

    // Act
    fireEvent.click(screen.getByRole('button', { name: /excluir/i }));

    // Assert
    expect(screen.queryByText('Contrato 2024')).not.toBeInTheDocument();
  } finally {
    window.confirm.mockRestore();
    vi.useRealTimers();
  }
});

test('cancelar exclusao mantem o documento', () => {
  vi.useFakeTimers();
  try {
    vi.spyOn(window, 'confirm').mockReturnValue(false);
    render(<Documentos />);
    preencheEEnvia(arquivo('contrato.pdf', 'application/pdf', 1024));

    // Act
    fireEvent.click(screen.getByRole('button', { name: /excluir/i }));

    // Assert
    expect(screen.getByText('Contrato 2024')).toBeInTheDocument();
  } finally {
    window.confirm.mockRestore();
    vi.useRealTimers();
  }
});
