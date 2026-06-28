---
template: home.html
hide:
  - toc
---

# CrediFab — Documentação do Grupo Parnas

> Governança financeira e preparação para o acesso ao crédito de micro e
> pequenas empresas (MPEs).

Bem-vindo à central de documentação do **CrediFab**, projeto desenvolvido pelo
Grupo Parnas na disciplina de Métodos de Desenvolvimento de Software
(MDS) da Universidade de Brasília (UnB), no semestre 2026.1.

Este site reúne, em um único lugar, os artefatos formais do projeto, os
registros de gestão (atas e presenças) e — com destaque — a documentação de
qualidade e testes produzida ao longo das Sprints.

---

## O que é o CrediFab

O CrediFab é uma **aplicação web** voltada a apoiar micro e pequenas empresas na
**organização das suas finanças** e na **preparação para solicitar crédito**.
A ideia central é dar ao empreendedor uma visão clara da saúde financeira do seu
negócio — categorizando receitas e despesas, registrando transações, oferecendo
histórico e relatórios — para que ele chegue mais bem preparado ao banco.

O projeto está alinhado à meta **ODS 9.3** da ONU, que trata de *ampliar o
acesso das pequenas empresas a serviços financeiros e crédito acessível*.

|                 |                                               |
|-----------------|-----------------------------------------------|
| **Disciplina**  | Métodos de Desenvolvimento de Software (MDS)  |
| **Instituição** | Universidade de Brasília — FGA                |
| **Semestre**    | 2026.1                                        |
| **Turma**       | T01                                           |
| **Docente**     | Ricardo Ajax Dias Kosloski                    |
| **Grupo**       | Parnas (12 integrantes)                       |
| **ODS**         | 9.3 — Acesso a crédito para pequenas empresas |

---

## Propósito desta documentação

Esta documentação tem três objetivos:

1. **Centralizar os artefatos do projeto** — Documento de Visão, Documento de
   Arquitetura, atas de reunião e registros de presença ficam acessíveis em um
   só endereço, versionados junto ao código.
2. **Tornar a qualidade rastreável** — cada feature testada gera um documento de
   teste próprio; cada Sprint gera um consolidado e uma análise GQM. Assim é
   possível acompanhar a evolução da cobertura e dos defeitos ao longo do tempo.
3. **Servir de referência ao time** — integrantes e avaliadores encontram
   aqui a stack, a arquitetura, os requisitos e a estratégia de testes do
   produto.

---

## Por onde navegar

| Seção                                    |  O que você encontra                                                          |
|------------------------------------------|-------------------------------------------------------------------------------|
| [O Grupo](sobre/index.md)                | Quem é o Grupo Parnas, a disciplina e os integrantes                          |
| [Produto](produto/index.md)              | O CrediFab, o Documento de Visão e o de Arquitetura                           |
| [Qualidade](qualidade/index.md)          | Estratégia de testes, roteiro, docs por feature, consolidados de Sprint e GQM |
| [Issues](issues/index.md)                | Histórias de usuário, tarefas técnicas e correções (fixes)                    |
| [Atas de Reunião](atas-reuniao/index.md) | Registros das reuniões do grupo                                               |
| [Presenças (gov.br)](presencas/index.md) | Listas de presença assinadas digitalmente                                     |

---

## Status atual

O projeto é desenvolvido em ciclos semanais (Sprints), do cadastro de
usuário/empresa até a simulação de crédito. O acompanhamento detalhado de cada
ciclo está em [Consolidados por Sprint](qualidade/sprints/index.md).

| Sprint  |    Período    |  Foco                                                             |  Cenário |
|:-------:|:-------------:|-------------------------------------------------------------------|:--------:|
|    4    |   17–23/mai   | Cadastro e autenticação de usuário/empresa                        |  CEN-00  |
|    5    |   24–30/mai   | Registro de dados financeiros (categorias, transações, histórico) |  CEN-01  |
|    6    | 31/mai–06/jun | Centralização documental                                          |  CEN-02  |
|    7    |   07–13/jun   | Relatórios financeiros                                            |  CEN-03  |
|   8–9   |   14–27/jun   | Diagnóstico e simulação de crédito                                |  CEN-04  |
|   10    | 28/jun–04/jul | Produto final                                                     |    —     |

---

## Atalhos de teclado

Este site tem atalhos de teclado para navegar mais rápido. São eles:
=== "Ir para"

    Pressione `g` e, em seguida, a tecla do destino:

    | Sequência | Destino |
    | :-------: | --- |
    | `g` `h` | Home |
    | `g` `g` | O Grupo |
    | `g` `p` | Produto |
    | `g` `v` | Documento de Visão |
    | `g` `a` | Documento de Arquitetura |
    | `g` `q` | Qualidade |
    | `g` `r` | Roteiro de Testes |
    | `g` `t` | Atas de Reunião |

=== "Utilitários"

    | Tecla | Ação |
    | :---: | --- |
    | `m` | Alternar tema (claro/escuro/preferência do sistema) |
    | `y` | Copiar a URL da página atual |

=== "Nativos do tema"

    | Tecla | Ação |
    | :----------: | --- |
    | `f` `s` `/` | Focar a busca |
    | `p` | Página anterior |
    | `n` | Próxima página |
    | `Esc` | Fechar a busca |

!!! tip "Dica"
    O prefixo `g` fica ativo por ~1,5 s aguardando a segunda tecla. Os atalhos
    não disparam enquanto você digita na caixa de busca.

---
