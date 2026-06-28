import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../../components/Finance/PageHeader';
import SummaryCards from '../../components/Finance/SummaryCards';
import FilterPanel from '../../components/Finance/FilterPanel';
import useTransacoes from '../../hooks/useTransacoes';
import ModalTransacao from './ModalTransacao'; // Agora estão na mesma pasta!
import ConfirmacaoExclusao from './ConfirmacaoExclusao'; // Agora estão na mesma pasta!
import formatCurrency from '../../utils/formatCurrency';
import formatDate from '../../utils/formatDate';
import './Transacoes.css'; // Nome do CSS atualizado

const Transacoes = () => { // Nome do componente alterado
  const navigate = useNavigate();
  const {
    filtros,
    transacoes,
    totais,
    saldoContaSelecionada,
    contaCaixaSelecionada,
    paginaAtual,
    totalPaginas,
    totalTransacoes,
    categorias,
    contasCaixa,
    handleFiltroChange,
    aplicarFiltros,
    limparFiltros,
    mudarPagina,
    salvarTransacao, 
    excluirTransacao 
  } = useTransacoes();

  const [modalAberto, setModalAberto] = useState(false);
  const [transacaoParaEditar, setTransacaoParaEditar] = useState(null);
  const [confirmacaoAberta, setConfirmacaoAberta] = useState(false);
  const [transacaoParaExcluir, setTransacaoParaExcluir] = useState(null);

  const categoriesMapeadas = categorias.map((cat, index) => ({
    id: index + 1,
    nome: cat,
    tipo: ''
  }));

  const abrirModalNova = () => {
    setTransacaoParaEditar(null);
    setModalAberto(true);
  };

  const abrirModalEditar = (transacao) => {
    setTransacaoParaEditar(transacao);
    setModalAberto(true);
  };

  const fecharModal = () => {
    setModalAberto(false);
    setTransacaoParaEditar(null);
  };

  const handleSalvar = async (dadosFormulario) => {
    if (typeof salvarTransacao === 'function') {
      await salvarTransacao(dadosFormulario, transacaoParaEditar?.id);
    }
    fecharModal();
  };

  const abrirConfirmacaoExclusao = (transacao) => {
    setTransacaoParaExcluir(transacao);
    setConfirmacaoAberta(true);
  };

  const confirmarExclusao = async () => {
    if (typeof excluirTransacao === 'function') {
      await excluirTransacao(transacaoParaExcluir.id);
    }
    setConfirmacaoAberta(false);
    setTransacaoParaExcluir(null);
  };

  const cancelarExclusao = () => {
    setConfirmacaoAberta(false);
    setTransacaoParaExcluir(null);
  };

  return (
    <div className="transacoes-container"> {/* Classe base atualizada */}

      <PageHeader
        className="transacoes-header"
        title="Transações Financeiras"
        description="Cadastre, consulte e filtre as movimentações financeiras da sua empresa."
        actionLabel="Nova Transação"
        onAction={abrirModalNova}
      />

      <SummaryCards
        items={[
          { label: 'Total de Receitas', value: formatCurrency(totais.totalReceitas), className: 'total-receita' },
          { label: 'Total de Despesas', value: formatCurrency(totais.totalDespesas), className: 'total-despesa' },
          {
            label: 'Saldo',
            value: formatCurrency(totais.saldo),
            className: (totais.saldo || 0) >= 0 ? 'saldo-positivo' : 'saldo-negativo',
          },
          ...(saldoContaSelecionada !== null ? [{
            label: `Saldo Atual - ${contaCaixaSelecionada?.nome || 'Conta/Caixa'}`,
            value: formatCurrency(saldoContaSelecionada),
            className: saldoContaSelecionada >= 0 ? 'saldo-positivo' : 'saldo-negativo',
          }] : []),
        ]}
      />

      <FilterPanel onClear={limparFiltros} onApply={aplicarFiltros}>
        <div className="filtro-group">
          <label>Data inicial</label>
          <input type="date" name="dataInicio" value={filtros.dataInicio} onChange={handleFiltroChange} />
        </div>
        <div className="filtro-group">
          <label>Data final</label>
          <input type="date" name="dataFim" value={filtros.dataFim} onChange={handleFiltroChange} />
        </div>
        <div className="filtro-group">
          <label>Tipo</label>
          <select name="tipo" value={filtros.tipo} onChange={handleFiltroChange}>
            <option value="">Todos</option>
            <option value="receita">Receita</option>
            <option value="despesa">Despesa</option>
          </select>
        </div>
        <div className="filtro-group">
          <div className="campo-label-acoes">
            <label>Categoria</label>
            <button
              type="button"
              className="btn-link-categoria"
              onClick={() => navigate('/categorias')}
            >
              Cadastrar
            </button>
          </div>
          <select name="categoria" value={filtros.categoria} onChange={handleFiltroChange}>
            <option value="">Todas</option>
            {categorias.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div className="filtro-group">
          <div className="campo-label-acoes">
            <label>Conta/Caixa</label>
            <button
              type="button"
              className="btn-link-categoria"
              onClick={() => navigate('/contas-caixa')}
            >
              Cadastrar
            </button>
          </div>
          <select name="contaCaixaId" value={filtros.contaCaixaId} onChange={handleFiltroChange}>
            <option value="">Todas</option>
            {contasCaixa.map((contaCaixa) => (
              <option key={contaCaixa.id} value={contaCaixa.id}>
                {contaCaixa.nome}
              </option>
            ))}
          </select>
        </div>
        <div className="filtro-group">
          <label>Valor mínimo (R$)</label>
          <input type="number" name="valorMin" placeholder="0,00" value={filtros.valorMin} onChange={handleFiltroChange} min="0" />
        </div>
        <div className="filtro-group">
          <label>Valor máximo (R$)</label>
          <input type="number" name="valorMax" placeholder="0,00" value={filtros.valorMax} onChange={handleFiltroChange} min="0" />
        </div>
      </FilterPanel>

      <div className="transacoes-tabela-wrapper">
        <div className="tabela-info">
          <span>{totalTransacoes} transação(ões) encontrada(s)</span>
        </div>

        {transacoes.length === 0 ? (
          <div className="transacoes-vazio">
            <p>Nenhuma transação encontrada com os filtros aplicados.</p>
          </div>
        ) : (
          <table className="transacoes-tabela">
            <thead>
              <tr>
                <th>Data</th>
                <th>Descrição</th>
                <th>Categoria</th>
                <th>Conta/Caixa</th>
                <th>Tipo</th>
                <th>Valor</th>
                <th className="col-acoes" style={{ textAlign: 'center' }}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {transacoes.map((t) => (
                <tr key={t.id}>
                  <td>{formatDate(t.data)}</td>
                  <td>{t.descricao}</td>
                  <td>{t.categoria || t.categoriaNome}</td>
                  <td>{t.contaCaixaNome || 'Sem conta/caixa'}</td>
                  <td>
                    <span className={`badge badge-${t.tipo}`}>
                      {t.tipo === 'receita' ? '↑ Receita' : '↓ Despesa'}
                    </span>
                  </td>
                  <td className={`valor-${t.tipo}`}>
                    {t.tipo === 'despesa' ? '- ' : '+ '}
                    {formatCurrency(t.valor)}
                  </td>
                  <td className="col-acoes" style={{ textAlign: 'center' }}>
                    {!t.transferenciaId && (
                      <button
                        className="btn-acao btn-editar"
                        onClick={() => abrirModalEditar(t)}
                        title="Editar transação"
                      >
                        ✎
                      </button>
                    )}
                    <button
                      className="btn-acao btn-excluir"
                      onClick={() => abrirConfirmacaoExclusao(t)}
                      title="Excluir transação"
                    >
                      ✕
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {totalPaginas > 1 && (
        <div className="transacoes-paginacao">
          <button className="btn-pagina btn-pagina-nav" onClick={() => mudarPagina(paginaAtual - 1)} disabled={paginaAtual === 1}>
            Anterior
          </button>
          {Array.from({ length: totalPaginas }, (_, i) => i + 1).map((pagina) => (
            <button
              key={pagina}
              className={`btn-pagina ${pagina === paginaAtual ? 'btn-pagina-ativa' : ''}`}
              onClick={() => mudarPagina(pagina)}
            >
              {pagina}
            </button>
          ))}
          <button className="btn-pagina btn-pagina-nav" onClick={() => mudarPagina(paginaAtual + 1)} disabled={paginaAtual === totalPaginas}>
            Próxima
          </button>
        </div>
      )}

      {modalAberto && (
        <ModalTransacao
          transacaoParaEditar={transacaoParaEditar}
          categorias={categoriesMapeadas}
          contasCaixa={contasCaixa}
          onSalvar={handleSalvar}
          onFechar={fecharModal}
        />
      )}

      {confirmacaoAberta && (
        <ConfirmacaoExclusao
          transacao={transacaoParaExcluir}
          onConfirmar={confirmarExclusao}
          onCancelar={cancelarExclusao}
        />
      )}

    </div>
  );
};

export default Transacoes; // Exportação atualizada
