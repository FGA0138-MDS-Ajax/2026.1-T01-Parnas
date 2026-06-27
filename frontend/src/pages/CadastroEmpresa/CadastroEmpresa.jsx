import React, { useState } from 'react';
import { useEmpresa } from '../../context/EmpresaContext';
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
  const [loading, setLoading] = useState(false);

  const { setIdEmpresaLogada } = useEmpresa();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (eventoFormulario) => {
    eventoFormulario.preventDefault();
    setError('');
    setSuccess(false);
    setLoading(true);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('Sessão expirada. Por favor, faça login novamente.');
      setLoading(false);
      return;
    }

    const cnpjApenasNumeros = formData.cnpj.replace(/\D/g, '');

    try {
      const response = await fetch('/api/companies/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: formData.nome,
          cnpj: cnpjApenasNumeros,
          email: formData.email,
          phone: formData.telefone
        })
      });

      const responseText = await response.text();
      const data = responseText ? JSON.parse(responseText) : {};

      if (!response.ok) {
        if (data.erros_de_validacao) {
          const mensagensDeErro = Object.values(data.erros_de_validacao).flat().join(' ');
          throw new Error(mensagensDeErro);
        }
        throw new Error(data.erro || 'Erro ao cadastrar empresa.');
      }

      setIdEmpresaLogada(data.company_id);
      setSuccess(true);

      const historicoReal = JSON.parse(localStorage.getItem('credifab_empresas_reais') || '[]');
      historicoReal.push({
        company_id: data.company_id,
        name: data.name || formData.nome,
        cnpj: data.cnpj || cnpjApenasNumeros,
        email: formData.email,
        phone: formData.telefone
      });
      localStorage.setItem('credifab_empresas_reais', JSON.stringify(historicoReal));

      setFormData({ nome: '', cnpj: '', email: '', telefone: '' });

    } catch (err) {
      setError(err.message || 'Ocorreu um erro ao tentar cadastrar a empresa.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cadastro-empresa-pagina">
      <div className="container-cadastro">
        <div className="form-content">
          <div className="form-header">
            <h2>Cadastro de Nova Empresa</h2>
          </div>

          {error && <p className="msg-error">{error}</p>}
          {success && <p className="msg-success">Empresa cadastrada com sucesso!</p>}

          <form onSubmit={handleSubmit} className="form-grid">
            <div className="input-group">
              <label>Nome da empresa</label>
              <input
                type="text"
                name="nome"
                placeholder="Nome da sua empresa"
                value={formData.nome}
                onChange={handleChange}
                disabled={loading}
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
                disabled={loading}
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
                disabled={loading}
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
                disabled={loading}
                required
              />
            </div>

            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? 'Cadastrando...' : 'Cadastrar Empresa'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CadastroEmpresa;