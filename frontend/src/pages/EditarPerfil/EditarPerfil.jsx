import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import "./EditarPerfil.css";

const EditarPerfil = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    cpf: "",
    birth_date: "",
  });

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const carregarDadosPerfil = async () => {
      try {
        const response = await api.get("/api/profile");
        const dadosUsuario = response.data;

        setFormData({
          name: dadosUsuario.name || "",
          email: dadosUsuario.email || "",
          cpf: dadosUsuario.cpf || "",
          birth_date: dadosUsuario.birth_date || "",
        });
      } catch (err) {
        console.error("Erro ao carregar dados do perfil:", err);
        setError("Não foi possível carregar as informações do seu perfil.");
      } finally {
        setLoading(false);
      }
    };

    carregarDadosPerfil();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setSubmitting(true);

    try {
      const response = await api.put("/api/profile", {
        name: formData.name,
        email: formData.email,
        cpf: formData.cpf.replace(/\D/g, ""), 
        birth_date: formData.birth_date,
      });

      setSuccess(true);
      alert(response.data.mensagem || "Perfil atualizado com sucesso!");
      navigate("/configuracoes");
    } catch (err) {
      console.error("Erro ao atualizar perfil:", err);
      setError(
        err.response?.data?.erro ||
          "Ocorreu um erro ao tentar salvar as alterações.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">Carregando dados do perfil...</div>
    );
  }

  return (
    <div className="editar-perfil-pagina">
      <div className="container-edicao">
        <div className="form-content">
          <div className="form-header">
            <h2>Editar Meus Dados</h2>
            <p>Modifique as informações da sua conta de usuário.</p>
          </div>

          {error && <p className="msg-error">{error}</p>}
          {success && (
            <p className="msg-success">Alterações salvas com sucesso!</p>
          )}

          <form onSubmit={handleSubmit} className="form-grid">
            <div className="input-group">
              <label>Nome Completo</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                disabled={submitting}
                required
              />
            </div>

            <div className="input-group">
              <label>E-mail</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                disabled={submitting}
                required
              />
            </div>

            <div className="input-group">
              <label>CPF</label>
              <input
                type="text"
                name="cpf"
                value={formData.cpf}
                onChange={handleChange}
                disabled={submitting}
                required
              />
            </div>

            <div className="input-group">
              <label>Data de Nascimento</label>
              <input
                type="date"
                name="birth_date"
                value={formData.birth_date}
                onChange={handleChange}
                disabled={submitting}
                required
              />
            </div>

            <div className="form-botoes-acoes">
              <button
                type="button"
                className="btn-cancelar"
                onClick={() => navigate("/configuracoes")}
                disabled={submitting}
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="btn-salvar"
                disabled={submitting}
              >
                {submitting ? "Salvando..." : "Salvar Alterações"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditarPerfil;
