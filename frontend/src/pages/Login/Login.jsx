import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import logoImg from "../../assets/LogoFundoBranco.png";
import "./Login.css";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (!formData.email || !formData.password) {
      setError("Preencha todos os campos.");
      setLoading(false);
      return;
    }

    if (formData.password.length < 8) {
      setError("Credenciais inválidas. Verifique seus dados.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.erro || "Erro ao realizar o login.");
      }

      // Passa o token JWT real retornado pelo AuthService para o seu hook global
      if (data.token) {
        login(data.token);
      } else if (data.access_token) {
        login(data.access_token);
      }

      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Erro ao conectar ao servidor.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoAccess = () => {
    login(`mock_demo_${Date.now()}`);
    navigate("/dashboard");
  };

  return (
    <div className="login-card">
      <div className="login-header">
        <div className="login-logo-container">
          <img src={logoImg} alt="Logo CREDIFAB" className="login-logo-img" />
        </div>
        <h1 className="login-brand">CREDIFAB</h1>
        <p className="login-brand-sub">Plataforma de Acesso a Crédito</p>
      </div>

      <div className="login-body">
        <h2 className="login-title">Bem-vindo de volta</h2>
        <p className="login-subtitle">
          Entre com suas credenciais para continuar
        </p>

        {error && <p className="msg-error">{error}</p>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <label>E-mail</label>
            <div className="input-icon-wrapper">
              <svg
                className="input-icon"
                width="15"
                height="15"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                <polyline points="22,6 12,13 2,6" />
              </svg>
              <input
                type="email"
                name="email"
                placeholder="seu@email.com.br"
                value={formData.email}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>
          </div>

          <div className="input-group">
            <label>Senha</label>
            <div className="input-icon-wrapper">
              <svg
                className="input-icon"
                width="15"
                height="15"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                disabled={loading}
                required
              />
            </div>
          </div>

          <div className="login-options">
            <label className="remember-label">
              <input
                type="checkbox"
                name="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
                disabled={loading}
              />
              <span>Lembrar-me</span>
            </label>
            <Link to="/esqueci-senha" className="forgot-link">
              Esqueceu a senha?
            </Link>
          </div>

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div className="divider">
          <span>ou</span>
        </div>

        <button
          type="button"
          className="btn-demo"
          onClick={handleDemoAccess}
          disabled={loading}
        >
          Acessar Conta Demo
        </button>

        <p className="login-register">
          Não tem uma conta?{" "}
          <Link to="/Register" className="register-link">
            Cadastre-se gratuitamente
          </Link>
        </p>

        <p className="login-footer-text">
          Contribuindo para o ODS 9.3 - Democratizando o acesso ao crédito
        </p>
      </div>
    </div>
  );
};

export default Login;
