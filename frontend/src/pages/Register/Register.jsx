import React, { useState } from "react";
import logoImg from "../../assets/LogoFundoBranco.png";
import "./Register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    cpf: "",
    senha: "",
    confirmarSenha: "",
    dataNascimento: "",
  });

  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const [verSenha, setVerSenha] = useState(false);
  const [verConfirmarSenha, setVerConfirmarSenha] = useState(false);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setLoading(true);

    const hoje = new Date();
    const nacimiento = new Date(formData.dataNascimento);

    if (nascimento > hoje) {
      setErro("Data de nascimento inválida");
      setLoading(false);
      return;
    }

    let idade = hoje.getFullYear() - nacimiento.getFullYear();
    const mes = hoje.getMonth() - nacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoje.getDate() < nacimiento.getDate())) {
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

    if (formData.senha !== formData.confirmarSenha) {
      setErro(
        "As senhas informadas não coincidem. Verifique e tente novamente.",
      );
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
            <h2>Cadastre-se</h2>
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
              <div className="password-input-wrapper">
                <input
                  type={verSenha ? "text" : "password"}
                  name="senha"
                  placeholder="No mínimo 8 caracteres"
                  value={formData.senha}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
                <button
                  type="button"
                  className="password-toggle-button"
                  onClick={() => setVerSenha(!verSenha)}
                  title={verSenha ? "Ocultar senha" : "Exibir senha"}
                >
                  {verSenha ? (
                    /* icone de Olho Fechado */
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-10-7-10-7a19.08 19.08 0 0 1 2.18-3M12 5c7 0 10 7 10 7a19.08 19.08 0 0 1-2.18 3M1 1l22 22" />
                      <path d="M12 9a3 3 0 0 0-3 3" />
                    </svg>
                  ) : (
                    /* icone de Olho Aberto */
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <div className="register-input-group">
              <label>Confirmar Senha</label>
              <div className="password-input-wrapper">
                <input
                  type={verConfirmarSenha ? "text" : "password"}
                  name="confirmarSenha"
                  placeholder="Digite a senha novamente"
                  value={formData.confirmarSenha}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
                <button
                  type="button"
                  className="password-toggle-button"
                  onClick={() => setVerConfirmarSenha(!verConfirmarSenha)}
                  title={verConfirmarSenha ? "Ocultar senha" : "Exibir senha"}
                >
                  {verConfirmarSenha ? (
                    /* icone de Olho Fechado */
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-10-7-10-7a19.08 19.08 0 0 1 2.18-3M12 5c7 0 10 7 10 7a19.08 19.08 0 0 1-2.18 3M1 1l22 22" />
                      <path d="M12 9a3 3 0 0 0-3 3" />
                    </svg>
                  ) : (
                    /* icone de Olho Aberto */
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {erro && <p className="register-error">{erro}</p>}

            <button
              type="submit"
              className="register-button"
              disabled={loading}
            >
              {loading ? "Cadastrando..." : "Cadastrar"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
