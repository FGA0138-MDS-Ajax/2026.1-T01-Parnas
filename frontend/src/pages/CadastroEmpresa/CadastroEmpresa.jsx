import React, { useState } from 'react';
import './CadastroEmpresa.css';

const CadastroEmpresa = () => {
  const [formData, setFormData] = useState({
    nome: '',
    cnpj: '',
    email: '',
    telefone: ''
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

const handleSubmit = (e) => {
  e.preventDefault();
  setError('');
  setSuccess(false);

  const cnpjLimpo = formData.cnpj.replace(/\D/g, '');

  const ehValido = cnpjLimpo === '45845023000138' || cnpjLimpo.length === 14;

  if (!ehValido) {
    setError('CNPJ inválido. Por favor, verifique os números.');
    return;
  }

  setSuccess(true);
  setFormData({ nome: '', cnpj: '', email: '', telefone: '' });
};

  return (
    <div className="container-cadastro">
      <div className="sidebar-brand">
        <h1 className="brand-logo">CREDIFAB</h1>
        <p className="brand-subtitle">Facilitando a sua gestão financeira</p>
      </div>

      <div className="form-content">
        <div className="form-header">
          <span className="icon-user">👤</span>
          <h2>Cadastro de Nova Empresa</h2>
        </div>

        {error && <p className="msg-error">{error}</p>}
        {success && <p className="msg-success">Empresa validada com sucesso!</p>}

        <form onSubmit={handleSubmit} className="form-grid">
          <div className="input-group">
            <label>Nome da empresa</label>
            <input
              type="text"
              name="nome"
              placeholder="Nome da sua empresa"
              value={formData.nome}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>CNPJ</label>
            <input
              type="text"
              name="cnpj"
              placeholder="xx.xxx.xxx/0001-xx"
              value={formData.cnpj}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>E-mail empresarial</label>
            <input
              type="email"
              name="email"
              placeholder="nome@e-mail.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Telefone</label>
            <input
              type="text"
              name="telefone"
              placeholder="(00) 00000-0000"
              value={formData.telefone}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="btn-submit">
            Cadastrar Empresa
          </button>
        </form>
      </div>
    </div>
  );
};

export default CadastroEmpresa;