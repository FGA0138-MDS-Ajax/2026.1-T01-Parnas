import React from 'react';
import useTransacoes from '../../hooks/useTransacoes';
import './Historico.css';

const formatarMoeda = (valor) =>
  valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const formatarData = (dataStr) => {
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
};

const Historico = () => {
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
  } = useTransacoes();

  return (
    <div className="historico-container">

      <div className="historico-header">
        <h2>Histórico de Transações</h2>
        <p>Consulte e filtre as movimentações financeiras da sua empresa.</p>
      </div>

      <div className="historico-totais">
        <div className="total-card total-receita">
          <span className="total-label">Total de Receitas</span>
          <span className="total-valor">{formatarMoeda(totais.totalReceitas)}</span>
        </div>
        <div className="total-card total-despesa">
          <span className="total-label">Total de Despesas</span>
          <span className="total-valor">{formatarMoeda(totais.totalDespesas)}</span>
        </div>
        <div className={`total-card ${totais.saldo >= 0 ? 'saldo-positivo' : 'saldo-negativo'}`}>
          <span className="total-label">Saldo</span>
          <span className="total-valor">{formatarMoeda(totais.saldo)}</span>
        </div>
      </div>

      <div className="historico-filtros">
        <div className="filtros-grid">
          <div className="filtro-group">
            <label>Data inicial</label>
            <input
              type="date"
              name="dataInicio"
              value={filtros.dataInicio}
              onChange={handleFiltroChange}
            />
          </div>
          <div className="filtro-group">
            <label>Data final</label>
            <input
              type="date"
              name="dataFim"
              value={filtros.dataFim}
              onChange={handleFiltroChange}
            />
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
            <label>Categoria</label>
            <select name="categoria" value={filtros.categoria} onChange={handleFiltroChange}>
              <option value="">Todas</option>
              {categorias.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
          <div className="filtro-group">
            <label>Valor mínimo (R$)</label>
            <input
              type="number"
              name="valorMin"
              placeholder="0,00"
              value={filtros.valorMin}
              onChange={handleFiltroChange}
              min="0"
            />
          </div>
          <div className="filtro-group">
            <label>Valor máximo (R$)</label>
            <input
              type="number"
              name="valorMax"
              placeholder="0,00"
              value={filtros.valorMax}
              onChange={handleFiltroChange}
              min="0"
            />
          </div>
        </div>
        <div className="filtros-acoes">
          <button className="btn-limpar" onClick={limparFiltros}>
            Limpar filtros
          </button>
          <button className="btn-aplicar" onClick={aplicarFiltros}>
            Aplicar filtros
          </button>
        </div>
      </div>

      <div className="historico-tabela-wrapper">
        <div className="tabela-info">
          <span>{totalTransacoes} transação(ões) encontrada(s)</span>
        </div>

        {transacoes.length === 0 ? (
          <div className="historico-vazio">
            <p>Nenhuma transação encontrada com os filtros aplicados.</p>
          </div>
        ) : (
          <table className="historico-tabela">
            <thead>
              <tr>
                <th>Data</th>
                <th>Descrição</th>
                <th>Categoria</th>
                <th>Tipo</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {transacoes.map((t) => (
                <tr key={t.id}>
                  <td>{formatarData(t.data)}</td>
                  <td>{t.descricao}</td>
                  <td>{t.categoria}</td>
                  <td>
                    <span className={`badge badge-${t.tipo}`}>
                      {t.tipo === 'receita' ? 'Receita' : 'Despesa'}
                    </span>
                  </td>
                  <td className={`valor-${t.tipo}`}>
                    {formatarMoeda(t.valor)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {totalPaginas > 1 && (
        <div className="historico-paginacao">
          <button
            className="btn-pagina btn-pagina-nav"
            onClick={() => mudarPagina(paginaAtual - 1)}
            disabled={paginaAtual === 1}
          >
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
          <button
            className="btn-pagina btn-pagina-nav"
            onClick={() => mudarPagina(paginaAtual + 1)}
            disabled={paginaAtual === totalPaginas}
          >
            Próxima
          </button>
        </div>
      )}

    </div>
  );
};

export default Historico;
