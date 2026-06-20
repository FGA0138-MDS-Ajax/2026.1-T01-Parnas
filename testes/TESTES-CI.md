# Integração Contínua (CI)

> Como a pipeline de testes roda sozinha no GitHub Actions a cada push/PR.
> Mantido pela dupla de Qualidade (Daniel Filipe / Matheus Moretti).

---

## 1. Como funciona a CI:

A **Integração Contínua (CI)** funciona ao deixar uma máquina rodar nossa suíte de testes
**automaticamente**, toda vez que código novo chega no repositório. Em vez de
confiar que cada pessoa lembrou de rodar `pytest`/`vitest` antes de subir, o
GitHub roda por nós e mostra um ✅ ou ❌ no Pull Request.

---

## 2. Onde mora a pipeline

Um único arquivo:

```
.github/workflows/tests.yml
```

> **Regra de ouro do GitHub Actions:** para eventos de `push`, o workflow é lido
> **da branch onde o commit caiu**. Um workflow que só existe numa branch é
> invisível para as outras. Por isso o `tests.yml` precisa estar na `develop`
> (e na `main`) — assim ele vale para o que a gente realmente entrega.
>
> Já o evento `pull_request` lê o workflow **da branch de destino**. Como o
> destino é a `develop`, **todo PR que aponta para a `develop` roda os testes**,
> mesmo vindo de uma branch criada antes do workflow existir.

---

## 3. Quando ela roda

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

- **Push** direto em `main` ou `develop`.
- **Pull Request** cujo destino seja `main` ou `develop` (abrir o PR e cada novo
  push nele re-disparam a checagem).

---

## 4. O que ela faz

Dois **jobs** independentes, rodando **em paralelo**, cada um numa máquina
virtual Ubuntu **limpa** (nasce sem nada do nosso projeto):

| Job        | Pasta       | Passos                                                                                           |
|------------|-------------|--------------------------------------------------------------------------------------------------|
| `backend`  | `backend/`  | clona o repo → instala Python 3.14 → `pip install -r requirements.txt` → `pytest` + coverage     |
| `frontend` | `frontend/` | clona o repo → instala Node 20 → `npm ci` → `npm run test:coverage` (vitest)                     |

Como são jobs separados, o tempo total é o do mais lento, não a soma. Cada um
usa cache (de `pip` e de `npm`) para não reinstalar tudo do zero quando as
dependências não mudam.

### Passou ou falhou?

Cada comando é avaliado pelo **exit code**: `0` = sucesso, qualquer outra coisa =
falha. O `pytest` retorna `0` se tudo passou; o `vitest`, idem. Se um passo
falha, o job fica **vermelho** e aquele check do PR reprova.

---

## 5. Testes "amarelos": `xfail` e `skip`

Nem todo teste vermelho é culpa do CI — alguns documentam **bugs/lacunas
conhecidos** que ainda não foram corrigidos. Para esses, em vez de apagar o
teste (e perder o registro do problema), a gente o mantém **marcado**:

- **Backend — `@pytest.mark.xfail(reason="...", strict=False)`**
  O pytest roda o teste, vê que ele falha *como esperado*, e conta como
  `xfailed` (não quebra o CI). Se um dia o bug for corrigido, ele passa a
  `xpassed` — um aviso gentil de que dá para remover a marca.

- **Frontend — `test.skip('...')`** com um comentário `// TODO:` em cima
  explicando o motivo e quando remover.

> **Regra:** toda marca `xfail`/`skip` tem que dizer **por quê** e **quando sai**.
> Ela é dívida técnica rastreável, não tapete para esconder sujeira. Ao corrigir
> o código, **remova a marca** no mesmo PR.

Pendências atuais (a corrigir em PRs próprios):

| Teste                                    | Marca    | Motivo                                                          |
|------------------------------------------|----------|-----------------------------------------------------------------|
| histórico — filtro por tipo / totais     | `xfail`  | bug real: `Decimal - float` estoura em `transaction_service.py` |
| senha com espaço (2 casos)               | `xfail`  | `is_valid_password` ainda aceita espaço (decisão de produto)    |
| register — erro interno de banco         | `xfail`  | `register_user` não faz `rollback`/500 em erro de commit        |
| cadastro — data futura / menor de 18     | `skip`   | `Register.jsx` ainda não valida data/idade                      |

---

## 6. Rodar a mesma coisa na sua máquina

O CI não faz mágica — roda os mesmos comandos que você roda local:

**Backend** (dentro de `backend/`):
```bash
pip install -r requirements.txt
pytest                     # esperado: passed + alguns xfailed, 0 failed
```

**Frontend** (dentro de `frontend/`):
```bash
npm ci
npm run test:run           # esperado: passed + alguns skipped, 0 failed
```

Se passa local, passa no CI. Se falhar só no CI, quase sempre é dependência que
você tem instalada na mão mas não está no `requirements.txt`/`package.json`.

---

## 7. Coverage e os artifacts (insumo do relatório de feature)

Além de passar/falhar, a pipeline **mede a cobertura** (quais linhas do código os
testes exercitam) e **guarda os resultados** como *artifacts* — arquivos que você
baixa pela aba **Actions** do GitHub, na seção **Artifacts** do rodapé do run.

| Artifact             | O que tem dentro                                                                          |
|----------------------|-------------------------------------------------------------------------------------------|
| `relatorio-backend`  | `test-output.txt` (resultado + coverage por arquivo), `coverage.xml`, `test-results.xml`  |
| `relatorio-frontend` | `test-output.txt` (resultado + tabela de coverage) e a pasta `coverage/` (HTML navegável) |

O passo de upload usa `if: always()`, então os dados são publicados **mesmo quando
algum teste falha** — útil justamente pra investigar a falha.

> **Por que isso existe:** o CI **não** gera o relatório de QA sozinho (isso exigiria
> um modelo de IA rodando no CI, que é pago). O relatório continua sendo um passo
> da dupla de QA — a pipeline só entrega os números.

---
