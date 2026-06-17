import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useTransacoes from '../../hooks/useTransacoes';
import ModalTransacao from './ModalTransacao'; // Agora estão na mesma pasta!
import ConfirmacaoExclusao from './ConfirmacaoExclusao'; // Agora estão na mesma pasta!
import './Transacoes.css'; // Nome do CSS atualizado

const formatarMoeda = (valor) =>
  valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const formatarData = (dataStr) => {
  if (!dataStr) return '';
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
};

const Transacoes = () => { // Nome do componente alterado
  const navigate = useNavigate();
  const {
    filtros,
    transacoes,
    totais,
    paginaAtual,
    totalPaginas,
    totalTransacoes,
    categorias,
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

      <div className="transacoes-header">
        <div>
          <h2>Transações Financeiras</h2> {/* Título mais limpo e direto */}
          <p>Cadastre, consulte e filtre as movimentações financeiras da sua empresa.</p>
        </div>
        <button className="btn-nova-transacao" onClick={abrirModalNova}>
          <span className="btn-icon">+</span>
          Nova Transação
        </button>
      </div>

      <div className="transacoes-totais">
        <div className="total-card total-receita">
          <span className="total-label">Total de Receitas</span>
          <span className="total-valor">{formatarMoeda(totais.totalReceitas || 0)}</span>
        </div>
        <div className="total-card total-despesa">
          <span className="total-label">Total de Despesas</span>
          <span className="total-valor">{formatarMoeda(totais.totalDespesas || 0)}</span>
        </div>
        <div className={`total-card ${(totais.saldo || 0) >= 0 ? 'saldo-positivo' : 'saldo-negativo'}`}>
          <span className="total-label">Saldo</span>
          <span className="total-valor">{formatarMoeda(totais.saldo || 0)}</span>
        </div>
      </div>

      <div className="transacoes-filtros">
        <div className="filtros-grid">
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
            <label>Valor mínimo (R$)</label>
            <input type="number" name="valorMin" placeholder="0,00" value={filtros.valorMin} onChange={handleFiltroChange} min="0" />
          </div>
          <div className="filtro-group">
            <label>Valor máximo (R$)</label>
            <input type="number" name="valorMax" placeholder="0,00" value={filtros.valorMax} onChange={handleFiltroChange} min="0" />
          </div>
        </div>
        <div className="filtros-acoes">
          <button className="btn-limpar" onClick={limparFiltros}>Limpar filtros</button>
          <button className="btn-aplicar" onClick={aplicarFiltros}>Aplicar filtros</button>
        </div>
      </div>

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
                <th>Tipo</th>
                <th>Valor</th>
                <th className="col-acoes" style={{ textAlign: 'center' }}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {transacoes.map((t) => (
                <tr key={t.id}>
                  <td>{formatarData(t.data)}</td>
                  <td>{t.descricao}</td>
                  <td>{t.categoria || t.categoriaNome}</td>
                  <td>
                    <span className={`badge badge-${t.tipo}`}>
                      {t.tipo === 'receita' ? '↑ Receita' : '↓ Despesa'}
                    </span>
                  </td>
                  <td className={`valor-${t.tipo}`}>
                    {t.tipo === 'despesa' ? '- ' : '+ '}
                    {formatarMoeda(t.valor)}
                  </td>
                  <td className="col-acoes" style={{ textAlign: 'center' }}>
                    <button
                      className="btn-acao btn-editar"
                      onClick={() => abrirModalEditar(t)}
                      title="Editar transação"
                    >
                      ✎
                    </button>
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
