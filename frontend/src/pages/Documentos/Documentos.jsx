import { useState } from "react";
import "./Documentos.css";
import { FolderOpen } from "lucide-react";

function Documentos() {
  const [nome, setNome] = useState("");
  const [tipo, setTipo] = useState("Contrato");
  const [descricao, setDescricao] = useState("");
  const [arquivo, setArquivo] = useState(null);

  const [erro, setErro] = useState("");
  const [progresso, setProgresso] = useState(0);

  const [documentos, setDocumentos] = useState([]);

  const validarArquivo = (file) => {
    if (!file) return;

    const tiposPermitidos = [
      "application/pdf",
      "image/png",
      "image/jpeg",
    ];

    const tamanhoMaximo = 5 * 1024 * 1024;

    if (!tiposPermitidos.includes(file.type)) {
      setErro("Apenas arquivos PDF, PNG ou JPG são permitidos.");
      return;
    }

    if (file.size > tamanhoMaximo) {
      setErro("O arquivo deve ter no máximo 5 MB.");
      return;
    }

    setErro("");
    setArquivo(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();

    const file = e.dataTransfer.files[0];

    validarArquivo(file);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!arquivo) {
      setErro("Selecione um arquivo.");
      return;
    }

    let valor = 0;

    const intervalo = setInterval(() => {
      valor += 10;

      setProgresso(valor);

      if (valor >= 100) {
        clearInterval(intervalo);

        const novoDocumento = {
          id: Date.now(),
          nome,
          tipo,
          descricao,
          arquivo,
          data: new Date().toLocaleDateString("pt-BR"),
          tamanho: (
            arquivo.size /
            1024 /
            1024
          ).toFixed(2),
        };

        setDocumentos([
          ...documentos,
          novoDocumento,
        ]);

        setNome("");
        setTipo("Contrato");
        setDescricao("");
        setArquivo(null);
        setProgresso(0);
      }
    }, 120);
  };

  const excluirDocumento = (id) => {
    const confirmar = window.confirm(
      "Deseja excluir este documento?"
    );

    if (!confirmar) return;

    setDocumentos(
      documentos.filter(
        (doc) => doc.id !== id
      )
    );
  };

  const downloadDocumento = (arquivo) => {
    const url =
      URL.createObjectURL(arquivo);

    const link =
      document.createElement("a");

    link.href = url;
    link.download = arquivo.name;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  return (
    <div className="documentos-page">
      <header className="documentos-header">
        <div className="header-logo">
        <div className="logo-icon">
           <FolderOpen size={18} color="white" />
        </div>
        <div className="logo-text">
          <h1>CREDIFAB</h1>
          <p>Plataforma de Acesso a Crédito</p>
        </div>
        </div>
      </header>

      <main className="documentos-content">
        <section className="documentos-card">
          <h2>Novo Documento</h2>

          <form
            className="documentos-form"
            onSubmit={handleSubmit}
          >
            <input
              type="text"
              placeholder="Nome do documento"
              value={nome}
              onChange={(e) =>
                setNome(e.target.value)
              }
              required
            />

            <select
              value={tipo}
              onChange={(e) =>
                setTipo(e.target.value)
              }
            >
              <option>Contrato</option>
              <option>Comprovante</option>
              <option>Declaração</option>
              <option>Relatório</option>
            </select>

            <textarea
              placeholder="Descrição do documento"
              value={descricao}
              onChange={(e) =>
                setDescricao(
                  e.target.value
                )
              }
              required
            />

            <div
              className="dropzone"
              onDragOver={(e) =>
                e.preventDefault()
              }
              onDrop={handleDrop}
            >
              {arquivo
                ? arquivo.name
                : "Arraste o arquivo aqui"}
            </div>

            <input
              type="file"
              onChange={(e) =>
                validarArquivo(
                  e.target.files[0]
                )
              }
            />

            {erro && (
              <p className="erro">
                {erro}
              </p>
            )}

            {progresso > 0 && (
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width: `${progresso}%`,
                  }}
                ></div>
              </div>
            )}

            <button type="submit">
              Enviar Documento
            </button>
          </form>
        </section>

        <section className="documentos-card">
          <h2>
            Documentos Cadastrados
          </h2>

          <table className="documentos-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Tipo</th>
                <th>Data</th>
                <th>Tamanho</th>
                <th>Ações</th>
              </tr>
            </thead>

            <tbody>
              {documentos.map((doc) => (
                <tr key={doc.id}>
                  <td>{doc.nome}</td>
                  <td>{doc.tipo}</td>
                  <td>{doc.data}</td>
                  <td>
                    {doc.tamanho} MB
                  </td>

                  <td>
                    <div className="acoes">
                      <button
                        className="btn-download"
                        onClick={() =>
                          downloadDocumento(
                            doc.arquivo
                          )
                        }
                      >
                        Download
                      </button>

                      <button
                        className="btn-excluir"
                        onClick={() =>
                          excluirDocumento(
                            doc.id
                          )
                        }
                      >
                        Excluir
                      </button>
                    </div>
                  </td>
                </tr>
              ))}

              {documentos.length === 0 && (
                <tr>
                  <td
                    colSpan="5"
                    className="sem-documentos"
                  >
                    Nenhum documento cadastrado.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default Documentos;