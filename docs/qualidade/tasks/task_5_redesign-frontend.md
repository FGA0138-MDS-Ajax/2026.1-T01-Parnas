# Documentação de Teste - Tarefa V: Redesign do Frontend

## 1. Identificação

| Campo                          | Valor                                                                     |
|--------------------------------|---------------------------------------------------------------------------|
| **Tarefa**                     | Tarefa V - redesign do frontend (parte da issue `task5`, DTOs e redesign) |
| **Escopo deste relatório**     | Somente frontend (marcação, CSS e testes)                                 |
| **Telas**                      | Autenticação, categorias e painel                                         |
| **Branch de desenvolvimento**  | `refactor/redesign-frontend`                                              |
| **Branch base comparada**      | `develop`                                                                 |
| **Sprint**                     | 8                                                                         |
| **Responsáveis (QA)**          | Daniel Filipe / Matheus Moretti                                           |
| **Data**                       | 21/06/2026                                                                |
| **Evidências**                 | Pipeline CI - job `frontend` (artifact `relatorio-frontend`)              |
| **Parecer**                    | **APROVADA** (ver §6)                                                     |

---

## 2. Escopo e fronteira do relatório

Esta refatoração mexe **apenas no frontend**: marcação, CSS e os respectivos
testes. Não altera contrato, rotas nem regras do backend, então a avaliação se
restringe ao **job `frontend`** da pipeline, que o GitHub Actions aprovou
(verde). O job de backend está fora do escopo desta entrega.

O commit `style: refatora interface do fluxo de autenticação e painéis para nova
identidade visual` redesenhou as telas:

- `Login`, `Register`, `EsqueciSenha`, `RedefinirSenha` (fluxo de autenticação);
- `Categorias`, `Dashboard`, `Transacoes` e o `LayoutBase`.

Ganho colateral observado: o `Register.jsx` deixou de ter os campos Nome e Senha
"soltos" - agora são controlados, e as validações de data futura, idade mínima
(16) e senha curta funcionam (eram `test.skip` na `develop`).
---

## 3. Casos executados (frontend)

Suíte Vitest + Testing Library, criada para cobrir as telas redesenhadas
(`npm run test:coverage`). **72 testes em 12 arquivos, 0 falhas.** Os casos
abaixo são os criados para o redesign.

| Caso  | Descrição                                                         | Nível      | Esperado                                    | Status |
|-------|-------------------------------------------------------------------|------------|---------------------------------------------|:------:|
| TS-01 | Login renderiza e-mail, senha e botão Entrar                      | Unitário   | Campos e botão presentes                    | Passou |
| TS-02 | Login com sucesso guarda token e redireciona ao dashboard         | Integração | `POST /auth/login`, token salvo, navegou    | Passou |
| TS-03 | Login com credenciais inválidas mostra erro da API                | Integração | Mensagem do backend, sem token/redirect     | Passou |
| TS-04 | Login barra senha < 8 antes da API                                | Unitário   | Erro local, `fetch` não chamado             | Passou |
| TS-05 | Acesso demo gera token e leva ao dashboard sem API                | Unitário   | Token demo, navegou, sem `fetch`            | Passou |
| TS-06 | Register valida data de nascimento futura                         | Componente | "Data de nascimento inválida"               | Passou |
| TS-07 | Register valida idade mínima de 16 anos                           | Unitário   | "pelo menos 16 anos"                        | Passou |
| TS-08 | Register valida senha < 8                                         | Unitário   | "no mínimo 8 caracteres"                    | Passou |
| TS-09 | Register válido chama `POST /api/register` com CPF limpo          | Integração | Payload com `"cpf":"12345678900"`           | Passou |
| TS-10 | EsqueciSenha: solicitação e erro da API                           | Integração | Sucesso e mensagem de falha                 | Passou |
| TS-11 | EsqueciSenha: token na URL abre o formulário de nova senha        | Unitário   | Tela "Nova senha", valida senha/divergência | Passou |
| TS-12 | RedefinirSenha valida senha curta, divergência e sucesso          | Unitário   | Mensagens corretas em cada caso             | Passou |
| TS-13 | Categorias: listar, adicionar, editar inline, excluir/cancelar    | Unitário   | CRUD em memória consistente                 | Passou |
| TS-14 | Dashboard: painel, navegação e listagem de empresas               | Unitário   | Render, navega, lê `localStorage`           | Passou |

> A suíte completa do front também inclui testes herdados de Contas, Documentos,
> Configuracoes, Transacoes e hooks, todos verdes, somando os 72.

---

## 4. Evidências

Job `frontend` da pipeline (`npm run test:coverage`):

```
 Test Files  12 passed (12)
      Tests  72 passed (72)
```

Comando reproduzível localmente (a partir de `frontend/`):

```bash
npm ci
npm run test:run
```

---

## 5. Cobertura (frontend)

Telas do redesign (`npm run test:coverage`, v8):

| Módulo                | % Stmts  | % Branch  |
|-----------------------|:--------:|:---------:|
| `Login.jsx`           | 96.57    | 72.22     |
| `Register.jsx`        |  94.04   |   80.00   |
| `EsqueciSenha.jsx`    |  85.63   |   77.77   |
| `RedefinirSenha.jsx`  |  98.86   |   92.85   |
| `Categorias.jsx`      |   100    |    100    |
| `Dashboard.jsx`       |   100    |   83.33   |

> O total do projeto (47.8%) é puxado para baixo por módulos fora do escopo do
> redesign (`Comparacoes`, `Relatorios`, `Simulacoes`, `services/`, `utils/`),
> sem teste; não reflete a qualidade das telas refatoradas.

---

## 6. Parecer final

**APROVADA.**

A refatoração é **somente de frontend** (marcação, CSS e testes) e está íntegra:
o job `frontend` da pipeline passou no GitHub Actions, com **72 testes verdes** e
boa cobertura nas telas redesenhadas. Ainda houve ganho de validações no
`Register`, que voltaram a funcionar.

Sem pendências. A entrega pode ser mesclada do ponto de vista do frontend.
