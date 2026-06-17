# Documentação de Testes por Feature

Para cada feature testada, a dupla de Qualidade produz um **relatório de teste
próprio**, com identificação, casos executados (referenciando o
[roteiro TS-0X](../roteiro-testes.md)), resultado esperado × observado,
evidências, defeitos encontrados e o **status final** da feature.

---
## Relatórios disponíveis

| Feature | Func. | Sprint | Status |
|---|:--:|:--:|---|
| [Cadastro de Usuário](feature_1_cadastro-usuario.md) | A | 4 | 🚧 Aprovada com pendências |
| [Autenticação e Login](feature_2_autenticacao-login.md) | A | 4 | 🚧 Aprovada com pendências |
| [Recuperação de Senha](feature_3_recuperacao-senha.md) | A | 5 | 🚧 A preencher |
| [Cadastro de Empresa](feature_4_cadastro-empresa.md) | A | 4 | 🚧 A preencher |
| [Cadastro de Categoria](feature_5_cadastro-categoria.md) | B | 5 | 🚧 A preencher |
| [Cadastro de Transação](feature_6_cadastro-transacao.md) | C | 6 | 🚧 A preencher |
| [Histórico de Transações](feature_7_historico-transacoes.md) | D | 6 | ❌ Reprovada |
| [Exclusão de Usuário/Empresa](feature_8_exclusao-usuario-empresa.md) | A | 5 | 🚧 A preencher |
| [Centralização Documental](feature_9_centralizacao-documental.md) | G | 8 | 🚧 A preencher |
| [Simulação de Crédito](feature_10_simulacao-credito.md) | H | 9 | ❌ Reprovada |
| [Cadastro de Contas](feature_11_cadastro-contas.md) | J | 7 | 🚧 A preencher |
| [Relatórios Financeiros](feature_12_relatorios-financeiros.md) | F | 8 | 🚧 A preencher |
| [Comparação de Modalidades de Crédito](feature_14_modalidades-credito.md) | I | 9 | ❌ Reprovada |
| [Seleção de Empresa Ativa](feature_15_selecao-empresa-ativa.md) | A | 7 | 🚧 A preencher |
| [Dashboard Financeiro](feature_16_dashboard-financeiro.md) | E | 7 | 🚧 A preencher |

> Cada novo relatório segue a mesma estrutura: identificação, critérios testáveis,
> casos executados (referenciando o [Roteiro de Testes](../roteiro-testes.md)),
> evidências, defeitos e parecer final.

---
## Status possíveis

| Status                         | Significado                                           |
|--------------------------------|-------------------------------------------------------|
| ✅ **Aprovada**                 | Todos os casos passaram; feature pronta para merge    |
| 🚧 **Aprovada com pendências** | Funciona, mas há ajustes/defeitos menores registrados |
| ❌ **Reprovada**                | Casos críticos falharam; volta para desenvolvimento   |
