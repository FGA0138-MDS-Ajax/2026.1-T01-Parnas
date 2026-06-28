import { useState, useEffect } from "react";
import emailjs from "@emailjs/browser";
import logoImg from "../../assets/CredifabLogo.png";
import "./EsqueciSenha.css";

export function EsqueciSenha() {
  const [email, setEmail] = useState("");
  const [token, setToken] = useState(null);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = queryParams.get("token");
    if (tokenFromUrl) {
      setToken(decodeURIComponent(tokenFromUrl));
    }
  }, []);

  async function handleRequestToken(event) {
    event.preventDefault();
    setSuccessMessage("");
    setErrorMessage("");
    setLoading(true);

    if (!email.includes("@")) {
      setErrorMessage("Digite um e-mail válido.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.erro || "Erro ao processar solicitação.");
      }

      // daniel: consertei o token quebrado lendo o parametro ?token= da query
      const rawToken = new URL(data.reset_link).searchParams.get("token");
      const safeToken = encodeURIComponent(rawToken);
      const reactResetLink = `http://localhost:5173/esqueci-senha?token=${safeToken}`;

      emailjs.init("XadOERpbRkiSIy1-_");

      await emailjs.send("service_mr9gkdu", "template_zzte7bw", {
        email: data.email,
        reset_link: reactResetLink,
      });

      setSuccessMessage(
        "E-mail de recuperação enviado com sucesso! Verifique sua caixa de entrada.",
      );
      setEmail("");
    } catch (error) {
      setErrorMessage(error.message || "Erro ao enviar o link de recuperação.");
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(event) {
    event.preventDefault();
    setSuccessMessage("");
    setErrorMessage("");
    setLoading(true);

    if (newPassword.length < 8) {
      setErrorMessage("A nova senha deve ter no mínimo 8 caracteres.");
      setLoading(false);
      return;
    }

    if (newPassword !== confirmPassword) {
      setErrorMessage("As senhas não coincidem.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: token,
          new_password: newPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.erro || "Erro ao redefinir a senha.");
      }

      setSuccessMessage("Senha redefinida com sucesso! Redirecionando...");
      setTimeout(() => {
        window.location.href = "/";
      }, 2000);
    } catch (error) {
      setErrorMessage(error.message || "Erro ao atualizar a senha.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="forgot-password-container">
      <div className="forgot-password-card">
        <div className="forgot-password-brand">
          <div className="forgot-password-logo-container">
            <img
              src={logoImg}
              alt="Logo CREDIFAB"
              className="forgot-password-logo-img"
            />
          </div>
          <span>CREDIFAB</span>
        </div>

        <div className="forgot-password-header">
          <h1 className="forgot-password-title">
            {token ? "Nova senha" : "Recuperar senha"}
          </h1>
          <p className="forgot-password-description">
            {token
              ? "Digite sua nova senha de acesso abaixo."
              : "Enviaremos um link para redefinir sua senha."}
          </p>
        </div>

        {!token ? (
          <form className="forgot-password-form" onSubmit={handleRequestToken}>
            <div className="forgot-password-field-group">
              <label className="forgot-password-label">E-mail</label>
              <input
                className="forgot-password-input"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                disabled={loading}
                required
              />
            </div>

            {successMessage && (
              <div className="forgot-password-success">{successMessage}</div>
            )}
            {errorMessage && (
              <div className="forgot-password-error">{errorMessage}</div>
            )}

            <button
              className="forgot-password-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Enviando..." : "Enviar link"}
            </button>

            <a className="forgot-password-link" href="/">
              Voltar para login
            </a>
          </form>
        ) : (
          <form className="forgot-password-form" onSubmit={handleResetPassword}>
            <div className="forgot-password-field-group">
              <label className="forgot-password-label">Nova Senha</label>
              <input
                className="forgot-password-input"
                type="password"
                placeholder="••••••••"
                value={newPassword}
                onChange={(event) => setNewPassword(event.target.value)}
                disabled={loading}
                required
              />
            </div>

            <div
              className="forgot-password-field-group"
              style={{ marginTop: "15px" }}
            >
              <label className="forgot-password-label">
                Confirmar Nova Senha
              </label>
              <input
                className="forgot-password-input"
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                disabled={loading}
                required
              />
            </div>

            {successMessage && (
              <div className="forgot-password-success">{successMessage}</div>
            )}
            {errorMessage && (
              <div className="forgot-password-error">{errorMessage}</div>
            )}

            <button
              className="forgot-password-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Salvando..." : "Alterar senha"}
            </button>

            <a className="forgot-password-link" href="/">
              Cancelar
            </a>
          </form>
        )}
      </div>
    </section>
  );
}
