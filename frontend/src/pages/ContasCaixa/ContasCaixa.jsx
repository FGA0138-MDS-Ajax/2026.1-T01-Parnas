import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/Finance/PageHeader";
import {
  listarContasCaixa,
  criarContaCaixa,
  excluirContaCaixa,
} from "../../services/contaCaixa.service";
import "../Transacoes/Transacoes.css";
import "./ContasCaixa.css";

const ContasCaixa = () => {
  const navigate = useNavigate();
  const [nome, setNome] = useState("");
  const [contasCaixa, setContasCaixa] = useState([]);

  useEffect(() => {
    listarContasCaixa().then(setContasCaixa);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nome.trim()) return;

    const novaConta = await criarContaCaixa(nome);
    setContasCaixa((prev) => [...prev, novaConta]);
    setNome("");
  };

  const handleExcluir = async (id) => {
    if (window.confirm("Deseja realmente excluir esta Conta/Caixa?")) {
      await excluirContaCaixa(id);
      setContasCaixa((prev) => prev.filter((c) => c.id !== id));
    }
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
        onClick={() => navigate("/contas")}
      >
        Voltar para Contas
      </button>

      <section className="contas-caixa-card">
        <h3>Nova Conta/Caixa</h3>
        <form className="contas-caixa-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ex.: Inter, Caixa Vendas, Dinheiro em Espécie"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            required
          />
          <button type="submit" className="btn-submit">
            Adicionar
          </button>
        </form>
      </section>

      <section className="transacoes-tabela-wrapper">
        <table className="transacoes-tabela">
          <thead>
            <tr>
              <th>Nome</th>
              <th style={{ textAlign: "right" }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {contasCaixa.length === 0 ? (
              <tr>
                <td colSpan="2" style={{ textAlign: "center" }}>
                  Nenhuma conta cadastrada.
                </td>
              </tr>
            ) : (
              contasCaixa.map((conta) => (
                <tr key={conta.id}>
                  <td>{conta.nome}</td>
                  <td style={{ textAlign: "right" }}>
                    <button
                      className="btn-acao btn-excluir"
                      onClick={() => handleExcluir(conta.id)}
                    >
                      ✕ Excluir
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default ContasCaixa;
