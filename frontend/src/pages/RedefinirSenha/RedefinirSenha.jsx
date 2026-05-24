import { useState } from 'react';

import { TrendingUp } from 'lucide-react';

import './RedefinirSenha.css';

export function RedefinirSenha() {
  const [newPassword, setNewPassword] =
    useState('');

  const [confirmPassword, setConfirmPassword] =
    useState('');

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

    if (newPassword.length < 8) {
      setErrorMessage(
        'A senha deve possuir no mínimo 8 caracteres.'
      );

      return;
    }

    if (newPassword !== confirmPassword) {
      setErrorMessage(
        'As senhas não coincidem.'
      );

      return;
    }

    try {
      setLoading(true);

      // await api.post('/reset-password', {
      //   password: newPassword
      // });

      await new Promise((resolve) =>
        setTimeout(resolve, 1500)
      );

      setSuccessMessage(
        'Senha redefinida com sucesso.'
      );

      setNewPassword('');
      setConfirmPassword('');
    } catch {
      setErrorMessage(
        'Erro ao redefinir senha.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="reset-password-container">

      <div className="reset-password-card">

        <div className="reset-password-brand">

          <div className="reset-password-brand-icon">
            <TrendingUp
              size={34}
              strokeWidth={2.5}
            />
          </div>

          <span>CREDIFAB</span>

        </div>

        <div className="reset-password-header">

          <h1 className="reset-password-title">
            Redefinir senha
          </h1>

          <p className="reset-password-description">
            Crie uma nova senha segura para sua conta.
          </p>

        </div>

        <form
          className="reset-password-form"
          onSubmit={handleSubmit}
        >

          <div className="reset-password-field-group">

            <label className="reset-password-label">
              Nova senha
            </label>

            <input
              className="reset-password-input"
              type="password"
              placeholder="Digite sua nova senha"
              value={newPassword}
              onChange={(event) =>
                setNewPassword(event.target.value)
              }
              required
            />

          </div>

          <div className="reset-password-field-group">

            <label className="reset-password-label">
              Confirmar senha
            </label>

            <input
              className="reset-password-input"
              type="password"
              placeholder="Confirme sua nova senha"
              value={confirmPassword}
              onChange={(event) =>
                setConfirmPassword(event.target.value)
              }
              required
            />

          </div>

          {successMessage && (
            <div className="reset-password-success">
              {successMessage}
            </div>
          )}

          {errorMessage && (
            <div className="reset-password-error">
              {errorMessage}
            </div>
          )}

          <button
            className="reset-password-button"
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Redefinindo...'
              : 'Redefinir senha'}
          </button>

          <a
            className="reset-password-link"
            href="/login"
          >
            Voltar para login
          </a>

        </form>

      </div>

    </section>
  );
}