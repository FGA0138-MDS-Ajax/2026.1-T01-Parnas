# Documentação de Teste - Refactor de Bancos e Rotas

## 1. Identificação

| Campo | Valor |
|---|---|
| **Tarefa** | Refatoração da persistência (Repositories + migrations consolidadas) e rotas - implementação da task6 |
| **Branch de desenvolvimento** | `integration/refactor-banco-rotas` |
| **Branch base comparada** | `develop` |
| **PR** | #79 (aponta para a **`main`**) |
| **Sprint** | 8 |
| **Responsáveis (QA)** | Daniel Filipe / Matheus Moretti |
| **Data** | 27/06/2026 |
| **Parecer** | **REPROVADA** (ver §6) |

> Por ser uma tarefa de **refatoração**, não cabe "aprovada com pendências": ou a base
> está íntegra (suíte verde), ou é reprovada com os defeitos apontados.

---
## 2. Escopo e fronteira do relatório

PR **gigante** (46 arquivos vs `develop`; +18k/-1.5k vs `main`) que aponta direto para a
`main`. Por inviabilidade de cobrir todas as frentes, o QA focou no **núcleo da
refatoração: a camada de repositórios**, exercitada contra o BD em memória. As demais
frentes (rotas, services, migrations) foram avaliadas pelo estado da suíte existente.

---
## 3. Casos executados (núcleo - repositórios)

Suíte `tests/integration/refactor_repositorios/test_repositorios_core.py`.

| Caso | Descrição | Esperado | Status |
|---|---|---|:--:|
| QA-01 | `BaseRepository.save/find_by_id/delete` | CRUD genérico funciona | Passou |
| QA-02 | `UserRepository.get_by_email/get_by_cpf` | localiza o usuário | Passou |
| QA-03 | `UserRepository.update_active_company` | grava empresa ativa | Passou |
| QA-04 | `UserRepository.list_companies` | lista empresas do usuário | Passou |
| QA-05 | `CompanyRepository.create/get_by_id` | cria e recupera | Passou |
| QA-06 | `CompanyRepository.get_by_cnpj` limpa formatação | encontra por CNPJ formatado | Passou |
| QA-07 | `CompanyRepository.attach_user/check_user_access/get_all_by_user` | vínculo e acesso | Passou |

**7 testes, 0 falhas.** O núcleo de repositórios (Base, User, Company) está correto.

---
## 4. Evidências

```bash
python -m pytest tests/integration/refactor_repositorios -q
# 7 passed
```

Estado da suíte completa do backend na branch:

```bash
python -m pytest -q
# 2 errors during collection
#   ERROR tests/unit/feature_2/test_auth_service.py  (ImportError: cannot import name 'AuthService')
#   ERROR tests/unit/feature_11/test_bill_service.py
# (ignorando os 2 acima): 100 failed, 128 passed, 15 xfailed, 1 xpassed
```

---
## 5. Defeitos / bloqueios

| Item | Descrição | Status |
|---|---|---|
| BLK-1 | **Erros de coleção**: `auth_service` deixou de expor a classe `AuthService` (virou funções de módulo) e `bill_service` mudou; os testes antigos quebram a coleção do pytest, interrompendo a suíte. | Aberto |
| BLK-2 | **~100 testes falhando** após a reescrita dos services (feature_1, 4, 5, 6, 7, 8, 9, 10, 11, 12). São testes não reconciliados com a refatoração - mesma natureza da task7, porém em volume muito maior. | Aberto |

---
## 6. Parecer final

> **Status:** Reprovada
>
> O **núcleo** da refatoração (camada de repositórios) está correto e coberto (7/7). No
> entanto, a branch **não pode ser mesclada na `main`** no estado atual: a suíte de testes
> está quebrada (2 erros de coleção + ~100 falhas) porque os testes e parte dos services
> não foram reconciliados com a reescrita. Para um PR de refatoração que aponta para a
> `main`, isso é bloqueante.
>
> **Para reavaliação:** corrigir os erros de coleção (atualizar `tests/unit/feature_2` e
> `tests/unit/feature_11` às novas APIs), reconciliar a suíte com os novos services e
> repositórios (em coordenação com a task7), e só então abrir/atualizar o PR. O design da
> camada de repositórios em si está aprovado.
