import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../../components/Finance/PageHeader';
import { CONTAS_CAIXA_MOCK } from '../../services/contaCaixa.service';
import '../Transacoes/Transacoes.css';
import './ContasCaixa.css';

const ContasCaixa = () => {
  const navigate = useNavigate();
  const [nome, setNome] = useState('');
  const [contasCaixa, setContasCaixa] = useState(CONTAS_CAIXA_MOCK);

  const handleSubmit = (e) => {
    e.preventDefault();
    const nomeNormalizado = nome.trim();
    if (!nomeNormalizado) return;

    setContasCaixa((prev) => [
      ...prev,
      { id: Date.now(), nome: nomeNormalizado },
    ]);
    setNome('');
  };

  return (
    <div className="contas-caixa-container">
      <PageHeader
        className="transacoes-header"
        title="Contas/Caixas"
        description="Cadastre as contas bancárias e caixas usados nas contas a pagar e a receber."
      />

      <button
        type="button"
        className="btn-voltar-contas"
        onClick={() => navigate('/contas')}
      >
        Voltar para Contas
      </button>

      <section className="contas-caixa-card">
        <h3>Nova Conta/Caixa</h3>
        <form className="contas-caixa-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ex.: Inter, Caixa Vendas, Dinheiro em Especie"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            required
          />
          <button type="submit" className="btn-submit">Adicionar</button>
        </form>
      </section>

      <section className="transacoes-tabela-wrapper">
        <table className="transacoes-tabela">
          <thead>
            <tr>
              <th>Nome</th>
            </tr>
          </thead>
          <tbody>
            {contasCaixa.map((contaCaixa) => (
              <tr key={contaCaixa.id}>
                <td>{contaCaixa.nome}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default ContasCaixa;
