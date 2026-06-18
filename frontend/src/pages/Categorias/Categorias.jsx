import { useState, useEffect } from "react";
import api from "../../services/api";
import "./Categorias.css";

function Categorias() {
  const [nome, setNome] = useState("");
  const [tipo, setTipo] = useState("Receita");

  const [editandoId, setEditandoId] = useState(null);
  const [nomeEditado, setNomeEditado] = useState("");
  const [tipoEditado, setTipoEditado] = useState("");

  const [categorias, setCategorias] = useState([]);
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const obterCnpjEmpresa = () => {
    try {
      const empresas = JSON.parse(
        localStorage.getItem("credifab_empresas_reais") || "[]",
      );
      if (empresas.length > 0) {
        return empresas[0].cnpj;
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

  const cnpjAtivo = obterCnpjEmpresa();

  const carregarCategorias = async () => {
    if (!cnpjAtivo) {
      setErro(
        "Nenhuma empresa ativa encontrada. Cadastre ou selecione uma empresa primeiro.",
      );
      return;
    }

    setLoading(true);
    setErro("");
    try {
      const response = await api.get(`/api/categories?cnpj=${cnpjAtivo}`);
      if (response.data && response.data.categories) {
        setCategorias(response.data.categories);
      } else if (Array.isArray(response.data)) {
        setCategorias(response.data);
      }
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao carregar as categorias.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarCategorias();
  }, [cnpjAtivo]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!cnpjAtivo) return;

    setErro("");
    try {
      await api.post("/api/categories", {
        name: nome,
        type: tipo,
        cnpj: cnpjAtivo,
      });

      setNome("");
      setTipo("Receita");
      carregarCategorias();
    } catch (err) {
      if (err.response?.data?.erros_de_validcao) {
        const mensagens = Object.values(err.response.data.erros_de_validcao)
          .flat()
          .join(" | ");
        setErro(mensagens);
      } else {
        setErro(err.response?.data?.erro || "Erro ao adicionar categoria.");
      }
    }
  };

  const iniciarEdicao = (categoria) => {
    setEditandoId(categoria.id);
    setNomeEditado(categoria.name || categoria.nome);
    setTipoEditado(categoria.type || categoria.tipo);
  };

  const salvarEdicao = async (id) => {
    if (!cnpjAtivo) return;

    setErro("");
    try {
      await api.put("/api/categories", {
        id: id,
        name: nomeEditado,
        type: tipoEditado,
        cnpj: cnpjAtivo,
      });

      setEditandoId(null);
      carregarCategorias();
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao atualizar categoria.");
    }
  };

  const cancelarEdicao = () => {
    setEditandoId(null);
  };

  const excluirCategoria = async (id) => {
    if (!cnpjAtivo) return;

    const confirmar = window.confirm(
      "Deseja realmente excluir esta categoria?",
    );
    if (!confirmar) return;

    setErro("");
    try {
      await api.delete("/api/categories", {
        data: {
          id: id,
          cnpj: cnpjAtivo,
        },
      });

      carregarCategorias();
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao excluir categoria.");
    }
  };

  return (
    <div className="categorias-page">
      <main className="categorias-content">
        {erro && (
          <div
            style={{
              padding: "12px",
              background: "#fee2e2",
              color: "#991b1b",
              borderRadius: "10px",
              marginBottom: "1.5rem",
              fontSize: "0.9rem",
              fontWeight: "600",
            }}
          >
            {erro}
          </div>
        )}

        <section className="categorias-card">
          <h2>Nova Categoria</h2>

          <form className="categorias-form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Nome da categoria"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              disabled={loading || !cnpjAtivo}
              required
            />

            <select
              value={tipo}
              onChange={(e) => setTipo(e.target.value)}
              disabled={loading || !cnpjAtivo}
            >
              <option>Receita</option>
              <option>Despesa</option>
            </select>

            <button type="submit" disabled={loading || !cnpjAtivo}>
              {loading ? "Processando..." : "Adicionar Categoria"}
            </button>
          </form>
        </section>

        <section className="categorias-card">
          <h2>Categorias Cadastradas</h2>

          <table className="categorias-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Tipo</th>
                <th>Ações</th>
              </tr>
            </thead>

            <tbody>
              {categorias.length === 0 ? (
                <tr>
                  <td
                    colSpan="3"
                    style={{
                      textAlign: "center",
                      color: "#6b7280",
                      padding: "2rem",
                    }}
                  >
                    {loading
                      ? "Carregando categorias..."
                      : "Nenhuma categoria cadastrada."}
                  </td>
                </tr>
              ) : (
                categorias.map((categoria) => (
                  <tr key={categoria.id}>
                    <td>
                      {editandoId === categoria.id ? (
                        <input
                          type="text"
                          value={nomeEditado}
                          onChange={(e) => setNomeEditado(e.target.value)}
                        />
                      ) : (
                        categoria.name || categoria.nome
                      )}
                    </td>

                    <td>
                      {editandoId === categoria.id ? (
                        <select
                          value={tipoEditado}
                          onChange={(e) => setTipoEditado(e.target.value)}
                        >
                          <option>Receita</option>
                          <option>Despesa</option>
                        </select>
                      ) : (
                        <span
                          className={`tipo-badge ${
                            (categoria.type || categoria.tipo).toLowerCase() ===
                            "receita"
                              ? "receita"
                              : "despesa"
                          }`}
                        >
                          {categoria.type || categoria.tipo}
                        </span>
                      )}
                    </td>

                    <td>
                      <div className="acoes">
                        {editandoId === categoria.id ? (
                          <>
                            <button
                              className="btn-salvar"
                              onClick={() => salvarEdicao(categoria.id)}
                            >
                              Salvar
                            </button>

                            <button
                              className="btn-cancelar"
                              onClick={cancelarEdicao}
                            >
                              Cancelar
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              className="btn-editar"
                              onClick={() => iniciarEdicao(categoria)}
                            >
                              Editar
                            </button>

                            <button
                              className="btn-excluir"
                              onClick={() => excluirCategoria(categoria.id)}
                            >
                              Excluir
                            </button>
                          </>
                        )}
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

export default Categorias;
