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

  const { setIdEmpresaLogada } = useEmpresa();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (eventoFormulario) => {
    eventoFormulario.preventDefault();
    setError('');
    setSuccess(false);

    const cnpjApenasNumeros = formData.cnpj.replace(/\D/g, '');

    const quantidadeDigitosCnpjValido = 14;
    const cnpjPossuiFormatoValido = cnpjApenasNumeros === '45845023000138' || cnpjApenasNumeros.length === quantidadeDigitosCnpjValido;

    if (!cnpjPossuiFormatoValido) {
      setError('CNPJ inválido. Por favor, verifique os números.');
      return;
    }

    // SIMULAÇÃO DO CONTRATO DE INTEGRAÇÃO COM POST /api/companies/register
    const corpoRequisicaoParaBackend = {
      name: formData.nome,
      cnpj: cnpjApenasNumeros,
      email: formData.email,
      phone: formData.telefone
    };

    // GERANDO ID IDENTIFICADOR SIMULADO DO BANCO DE DADOS
    const idEmpresaGeradoPeloBancoSimulado = Math.floor(Math.random() * 5000) + 1;

    // SALVANDO ID NO CONTEXTO GLOBAL
    setIdEmpresaLogada(idEmpresaGeradoPeloBancoSimulado);

    setSuccess(true);
    setFormData({ nome: '', cnpj: '', email: '', telefone: '' });

    // Registros limpos no console para auditoria/teste
    console.log('[MOCK API] Dados preparados para o contrato da API:', corpoRequisicaoParaBackend);
    console.log('[MOCK CONTEXTO] ID salvo globalmente:', idEmpresaGeradoPeloBancoSimulado);
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