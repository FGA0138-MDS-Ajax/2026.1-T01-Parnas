import { useState, useEffect } from "react";
import PageHeader from "../../components/Finance/PageHeader";
import {
  listarDocumentos,
  uploadDocumento,
  excluirDocumentoApi,
  downloadDocumentoApi,
} from "../../services/documento.service";
import "./Documentos.css";

function Documentos() {
  const [nome, setNome] = useState("");
  const [tipo, setTipo] = useState("fiscal");
  const [descricao, setDescricao] = useState("");
  const [arquivo, setArquivo] = useState(null);

  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");
  const [progresso, setProgresso] = useState(0);
  const [carregando, setCarregando] = useState(false);

  const [documentos, setDocumentos] = useState([]);

  const carregarDocumentos = async () => {
    try {
      setCarregando(true);
      const data = await listarDocumentos();
      setDocumentos(data.documents || []);
    } catch (error) {
      setErro("Erro ao carregar documentos.");
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    carregarDocumentos();
  }, []);

  const formatarData = (dataStr) => {
    if (!dataStr) return "";
    const [ano, mes, dia] = dataStr.split("-");
    return `${dia}/${mes}/${ano}`;
  };

  const validarArquivo = (file) => {
    if (!file) return;

    const tiposPermitidos = ["application/pdf", "image/png", "image/jpeg"];
    const tamanhoMaximo = 5 * 1024 * 1024; // 5MB

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!arquivo) {
      setErro("Selecione um arquivo.");
      return;
    }

    try {
      setErro("");
      setSucesso("");
      await uploadDocumento(nome, tipo, descricao, arquivo, (porcentagem) => {
        setProgresso(porcentagem);
      });

      setSucesso("Documento enviado com sucesso!");
      setNome("");
      setTipo("fiscal");
      setDescricao("");
      setArquivo(null);

      setTimeout(() => {
        setProgresso(0);
        setSucesso("");
      }, 3000);

      carregarDocumentos();
    } catch (error) {
      setProgresso(0);
      setErro(error.response?.data?.erro || "Erro ao enviar o documento.");
    }
  };

  const excluirDocumento = async (id) => {
    if (!window.confirm("Deseja realmente excluir este documento?")) return;

    try {
      await excluirDocumentoApi(id);
      carregarDocumentos();
    } catch (error) {
      alert("Erro ao excluir o documento.");
    }
  };

  const downloadDocumento = async (id, nome) => {
    try {
      await downloadDocumentoApi(id, nome);
    } catch (error) {
      alert("Erro ao fazer o download.");
    }
  };

  return (
    <div className="documentos-page">
      <PageHeader
        className="documentos-header"
        title="Documentos"
        description="Gerencie e armazene arquivos físicos e jurídicos da sua empresa."
      />

      <main className="documentos-content">
        <section className="documentos-card">
          <h2>Novo Documento</h2>

          <form className="documentos-form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Nome do documento (Ex: Contrato de Aluguel)"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />

            <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
              <option value="fiscal">Fiscal (NF, Recibos)</option>
              <option value="contabil">Contábil (Relatórios)</option>
              <option value="juridico">Jurídico (Contratos)</option>
            </select>

            <textarea
              placeholder="Descrição do documento"
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
            />

            <div
              className="dropzone"
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
            >
              {arquivo
                ? arquivo.name
                : "Arraste o arquivo aqui (PDF, PNG ou JPG até 5MB)"}
            </div>

            <input
              type="file"
              accept=".pdf, .png, .jpg, .jpeg"
              onChange={(e) => validarArquivo(e.target.files[0])}
            />

            {erro && <p className="erro">{erro}</p>}
            {sucesso && (
              <p
                className="sucesso"
                style={{ color: "green", fontWeight: 600 }}
              >
                {sucesso}
              </p>
            )}

            {progresso > 0 && (
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${progresso}%` }}
                ></div>
              </div>
            )}

            <button type="submit">Enviar Documento</button>
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
              {carregando ? (
                <tr>
                  <td colSpan="5" className="sem-documentos">
                    Carregando documentos...
                  </td>
                </tr>
              ) : documentos.length === 0 ? (
                <tr>
                  <td colSpan="5" className="sem-documentos">
                    Nenhum documento cadastrado.
                  </td>
                </tr>
              ) : (
                documentos.map((doc) => (
                  <tr key={doc.document_id}>
                    <td>{doc.name}</td>
                    <td style={{ textTransform: "capitalize" }}>{doc.type}</td>
                    <td>{formatarData(doc.created_at)}</td>
                    <td>{(doc.size / 1024 / 1024).toFixed(2)} MB</td>
                    <td>
                      <div className="acoes">
                        <button
                          className="btn-download"
                          onClick={() =>
                            downloadDocumento(doc.document_id, doc.name)
                          }
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
