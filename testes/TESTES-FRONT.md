# Testes do Frontend — Componentes React

> Guia para testar a interface (React + Vite). Cobre a teoria, o ambiente (já
> configurado) e exemplos prontos. Não precisa saber backend para usar este guia.

---

## 1. Teoria: o que é um teste de frontend?

No front, a "unidade" que testamos é geralmente um **componente** — um botão, um
formulário, um card. O teste **renderiza o componente num DOM simulado**, interage
com ele como um usuário faria (clica, digita) e verifica o que apareceu na tela.

Usamos duas ferramentas:

- **Vitest** — o executor de testes (o equivalente ao pytest, mas para JS).
- **React Testing Library (RTL)** — renderiza o componente e oferece formas de
  consultá-lo.

### A filosofia da Testing Library: teste como um usuário

A RTL incentiva a buscar elementos pela forma como o **usuário** os enxerga
(o texto do botão, o rótulo do campo) — **não** por detalhes internos (classe CSS,
id). Isso deixa o teste resistente a refatorações: se você troca a cor ou a
estrutura do HTML mas o botão "Salvar" continua "Salvar", o teste segue passando.

Ordem de preferência das buscas: **`getByRole`** (ex.: botão, campo) →
`getByLabelText` (formulários) → `getByText`. Evite buscar por classe/id.

---

## 2. O ambiente (já está pronto)

A tooling já está instalada e configurada. Para usar, a partir de `frontend/`:

```bash
npm install     # instala vitest, @testing-library/react, jsdom etc.
```

O que já está montado:

| Arquivo                         | Papel                                                                                |
|---------------------------------|--------------------------------------------------------------------------------------|
| `vite.config.js` → bloco `test` | usa **jsdom** (DOM falso), ativa `globals` e carrega o setup                         |
| `src/test/setup.js`             | importa os matchers extras do `@testing-library/jest-dom` (ex.: `toBeInTheDocument`) |
| `package.json` → scripts        | `test`, `test:run`, `test:coverage`                                                  |

Trecho do `vite.config.js`:
```js
test: {
  globals: true,                     // describe/it/expect sem importar
  environment: 'jsdom',              // DOM simulado para renderizar React
  setupFiles: './src/test/setup.js', // matchers do jest-dom
  css: true,                         // não quebra ao importar .css
}
```

---

## 3. Onde escrever os testes

**Ao lado do componente que ele testa**, com a extensão `.test.jsx`:

```
src/
  components/
    Botao.jsx
    Botao.test.jsx        ← teste do Botao
  pages/
    Login/
      Login.jsx
      Login.test.jsx      ← teste da página de Login
```

> Alternativa aceita: agrupar em uma pasta `__tests__/` ao lado. Mantenha um
> padrão por área para não virar bagunça.

---

## 4. Exemplos

### Exemplo 1 — renderização simples

```jsx
// src/components/Botao.test.jsx
import { render, screen } from '@testing-library/react';
import Botao from './Botao';

test('renderiza o texto do botão', () => {
  // Arrange + Act: renderiza o componente
  render(<Botao>Salvar</Botao>);

  // Assert: o botão com o texto "Salvar" está na tela
  expect(screen.getByRole('button', { name: /salvar/i })).toBeInTheDocument();
});
```

### Exemplo 2 — interação do usuário + chamada de API mockada

Quando o componente conversa com a API (via axios), **mockamos o axios** para o
teste não bater na rede de verdade.

```jsx
// src/pages/Login/Login.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import axios from 'axios';
import Login from './Login';

vi.mock('axios');   // substitui o axios por uma versão falsa

test('envia email e senha ao clicar em Entrar', async () => {
  // Arrange: a API falsa responde com um token
  axios.post.mockResolvedValue({ data: { access_token: 'abc123' } });
  render(<Login />);

  // Act: usuário preenche e clica
  await userEvent.type(screen.getByLabelText(/email/i), 'joao@email.com');
  await userEvent.type(screen.getByLabelText(/senha/i), 'Senha@123');
  await userEvent.click(screen.getByRole('button', { name: /entrar/i }));

  // Assert: o axios foi chamado com os dados certos
  expect(axios.post).toHaveBeenCalledWith(
    expect.stringContaining('/auth/login'),
    { email: 'joao@email.com', password: 'Senha@123' },
  );
});
```

> `userEvent` simula interações reais (digitar, clicar) e é assíncrono — por isso
> o `await`.

---

## 5. Como rodar

```bash
npm test               # modo watch: re-roda ao salvar (use no dia a dia)
npm run test:run       # roda uma vez e sai (use no CI)
npm run test:coverage  # roda com relatório de cobertura
```

---

## 6. Checklist antes de dar o teste por pronto

- [ ] Arquivo `*.test.jsx` ao lado do componente.
- [ ] Busca elementos por **papel/texto** (`getByRole`, `getByText`), não por classe/id.
- [ ] Chamadas à API estão **mockadas** (`vi.mock('axios')`).
- [ ] Interações usam `userEvent` com `await`.
- [ ] Segue **AAA** e cobre **um** comportamento.
- [ ] Se aplicável, mapeado a um caso do roteiro (TS-03 é o teste de UI de cadastro/login).
