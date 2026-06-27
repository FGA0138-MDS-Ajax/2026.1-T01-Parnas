import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  BarChart2,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';
import useDashboard from '../../hooks/useDashboard';
import './Dashboard.css';

const CORES_CATEGORIAS = [
  '#0F4C81',
  '#03906C',
  '#e67e22',
  '#8e44ad',
  '#c0392b',
  '#2980b9',
  '#16a085',
];

const formatarMoeda = (valor) =>
  Number(valor ?? 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const formatarData = (dataStr) => {
  if (!dataStr) return '';
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
};

const SkeletonKpiCard = () => (
  <div className="dash-kpi-card dash-kpi-card--skeleton">
    <div className="skeleton skeleton--icon" />
    <div className="skeleton skeleton--label" />
    <div className="skeleton skeleton--value" />
    <div className="skeleton skeleton--sub" />
  </div>
);

const Dashboard = () => {
  const navigate = useNavigate();
  const { dados, carregando, erro, recarregar, idEmpresaLogada } = useDashboard();

  if (!idEmpresaLogada && !carregando) {
    return (
      <div className="dash-container">
        <div className="dash-header">
          <div>
            <h2>Dashboard Financeiro</h2>
            <p>Visualize os dados consolidados da sua empresa ativa.</p>
          </div>
        </div>
        <div className="dash-state-card dash-empty-state">
          <span className="dash-state-emoji">🏢</span>
          <h3>Nenhuma empresa selecionada</h3>
          <p>Selecione ou cadastre uma empresa para visualizar o dashboard financeiro.</p>
          <button className="btn-dash-primary" onClick={() => navigate('/cadastro-empresa')}>
            Cadastrar Empresa
          </button>
        </div>
      </div>
    );
  }

  if (erro && !carregando) {
    return (
      <div className="dash-container">
        <div className="dash-header">
          <div>
            <h2>Dashboard Financeiro</h2>
            <p>Visualize os dados consolidados da sua empresa ativa.</p>
          </div>
        </div>
        <div className="dash-state-card dash-error-state">
          <AlertCircle size={40} className="dash-error-icon" />
          <h3>Erro ao carregar dados</h3>
          <p>{erro}</p>
          <button className="btn-dash-retry" onClick={recarregar}>
            <RefreshCw size={15} />
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  const totais = dados?.totais_mes_atual;
  const categorias = dados?.grafico_categorias_mes ?? [];
  const contas = dados?.contas_proximas_vencimento ?? [];
  const saldoConsolidado = dados?.saldo_consolidado_atual ?? 0;
  const balancoPositivo = (totais?.balanco_mensal ?? 0) >= 0;
  const saldoPositivo = saldoConsolidado >= 0;

  return (
    <div className="dash-container">

      {/* ── Cabeçalho ── */}
      <div className="dash-header">
        <div>
          <h2>Dashboard Financeiro</h2>
          <p>
            {carregando
              ? 'Carregando dados...'
              : dados
              ? `Visão consolidada — mês de referência: ${dados.mes_referencia}`
              : 'Visualize os dados consolidados da sua empresa ativa.'}
          </p>
        </div>
        {!carregando && (
          <button className="btn-dash-reload" onClick={recarregar} title="Atualizar dados">
            <RefreshCw size={15} />
            Atualizar
          </button>
        )}
      </div>

      {/* ── KPI Cards ── */}
      <div className="dash-kpi-grid">
        {carregando ? (
          <>
            <SkeletonKpiCard />
            <SkeletonKpiCard />
            <SkeletonKpiCard />
            <SkeletonKpiCard />
          </>
        ) : (
          <>
            <div className="dash-kpi-card">
              <div className="kpi-icon-wrapper kpi-icon--saldo">
                <DollarSign size={20} />
              </div>
              <span className="kpi-label">Saldo Consolidado</span>
              <span className={`kpi-value ${saldoPositivo ? 'kpi-value--positivo' : 'kpi-value--negativo'}`}>
                {formatarMoeda(saldoConsolidado)}
              </span>
              <span className="kpi-sub">Acumulado total</span>
            </div>

            <div className="dash-kpi-card">
              <div className="kpi-icon-wrapper kpi-icon--receitas">
                <TrendingUp size={20} />
              </div>
              <span className="kpi-label">Receitas do Mês</span>
              <span className="kpi-value kpi-value--positivo">
                {formatarMoeda(totais?.receitas)}
              </span>
              <span className="kpi-sub">{dados?.mes_referencia}</span>
            </div>

            <div className="dash-kpi-card">
              <div className="kpi-icon-wrapper kpi-icon--despesas">
                <TrendingDown size={20} />
              </div>
              <span className="kpi-label">Despesas do Mês</span>
              <span className="kpi-value kpi-value--negativo">
                {formatarMoeda(totais?.despesas)}
              </span>
              <span className="kpi-sub">{dados?.mes_referencia}</span>
            </div>

            <div className="dash-kpi-card">
              <div className={`kpi-icon-wrapper ${balancoPositivo ? 'kpi-icon--balanco-pos' : 'kpi-icon--balanco-neg'}`}>
                <BarChart2 size={20} />
              </div>
              <span className="kpi-label">Balanço do Mês</span>
              <span className={`kpi-value ${balancoPositivo ? 'kpi-value--positivo' : 'kpi-value--negativo'}`}>
                {formatarMoeda(totais?.balanco_mensal)}
              </span>
              <span className="kpi-sub">{dados?.mes_referencia}</span>
            </div>
          </>
        )}
      </div>

      {/* ── Gráfico + Contas ── */}
      <div className="dash-content-grid">

        {/* Gráfico de Categorias */}
        <div className="dash-card">
          <h3 className="dash-card-titulo">Despesas por Categoria</h3>
          <p className="dash-card-sub">
            {carregando ? ' ' : (dados?.mes_referencia ?? '')}
          </p>

          {carregando ? (
            <div className="skeleton skeleton--chart" />
          ) : categorias.length === 0 ? (
            <div className="dash-empty-section">
              <p>Sem despesas registradas por categoria neste mês.</p>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={290}>
              <PieChart>
                <Pie
                  data={categorias}
                  dataKey="total"
                  nameKey="categoria"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  paddingAngle={3}
                >
                  {categorias.map((_, i) => (
                    <Cell
                      key={i}
                      fill={CORES_CATEGORIAS[i % CORES_CATEGORIAS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value, name) => [formatarMoeda(value), name]}
                  contentStyle={{
                    borderRadius: '10px',
                    border: '1px solid #E2E8F0',
                    fontSize: '0.85rem',
                    fontFamily: 'Poppins, sans-serif',
                  }}
                />
                <Legend
                  formatter={(value) => (
                    <span style={{ fontSize: '0.78rem', color: '#1A202C' }}>{value}</span>
                  )}
                />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Contas Próximas */}
        <div className="dash-card">
          <h3 className="dash-card-titulo">Contas Próximas do Vencimento</h3>
          <p className="dash-card-sub">Próximas pendências em aberto</p>

          {carregando ? (
            <div className="dash-bills-skeleton">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="skeleton skeleton--bill" />
              ))}
            </div>
          ) : contas.length === 0 ? (
            <div className="dash-empty-section">
              <p>Nenhuma conta pendente nos próximos dias.</p>
            </div>
          ) : (
            <ul className="dash-bills-list">
              {contas.map((conta) => (
                <li key={conta.id} className="dash-bill-item">
                  <div className="bill-info">
                    <span className="bill-desc">{conta.descricao}</span>
                    <span className="bill-date">{formatarData(conta.data_vencimento)}</span>
                  </div>
                  <div className="bill-right">
                    <span
                      className={`bill-valor ${
                        conta.tipo === 'Pagar' ? 'bill-valor--pagar' : 'bill-valor--receber'
                      }`}
                    >
                      {formatarMoeda(conta.valor)}
                    </span>
                    <span
                      className={`bill-badge ${
                        conta.tipo === 'Pagar' ? 'bill-badge--pagar' : 'bill-badge--receber'
                      }`}
                    >
                      {conta.tipo}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}

          {!carregando && (
            <button
              className="btn-dash-ver-todas"
              onClick={() => navigate('/contas')}
            >
              Ver todas as contas →
            </button>
          )}
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
