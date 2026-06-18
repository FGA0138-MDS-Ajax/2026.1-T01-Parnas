import { useState, useEffect } from "react";
import api from "../../services/api";
import "./Documentos.css";

function Documentos() {
  const [nome, setNome] = useState("");
  const [tipo, setTipo] = useState("fiscal");
  const [descricao, setDescricao] = useState("");
  const [arquivo, setArquivo] = useState(null);

  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);
  const [progresso, setProgresso] = useState(0);

  const [documentos, setDocumentos] = useState([]);

  const obterIdEmpresa = () => {
    try {
      const empresas = JSON.parse(
        localStorage.getItem("credifab_empresas_reais") || "[]",
      );
      if (empresas.length > 0) {
        return empresas[0].company_id;
      }
      const idSimulado = localStorage.getItem("idEmpresaSimulado");
      if (idSimulado) {
        return idSimulado;
      }
    } catch (e) {
      console.error("Erro ao ler dados da empresa", e);
    }
    return null;
  };

  const companyId = obterIdEmpresa();

  const carregarDocumentos = async () => {
    if (!companyId) return;
    setLoading(true);
    setErro("");
    try {
      const response = await api.get(`/api/documentos?company_id=${companyId}`);
      if (response.data && response.data.documentos) {
        setDocumentos(response.data.documentos);
      }
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao carregar documentos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDocumentos();
  }, [companyId]);

  const validarArquivo = (file) => {
    if (!file) return;

    const tiposPermitidos = ["application/pdf", "image/png", "image/jpeg"];
    const tamanhoMaximo = 5 * 1024 * 1024;

    if (!tiposPermitidos.includes(file.type)) {
      setErro("Apenas arquivos PDF, PNG ou JPG são permitidos.");
      return false;
    }

    if (file.size > tamanhoMaximo) {
      setErro("O arquivo deve ter no máximo 5 MB.");
      return false;
    }

    setErro("");
    setArquivo(file);
    return true;
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    validarArquivo(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!companyId) {
      setErro("Nenhuma empresa selecionada.");
      return;
    }

    if (!arquivo) {
      setErro("Selecione um arquivo.");
      return;
    }

    setLoading(true);
    setErro("");
    setProgresso(30);

    const formData = new FormData();
    formData.append("name", nome);
    formData.append("type", tipo);
    formData.append("description", descricao);
    formData.append("company_id", companyId);
    formData.append("file", arquivo);

    try {
      await api.post("/api/documentos", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total,
          );
          setProgresso(percentCompleted);
        },
      });

      setNome("");
      setTipo("fiscal");
      setDescricao("");
      setArquivo(null);
      setProgresso(0);
      carregarDocumentos();
    } catch (err) {
      setProgresso(0);
      if (err.response?.data?.erros_de_validacao) {
        const mensagens = Object.values(err.response.data.erros_de_validacao)
          .flat()
          .join(" | ");
        setErro(mensagens);
      } else {
        setErro(err.response?.data?.erro || "Erro ao enviar o documento.");
      }
    } finally {
      setLoading(false);
    }
  };

  const excluirDocumento = async (id) => {
    //FIXME: a rota de exclusão DELETE está retornando 404
    //investigar conflito de roteamento no Flask/Blueprint 
    const confirmar = window.confirm(
      "Deseja realmente excluir este documento?",
    );
    if (!confirmar) return;

    try {
      await api.delete(`/api/documentos/${id}`);
      carregarDocumentos();
    } catch (err) {
      console.error(err);
      setErro("Erro ao excluir o documento.");
    }
  };

  const downloadDocumento = async (doc) => {
    try {
      const response = await api.get(
        `/api/documentos/${doc.document_id}/download`,
        {
          responseType: "blob",
        },
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;

      const contentDisposition = response.headers["content-disposition"];
      let filename = doc.name;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch && filenameMatch.length === 2) {
          filename = filenameMatch[1];
        }
      }

      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setErro("Erro ao realizar o download do documento.");
    }
  };

  return (
    <div className="documentos-page">
      <main className="documentos-content">
        {erro && <div className="erro">{erro}</div>}

        <section className="documentos-card">
          <h2>Novo Documento</h2>

          <form className="documentos-form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Nome do documento"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              disabled={loading || !companyId}
              required
            />

            <select
              value={tipo}
              onChange={(e) => setTipo(e.target.value)}
              disabled={loading || !companyId}
            >
              <option value="fiscal">Fiscal</option>
              <option value="contabil">Contábil</option>
              <option value="juridico">Jurídico</option>
            </select>

            <textarea
              placeholder="Descrição do documento"
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
              disabled={loading || !companyId}
              required
            />

            <div
              className="dropzone"
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => document.getElementById("fileInput").click()}
            >
              {arquivo
                ? arquivo.name
                : "Arraste o arquivo aqui ou clique para selecionar"}
            </div>

            <input
              id="fileInput"
              type="file"
              style={{ display: "none" }}
              onChange={(e) => validarArquivo(e.target.files[0])}
              disabled={loading || !companyId}
            />

            {progresso > 0 && progresso < 100 && (
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${progresso}%` }}
                ></div>
              </div>
            )}

            <button type="submit" disabled={loading || !companyId}>
              {loading ? "Enviando..." : "Enviar Documento"}
            </button>
          </form>
        </section>

        <section className="documentos-card">
          <h2>Documentos Cadastrados</h2>

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
              {documentos.length === 0 ? (
                <tr>
                  <td colSpan="5" className="sem-documentos">
                    {loading
                      ? "Carregando documentos..."
                      : "Nenhum documento cadastrado."}
                  </td>
                </tr>
              ) : (
                documentos.map((doc) => (
                  <tr key={doc.document_id}>
                    <td>{doc.name}</td>
                    <td style={{ textTransform: "capitalize" }}>{doc.type}</td>
                    <td>
                      {new Date(doc.created_at).toLocaleDateString("pt-BR")}
                    </td>
                    <td>{(doc.size / 1024 / 1024).toFixed(2)} MB</td>
                    <td>
                      <div className="acoes">
                        <button
                          className="btn-download"
                          onClick={() => downloadDocumento(doc)}
                        >
                          Download
                        </button>

                        <button
                          className="btn-excluir"
                          onClick={() => excluirDocumento(doc.document_id)}
                        >
                          Excluir
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default Documentos;
