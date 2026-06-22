import { useState } from "react";
import "./Relatorios.css";
import { BarChart3 } from "lucide-react";

import {PieChart, Pie, Tooltip, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, BarChart, Bar, Legend,} from "recharts";

function Relatorios() {
  const [tipoPeriodo, setTipoPeriodo] = useState("mensal");

  const distribuicaoCategoria = [
    { name: "Alimentação", value: 2500 },
    { name: "Transporte", value: 1200 },
    { name: "Moradia", value: 3500 },
    { name: "Lazer", value: 800 },
  ];

  const evolucaoSaldo = [
    { mes: "Jan", saldo: 3000 },
    { mes: "Fev", saldo: 4200 },
    { mes: "Mar", saldo: 3900 },
    { mes: "Abr", saldo: 5100 },
    { mes: "Mai", saldo: 6200 },
  ];

  const comparativoMensal = [
    { mes: "Jan", receitas: 5000, despesas: 2000 },
    { mes: "Fev", receitas: 6000, despesas: 1800 },
    { mes: "Mar", receitas: 5500, despesas: 1600 },
    { mes: "Abr", receitas: 7000, despesas: 1900 },
    { mes: "Mai", receitas: 7500, despesas: 1300 },
  ];

  const cores = [
    "#0f4c81",
    "#2a9d8f",
    "#f4a261",
    "#e76f51",
  ];

  return (
    <div className="relatorios-page">
      <header className="relatorios-header">
        <div className="header-logo">
          <div className="logo-icon">
            <BarChart3 size={18} color="white" />
          </div>

          <div className="logo-text">
            <h1>CREDIFAB</h1>
            <p>Plataforma de Acesso a Crédito</p>
          </div>
        </div>
      </header>

      <main className="relatorios-content">
        <section className="relatorios-card">
          <h2>Filtros</h2>

          <div className="filtros">
            <select
              value={tipoPeriodo}
              onChange={(e) =>
                setTipoPeriodo(e.target.value)
              }
            >
              <option value="mensal">
                Mensal
              </option>

              <option value="anual">
                Anual
              </option>

              <option value="personalizado">
                Personalizado
              </option>
            </select>

            {tipoPeriodo === "mensal" && (
              <input type="month" />
            )}

            {tipoPeriodo === "anual" && (
              <input type="number" placeholder="Ano" />
            )}

            {tipoPeriodo === "personalizado" && (
              <>
                <input type="date" />

                <input type="date" />
              </>
            )}
          </div>
        </section>

        <section className="cards-resumo">
          <div className="resumo-card receita">
            <h3>Receitas</h3>
            <span>R$ 15.000</span>
          </div>

          <div className="resumo-card despesa">
            <h3>Despesas</h3>
            <span>R$ 8.500</span>
          </div>

          <div className="resumo-card saldo">
            <h3>Saldo</h3>
            <span>R$ 6.500</span>
          </div>
        </section>

        <section className="relatorios-card">
          <h2>
            Distribuição por Categoria
          </h2>

          <ResponsiveContainer
            width="100%"
            height={350}
          >
            <PieChart>
              <Pie
                data={distribuicaoCategoria}
                dataKey="value"
                nameKey="name"
                outerRadius={120}
              >
                {distribuicaoCategoria.map(
                  (_, index) => (
                    <Cell
                      key={index}
                      fill={
                        cores[
                          index % cores.length
                        ]
                      }
                    />
                  )
                )}
              </Pie>

              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </section>

        <section className="relatorios-card">
          <h2>Evolução do Saldo</h2>

          <ResponsiveContainer
            width="100%"
            height={350}
          >
            <LineChart data={evolucaoSaldo}>
              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="mes" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="saldo"
                stroke="#0f4c81"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </section>

        <section className="relatorios-card">
          <h2>
            Receitas x Despesas
          </h2>

          <ResponsiveContainer
            width="100%"
            height={350}
          >
            <BarChart
              data={comparativoMensal}
            >
              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="mes" />

              <YAxis />

              <Tooltip />

              <Legend />

              <Bar
                dataKey="receitas"
                fill="#2a9d8f"
              />

              <Bar
                dataKey="despesas"
                fill="#e76f51"
              />
            </BarChart>
          </ResponsiveContainer>
        </section>
      </main>
    </div>
  );
}

export default Relatorios;