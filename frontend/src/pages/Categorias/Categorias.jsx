import { useState } from "react";
import "./Categorias.css";
import { Tag } from "lucide-react";

function Categorias() {
  const [nome, setNome] = useState("");
  const [tipo, setTipo] = useState("Receita");

  const [editandoId, setEditandoId] = useState(null);
  const [nomeEditado, setNomeEditado] = useState("");
  const [tipoEditado, setTipoEditado] = useState("");

  const [categorias, setCategorias] = useState([
    {
      id: 1,
      nome: "Salário",
      tipo: "Receita",
    },
    {
      id: 2,
      nome: "Alimentação",
      tipo: "Despesa",
    },
  ]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const novaCategoria = {
      id: Date.now(),
      nome,
      tipo,
    };

    setCategorias([...categorias, novaCategoria]);

    setNome("");
    setTipo("Receita");
  };

  const iniciarEdicao = (categoria) => {
    setEditandoId(categoria.id);
    setNomeEditado(categoria.nome);
    setTipoEditado(categoria.tipo);
  };

  const salvarEdicao = (id) => {
    setCategorias(
      categorias.map((categoria) =>
        categoria.id === id
          ? {
              ...categoria,
              nome: nomeEditado,
              tipo: tipoEditado,
            }
          : categoria
      )
    );

    setEditandoId(null);
  };

  const cancelarEdicao = () => {
    setEditandoId(null);
  };

  const excluirCategoria = (id) => {
    const confirmar = window.confirm(
      "Deseja realmente excluir esta categoria?"
    );

    if (!confirmar) return;

    setCategorias(
      categorias.filter(
        (categoria) => categoria.id !== id
      )
    );
  };

  return (
    <div className="categorias-page">

      <header className="categorias-header">
        <div className="header-logo">

          <div className="logo-icon">
            <Tag size={18} color="white" />
          </div>

          <div className="logo-text">
            <h1>CREDIFAB</h1>
            <p>Plataforma de Acesso a Crédito</p>
          </div>
      
        </div>
      </header>

      <main className="categorias-content">

        <section className="categorias-card">
          <h2>Nova Categoria</h2>

          <form
            className="categorias-form"
            onSubmit={handleSubmit}
          >
            <input
              type="text"
              placeholder="Nome da categoria"
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
              <option>Receita</option>
              <option>Despesa</option>
            </select>

            <button type="submit">
              Adicionar Categoria
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
              {categorias.map((categoria) => (
                <tr key={categoria.id}>
                  <td>
                    {editandoId === categoria.id ? (
                      <input
                        type="text"
                        value={nomeEditado}
                        onChange={(e) =>
                          setNomeEditado(
                            e.target.value
                          )
                        }
                      />
                    ) : (
                      categoria.nome
                    )}
                  </td>

                  <td>
                    {editandoId === categoria.id ? (
                      <select
                        value={tipoEditado}
                        onChange={(e) =>
                          setTipoEditado(
                            e.target.value
                          )
                        }
                      >
                        <option>
                          Receita
                        </option>
                        <option>
                          Despesa
                        </option>
                      </select>
                    ) : (
                      <span
                        className={`tipo-badge ${
                          categoria.tipo ===
                          "Receita"
                            ? "receita"
                            : "despesa"
                        }`}
                      >
                        {categoria.tipo}
                      </span>
                    )}
                  </td>

                  <td>
                    <div className="acoes">
                      {editandoId ===
                      categoria.id ? (
                        <>
                          <button
                            className="btn-salvar"
                            onClick={() =>
                              salvarEdicao(
                                categoria.id
                              )
                            }
                          >
                            Salvar
                          </button>

                          <button
                            className="btn-cancelar"
                            onClick={
                              cancelarEdicao
                            }
                          >
                            Cancelar
                          </button>
                        </>
                      ) : (
                        <>
                          <button
                            className="btn-editar"
                            onClick={() =>
                              iniciarEdicao(
                                categoria
                              )
                            }
                          >
                            Editar
                          </button>

                          <button
                            className="btn-excluir"
                            onClick={() =>
                              excluirCategoria(
                                categoria.id
                              )
                            }
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
        </section>

      </main>
    </div>
  );
}

export default Categorias;