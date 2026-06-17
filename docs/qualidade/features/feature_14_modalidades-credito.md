# Relatório de QA — Feature 14: Comparação de Modalidades de Crédito

## 1. Identificação

| Campo                         | Valor                                                                                                                      |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **Feature**                   | US14 — Comparação de modalidades de crédito                                                                                |
| **Cenário**                   | — (não especificado na issue)                                                                                              |
| **Requisito**                 | — (não especificado na issue)                                                                                              |
| **Sprint**                    | — (não identificada)                                                                                                       |
| **Branch de desenvolvimento** | `feature/14-modalidades-credito`                                                                                           |
| **Branch de teste (QA)**      | `test/feature/14-modalidades-credito`                                                                                      |
| **Responsáveis (QA)**         | Daniel Filipe / Matheus Moretti                                                                                            |
| **Data**                      | 17/06/2026                                                                                                                 |

## 2. Critérios de aceitação testáveis

- [x] Gestor adiciona até 4 modalidades para comparar — `TS-07` (back), `TS-22` (front)
- [x] Cada modalidade tem nome, taxa de juros, prazo e tipo (PF/PJ) — `TS-03`, `TS-24`
- [x] Sistema calcula parcela, total pago e total de juros para cada — `TS-01`, `TS-02`, `TS-03`, `TS-24`
- [x] Sistema destaca a modalidade mais vantajosa (menor custo total) — `TS-04`, `TS-25`
- [x] Sistema alerta quando uma modalidade é de pessoa física — `TS-05`, `TS-26`
- [ ] Gestor exporta a comparação como PDF — lógica de geração do PDF coberta no unitário (`TS-16`) e UI verde com serviço mockado (`TS-28`), porém o **endpoint `GET /comparacoes/<id>/exportar` é inacessível** → ver **DEF-01**
- [ ] **(implícito) API da feature acessível** — todos os endpoints `/calcular`, salvar, listar, excluir e exportar retornam **404** → ver **DEF-01** (`TS-17` a `TS-20`)

## 3. Casos executados

| Caso   | Descrição                                                        | Nível      | Esperado                                | Observado                 | Status |
|--------|------------------------------------------------------------------|------------|-----------------------------------------|---------------------------|--------|
| TS-01  | `_calculate_price_table` sem juros (taxa 0)                      | Unitário   | parcela = principal/prazo, juros 0      | Conforme                  | ✅      |
| TS-02  | `_calculate_price_table` com juros (Tabela Price)                | Unitário   | parcela/total/juros da Price            | Conforme                  | ✅      |
| TS-03  | `calculate_simulation` devolve métricas por modalidade           | Unitário   | parcela, total e juros + tipo           | Conforme                  | ✅      |
| TS-04  | `calculate_simulation` destaca o menor custo total               | Unitário   | só a mais barata `is_best_option`       | Conforme                  | ✅      |
| TS-05  | `calculate_simulation` sinaliza modalidade PF                    | Unitário   | `warning_pf` só na PF, tipo normalizado | Conforme                  | ✅      |
| TS-06  | `calculate_simulation` sem modalidades                           | Unitário   | `400`                                   | Conforme                  | ✅      |
| TS-07  | `calculate_simulation` acima de 4 modalidades                    | Unitário   | `400`                                   | Conforme                  | ✅      |
| TS-08  | `_get_company_id` com usuário existente                          | Unitário   | retorna `company_id`                    | Conforme                  | ✅      |
| TS-09  | `_get_company_id` com usuário inexistente                        | Unitário   | retorna `None`                          | Conforme                  | ✅      |
| TS-10  | `save_comparison` com dados inválidos                            | Unitário   | `400` e não comita                      | Conforme                  | ✅      |
| TS-11  | `save_comparison` persiste cabeçalho + modalidades               | Unitário   | `201`, 3 `add`, 1 `commit`, id          | Conforme                  | ✅      |
| TS-12  | `get_comparisons` lista comparações da empresa                   | Unitário   | `200` + estrutura por modalidade        | Conforme                  | ✅      |
| TS-13  | `delete_comparison` de comparação existente                      | Unitário   | `200`, `delete` + `commit`              | Conforme                  | ✅      |
| TS-14  | `delete_comparison` inexistente                                  | Unitário   | `404`, sem `delete`                     | Conforme                  | ✅      |
| TS-15  | `generate_pdf_report` de comparação inexistente                  | Unitário   | `(None, 404)`                           | Conforme                  | ✅      |
| TS-16  | `generate_pdf_report` gera PDF em memória                        | Unitário   | `200` + buffer `%PDF`                   | Conforme                  | ✅      |
| TS-17  | `POST /api/comparacoes/calcular` com modalidades válidas         | Integração | `200` + 2 comparações                   | `404 NOT FOUND`           | ❌      |
| TS-18  | `POST /api/comparacoes/calcular` acima do limite                 | Integração | `400`                                   | `404 NOT FOUND`           | ❌      |
| TS-19  | `POST /api/comparacoes/` salva a comparação                      | Integração | `201` + id                              | `404 NOT FOUND`           | ❌      |
| TS-20  | `POST /api/comparacoes/calcular` sem token                       | Integração | `401`                                   | `404 NOT FOUND`           | ❌      |
| TS-21  | Página inicia com uma única modalidade                           | Unitário   | "Modalidade 1", botão calcular          | Conforme                  | ✅      |
| TS-22  | Adicionar modalidades até o limite de 4                          | Unitário   | 4 cards, botão "Adicionar" some         | Conforme                  | ✅      |
| TS-23  | Remover uma modalidade adicionada                                | Unitário   | volta a 1 modalidade                    | Conforme                  | ✅      |
| TS-24  | Calcular envia o payload e exibe métricas na tabela              | Unitário   | serviço chamado + tabela renderizada    | Conforme                  | ✅      |
| TS-25  | Destaca a modalidade mais vantajosa no resultado                 | Unitário   | selo "Melhor opção"                     | Conforme                  | ✅      |
| TS-26  | Exibe alerta quando há modalidade PF                             | Unitário   | aviso "Pessoa Física detectado"         | Conforme                  | ✅      |
| TS-27  | Não calcula quando o valor do empréstimo é inválido              | Unitário   | serviço não chamado + erro na tela      | Conforme                  | ✅      |
| TS-28  | Salvar habilita a exportação em PDF                              | Unitário   | salva e exporta pelo id retornado       | Conforme                  | ✅      |

## 4. Evidências

### Backend — unitário — `python -m pytest tests/unit/feature_14 -v`

```
tests/unit/feature_14/test_comparison_service.py::test_calculate_price_sem_juros PASSED
tests/unit/feature_14/test_comparison_service.py::test_calculate_price_com_juros PASSED
tests/unit/feature_14/test_comparison_service.py::test_calculate_simulation_retornar_metricas_por_modalidade PASSED
tests/unit/feature_14/test_comparison_service.py::test_calculate_simulation_destacar_menor_custo_total PASSED
tests/unit/feature_14/test_comparison_service.py::test_calculate_simulation_pessoa_fisica PASSED
tests/unit/feature_14/test_comparison_service.py::test_calculate_simulation_sem_modalidades PASSED
tests/unit/feature_14/test_comparison_service.py::test_calculate_simulation_acima_de_quatro_modalidades PASSED
tests/unit/feature_14/test_comparison_service.py::test_get_company_id_usuario_existente PASSED
tests/unit/feature_14/test_comparison_service.py::test_get_company_id_usuario_inexistente PASSED
tests/unit/feature_14/test_comparison_service.py::test_save_comparison_dados_invalidos PASSED
tests/unit/feature_14/test_comparison_service.py::test_save_comparison_persistir_modalidades PASSED
tests/unit/feature_14/test_comparison_service.py::test_get_comparisons_lista_da_empresa PASSED
tests/unit/feature_14/test_comparison_service.py::test_delete_comparison_existente PASSED
tests/unit/feature_14/test_comparison_service.py::test_delete_comparison_inexistente PASSED
tests/unit/feature_14/test_comparison_service.py::test_generate_pdf_report_comparacao_inexistente PASSED
tests/unit/feature_14/test_comparison_service.py::test_generate_pdf_report_gera_buffer_pdf PASSED
============================== 16 passed in 0.05s ==============================
```

> Pré-requisito de ambiente: `reportlab` precisou ser instalado no venv de teste
> para o módulo da service sequer importar — não está declarado no
> `requirements.txt` (**DEF-03**).

### Backend — integração — `python -m pytest tests/integration/feature_14 -v`

```
tests/integration/feature_14/test_comparison_endpoints.py::test_calcular_modalidades_validas FAILED
tests/integration/feature_14/test_comparison_endpoints.py::test_calcular_acima_do_limite FAILED
tests/integration/feature_14/test_comparison_endpoints.py::test_salva_comparacao FAILED
tests/integration/feature_14/test_comparison_endpoints.py::test_calcular_exige_autenticacao FAILED

E   assert 404 == 200   (where 404 = WrapperTestResponse [404 NOT FOUND])
======================== 4 failed, 3 warnings in 1.11s =========================
```

### Frontend — `npx vitest run src/pages/Comparacoes/Comparacoes.test.jsx`

```
 ✓ src/pages/Comparacoes/Comparacoes.test.jsx (8 tests) 888ms
 Test Files  1 passed (1)
      Tests  8 passed (8)
```

**Total:** 28 testes — **24 passaram, 4 falharam** (documentando **DEF-01**), 0 skip.

## 5. Defeitos encontrados

| ID     | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Branch de correção                   | Status |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|--------|
| DEF-01 | O blueprint `comparison_bp` **nunca é registrado** em `backend/app/__init__.py` (o módulo de rotas nem é importado). Todas as rotas da feature (`/calcular`, salvar, listar, excluir, exportar PDF) retornam **HTTP 404** — a API da feature está inteiramente inacessível. Confirmado por `app.url_map` (lista vazia) e pelos 4 testes de integração. Obs.: o frontend chama `/api/comparacoes/*`, então o registro precisa ser feito com esse `url_prefix`.                                                                                                                          | `fix/registra-blueprint-comparacoes` | Aberto |
| DEF-02 | No model `backend/app/models/comparison.py`, `Comparison.company`/`Comparison.user` usam `back_populates='comparisons'`, mas `Company` e `User` **não declaram** essa relação → `InvalidRequestError: Mapper 'Company' has no property 'comparisons'` ao configurar os mappers. **Raio de impacto:** importar o módulo de comparação (a própria service o faz) quebra qualquer teste/operação de banco de **outras features** — no `pytest` completo, os 11 testes de integração da feature 7 que passavam viram **ERROR**. Por isso os testes da feature 14 só rodam limpos isolados. | `fix/comparison-back-populates`      | Aberto |
| DEF-03 | `reportlab` é importado no topo de `backend/app/services/comparison_service.py`, mas **não está no `requirements.txt`** nem instalado. Numa instalação limpa o módulo da service não importa (`ModuleNotFoundError: No module named 'reportlab'`), derrubando rotas e testes.                                                                                                                                                                                                                                                                                                          | `fix/declara-reportlab-requirements` | Aberto |

> Nota (fora do escopo desta feature): a suíte completa já tinha vermelhos
> **pré-existentes** — backend: `feature_1` (`test_register_user_internal_error`,
> 2× `test_is_valid_password_spaces`) e `feature_7` (2 testes de totais com filtro);
> frontend: `Register.test.jsx` (2 testes de data de nascimento). Confirmado que
> falham independentemente desta branch; devem ser tratados nos relatórios das
> respectivas features.
>
> Nota (contaminação por outra feature): o **DEF-02** acima tem um análogo na
> **feature 10** — o **DEF-01 daquela feature** (`Simulation` → `Company` sem a
> relação `simulations`) é o mesmo tipo de quebra dos mappers do SQLAlchemy e também
> contamina a integração das features 2, 7 e 14 na suíte completa. As duas correções
> de `back_populates` (esta e a da feature 10) precisam entrar juntas para a suíte de
> integração voltar ao verde.

## 6. Cobertura

**Backend** — `pytest tests/unit/feature_14 --cov=app.services.comparison_service --cov-report=term-missing`

| Módulo                               | Cobertura | Observação                                                                                                             |
|--------------------------------------|-----------|------------------------------------------------------------------------------------------------------------------------|
| `app/services/comparison_service.py` | **100%**  | todas as 7 funções (cálculo Price, simulação, `_get_company_id`, salvar, listar, excluir e geração de PDF) exercitadas |

> As funções que tocam banco e a de PDF foram cobertas no nível **unitário** com
> mocks, pois o DEF-02 impede o uso dos models reais e o DEF-01 torna os endpoints inacessíveis.

**Frontend** — `npx vitest run src/pages/Comparacoes/Comparacoes.test.jsx --coverage`

| Módulo                                  | Cobertura | Linhas não cobertas                                                     |
|-----------------------------------------|-----------|-------------------------------------------------------------------------|
| `src/pages/Comparacoes/Comparacoes.jsx` | **96,3%** | ramos de erro/feedback (`95`, `109`, `122`) e selo PF combinado (`361`) |

Cobertura do núcleo da feature (service em 100%, página em 96,3%) acima da meta de **≥ 60%**.

## 7. Parecer final

**Reprovada.**

A lógica de negócio está totalmente coberta e verde: cálculo pela Tabela Price,
identificação da modalidade mais vantajosa, alerta de pessoa física, limite de 4
modalidades, persistência, listagem, exclusão e geração do PDF (service em 100%);
e a interface está verde e com 96,3% de cobertura. **Porém a feature não é
entregável como está**, por três defeitos de produção:

- **DEF-01** — a API inteira da feature retorna **404** (blueprint não registrado);
  nenhum dos critérios que dependem do backend (calcular, salvar, listar, exportar
  PDF) funciona ponta a ponta.
- **DEF-02** — o model quebra a configuração dos mappers do SQLAlchemy e
  **contamina o restante da suíte** (derruba a feature 7).
- **DEF-03** — a dependência de PDF (`reportlab`) não está declarada; o serviço não
  importa numa instalação limpa.

**Próximos passos para reavaliação:**
1. **DEF-01** — registrar `comparison_bp` em `app/__init__.py` com `url_prefix='/api/comparacoes'`.
2. **DEF-02** — declarar as relações `comparisons` em `Company` e `User` (ou remover o `back_populates`).
3. **DEF-03** — adicionar `reportlab` ao `requirements.txt`.
