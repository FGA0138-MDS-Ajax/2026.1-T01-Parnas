import React, { useState, useEffect, useCallback } from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
} from "recharts";
import { useEmpresa } from "../../context/EmpresaContext";
import api from "../../services/api"; // Importante: Adicionamos o axios
import {
  listarSimulacoes,
  salvarSimulacao as salvarSimulacaoAPI,
  excluirSimulacao as excluirSimulacaoAPI,
} from "../../services/simulacao.service";
import ConfirmacaoExclusaoSimulacao from "./ConfirmacaoExclusaoSimulacao";
import "./Simulacoes.css";

const FORM_INICIAL = {
  valor_solicitado: "",
  prazo_meses: "",
  modalidade: "PRICE",
  taxa_juros: "",
};

const formatarMoeda = (valor) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    valor || 0,
  );

const formatarData = (dataStr) => {
  if (!dataStr) return "";
  return new Date(dataStr).toLocaleDateString("pt-BR");
};

const calcularTabela = (valor, prazo, taxa, modalidade) => {
  const v = parseFloat(valor);
  const n = parseInt(prazo, 10);
  const i = parseFloat(taxa) / 100;

  if (!v || !n || !i || v <= 0 || n <= 0 || i <= 0) return null;

  const tabela = [];

  if (modalidade === "PRICE") {
    const parcela = (v * i * Math.pow(1 + i, n)) / (Math.pow(1 + i, n) - 1);
    let saldo = v;
    for (let k = 1; k <= n; k++) {
      const juros = saldo * i;
      const amortizacao = parcela - juros;
      saldo = Math.max(0, saldo - amortizacao);
      tabela.push({
        mes: k,
        parcela: parseFloat(parcela.toFixed(2)),
        amortizacao: parseFloat(amortizacao.toFixed(2)),
        juros: parseFloat(juros.toFixed(2)),
        saldo: parseFloat(saldo.toFixed(2)),
      });
    }
  } else {
    const amortizacao = v / n;
    let saldo = v;
    for (let k = 1; k <= n; k++) {
      const juros = saldo * i;
      const parcela = amortizacao + juros;
      saldo = Math.max(0, saldo - amortizacao);
      tabela.push({
        mes: k,
        parcela: parseFloat(parcela.toFixed(2)),
        amortizacao: parseFloat(amortizacao.toFixed(2)),
        juros: parseFloat(juros.toFixed(2)),
        saldo: parseFloat(saldo.toFixed(2)),
      });
    }
  }

  return tabela;
};

const calcularResumo = (tabela, valor) => {
  if (!tabela || tabela.length === 0) return null;
  const valorTotal = tabela.reduce((acc, item) => acc + item.parcela, 0);
  const totalJuros = valorTotal - parseFloat(valor);
  return {
    valorParcela: tabela[0].parcela,
    valorTotal: parseFloat(valorTotal.toFixed(2)),
    totalJuros: parseFloat(totalJuros.toFixed(2)),
  };
};

const amostrarDados = (tabela) => {
  if (!tabela) return [];
  if (tabela.length <= 60) return tabela;
  const passo = Math.ceil(tabela.length / 60);
  return tabela.filter(
    (_, idx) => idx % passo === 0 || idx === tabela.length - 1,
  );
};

const calcularViabilidade = (mediaSaldo, parcela) => {
  if (mediaSaldo <= 0)
    return {
      status: "risco",
      label: "Saldo Negativo",
      descricao:
        "A empresa opera com saldo negativo. Captar crédito representa alto risco financeiro.",
    };
  const ratio = mediaSaldo / parcela;
  if (ratio >= 1.5)
    return {
      status: "viavel",
      label: "Operação Viável",
      descricao: `O saldo disponível cobre ${(ratio * 100).toFixed(0)}% da parcela. Há folga financeira confortável.`,
    };
  if (ratio >= 1.0)
    return {
      status: "atencao",
      label: "Atenção — Margem Reduzida",
      descricao:
        "O saldo cobre a parcela, mas com margem reduzida. Avalie com cuidado antes de decidir.",
    };
  return {
    status: "risco",
    label: "Risco Alto",
    descricao: `A parcela representa ${((parcela / mediaSaldo) * 100).toFixed(0)}% do saldo médio disponível.`,
  };
};

const TooltipAmortizacao = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="grafico-tooltip">
      <p className="tooltip-mes">Mês {label}</p>
      {payload.map((entry) => (
        <p key={entry.name} style={{ color: entry.color }}>
          {entry.name}: {formatarMoeda(entry.value)}
        </p>
      ))}
    </div>
  );
};

const TooltipFluxo = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="grafico-tooltip">
      <p className="tooltip-mes">{label}</p>
      {payload.map((entry) => (
        <p key={entry.name} style={{ color: entry.color }}>
          {entry.name}: {formatarMoeda(entry.value)}
        </p>
      ))}
    </div>
  );
};

const Simulacoes = () => {
  const { idEmpresaLogada } = useEmpresa();

  const [form, setForm] = useState(FORM_INICIAL);
  const [erros, setErros] = useState({});
  const [tabela, setTabela] = useState(null);
  const [resumo, setResumo] = useState(null);

  const [salvando, setSalvando] = useState(false);
  const [mensagemSalvo, setMensagemSalvo] = useState("");
  const [erroSalvar, setErroSalvar] = useState("");

  const [simulacoes, setSimulacoes] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erroLista, setErroLista] = useState("");

  const [fluxoCaixa, setFluxoCaixa] = useState(null);
  const [carregandoFluxo, setCarregandoFluxo] = useState(false);

  const [confirmacaoAberta, setConfirmacaoAberta] = useState(false);
  const [simulacaoParaExcluir, setSimulacaoParaExcluir] = useState(null);

  const carregarSimulacoes = useCallback(async () => {
    if (!idEmpresaLogada) return;
    setCarregando(true);
    setErroLista("");
    try {
      const dados = await listarSimulacoes();
      //o backend devolve {"simulations": []}
      setSimulacoes(Array.isArray(dados) ? dados : dados.simulations || []);
    } catch (err) {
      setErroLista(err.message);
    } finally {
      setCarregando(false);
    }
  }, [idEmpresaLogada]);

  const carregarFluxoCaixa = useCallback(async () => {
    if (!idEmpresaLogada) return;
    setCarregandoFluxo(true);
    try {
      const hoje = new Date();
      const seisAtras = new Date(hoje.getFullYear(), hoje.getMonth() - 5, 1);
      const dataFim = hoje.toISOString().split("T")[0];
      const dataInicio = seisAtras.toISOString().split("T")[0];

      //usando o axios API para pegar as transações corretamente
      const { data } = await api.get(
        `/api/companies/${idEmpresaLogada}/transactions/`,
        {
          params: { data_inicio: dataInicio, data_fim: dataFim, per_page: 500 },
        },
      );

      const lista = data.transacoes || data.transactions || [];

      if (lista.length === 0) {
        setFluxoCaixa({ semDados: true });
        return;
      }

      const porMes = {};
      lista.forEach((t) => {
        const dataT = t.date || t.data || "";
        const mes = dataT.substring(0, 7);
        if (!mes) return;
        if (!porMes[mes]) porMes[mes] = { receita: 0, despesa: 0 };
        const valor = parseFloat(t.amount ?? t.valor ?? 0);
        const tipo = t.type || t.tipo || "";
        if (tipo === "receita") porMes[mes].receita += valor;
        else if (tipo === "despesa") porMes[mes].despesa += valor;
      });

      const meses = Object.keys(porMes)
        .sort()
        .map((m) => ({
          mes: m,
          receita: parseFloat(porMes[m].receita.toFixed(2)),
          despesa: parseFloat(porMes[m].despesa.toFixed(2)),
          saldo: parseFloat((porMes[m].receita - porMes[m].despesa).toFixed(2)),
        }));

      if (meses.length === 0) {
        setFluxoCaixa({ semDados: true });
        return;
      }

      const mediaReceita =
        meses.reduce((a, m) => a + m.receita, 0) / meses.length;
      const mediaDespesa =
        meses.reduce((a, m) => a + m.despesa, 0) / meses.length;
      const mediaSaldo = meses.reduce((a, m) => a + m.saldo, 0) / meses.length;

      setFluxoCaixa({
        semDados: false,
        mediaReceita: parseFloat(mediaReceita.toFixed(2)),
        mediaDespesa: parseFloat(mediaDespesa.toFixed(2)),
        mediaSaldo: parseFloat(mediaSaldo.toFixed(2)),
        meses,
      });
    } catch {
      setFluxoCaixa({ semDados: true });
    } finally {
      setCarregandoFluxo(false);
    }
  }, [idEmpresaLogada]);

  useEffect(() => {
    carregarSimulacoes();
    carregarFluxoCaixa();
  }, [carregarSimulacoes, carregarFluxoCaixa]);

  useEffect(() => {
    const novaTabela = calcularTabela(
      form.valor_solicitado,
      form.prazo_meses,
      form.taxa_juros,
      form.modalidade,
    );
    setTabela(novaTabela);
    setResumo(calcularResumo(novaTabela, form.valor_solicitado));
  }, [
    form.valor_solicitado,
    form.prazo_meses,
    form.taxa_juros,
    form.modalidade,
  ]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (erros[name]) setErros((prev) => ({ ...prev, [name]: "" }));
    setMensagemSalvo("");
    setErroSalvar("");
  };

  const validar = () => {
    const novosErros = {};
    const valor = parseFloat(form.valor_solicitado);
    const prazo = parseInt(form.prazo_meses, 10);
    const taxa = parseFloat(form.taxa_juros);

    if (!form.valor_solicitado || isNaN(valor) || valor <= 0)
      novosErros.valor_solicitado = "Informe um valor válido e positivo.";
    if (!form.prazo_meses || isNaN(prazo) || prazo < 1 || prazo > 360)
      novosErros.prazo_meses = "Prazo deve ser entre 1 e 360 meses.";
    if (!form.taxa_juros || isNaN(taxa) || taxa <= 0 || taxa > 100)
      novosErros.taxa_juros = "Informe uma taxa entre 0,01% e 100%.";

    setErros(novosErros);
    return Object.keys(novosErros).length === 0;
  };

  const handleSalvar = async () => {
    if (!validar() || !resumo) return;
    if (!idEmpresaLogada) {
      setErroSalvar(
        "Nenhuma empresa selecionada. Cadastre ou selecione uma empresa primeiro.",
      );
      return;
    }

    setSalvando(true);
    setErroSalvar("");
    setMensagemSalvo("");

    try {
      await salvarSimulacaoAPI({
        valor_solicitado: form.valor_solicitado,
        prazo_meses: form.prazo_meses,
        modalidade: form.modalidade,
        taxa_juros: form.taxa_juros,
      });

      setMensagemSalvo("Simulação salva com sucesso!");
      setForm(FORM_INICIAL);
      carregarSimulacoes();
    } catch (err) {
      setErroSalvar(err.response?.data?.erro || err.message);
    } finally {
      setSalvando(false);
    }
  };

  const abrirConfirmacao = (simulacao) => {
    setSimulacaoParaExcluir(simulacao);
    setConfirmacaoAberta(true);
  };

  const cancelarExclusao = () => {
    setConfirmacaoAberta(false);
    setSimulacaoParaExcluir(null);
  };

  const confirmarExclusao = async () => {
    if (!simulacaoParaExcluir) return;
    try {
      await excluirSimulacaoAPI(simulacaoParaExcluir.simulation_id); // Corrigido de id_simulacao
      setConfirmacaoAberta(false);
      setSimulacaoParaExcluir(null);
      carregarSimulacoes();
    } catch (err) {
      setErroLista(err.message);
      setConfirmacaoAberta(false);
    }
  };

  const dadosGrafico = amostrarDados(tabela);

  return (
    <div className="simulacoes-container">
      <div className="simulacoes-header">
        <div>
          <h2>Simulação de Crédito</h2>
          <p>
            Simule empréstimos e entenda o impacto no fluxo de caixa antes de
            captar recursos
          </p>
        </div>
      </div>

      {/* === Formulário === */}
      <div className="simulacoes-formulario-card">
        <h3 className="secao-titulo">Nova Simulação</h3>
        <div className="simulacoes-form-grid">
          <div className="input-group">
            <label htmlFor="sim-valor">Valor Solicitado (R$)</label>
            <input
              id="sim-valor"
              type="number"
              name="valor_solicitado"
              placeholder="Ex.: 10000"
              min="1"
              step="0.01"
              value={form.valor_solicitado}
              onChange={handleChange}
              className={erros.valor_solicitado ? "input-erro" : ""}
            />
            {erros.valor_solicitado && (
              <span className="msg-campo-erro">{erros.valor_solicitado}</span>
            )}
          </div>

          <div className="input-group">
            <label htmlFor="sim-prazo">Prazo (meses)</label>
            <input
              id="sim-prazo"
              type="number"
              name="prazo_meses"
              placeholder="Ex.: 24"
              min="1"
              max="360"
              step="1"
              value={form.prazo_meses}
              onChange={handleChange}
              className={erros.prazo_meses ? "input-erro" : ""}
            />
            {erros.prazo_meses && (
              <span className="msg-campo-erro">{erros.prazo_meses}</span>
            )}
          </div>

          <div className="input-group">
            <label htmlFor="sim-modalidade">Modalidade</label>
            <select
              id="sim-modalidade"
              name="modalidade"
              value={form.modalidade}
              onChange={handleChange}
            >
              <option value="PRICE">PRICE (parcelas fixas)</option>
              <option value="SAC">SAC (amortização constante)</option>
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="sim-taxa">Taxa de Juros (% a.m.)</label>
            <input
              id="sim-taxa"
              type="number"
              name="taxa_juros"
              placeholder="Ex.: 2.5"
              min="0.01"
              max="100"
              step="0.01"
              value={form.taxa_juros}
              onChange={handleChange}
              className={erros.taxa_juros ? "input-erro" : ""}
            />
            {erros.taxa_juros && (
              <span className="msg-campo-erro">{erros.taxa_juros}</span>
            )}
          </div>
        </div>
      </div>

      {resumo && (
        <>
          {/* === Resultado do cálculo === */}
          <div className="simulacoes-resultado">
            <div className="resultado-card resultado-parcela">
              <span className="resultado-label">
                {form.modalidade === "SAC" ? "1ª Parcela" : "Valor da Parcela"}
              </span>
              <span className="resultado-valor">
                {formatarMoeda(resumo.valorParcela)}
              </span>
              {form.modalidade === "SAC" && tabela && (
                <span className="resultado-sub">
                  Última: {formatarMoeda(tabela[tabela.length - 1].parcela)}
                </span>
              )}
            </div>

            <div className="resultado-card resultado-total">
              <span className="resultado-label">Total a Pagar</span>
              <span className="resultado-valor">
                {formatarMoeda(resumo.valorTotal)}
              </span>
            </div>

            <div className="resultado-card resultado-juros">
              <span className="resultado-label">Total de Juros</span>
              <span className="resultado-valor juros-valor">
                {formatarMoeda(resumo.totalJuros)}
              </span>
              {form.valor_solicitado && (
                <span className="resultado-sub">
                  {(
                    (resumo.totalJuros / parseFloat(form.valor_solicitado)) *
                    100
                  ).toFixed(1)}
                  % do valor solicitado
                </span>
              )}
            </div>
          </div>

          {/* === Impacto no Fluxo de Caixa === */}
          <div className="simulacoes-impacto-card">
            <h3 className="secao-titulo">Impacto no Fluxo de Caixa</h3>
            <p className="secao-descricao">
              Comparativo entre a parcela simulada e o histórico financeiro da
              empresa (últimos 6 meses)
            </p>

            {!idEmpresaLogada ? (
              <div className="impacto-sem-dados">
                <p>
                  Selecione uma empresa para visualizar o impacto no fluxo de
                  caixa.
                </p>
              </div>
            ) : carregandoFluxo ? (
              <div className="impacto-sem-dados">
                <p>Carregando dados financeiros...</p>
              </div>
            ) : !fluxoCaixa || fluxoCaixa.semDados ? (
              <div className="impacto-sem-dados">
                <p>
                  Sem transações registradas nos últimos 6 meses. Registre
                  transações para visualizar o impacto no fluxo de caixa.
                </p>
              </div>
            ) : (
              <>
                <div className="impacto-resumo-grid">
                  <div className="impacto-card">
                    <span className="impacto-label">Receita Média Mensal</span>
                    <span className="impacto-valor impacto-receita">
                      {formatarMoeda(fluxoCaixa.mediaReceita)}
                    </span>
                  </div>
                  <div className="impacto-card">
                    <span className="impacto-label">Despesa Média Mensal</span>
                    <span className="impacto-valor impacto-despesa">
                      {formatarMoeda(fluxoCaixa.mediaDespesa)}
                    </span>
                  </div>
                  <div className="impacto-card">
                    <span className="impacto-label">
                      Saldo Médio Disponível
                    </span>
                    <span
                      className={`impacto-valor ${
                        fluxoCaixa.mediaSaldo >= 0
                          ? "impacto-positivo"
                          : "impacto-negativo"
                      }`}
                    >
                      {formatarMoeda(fluxoCaixa.mediaSaldo)}
                    </span>
                  </div>
                </div>

                {(() => {
                  const viab = calcularViabilidade(
                    fluxoCaixa.mediaSaldo,
                    resumo.valorParcela,
                  );
                  return (
                    <div
                      className={`viabilidade-banner viabilidade-${viab.status}`}
                    >
                      <div className="viabilidade-indicador" />
                      <div className="viabilidade-info">
                        <strong className="viabilidade-label">
                          {viab.label}
                        </strong>
                        <span className="viabilidade-descricao">
                          {viab.descricao}
                        </span>
                      </div>
                      <div className="viabilidade-numeros">
                        <div className="vn-item">
                          <span className="vn-label">Parcela simulada</span>
                          <span className="vn-valor">
                            {formatarMoeda(resumo.valorParcela)}
                          </span>
                        </div>
                        <span className="vn-vs">vs</span>
                        <div className="vn-item">
                          <span className="vn-label">Saldo médio</span>
                          <span className="vn-valor">
                            {formatarMoeda(fluxoCaixa.mediaSaldo)}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })()}

                <div className="impacto-grafico">
                  <p className="impacto-grafico-legenda">
                    Histórico mensal de receitas, despesas e saldo — linha
                    laranja indica a parcela simulada
                  </p>
                  <ResponsiveContainer width="100%" height={260}>
                    <ComposedChart
                      data={fluxoCaixa.meses}
                      margin={{ top: 8, right: 24, left: 24, bottom: 8 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                      <XAxis
                        dataKey="mes"
                        tick={{ fontSize: 11, fill: "#718096" }}
                      />
                      <YAxis
                        tick={{ fontSize: 11, fill: "#718096" }}
                        tickFormatter={(v) => `R$${(v / 1000).toFixed(0)}k`}
                        width={56}
                      />
                      <Tooltip content={<TooltipFluxo />} />
                      <Legend wrapperStyle={{ fontSize: 12, paddingTop: 8 }} />
                      <Bar
                        dataKey="receita"
                        name="Receita"
                        fill="#03906C"
                        opacity={0.75}
                        radius={[3, 3, 0, 0]}
                      />
                      <Bar
                        dataKey="despesa"
                        name="Despesa"
                        fill="#E53E3E"
                        opacity={0.75}
                        radius={[3, 3, 0, 0]}
                      />
                      <Line
                        type="monotone"
                        dataKey="saldo"
                        name="Saldo"
                        stroke="#0F4C81"
                        strokeWidth={2.5}
                        dot={{ r: 4, fill: "#0F4C81" }}
                      />
                      <ReferenceLine
                        y={resumo.valorParcela}
                        stroke="#E07D10"
                        strokeWidth={2}
                        strokeDasharray="8 4"
                        label={{
                          value: `Parcela: ${formatarMoeda(resumo.valorParcela)}`,
                          fill: "#E07D10",
                          fontSize: 11,
                          position: "insideTopRight",
                        }}
                      />
                    </ComposedChart>
                  </ResponsiveContainer>
                </div>
              </>
            )}
          </div>

          {/* === Gráfico de amortização === */}
          <div className="simulacoes-grafico-card">
            <h3 className="secao-titulo">Evolução das Parcelas</h3>
            <p className="secao-descricao">
              Distribuição de amortização e juros ao longo do prazo —{" "}
              {form.modalidade}
            </p>
            <ResponsiveContainer width="100%" height={320}>
              <ComposedChart
                data={dadosGrafico}
                margin={{ top: 8, right: 24, left: 24, bottom: 8 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis
                  dataKey="mes"
                  tick={{ fontSize: 12, fill: "#718096" }}
                  label={{
                    value: "Mês",
                    position: "insideBottom",
                    offset: -2,
                    fill: "#718096",
                    fontSize: 12,
                  }}
                />
                <YAxis
                  tick={{ fontSize: 12, fill: "#718096" }}
                  tickFormatter={(v) => `R$${(v / 1000).toFixed(0)}k`}
                  width={56}
                />
                <Tooltip content={<TooltipAmortizacao />} />
                <Legend wrapperStyle={{ fontSize: 13, paddingTop: 12 }} />
                <Bar
                  dataKey="amortizacao"
                  name="Amortização"
                  stackId="parcela"
                  fill="#0F4C81"
                />
                <Bar
                  dataKey="juros"
                  name="Juros"
                  stackId="parcela"
                  fill="#03906C"
                  radius={[3, 3, 0, 0]}
                />
                <Line
                  type="monotone"
                  dataKey="parcela"
                  name="Parcela Total"
                  stroke="#E53E3E"
                  strokeWidth={2}
                  dot={false}
                />
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* === Salvar === */}
          <div className="simulacoes-acoes">
            {erroSalvar && <p className="msg-error">{erroSalvar}</p>}
            {mensagemSalvo && <p className="msg-success">{mensagemSalvo}</p>}
            <button
              className="btn-salvar-simulacao"
              onClick={handleSalvar}
              disabled={salvando}
            >
              {salvando ? "Salvando..." : "Salvar Simulação"}
            </button>
          </div>
        </>
      )}

      {/* === Simulações salvas === */}
      <div className="simulacoes-historico">
        <div className="historico-header">
          <h3 className="secao-titulo">Simulações Salvas</h3>
          {!idEmpresaLogada && (
            <p className="aviso-empresa">
              Cadastre uma empresa para salvar e visualizar simulações.
            </p>
          )}
        </div>

        {erroLista && <p className="msg-error">{erroLista}</p>}

        <div className="historico-tabela-wrapper">
          {carregando ? (
            <div className="simulacoes-vazio">
              <p>Carregando simulações...</p>
            </div>
          ) : simulacoes.length === 0 ? (
            <div className="simulacoes-vazio">
              <p>Nenhuma simulação salva ainda.</p>
            </div>
          ) : (
            <>
              <div className="tabela-info">
                <span>{simulacoes.length} simulação(ões) encontrada(s)</span>
              </div>
              <table className="historico-tabela">
                <thead>
                  <tr>
                    <th>Data</th>
                    <th>Valor Solicitado</th>
                    <th>Prazo</th>
                    <th>Modalidade</th>
                    <th>Taxa (a.m.)</th>
                    <th>Parcela</th>
                    <th>Total</th>
                    <th>Juros</th>
                    <th className="col-acoes">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {simulacoes.map((sim) => (
                    <tr key={sim.simulation_id}>
                      <td>{formatarData(sim.data_simulacao)}</td>
                      <td>{formatarMoeda(sim.valor_solicitado)}</td>
                      <td>{sim.prazo_meses} meses</td>
                      <td>
                        <span
                          className={`badge-modalidade badge-${sim.modalidade?.toLowerCase()}`}
                        >
                          {sim.modalidade}
                        </span>
                      </td>
                      <td>{parseFloat(sim.taxa_juros).toFixed(2)}%</td>
                      <td>{formatarMoeda(sim.valor_parcela)}</td>
                      <td>{formatarMoeda(sim.valor_total)}</td>
                      <td className="valor-juros">
                        {formatarMoeda(sim.total_juros)}
                      </td>
                      <td className="col-acoes">
                        <button
                          className="btn-acao btn-excluir"
                          onClick={() => abrirConfirmacao(sim)}
                          title="Excluir simulação"
                        >
                          ✕
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      </div>

      {confirmacaoAberta && (
        <ConfirmacaoExclusaoSimulacao
          simulacao={simulacaoParaExcluir}
          onConfirmar={confirmarExclusao}
          onCancelar={cancelarExclusao}
        />
      )}
    </div>
  );
};

export default Simulacoes;
