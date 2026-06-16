# Documentação de Testes por Feature

Para cada feature testada, a dupla de Qualidade produz um **relatório de teste
próprio**, com identificação, casos executados (referenciando o
[roteiro TS-0X](../roteiro-testes.md)), resultado esperado × observado,
evidências, defeitos encontrados e o **status final** da feature.

---
## Relatórios disponíveis

| Feature                                                 | Sprint | Status                     |
|---------------------------------------------------------|:------:|----------------------------|
| [Cadastro de Usuário](feature_1_cadastro-usuario.md)    |   4    | 🚧 Aprovada com pendências |
| [Autenticação e Login](feature_2_autenticacao-login.md) |  4–5   | 🚧 Aprovada com pendências |

> Use o [Template de Documentação de Testes](_template.md) como ponto de partida
> para cada nova feature.

---
## Status possíveis

| Status                         | Significado                                           |
|--------------------------------|-------------------------------------------------------|
| ✅ **Aprovada**                 | Todos os casos passaram; feature pronta para merge    |
| 🚧 **Aprovada com pendências** | Funciona, mas há ajustes/defeitos menores registrados |
| ❌ **Reprovada**                | Casos críticos falharam; volta para desenvolvimento   |
