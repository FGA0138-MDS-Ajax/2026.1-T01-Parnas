import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from 'recharts';
import {
  calcularComparacao,
  salvarComparacao,
  exportarPDF,
} from '../../services/comparacao.service';
import './Comparacoes.css';

const MODALIDADE_VAZIA = { name: '', interest_rate: '', term_months: '', type: 'PJ' };

const formatarMoeda = (valor) =>
  Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const CORES = ['#0F4C81', '#03906C', '#e67e22', '#8e44ad'];

const Comparacoes = () => {
  const [valorEmprestimo, setValorEmprestimo] = useState('');
  const [modalidades, setModalidades] = useState([{ ...MODALIDADE_VAZIA }]);
  const [resultado, setResultado] = useState(null);
  const [savedId, setSavedId] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [exportando, setExportando] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const mostrarFeedback = (mensagem, tipo = 'sucesso') => {
    setFeedback({ mensagem, tipo });
    setTimeout(() => setFeedback(null), 4000);
  };

  const adicionarModalidade = () => {
    if (modalidades.length >= 4) return;
    setModalidades([...modalidades, { ...MODALIDADE_VAZIA }]);
  };

  const removerModalidade = (index) => {
    if (modalidades.length <= 1) return;
    setModalidades(modalidades.filter((_, i) => i !== index));
    setResultado(null);
    setSavedId(null);
  };

  const atualizarModalidade = (index, campo, valor) => {
    const novas = [...modalidades];
    novas[index] = { ...novas[index], [campo]: valor };
    setModalidades(novas);
    setResultado(null);
    setSavedId(null);
  };

  const validar = () => {
    if (!valorEmprestimo || Number(valorEmprestimo) <= 0) {
      mostrarFeedback('Informe um valor de empréstimo válido.', 'erro');
      return false;
    }
    for (let i = 0; i < modalidades.length; i++) {
      const m = modalidades[i];
      if (!m.name.trim()) {
        mostrarFeedback(`Modalidade ${i + 1}: informe o nome.`, 'erro');
        return false;
      }
      if (!m.interest_rate || Number(m.interest_rate) <= 0) {
        mostrarFeedback(`Modalidade ${i + 1}: informe a taxa de juros.`, 'erro');
        return false;
      }
      if (!m.term_months || Number(m.term_months) <= 0) {
        mostrarFeedback(`Modalidade ${i + 1}: informe o prazo.`, 'erro');
        return false;
      }
    }
    return true;
  };

  const montarPayload = () => ({
    loan_amount: Number(valorEmprestimo),
    modalities: modalidades.map((m) => ({
      name: m.name.trim(),
      interest_rate: Number(m.interest_rate),
      term_months: Number(m.term_months),
      type: m.type,
    })),
  });

  const handleCalcular = async () => {
    if (!validar()) return;
    setCarregando(true);
    setSavedId(null);
    try {
      const dados = await calcularComparacao(montarPayload());
      setResultado(dados);
    } catch {
      mostrarFeedback('Erro ao calcular. Verifique os dados e tente novamente.', 'erro');
    } finally {
      setCarregando(false);
    }
  };

  const handleSalvar = async () => {
    if (!resultado) return;
    setSalvando(true);
    try {
      const dados = await salvarComparacao(montarPayload());
      setSavedId(dados.id);
      mostrarFeedback('Comparação salva com sucesso!');
    } catch {
      mostrarFeedback('Erro ao salvar a comparação.', 'erro');
    } finally {
      setSalvando(false);
    }
  };

  const handleExportarPDF = async () => {
    if (!savedId) return;
    setExportando(true);
    try {
      await exportarPDF(savedId);
      mostrarFeedback('PDF baixado com sucesso!');
    } catch {
      mostrarFeedback('Erro ao exportar PDF.', 'erro');
    } finally {
      setExportando(false);
    }
  };

  const dadosGrafico = resultado
    ? resultado.comparisons.map((c, i) => ({
        name: c.name,
        total: c.total_amount,
        fill: CORES[i % CORES.length],
      }))
    : [];

  return (
    <div className="comp-container">

      {feedback && (
        <div className={`comp-feedback comp-feedback--${feedback.tipo}`}>
          {feedback.tipo === 'sucesso' ? '✓' : '✕'} {feedback.mensagem}
        </div>
      )}

      {/* Cabeçalho */}
      <div className="comp-header">
        <div>
          <h2>Comparação de Modalidades de Crédito</h2>
          <p>Compare até 4 linhas de crédito lado a lado e encontre a mais vantajosa para o seu negócio.</p>
        </div>
      </div>

      {/* Formulário */}
      <div className="comp-card">
        <h3 className="comp-card-titulo">Dados da Simulação</h3>

        <div className="comp-valor-emprestimo">
          <div className="input-group">
            <label>Valor do Empréstimo (R$)</label>
            <input
              type="number"
              min="1"
              placeholder="Ex: 50000"
              value={valorEmprestimo}
              onChange={(e) => { setValorEmprestimo(e.target.value); setResultado(null); setSavedId(null); }}
            />
          </div>
        </div>

        <div className="comp-modalidades-header">
          <h4>Modalidades</h4>
          {modalidades.length < 4 && (
            <button className="btn-adicionar-modalidade" onClick={adicionarModalidade}>
              + Adicionar Modalidade
            </button>
          )}
        </div>

        <div className="comp-modalidades-grid">
          {modalidades.map((mod, index) => (
            <div key={index} className="comp-modalidade-card">
              <div className="comp-modalidade-header">
                <span
                  className="comp-modalidade-num"
                  style={{ backgroundColor: CORES[index % CORES.length] }}
                >
                  {index + 1}
                </span>
                <span className="comp-modalidade-label">Modalidade {index + 1}</span>
                {modalidades.length > 1 && (
                  <button
                    className="btn-remover-modalidade"
                    onClick={() => removerModalidade(index)}
                    title="Remover modalidade"
                  >
                    ✕
                  </button>
                )}
              </div>

              <div className="input-group">
                <label>Nome da Modalidade</label>
                <input
                  type="text"
                  placeholder="Ex: Caixa Econômica 36 meses"
                  value={mod.name}
                  onChange={(e) => atualizarModalidade(index, 'name', e.target.value)}
                />
              </div>

              <div className="form-row">
                <div className="input-group">
                  <label>Taxa de Juros (% a.m.)</label>
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    placeholder="Ex: 1.5"
                    value={mod.interest_rate}
                    onChange={(e) => atualizarModalidade(index, 'interest_rate', e.target.value)}
                  />
                </div>
                <div className="input-group">
                  <label>Prazo (meses)</label>
                  <input
                    type="number"
                    min="1"
                    placeholder="Ex: 36"
                    value={mod.term_months}
                    onChange={(e) => atualizarModalidade(index, 'term_months', e.target.value)}
                  />
                </div>
              </div>

              <div className="input-group">
                <label>Tipo de Crédito</label>
                <div className="tipo-toggle">
                  <button
                    type="button"
                    className={`tipo-btn ${mod.type === 'PJ' ? 'tipo-btn--pj ativo' : ''}`}
                    onClick={() => atualizarModalidade(index, 'type', 'PJ')}
                  >
                    Pessoa Jurídica (PJ)
                  </button>
                  <button
                    type="button"
                    className={`tipo-btn ${mod.type === 'PF' ? 'tipo-btn--pf ativo' : ''}`}
                    onClick={() => atualizarModalidade(index, 'type', 'PF')}
                  >
                    Pessoa Física (PF)
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="comp-acoes-form">
          <button
            className="btn-calcular"
            onClick={handleCalcular}
            disabled={carregando}
          >
            {carregando ? 'Calculando...' : 'Calcular Comparação'}
          </button>
        </div>
      </div>

      {/* Resultados */}
      {resultado && (
        <>
          {/* Alertas PF */}
          {resultado.comparisons.some((c) => c.warning_pf) && (
            <div className="comp-alerta-pf">
              <span className="comp-alerta-pf-icone">⚠</span>
              <div>
                <strong>Atenção: Crédito de Pessoa Física detectado</strong>
                <p>
                  {resultado.comparisons.filter((c) => c.warning_pf).map((c) => c.name).join(', ')}{' '}
                  utiliza linha de crédito PF. Para empresas, recomenda-se utilizar linhas PJ para
                  manter a separação patrimonial e obter melhores condições.
                </p>
              </div>
            </div>
          )}

          {/* Tabela Comparativa */}
          <div className="comp-card">
            <div className="comp-resultado-header">
              <h3 className="comp-card-titulo">Resultado da Comparação</h3>
              <div className="comp-acoes-resultado">
                <button
                  className="btn-salvar"
                  onClick={handleSalvar}
                  disabled={salvando || !!savedId}
                >
                  {savedId ? '✓ Salvo' : salvando ? 'Salvando...' : 'Salvar Comparação'}
                </button>
                <button
                  className="btn-exportar"
                  onClick={handleExportarPDF}
                  disabled={!savedId || exportando}
                  title={!savedId ? 'Salve a comparação antes de exportar' : ''}
                >
                  {exportando ? 'Exportando...' : 'Exportar PDF'}
                </button>
              </div>
            </div>

            <p className="comp-valor-referencia">
              Valor simulado: <strong>{formatarMoeda(resultado.loan_amount)}</strong>
            </p>

            <div className="comp-tabela-wrapper">
              <table className="comp-tabela">
                <thead>
                  <tr>
                    <th>Modalidade</th>
                    <th>Tipo</th>
                    <th>Taxa a.m.</th>
                    <th>Prazo</th>
                    <th>Parcela Mensal</th>
                    <th>Total de Juros</th>
                    <th>Custo Total</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {resultado.comparisons.map((comp, index) => (
                    <tr
                      key={index}
                      className={comp.is_best_option ? 'comp-linha-melhor' : ''}
                    >
                      <td>
                        <div className="comp-nome-celula">
                          <span
                            className="comp-cor-dot"
                            style={{ backgroundColor: CORES[index % CORES.length] }}
                          />
                          <strong>{comp.name}</strong>
                        </div>
                      </td>
                      <td>
                        <span className={`badge-tipo badge-tipo--${comp.type.toLowerCase()}`}>
                          {comp.type}
                        </span>
                      </td>
                      <td>{Number(comp.interest_rate).toFixed(2)}%</td>
                      <td>{comp.term_months} meses</td>
                      <td className="comp-valor-destaque">{formatarMoeda(comp.monthly_payment)}</td>
                      <td className="comp-juros">{formatarMoeda(comp.total_interest)}</td>
                      <td className="comp-total">{formatarMoeda(comp.total_amount)}</td>
                      <td>
                        {comp.is_best_option && (
                          <span className="badge-melhor">★ Melhor opção</span>
                        )}
                        {comp.warning_pf && !comp.is_best_option && (
                          <span className="badge-pf">⚠ PF</span>
                        )}
                        {comp.warning_pf && comp.is_best_option && (
                          <span className="badge-pf">⚠ PF</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Gráfico de Barras */}
          <div className="comp-card">
            <h3 className="comp-card-titulo">Custo Total por Modalidade</h3>
            <p className="comp-grafico-legenda">Quanto você pagará ao final do contrato em cada modalidade.</p>
            <div className="comp-grafico-wrapper">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dadosGrafico} margin={{ top: 10, right: 20, left: 20, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 12, fill: '#718096' }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tickFormatter={(v) => `R$ ${(v / 1000).toFixed(0)}k`}
                    tick={{ fontSize: 11, fill: '#718096' }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip
                    formatter={(value) => [formatarMoeda(value), 'Custo Total']}
                    contentStyle={{
                      borderRadius: '10px',
                      border: '1px solid #E2E8F0',
                      fontSize: '0.85rem',
                    }}
                  />
                  <Bar dataKey="total" radius={[6, 6, 0, 0]}>
                    {dadosGrafico.map((entry, index) => (
                      <Cell key={index} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Comparacoes;
