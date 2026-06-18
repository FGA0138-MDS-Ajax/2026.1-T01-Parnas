# Relatório de QA — Tarefa IV: Integração do Ciclo de Vida (Usuário / Empresa / Autenticação)

## 1. Identificação

| Campo                         | Valor                                                        |
|-------------------------------|-------------------------------------------------------------|
| **Tarefa**                    | Tarefa IV — Integração ponta a ponta (issue #26)            |
| **Requisitos**                | R01, R02, R03, R04, R05                                      |
| **Casos do roteiro**          | TS-12, TS-13, TS-14, TS-18                                   |
| **Branch de desenvolvimento** | `task/integracao`                                           |
| **Branch base comparada**     | `develop`                                                    |
| **Branch de teste (QA)**      | `test/task/integracao-qa`                                    |
| **Data**                      | 18/06/2026                                                   |
| **Parecer**                   | **❌ REPROVADA** (ver §6)                                    |

> Por ser uma tarefa de **integração/refatoração**, não cabe "aprovada com
> pendências": ou o fluxo está íntegro, ou é reprovada com os defeitos apontados.

---

## 2. Como ler este relatório (para back e front)

Cada defeito abaixo aponta **arquivo:linha**, o que está errado, o impacto para o
usuário e a correção sugerida. A severidade é:

- 🔴 **Crítico** — quebra o fluxo (erro 500, tela que não funciona, dado corrompido).
- 🟠 **Alto** — funciona em parte, mas viola o critério de aceitação ou expõe risco.
- 🟡 **Médio** — inconsistência/desvio de arquitetura que precisa ser alinhado.

---

## 3. Defeitos de BACKEND

### 🔴 DEF-B1 — Exclusão **e** atualização de empresa quebradas (erro 500)

**Arquivo:** `backend/app/services/company_service.py`

A função é **declarada com 2 parâmetros**, mas é **chamada com 1** em três pontos:

```python
45:  def find_company(company_CNPJ, user_id):      # <- exige 2 argumentos
...
52:      company = find_company(cnpj_clean)        # delete_company  -> 1 argumento
75:      company = find_company(cnpj_clean)        # update_company  -> 1 argumento
93:      if find_company(novo_cnpj_clean):         # update_company  -> 1 argumento
```

**Impacto:** toda chamada a `DELETE /api/companies/delete` e `PUT /api/companies/update`
estoura `TypeError: find_company() missing 1 required positional argument: 'user_id'`,
que vira **HTTP 500**. Ou seja, **na `develop` ninguém consegue excluir nem editar empresa.**
Isso derruba os casos **TS-14** (exclusão/cascata) e **TS-18** (isolamento), pois o
erro acontece **antes** da verificação de permissão.

> Observação importante: a branch `task/integracao` **já corrige** isto
> (lá `find_company` tem 1 parâmetro). O defeito está hoje na **`develop`** —
> provavelmente um `user_id` foi adicionado à assinatura em outro merge sem
> atualizar as chamadas.

**Correção (back):** remover o parâmetro não usado na linha 45:

```python
def find_company(company_CNPJ):
```

---

### 🔴 DEF-B2 — `task/integracao` está atrasada e o merge **apaga features inteiras**

**Escopo:** diff `develop → task/integracao` (backend).

A branch foi criada antes de várias features entrarem na `develop` e, ao ser mesclada,
**remove** código que hoje está em produção interna:

```
backend/app/models/comparison.py            (removido)
backend/app/models/simulation.py            (removido)
backend/app/routes/comparison_routes.py     (removido)
backend/app/routes/report_routes.py         (removido)
backend/app/routes/simulation_routes.py     (removido)
backend/app/services/comparison_service.py  (removido)
backend/app/services/report_service.py      (removido)
backend/app/services/simulation_service.py  (removido)
backend/app/schemas/report_schema.py        (removido)
backend/app/schemas/simulation_schema.py    (removido)
```

**Impacto:** abrir PR desta branch para a `develop` **regride as features 10/12/13/14**
(simulação de crédito, relatórios, comparação de modalidades). Risco de regressão massiva.

**Correção (back):** **atualizar a branch com a `develop`** (`git merge develop` ou rebase)
e resolver os conflitos **antes** de abrir o PR. O PR só deve conter o que a Tarefa IV
adiciona, nunca remoções das outras features.

---

### 🟠 DEF-B3 — Token de redefinição expira em 60 min (critério pede 30)

**Arquivo:** `backend/app/utils/reset_token.py:7`

```python
def verify_reset_token(token, expiration=3600):   # 3600s = 60 min
```

**Impacto:** viola o critério da issue #3/#26 ("link expira em **30 minutos**").

**Correção (back):** usar `expiration=1800`.

---

### 🟠 DEF-B4 — Token de reset volta no corpo da resposta e não há e-mail no backend

**Arquivo:** `backend/app/routes/auth_routes.py:46-51`

```python
46:  reset_link = f"http://localhost:5173/esqueci-senha?token={token}"
48:  return jsonify({
49:      "mensagem": "Token gerado",
50:      "reset_link": reset_link,        # <- token exposto na resposta da API
51:      "email": user.email
```

**Impacto:** qualquer um que chame `POST /auth/forgot-password` recebe o token de
redefinição de outra conta no corpo do JSON. O requisito pedia envio por **Flask-Mail**
no backend; aqui o envio foi empurrado para o frontend (ver DEF-F4).

**Correção (back):** enviar o link por e-mail no backend e **não** retornar o token na resposta.

---

## 4. Defeitos de FRONTEND

### 🔴 DEF-F1 — A tela "Redefinir Senha" é um stub: não faz nada

**Arquivo:** `frontend/src/pages/RedefinirSenha/RedefinirSenha.jsx:45-58`

```jsx
48:  // await api.post('/reset-password', {     <- chamada real comentada
49:  //   password: newPassword
50:  // });
52:  await new Promise((resolve) =>             <- "sucesso" falso por timeout
53:    setTimeout(resolve, 1500)
54:  );
56:  setSuccessMessage('Senha redefinida com sucesso.');
```

**Impacto:** a rota `/redefinir-senha` (`routes.jsx:69`) **nunca lê o token da URL** e
**nunca chama** `POST /auth/reset-password`. Ela só exibe "Senha redefinida com sucesso"
sem alterar nada no banco. A tarefa marcou "Criar a tela de Redefinir Senha" como
concluída, mas a tela não está integrada.

**Correção (front):** ou implementar de fato a chamada (ler `token` da URL + `api.post`),
ou remover a rota/página e consolidar tudo em `EsqueciSenha.jsx` (ver DEF-F2).

---

### 🔴 DEF-F2 — Token extraído errado: o link de e-mail nasce quebrado

**Arquivo:** `frontend/src/pages/EsqueciSenha/EsqueciSenha.jsx:49-51`

```jsx
49:  const rawToken = data.reset_link.substring(data.reset_link.lastIndexOf('/') + 1);
51:  const reactResetLink = `http://localhost:5173/esqueci-senha?token=${safeToken}`;
```

O backend devolve `reset_link = ".../esqueci-senha?token=<TOKEN>"`. Como o token vem
após `?token=` (e não após uma `/`), `lastIndexOf('/')` pega o trecho
**`esqueci-senha?token=<TOKEN>`** inteiro como se fosse o token.

**Impacto:** o link enviado por e-mail fica com o token corrompido
(`...?token=esqueci-senha%3Ftoken%3D<TOKEN>`). Quando o usuário clica, o
`POST /auth/reset-password` recebe um token inválido e responde **"Token inválido
ou expirado"**. **O fluxo real (por e-mail) de redefinição não funciona.**

**Correção (front):** ler o parâmetro de query corretamente, por exemplo:

```jsx
const url = new URL(data.reset_link);
const rawToken = url.searchParams.get('token');
```

---

### 🟠 DEF-F3 — Dois fluxos de redefinição concorrentes / página órfã

**Arquivos:** `EsqueciSenha.jsx` (linhas 139 e 163) · `RedefinirSenha.jsx` · `routes.jsx:68-69` · `auth_routes.py:46`

`EsqueciSenha.jsx` faz **as duas coisas** (pedir token *e* redefinir senha, decidindo
pela presença de `?token=` na URL). Ao mesmo tempo existe a página dedicada
`RedefinirSenha` (DEF-F1, morta). E o backend aponta o link para `/esqueci-senha`,
deixando `/redefinir-senha` **sem uso**.

**Impacto:** arquitetura confusa, código duplicado e uma rota que nunca é alcançada.

**Correção (front + back):** escolher **um** fluxo. Sugestão: link aponta para
`/redefinir-senha`, que passa a ser a tela funcional; `EsqueciSenha` cuida só do pedido.

---

### 🟠 DEF-F4 — Envio de e-mail no cliente com credenciais hardcoded

**Arquivo:** `frontend/src/pages/EsqueciSenha/EsqueciSenha.jsx:53-62`

```jsx
53:  emailjs.init("XadOERpbRkiSIy1-_");
55:  await emailjs.send('service_mr9gkdu', 'template_zzte7bw', { ... });
```

**Impacto:** chaves do EmailJS expostas no bundle do frontend (qualquer um inspeciona e
usa). Além disso, o envio é client-side, divergindo do requisito de **Flask-Mail** no
backend — se o JS falhar/for bloqueado, nenhum e-mail sai.

**Correção:** mover o envio para o backend (Flask-Mail) e tirar as chaves do código do front.

---

### 🟡 DEF-F5 — Proxy do Vite tem entrada que não corresponde ao backend

**Arquivo:** `frontend/vite.config.js:18-22`

Há proxy para `/company`, mas o blueprint de empresa está registrado em
`/api/companies` (`backend/app/__init__.py:42`). A entrada `/company` nunca é usada.

**Impacto:** baixo (entrada morta), mas indica chamada de empresa apontando para prefixo errado.

**Correção (front):** padronizar as chamadas de empresa em `/api/companies` e remover o proxy `/company`.

---

## 5. O que está correto (validado pelos testes de QA)

A suíte `backend/tests/e2e/task_4/test_lifecycle_integration.py` exercitou o ciclo
ponta a ponta contra a `develop`:

| Fluxo                                                       | Caso  | Resultado |
|------------------------------------------------------------|-------|-----------|
| Cadastro → login → JWT abre rota protegida de empresa      | TS-12 | ✅ passou |
| Empresa criada fica vinculada ao usuário criador           | TS-18 | ✅ passou |
| Recuperação de senha (gera token → redefine → login novo)  | TS-13 | ✅ passou (via token direto, sem o link do e-mail — ver DEF-F2) |
| Exclusão do próprio usuário                                 | TS-14 | ✅ passou |
| Exclusão de empresa (cascata no vínculo)                   | TS-14 | ⚠️ bloqueado por **DEF-B1** |
| Isolamento: usuário não exclui empresa de outro            | TS-18 | ⚠️ bloqueado por **DEF-B1** |

> A mecânica de login/JWT, vínculo usuário-empresa e o núcleo da redefinição de senha
> (token) funcionam. O que reprova a tarefa são os defeitos que **impedem** exclusão/edição
> de empresa (back) e a redefinição via e-mail (front), além da branch desatualizada.

---

## 6. Parecer final

**❌ REPROVADA.**

A integração não pode ser mesclada no estado atual por três motivos bloqueantes:

1. **DEF-B1** — exclusão e atualização de empresa retornam 500 na `develop`
   (assinatura de `find_company`); derruba TS-14 e TS-18.
2. **DEF-B2** — a branch `task/integracao` está atrás da `develop` e seu merge
   **apaga** as features 10/12/13/14. Precisa ser atualizada antes do PR.
3. **DEF-F1 + DEF-F2** — o fluxo de redefinição de senha por e-mail está quebrado
   no front (tela stub + token mal extraído).

**Para reavaliação, corrigir na ordem:** DEF-B1 → DEF-B2 (atualizar branch) →
DEF-F2 → DEF-F1/F3 → DEF-B3/B4/F4/F5.
