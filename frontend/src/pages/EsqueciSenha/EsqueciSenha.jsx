import { useState } from 'react';

import { TrendingUp } from 'lucide-react';

import './EsqueciSenha.css';

export function EsqueciSenha() {
  const [email, setEmail] = useState('');

  const [successMessage, setSuccessMessage] =
    useState('');

  const [errorMessage, setErrorMessage] =
    useState('');

  const [loading, setLoading] =
    useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setSuccessMessage('');
    setErrorMessage('');

    if (!email.includes('@')) {
      setErrorMessage(
        'Digite um e-mail válido.'
      );

      return;
    }

    try {
      setLoading(true);

      // await api.post('/forgot-password', {
      //   email
      // });

      await new Promise((resolve) =>
        setTimeout(resolve, 1500)
      );

      setSuccessMessage(
        'Link de recuperação enviado com sucesso.'
      );

      setEmail('');
    } catch {
      setErrorMessage(
        'Erro ao enviar link de recuperação.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="forgot-password-container">

      <div className="forgot-password-card">

        <div className="forgot-password-brand">

          <div className="forgot-password-brand-icon">
            <TrendingUp
              size={34}
              strokeWidth={2.5}
            />
          </div>

          <span>CREDIFAB</span>

        </div>

        <div className="forgot-password-header">

          <h1 className="forgot-password-title">
            Recuperar senha
          </h1>

          <p className="forgot-password-description">
            Enviaremos um link para redefinir sua senha.
          </p>

        </div>

        <form
          className="forgot-password-form"
          onSubmit={handleSubmit}
        >

          <div className="forgot-password-field-group">

            <label className="forgot-password-label">
              E-mail
            </label>

            <input
              className="forgot-password-input"
              type="email"
              placeholder="seu@email.com"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />

          </div>

          {successMessage && (
            <div className="forgot-password-success">
              {successMessage}
            </div>
          )}

          {errorMessage && (
            <div className="forgot-password-error">
              {errorMessage}
            </div>
          )}

          <button
            className="forgot-password-button"
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Enviando...'
              : 'Enviar link'}
          </button>

          <a
            className="forgot-password-link"
            href="/login"
          >
            Voltar para login
          </a>

        </form>

      </div>

    </section>
  );
}