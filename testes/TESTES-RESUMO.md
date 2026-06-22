# Testes do CrediFab — Resumão (comece por aqui)

> Leitura para entender tudo de **forma geral**. Depois, cada tipo
> de teste tem seu próprio guia detalhado. Mantido pela dupla de Qualidade
> (Daniel Filipe / Matheus Moretti).

---

## 1. Por que testamos?

Teste automatizado é código que **verifica se o nosso código funciona** — sozinho,
toda vez que rodamos. Em vez de abrir o navegador e clicar manualmente a cada
mudança, escrevemos um teste uma vez e ele nos avisa na hora se algo quebrou.

Para o QA isso traz três coisas:
- **Confiança para mexer:** se um teste passa hoje e falha amanhã, sabemos
  exatamente o que quebrou.
- **Documentação viva:** um bom teste mostra como uma função deve se comportar.
- **Critério objetivo de merge:** "passou nos testes" vira parte da régua de
  aprovação do PR.

---

## 2. A pirâmide de testes (nossa estratégia)

Nem todo teste é igual. Organizamos em três níveis, na proporção de uma pirâmide:
**muitos testes rápidos e baratos embaixo, poucos testes lentos e caros no topo.**

```
E2E  — fluxo completo do usuário (poucos, lentos)

INTEGRAÇÃO — partes reais conversando (médios)

UNITÁRIO — função/componente isolado (muitos, rápidos)
```

| Nível          | O que testa                                | Velocidade     | Quantos |
|----------------|--------------------------------------------|----------------|---------|
| **Unitário**   | Uma função/componente sozinho, com *mocks* | ⚡ muito rápido | muitos  |
| **Integração** | Rota + service + banco juntos, de verdade  | 🚶 médio       | alguns  |
| **E2E**        | Jornada inteira do usuário, vários passos  | 🐢 lento       | poucos  |

A regra prática: **se dá pra testar embaixo, teste embaixo.** Só sobe na pirâmide
o que realmente precisa de várias peças trabalhando juntas.

---

## 3. Onde fica cada coisa

```
backend/
  pytest.ini                 # config: só roda o que está em tests/
  tests/
    conftest.py              # fixtures compartilhadas (app, client, banco limpo, login...)
    unit/                    # testes UNITÁRIOS do back  → ver TESTES-BACK.md
    integration/             # testes de INTEGRAÇÃO       → ver TESTES-INT.md
    e2e/                     # testes E2E de API          → ver TESTES-E2E.md

frontend/
  vite.config.js             # bloco `test` (jsdom + setup)
  src/test/setup.js          # matchers do jest-dom
  src/**/*.test.jsx          # testes ao lado do componente → ver TESTES-FRONT.md
```

---

## 4. Qual guia ler para cada tarefa

| Você vai...                                       | Leia                |
|---------------------------------------------------|---------------------|
| Testar uma função/service do backend isolada      | **TESTES-BACK.md**  |
| Testar um componente React                        | **TESTES-FRONT.md** |
| Testar um endpoint de verdade (rota + banco)      | **TESTES-INT.md**   |
| Testar um fluxo completo (cadastro → login → ...) | **TESTES-E2E.md**   |

Cada guia é **auto-suficiente**: tem a teoria do nível, como rodar e um ou dois
exemplos prontos para copiar e adaptar.

---

## 5. Start rápido (instalar e rodar)

**Backend** (dentro de `backend/`):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                     # roda todos os testes do back
```

**Frontend** (dentro de `frontend/`):
```bash
npm install                # já inclui vitest + testing-library + jsdom
npm test                   # roda os testes do front em modo watch
```

---

## 6. Regras de ouro (valem para todos os níveis)

1. **Um teste = um comportamento.** Nome descritivo do que ele verifica.
2. **AAA:** *Arrange* (prepara) → *Act* (executa) → *Assert* (verifica).
3. **Nome de arquivo:** `test_*.py` no back, `*.test.jsx` no front.
4. Sempre que der, **ligue o teste a um caso do roteiro** (TS-01…TS-14) na
   documentação da feature.
5. Falhou? Abra issue com label `bug` e corrija numa branch `fix/<nome>`.

---

## 7. Documentação por feature

Além de escrever os testes, o QA produz um **relatório por feature** (template na
branch `docs`: `docs/qualidade/features/_template.md`), referenciando os casos do
roteiro **TS-01 a TS-14** e dando o parecer final (Aprovada / com pendências /
Reprovada). Esse passo é o "fechamento" do trabalho de QA de cada feature.
