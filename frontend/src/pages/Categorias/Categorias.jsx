import { useEffect, useState } from "react";
import {
  listarCategorias,
  criarCategoria,
  atualizarCategoria,
  excluirCategoria as excluirCategoriaApi,
} from "../../services/categoria.service";
import "./Categorias.css";
import ConfirmacaoExclusaoCategoria from './ConfirmacaoExclusaoCategoria';

function Categorias() {
  const [nome, setNome] = useState("");
  const [tipo, setTipo] = useState("Receita");

  const [editandoId, setEditandoId] = useState(null);
  const [nomeEditado, setNomeEditado] = useState("");
  const [tipoEditado, setTipoEditado] = useState("");

  const [categorias, setCategorias] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [feedback, setFeedback] = useState("");

  const [confirmacaoAberta, setConfirmacaoAberta] = useState(false);
  const [categoriaParaExcluir, setCategoriaParaExcluir] = useState(null);

  const carregarCategorias = async () => {
    try {
      setCarregando(true);
      setErro("");
      const dados = await listarCategorias();
      setCategorias(dados);
    } catch (error) {
      setErro(error.message || "Erro ao carregar categorias.");
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    carregarCategorias();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!nome.trim()) {
      setErro("Informe o nome da categoria.");
      return;
    }

    try {
      setErro("");
      await criarCategoria({ nome, tipo: tipo.toLowerCase() });
      setNome("");
      setTipo("Receita");
      setFeedback("Categoria cadastrada com sucesso!");
      await carregarCategorias();
    } catch (error) {
      setErro(
        error.response?.data?.erro ||
          error.message ||
          "Erro ao salvar categoria.",
      );
    }
  };

  const iniciarEdicao = (categoria) => {
    setEditandoId(categoria.id);
    setNomeEditado(categoria.nome);
    setTipoEditado(categoria.tipoExibicao || categoria.tipo || "Receita");
  };

  const salvarEdicao = async (id) => {
    try {
      setErro("");
      await atualizarCategoria(id, {
        nome: nomeEditado,
        tipo: tipoEditado.toLowerCase(),
      });
      setEditandoId(null);
      setFeedback("Categoria atualizada com sucesso!");
      await carregarCategorias();
    } catch (error) {
      setErro(
        error.response?.data?.erro ||
          error.message ||
          "Erro ao atualizar categoria.",
      );
    }
  };

  const cancelarEdicao = () => {
    setEditandoId(null);
  };

  const abrirConfirmacao = (categoria) => {
    setCategoriaParaExcluir(categoria);
    setConfirmacaoAberta(true);
  };

  const cancelarExclusao = () => {
    setConfirmacaoAberta(false);
    setCategoriaParaExcluir(null);
  };

  const confirmarExclusao = async () => {
    if (!categoriaParaExcluir) return;
    try {
      setErro("");
      await excluirCategoriaApi(categoriaParaExcluir.id);
      setFeedback("Categoria excluída com sucesso!");
      setConfirmacaoAberta(false);
      setCategoriaParaExcluir(null);
      await carregarCategorias();
    } catch (error) {
      setErro(
        error.response?.data?.erro ||
          error.message ||
          "Erro ao excluir categoria.",
      );
      setConfirmacaoAberta(false);
    }
  };

  return (
    <div className="categorias-page">
      <main className="categorias-content">
        <section className="categorias-card">
          <h2>Nova Categoria</h2>

          {feedback && <p className="msg-success">{feedback}</p>}
          {erro && <p className="msg-erro">{erro}</p>}

          <form className="categorias-form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Nome da categoria"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />

            <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
              <option>Receita</option>
              <option>Despesa</option>
            </select>

            <button type="submit" className="btn-adicionar">
              Adicionar Categoria
            </button>
          </form>
        </section>

        <section className="categorias-card">
          <h2>Categorias Cadastradas</h2>

          {carregando ? (
            <p>Carregando categorias...</p>
          ) : (
            <table className="categorias-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Tipo</th>
                  <th>Ações</th>
                </tr>
              </thead>

              <tbody>
                {categorias.map((categoria) => (
                  <tr key={categoria.id}>
                    <td>
                      {editandoId === categoria.id ? (
                        <input
                          className="table-input"
                          type="text"
                          value={nomeEditado}
                          onChange={(e) => setNomeEditado(e.target.value)}
                        />
                      ) : (
                        categoria.nome
                      )}
                    </td>

                    <td>
                      {editandoId === categoria.id ? (
                        <select
                          className="table-select"
                          value={tipoEditado}
                          onChange={(e) => setTipoEditado(e.target.value)}
                        >
                          <option>Receita</option>
                          <option>Despesa</option>
                        </select>
                      ) : (
                        <span
                          className={`tipo-badge ${
                            (categoria.tipoExibicao || categoria.tipo) ===
                            "Receita"
                              ? "receita"
                              : "despesa"
                          }`}
                        >
                          {categoria.tipoExibicao || categoria.tipo}
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
                              onClick={() => abrirConfirmacao(categoria)}
                            >
                              Excluir
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
      {/* Modal de confirmação para exclusão */}
      {confirmacaoAberta && (
        <ConfirmacaoExclusaoCategoria
          categoria={categoriaParaExcluir}
          onConfirmar={confirmarExclusao}
          onCancelar={cancelarExclusao}
        />
      )}
    </div>
  );
}

export default Categorias;
