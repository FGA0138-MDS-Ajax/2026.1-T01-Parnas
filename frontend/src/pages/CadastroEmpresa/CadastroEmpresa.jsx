import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  const [loading, setLoading] = useState(false);

  const { recarregarEmpresas, selecionarEmpresa } = useEmpresa();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (eventoFormulario) => {
    eventoFormulario.preventDefault();
    setError('');
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
        if (response.status === 401) {
          localStorage.removeItem('token');
          navigate('/login');
          return;
        }
        if (response.status === 409) {
          throw new Error(data.erro || 'Dado já cadastrado. Verifique o CNPJ e o e-mail informados.');
        }
        if (data.erros_de_validacao) {
          const mensagensDeErro = Object.values(data.erros_de_validacao).flat().join(' ');
          throw new Error(mensagensDeErro);
        }
        throw new Error(data.erro || data.msg || 'Erro ao cadastrar empresa.');
      }

      const empresasAtualizadas = await recarregarEmpresas();
      if (empresasAtualizadas.length !== 1) {
        await selecionarEmpresa({
          company_id: data.company_id,
          name: data.name || formData.nome,
          cnpj: data.cnpj || cnpjApenasNumeros,
        });
      }
      navigate('/selecao-empresa');

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
