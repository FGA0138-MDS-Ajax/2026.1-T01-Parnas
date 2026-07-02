import React, { useState, useEffect, useCallback } from "react";
import PageHeader from "../../components/Finance/PageHeader";
import api from "../../services/api";
import { obterEmpresaAtiva } from "../../services/empresa.service";
import "./Relatorios.css";
import {
  PieChart,
  Pie,
  Tooltip,
  Cell,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  BarChart,
  Bar,
  Legend,
} from "recharts";

const formatCurrency = (valor) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    valor || 0,
  );

function Relatorios() {
  const [tipoPeriodo, setTipoPeriodo] = useState("mensal");
  const [mesAno, setMesAno] = useState(new Date().toISOString().slice(0, 7));
  const [ano, setAno] = useState(new Date().getFullYear());
  const [dataInicio, setDataInicio] = useState("");
  const [dataFim, setDataFim] = useState("");

  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");

  const [dados, setDados] = useState({
    totais: { total_receitas: 0, total_despesas: 0, saldo: 0 },
    distribuicao: [],
    evolucao: [],
    comparativo: [],
  });

  const cores = [
    "#0f4c81",
    "#2a9d8f",
    "#f4a261",
    "#e76f51",
    "#8e44ad",
    "#34495e",
  ];

  const carregarRelatorio = useCallback(async () => {
    try {
      setCarregando(true);
      setErro("");
      const empresa = await obterEmpresaAtiva();
      if (!empresa?.company_id) {
        setErro("Selecione uma empresa ativa.");
        return;
      }

      const params = {};

      if (tipoPeriodo === "mensal") {
        params.period = "mensal";
        params.year = parseInt(mesAno.split("-")[0]);
        params.month = parseInt(mesAno.split("-")[1]);
      } else if (tipoPeriodo === "anual") {
        params.period = "anual";
        params.year = ano;
      } else {
        if (!dataInicio || !dataFim) {
          setCarregando(false);
          return;
        }
        params.start_date = dataInicio;
        params.end_date = dataFim;
      }

      const { data } = await api.get(
        `/api/companies/${empresa.company_id}/reports/`,
        { params },
      );

      const dist = (data.distribuicao_categorias || []).map((d) => ({
        name: d.categoria,
        value: d.total,
      }));

      let saldoAcumulado = 0;
      const evol = (data.evolucao || []).map((e) => {
        saldoAcumulado += e.valor;
        const dataCurta = e.data.split("-").reverse().slice(0, 2).join("/");
        return { data: dataCurta, saldo: saldoAcumulado };
      });

      const comp = [
        {
          mes: tipoPeriodo === "mensal" ? mesAno : "Período",
          receitas: data.totais.total_receitas,
          despesas: data.totais.total_despesas,
        },
      ];

      setDados({
        totais: data.totais,
        distribuicao: dist,
        evolucao: evol,
        comparativo: comp,
      });
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao carregar relatório.");
    } finally {
      setCarregando(false);
    }
  }, [tipoPeriodo, mesAno, ano, dataInicio, dataFim]);

  useEffect(() => {
    carregarRelatorio();
  }, [carregarRelatorio]);

  return (
    <div className="relatorios-container">
      <PageHeader
        title="Relatórios Financeiros"
        description="Analise o desempenho financeiro da sua empresa com gráficos dinâmicos."
      />

      <div className="relatorios-filtros">
        <div className="filtros-grid">
          <div className="filtro-group">
            <label>Período</label>
            <select
              value={tipoPeriodo}
              onChange={(e) => setTipoPeriodo(e.target.value)}
            >
              <option value="mensal">Mensal</option>
              <option value="anual">Anual</option>
              <option value="personalizado">Personalizado</option>
            </select>
          </div>

          {tipoPeriodo === "mensal" && (
            <div className="filtro-group">
              <label>Mês e Ano</label>
              <input
                type="month"
                value={mesAno}
                onChange={(e) => setMesAno(e.target.value)}
              />
            </div>
          )}

          {tipoPeriodo === "anual" && (
            <div className="filtro-group">
              <label>Ano</label>
              <input
                type="number"
                placeholder="Ex: 2026"
                value={ano}
                onChange={(e) => setAno(e.target.value)}
              />
            </div>
          )}

          {tipoPeriodo === "personalizado" && (
            <>
              <div className="filtro-group">
                <label>Data Inicial</label>
                <input
                  type="date"
                  value={dataInicio}
                  onChange={(e) => setDataInicio(e.target.value)}
                />
              </div>
              <div className="filtro-group">
                <label>Data Final</label>
                <input
                  type="date"
                  value={dataFim}
                  onChange={(e) => setDataFim(e.target.value)}
                />
              </div>
            </>
          )}
        </div>
        {erro && <p className="msg-erro">{erro}</p>}
      </div>

      {carregando ? (
        <div className="msg-carregando">Gerando relatórios...</div>
      ) : (
        <>
          <div className="relatorios-totais">
            <div className="total-card total-receita">
              <span className="total-label">Total de Receitas</span>
              <span className="total-valor">
                {formatCurrency(dados.totais.total_receitas)}
              </span>
            </div>
            <div className="total-card total-despesa">
              <span className="total-label">Total de Despesas</span>
              <span className="total-valor">
                {formatCurrency(dados.totais.total_despesas)}
              </span>
            </div>
            <div
              className={`total-card ${dados.totais.saldo < 0 ? "saldo-negativo" : "saldo-positivo"}`}
            >
              <span className="total-label">Saldo do Período</span>
              <span className="total-valor">
                {formatCurrency(dados.totais.saldo)}
              </span>
            </div>
          </div>

          <div className="relatorios-graficos-grid">
            <div className="relatorios-grafico-card">
              <h2>Distribuição por Categoria (Despesas)</h2>
              {dados.distribuicao.length === 0 ? (
                <div className="msg-vazio">
                  Sem despesas cadastradas neste período.
                </div>
              ) : (
                <ResponsiveContainer width="100%" height={320}>
                  <PieChart>
                    <Pie
                      data={dados.distribuicao}
                      dataKey="value"
                      nameKey="name"
                      outerRadius={100}
                      label
                    >
                      {dados.distribuicao.map((_, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={cores[index % cores.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => formatCurrency(value)} />
                    <Legend wrapperStyle={{ fontSize: 13, paddingTop: 16 }} />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="relatorios-grafico-card">
              <h2>Evolução do Saldo Acumulado</h2>
              {dados.evolucao.length === 0 ? (
                <div className="msg-vazio">
                  Nenhuma transação neste período.
                </div>
              ) : (
                <ResponsiveContainer width="100%" height={320}>
                  <LineChart
                    data={dados.evolucao}
                    margin={{ top: 8, right: 24, left: 24, bottom: 8 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                    <XAxis
                      dataKey="data"
                      tick={{ fontSize: 12, fill: "#718096" }}
                    />
                    <YAxis
                      tick={{ fontSize: 12, fill: "#718096" }}
                      tickFormatter={(val) => `R$${(val / 1000).toFixed(0)}k`}
                      width={56}
                    />
                    <Tooltip formatter={(value) => formatCurrency(value)} />
                    <Line
                      type="monotone"
                      dataKey="saldo"
                      stroke="var(--azul)"
                      strokeWidth={3}
                      dot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="relatorios-grafico-card">
              <h2>Receitas x Despesas</h2>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart
                  data={dados.comparativo}
                  margin={{ top: 8, right: 24, left: 24, bottom: 8 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                  <XAxis
                    dataKey="mes"
                    tick={{ fontSize: 12, fill: "#718096" }}
                  />
                  <YAxis
                    tick={{ fontSize: 12, fill: "#718096" }}
                    tickFormatter={(val) => `R$${(val / 1000).toFixed(0)}k`}
                    width={56}
                  />
                  <Tooltip
                    formatter={(value) => formatCurrency(value)}
                    cursor={{ fill: "#f8fafc" }}
                  />
                  <Legend wrapperStyle={{ fontSize: 13, paddingTop: 16 }} />
                  <Bar
                    dataKey="receitas"
                    name="Receitas"
                    fill="var(--verde)"
                    radius={[4, 4, 0, 0]}
                  />
                  <Bar
                    dataKey="despesas"
                    name="Despesas"
                    fill="var(--erro)"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Relatorios;
