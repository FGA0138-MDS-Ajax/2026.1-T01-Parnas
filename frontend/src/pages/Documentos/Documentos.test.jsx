import { render, screen, fireEvent } from '@testing-library/react';
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
