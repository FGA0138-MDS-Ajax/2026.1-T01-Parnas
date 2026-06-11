import React, { useState } from "react";
import "./Register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    senha: "",
    dataNascimento: "",
  });

  const [erro, setErro] = useState("");
  const [success, setSuccess] = useState(false);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  }
const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setSuccess(false);

    const hoje = new Date();

  const nascimento = new Date(
    formData.dataNascimento
  );

  if (nascimento > hoje) {
    setErro("Data de nascimento inválida");
    return;
  }

  let idade =
    hoje.getFullYear() -
    nascimento.getFullYear();

  const mes =
    hoje.getMonth() -
    nascimento.getMonth();

  if (
    mes < 0 ||
    (
      mes === 0 &&
      hoje.getDate() < nascimento.getDate()
    )
  ) {
    idade--;
  }

  if (idade < 18) {
    setErro(
      "Você precisa ter pelo menos 18 anos"
    );
    return;
  }

    if (formData.senha.length < 8) {
      setErro("Sua senha deve ter no mínimo 8 caracteres");
      return;
    }

    try {

      const response = await fetch(
        "http://localhost:3000/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setErro(data.message || "Erro ao cadastrar");
        return;
      }

      window.location.href = "/";

    } catch (error) {
      setErro("Erro ao conectar ao servidor");
    }
  }

  return (
    <div className="register-container">

      <div className="register-card">

        <div className="register-sidebar">

          <h1 className="register-logo">
            CREDIFAB
          </h1>

          <p className="register-subtitle">
            Facilitando sua gestão financeira
          </p>

        </div>

        <div className="register-form-content">

          <div className="register-header">
            <span className="icon-user">👤</span>
            <h2>Registre-se</h2>
          </div>

          <form
            className="register-form"
            onSubmit={handleSubmit}
          >

            <div className="register-row">

              <div className="register-input-group">

                <label>
                  Nome
                </label>

                <input
                   type="text"
                    name="nome"
                    required
                />

              </div>

              <div className="register-input-group">

                <label>
                  Email
                </label>

                <input
                   type="email"
                    name="email"
                    placeholder="nome@email.com"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />

              </div>

            </div>

            <div className="register-row">

              <div className="register-input-group">

                <label>
                  Senha
                </label>

                <input
                  type="password"
                  name="senha"
                  placeholder="********"
                  required
                />

              </div>

              <div className="register-input-group">

                <label>
                  Data de nascimento
                </label>

                <input
                  type="date"
                  name="dataNascimento"
                  value={formData.dataNascimento}
                  onChange={handleChange}
                />

              </div>

            </div>

            {erro && (
              <p className="register-error">
                {erro}
              </p>
            )}

            <button
              type="submit"
              className="register-button"
            >
              Finalizar registro
            </button>

          </form>

        </div>

      </div>

    </div>
  );
}

export default Register;