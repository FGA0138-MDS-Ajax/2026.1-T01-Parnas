import React, { useState } from "react";
import logoImg from "../../assets/LogoFundoBranco.png";
import "./Register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    cpf: "",
    senha: "",
    dataNascimento: "",
  });

  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setLoading(true);

    const hoje = new Date();
    const nascimento = new Date(formData.dataNascimento);

    if (nascimento > hoje) {
      setErro("Data de nascimento inválida");
      setLoading(false);
      return;
    }

    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const mes = hoje.getMonth() - nascimento.getMonth();
    if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
      idade--;
    }

    if (idade < 16) {
      setErro("Você precisa ter pelo menos 16 anos para se cadastrar.");
      setLoading(false);
      return;
    }

    if (formData.senha.length < 8) {
      setErro("Sua senha deve ter no mínimo 8 caracteres.");
      setLoading(false);
      return;
    }

    const cpfLimpo = formData.cpf.replace(/\D/g, "");

    const payloadParaBackend = {
      name: formData.nome,
      email: formData.email,
      cpf: cpfLimpo,
      password: formData.senha,
      birth_date: formData.dataNascimento,
    };

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payloadParaBackend),
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.erros_de_validcao) {
          const mensagens = Object.values(data.erros_de_validcao)
            .flat()
            .join(" | ");
          throw new Error(mensagens);
        }
        throw new Error(data.erro || "Erro ao realizar o cadastro.");
      }

      window.location.href = "/";
    } catch (error) {
      setErro(error.message || "Erro ao conectar ao servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="register-sidebar">
          <div className="register-logo-container">
            <img
              src={logoImg}
              alt="Logo CREDIFAB"
              className="register-logo-img"
            />
          </div>
          <h1 className="register-logo">CREDIFAB</h1>
          <p className="register-subtitle">Facilitando sua gestão financeira</p>
        </div>

        <div className="register-form-content">
          <div className="register-header">
            <span className="icon-user">👤</span>
            <h2>Registre-se</h2>
          </div>

          <form className="register-form" onSubmit={handleSubmit}>
            <div className="register-input-group">
              <label>Nome</label>
              <input
                type="text"
                name="nome"
                value={formData.nome}
                onChange={handleChange}
                placeholder="Seu nome completo"
                disabled={loading}
                required
              />
            </div>

            <div className="register-input-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="nome@email.com"
                value={formData.email}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>

            <div className="register-input-group">
              <label>CPF</label>
              <input
                type="text"
                name="cpf"
                placeholder="000.000.000-00"
                value={formData.cpf}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>

            <div className="register-input-group">
              <label>Data de nascimento</label>
              <input
                type="date"
                name="dataNascimento"
                value={formData.dataNascimento}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>

            <div className="register-input-group">
              <label>Senha</label>
              <input
                type="password"
                name="senha"
                placeholder="No mínimo 8 caracteres"
                value={formData.senha}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>

            {erro && <p className="register-error">{erro}</p>}

            <button
              type="submit"
              className="register-button"
              disabled={loading}
            >
              {loading ? "Cadastrando..." : "Finalizar registro"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;