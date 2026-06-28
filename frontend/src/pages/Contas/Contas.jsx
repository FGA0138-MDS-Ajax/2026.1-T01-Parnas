import React, { useState } from 'react';
import PageHeader from '../../components/Finance/PageHeader';
import SummaryCards from '../../components/Finance/SummaryCards';
import FilterPanel from '../../components/Finance/FilterPanel';
import useContas from './Usecontas';
import ModalConta from './Modalconta';
import ConfirmacaoQuitar from './Confirmacaoquitar';
import ConfirmacaoExclusaoConta from './Confirmacaoexclusaoconta';
import formatCurrency from '../../utils/formatCurrency';
import formatDate from '../../utils/formatDate';
import './Contas.css';

const isVencida = (dataVencimento, status) => {
  if (status === 'quitada') return false;
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  const venc = new Date(dataVencimento + 'T00:00:00');
  return venc < hoje;
};

const Contas = () => {
  const {
    pendentes,
    quitadas,
    filtros,
    carregando,
    erro,
    feedback,
    categorias,
    contasCaixa,
    totalPendentesReceitas,
    totalPendentesDespesas,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
    salvarConta,
    removerConta,
    liquidarConta,
  } = useContas();

  // Estado dos modais
  const [modalAberto, setModalAberto] = useState(false);
  const [contaParaEditar, setContaParaEditar] = useState(null);
  const [confirmacaoQuitarAberta, setConfirmacaoQuitarAberta] = useState(false);
  const [contaParaQuitar, setContaParaQuitar] = useState(null);
  const [confirmacaoExclusaoAberta, setConfirmacaoExclusaoAberta] = useState(false);
  const [contaParaExcluir, setContaParaExcluir] = useState(null);

  // Ações de modal
  const abrirModalNova = () => {
    setContaParaEditar(null);
    setModalAberto(true);
  };

  const abrirModalEditar = (conta) => {
    setContaParaEditar(conta);
    setModalAberto(true);
  };

  const fecharModal = () => {
    setModalAberto(false);
    setContaParaEditar(null);
  };

  const handleSalvar = async (dados) => {
    await salvarConta(dados, contaParaEditar?.id);
    fecharModal();
  };

  const abrirConfirmacaoQuitar = (conta) => {
    setContaParaQuitar(conta);
    setConfirmacaoQuitarAberta(true);
  };

  const confirmarQuitar = async () => {
    if (!contaParaQuitar) return;
    await liquidarConta(contaParaQuitar.id);
    setConfirmacaoQuitarAberta(false);
    setContaParaQuitar(null);
  };

  const cancelarQuitar = () => {
    setConfirmacaoQuitarAberta(false);
    setContaParaQuitar(null);
  };

  const abrirConfirmacaoExclusao = (conta) => {
    setContaParaExcluir(conta);
    setConfirmacaoExclusaoAberta(true);
  };

  const confirmarExclusao = async () => {
    if (!contaParaExcluir) return;
    await removerConta(contaParaExcluir.id);
    setConfirmacaoExclusaoAberta(false);
    setContaParaExcluir(null);
  };

  const cancelarExclusao = () => {
    setConfirmacaoExclusaoAberta(false);
    setContaParaExcluir(null);
  };

  return (
    <div className="contas-container">

      {/* Feedback toast */}
      {feedback && (
        <div className={`contas-feedback contas-feedback--${feedback.tipo}`}>
          {feedback.tipo === 'sucesso' ? '✓' : '✕'} {feedback.mensagem}
        </div>
      )}

      {/* Header */}
      <PageHeader
        className="contas-header"
        title="Contas a Pagar e a Receber"
        description="Gerencie seus compromissos financeiros futuros e acompanhe vencimentos."
        actionLabel="Nova Conta"
        onAction={abrirModalNova}
      />

      {/* Resumo */}
      <SummaryCards
        items={[
          { label: 'A Receber (pendente)', value: formatCurrency(totalPendentesReceitas), className: 'total-receita' },
          { label: 'A Pagar (pendente)', value: formatCurrency(totalPendentesDespesas), className: 'total-despesa' },
          {
            label: 'Saldo Projetado',
            value: formatCurrency(totalPendentesReceitas - totalPendentesDespesas),
            className: totalPendentesReceitas - totalPendentesDespesas >= 0 ? 'saldo-positivo' : 'saldo-negativo',
          },
        ]}
      />

      {/* Filtros */}
      <FilterPanel onClear={limparFiltros} onApply={aplicarFiltros}>
        <div className="filtro-group">
          <label>Tipo</label>
          <select name="tipo" value={filtros.tipo} onChange={handleFiltroChange}>
            <option value="">Todos</option>
            <option value="receita">A Receber</option>
            <option value="despesa">A Pagar</option>
          </select>
        </div>
        <div className="filtro-group">
          <label>Status</label>
          <select name="status" value={filtros.status} onChange={handleFiltroChange}>
            <option value="">Todos</option>
            <option value="pendente">Pendente</option>
            <option value="quitada">Quitada</option>
          </select>
        </div>
        <div className="filtro-group">
          <label>Vencimento inicial</label>
          <input type="date" name="dataInicio" value={filtros.dataInicio} onChange={handleFiltroChange} />
        </div>
        <div className="filtro-group">
          <label>Vencimento final</label>
          <input type="date" name="dataFim" value={filtros.dataFim} onChange={handleFiltroChange} />
        </div>
      </FilterPanel>

      {/* Estado de carregamento / erro */}
      {carregando && (
        <div className="transacoes-vazio"><p>Carregando contas...</p></div>
      )}
      {erro && !carregando && (
        <div className="contas-erro"><p>Erro ao carregar contas: {erro}</p></div>
      )}

      {/* Seção: Pendentes */}
      {!carregando && (
        <>
          <div className="contas-secao">
            <div className="contas-secao-header">
              <h3 className="contas-secao-titulo">
                Pendentes
                <span className="contas-secao-badge">{pendentes.length}</span>
              </h3>
            </div>

            {pendentes.length === 0 ? (
              <div className="transacoes-vazio">
                <p>Nenhuma conta pendente encontrada.</p>
              </div>
            ) : (
              <div className="transacoes-tabela-wrapper">
                <table className="transacoes-tabela">
                  <thead>
                    <tr>
                      <th>Descrição</th>
                      <th>Categoria</th>
                      <th>Conta/Caixa</th>
                      <th>Tipo</th>
                      <th>Vencimento</th>
                      <th>Valor</th>
                      <th className="col-acoes" style={{ textAlign: 'center' }}>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pendentes.map((conta) => {
                      const vencida = isVencida(conta.dataVencimento, conta.status);
                      return (
                        <tr key={conta.id} className={vencida ? 'conta-vencida' : ''}>
                          <td>
                            {conta.descricao}
                            {vencida && <span className="badge-vencida">Vencida</span>}
                          </td>
                          <td>{conta.categoriaNome || 'Sem categoria'}</td>
                          <td>{conta.contaCaixaNome || 'Sem conta/caixa'}</td>
                          <td>
                            <span className={`badge badge-${conta.tipo}`}>
                              {conta.tipo === 'receita' ? '↑ A Receber' : '↓ A Pagar'}
                            </span>
                          </td>
                          <td className={vencida ? 'data-vencida' : ''}>
                            {formatDate(conta.dataVencimento)}
                          </td>
                          <td className={`valor-${conta.tipo}`}>
                            {formatCurrency(conta.valor)}
                          </td>
                          <td className="col-acoes" style={{ textAlign: 'center' }}>
                            <button
                              className="btn-acao btn-quitar"
                              onClick={() => abrirConfirmacaoQuitar(conta)}
                              title="Quitar conta"
                            >
                              ✓
                            </button>
                            <button
                              className="btn-acao btn-editar"
                              onClick={() => abrirModalEditar(conta)}
                              title="Editar conta"
                            >
                              ✎
                            </button>
                            <button
                              className="btn-acao btn-excluir"
                              onClick={() => abrirConfirmacaoExclusao(conta)}
                              title="Excluir conta"
                            >
                              ✕
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Seção: Quitadas */}
          <div className="contas-secao">
            <div className="contas-secao-header">
              <h3 className="contas-secao-titulo contas-secao-titulo--quitadas">
                Quitadas
                <span className="contas-secao-badge contas-secao-badge--quitadas">{quitadas.length}</span>
              </h3>
            </div>

            {quitadas.length === 0 ? (
              <div className="transacoes-vazio">
                <p>Nenhuma conta quitada encontrada.</p>
              </div>
            ) : (
              <div className="transacoes-tabela-wrapper">
                <table className="transacoes-tabela">
                  <thead>
                    <tr>
                      <th>Descrição</th>
                      <th>Categoria</th>
                      <th>Conta/Caixa</th>
                      <th>Tipo</th>
                      <th>Vencimento</th>
                      <th>Data Quitação</th>
                      <th>Valor</th>
                      <th className="col-acoes" style={{ textAlign: 'center' }}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {quitadas.map((conta) => (
                      <tr key={conta.id} className="conta-quitada">
                        <td>{conta.descricao}</td>
                        <td>{conta.categoriaNome || 'Sem categoria'}</td>
                        <td>{conta.contaCaixaNome || 'Sem conta/caixa'}</td>
                        <td>
                          <span className={`badge badge-${conta.tipo}`}>
                            {conta.tipo === 'receita' ? '↑ A Receber' : '↓ A Pagar'}
                          </span>
                        </td>
                        <td>{formatDate(conta.dataVencimento)}</td>
                        <td>{formatDate(conta.dataQuitacao)}</td>
                        <td className={`valor-${conta.tipo}`}>
                          {formatCurrency(conta.valor)}
                        </td>
                        <td className="col-acoes" style={{ textAlign: 'center' }}>
                          <span className="badge-status-quitada">✓ Quitada</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}

      {/* Modais */}
      {modalAberto && (
        <ModalConta
          contaParaEditar={contaParaEditar}
          categorias={categorias}
          contasCaixa={contasCaixa}
          onSalvar={handleSalvar}
          onFechar={fecharModal}
        />
      )}

      {confirmacaoQuitarAberta && (
        <ConfirmacaoQuitar
          conta={contaParaQuitar}
          onConfirmar={confirmarQuitar}
          onCancelar={cancelarQuitar}
        />
      )}

      {confirmacaoExclusaoAberta && (
        <ConfirmacaoExclusaoConta
          conta={contaParaExcluir}
          onConfirmar={confirmarExclusao}
          onCancelar={cancelarExclusao}
        />
      )}
    </div>
  );
};

export default Contas;
