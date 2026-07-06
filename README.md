Readme · MD
# Credifab — Sistema de Gestão Financeira
 
> Projeto desenvolvido para a disciplina de **Métodos de Desenvolvimento de Software (MDS)**
> Universidade de Brasília — FGA | Prof. Ricardo Ajax Dias Kosloski
 
O **Credifab** é uma plataforma de controle e gestão financeira voltada para microempresas. O sistema permite o gerenciamento completo de fluxo de caixa, controle de usuários, organizações, categorias, contas a pagar e a receber, simulações de crédito e centralização documental.
 
---
 
## Tecnologias Utilizadas
 
### Backend
| Tecnologia | Uso |
|---|---|
| Python 3.12 + Flask | API REST |
| SQLAlchemy | ORM e mapeamento de dados |
| Alembic / Flask-Migrate | Controle de migrações |
| PyJWT + Bcrypt | Autenticação e segurança |
| Marshmallow | Validação e serialização (DTOs) |
| PostgreSQL + Psycopg2 | Banco de dados relacional |
| Pytest + Coverage | Testes automatizados |
 
### Frontend
| Tecnologia | Uso |
|---|---|
| React + Vite | Interface do usuário |
| React Router DOM | Navegação entre páginas |
| Axios | Consumo da API |
| Recharts | Gráficos e visualizações |
 
---
 
## Como Executar o Projeto Localmente

O projeto é desacoplado — backend e frontend rodam em terminais separados.

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- PostgreSQL rodando localmente (instalado e com o serviço ativo antes de qualquer comando abaixo)

### 1. Banco de Dados (PostgreSQL)

Antes de criar o banco, garanta que o PostgreSQL está instalado e o serviço está rodando na sua máquina.

**Linux (Arch/Manjaro):**
```bash
sudo pacman -S postgresql
sudo -u postgres initdb -D /var/lib/postgres/data   # apenas na primeira instalação
sudo systemctl enable --now postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

**macOS (Homebrew):**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Windows:**
Baixe o instalador em [postgresql.org/download](https://www.postgresql.org/download/windows/) e siga o assistente — ele já configura o serviço para iniciar automaticamente.

Confirme que o serviço está ativo antes de continuar:
```bash
pg_isready
# Deve retornar algo como: /tmp:5432 - accepting connections
```

Se o usuário `postgres` ainda não tiver senha definida (comum em instalações novas no Linux), defina uma:
```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

Com o serviço rodando, crie o banco localmente. Os comandos abaixo assumem um usuário `postgres` com senha `postgres` — ajuste conforme a configuração da sua máquina.

```bash
# Cria o banco (rode uma única vez)
createdb -U postgres parnas_db

# Caso o comando acima dê erro de permissão, use:
sudo -u postgres psql -c "CREATE DATABASE parnas_db;"
```

> **Atenção:** o nome do banco (`parnas_db`) precisa ser o mesmo configurado em `DATABASE_URL` no seu `.env` (próximo passo). Se já existir um banco antigo com schema desatualizado, prefira recriá-lo do zero (`dropdb` + `createdb`) em vez de tentar consertar manualmente — é mais rápido e evita inconsistência de migrations.

### 2. Backend

```bash
cd backend

# Criar e ativar ambiente virtual — sempre dentro de backend/, nunca na raiz do projeto
python3 -m venv venv
source venv/bin/activate         # Linux/macOS
venv\Scripts\activate            # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Abra o .env e edite os valores reais (veja a seção "Variáveis de Ambiente" abaixo)

# Aplicar migrações no banco que você criou no passo 1
flask db upgrade

# Subir o servidor
flask run
```

O backend estará disponível em `http://localhost:5000`.

> **Importante sobre migrations:** se você trocar de branch (ex: `develop` ↔ `integration/...`) e o schema de banco for diferente entre elas, vai aparecer erro de coluna inexistente (`UndefinedColumn`). Nesse caso, **não tente misturar** — escolha uma branch, recrie o banco do zero (`dropdb`/`createdb`) e rode `flask db upgrade` de novo antes de testar.

> **Cuidado com ambientes virtuais duplicados:** crie o `venv` **somente** dentro da pasta `backend/`. Se você tiver um `venv` na raiz do projeto também, o `flask run` pode acabar usando o errado (dependências desatualizadas) sem nenhum aviso claro. Se isso já aconteceu, remova o venv da raiz e ative explicitamente o de `backend/venv`.

### 3. Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Subir o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

---

## Variáveis de Ambiente

O backend não vem com um `.env` pronto — você precisa criá-lo a partir do exemplo:

```bash
cd backend
cp .env.example .env
```

Depois, abra o `.env` e ajuste os valores reais. O `.env.example` traz esta estrutura:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/parnas_db
FRONTEND_URL=http://localhost:5173/
FLASK_APP=run.py
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-ou-app-password
MAIL_DEFAULT_SENDER=seu-email@gmail.com
```

Detalhes por variável:

| Variável | Obrigatória? | Observação |
|---|---|---|
| `DATABASE_URL` | Sim | Precisa apontar para o banco PostgreSQL que você criou no passo anterior. Usuário/senha/porta devem bater com sua instalação local. |
| `FRONTEND_URL` | Sim | Mantenha `http://localhost:5173/` se não alterou a porta padrão do Vite. |
| `FLASK_APP` | Sim | Sem essa variável, `flask run` e `flask db upgrade` falham com "Could not locate a Flask application" — o Flask não descobre `run.py` sozinho. |
| `MAIL_*` | Não, para uso geral | Só é necessário se for testar o fluxo de recuperação de senha (envio de e-mail real). Pode deixar os valores de exemplo se não for testar isso — o restante do sistema funciona normalmente sem credenciais de e-mail válidas. Se for testar, `MAIL_PASSWORD` precisa ser uma **App Password** do Gmail (não a senha normal da conta), exigindo 2FA habilitado. |

Não comite o `.env` real — apenas o `.env.example` deve ir para o repositório.

---
 
## Estrutura do Projeto
 
```
credifab/
├── backend/
│   ├── app/
│   │   ├── models/        # Entidades e mapeamento SQLAlchemy
│   │   ├── schemas/        # DTOs de entrada e saída (Marshmallow)
│   │   ├── services/       # Regras de negócio
│   │   ├── repositories/   # Queries ao banco de dados
│   │   ├── routes/         # Endpoints da API (Blueprints)
│   │   ├── exceptions/     # Exceções customizadas
│   │   └── utils/          # Helpers, validadores e JWT
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis (ui, layout, charts)
│   │   ├── pages/          # Telas da aplicação
│   │   ├── services/       # Chamadas à API (Axios)
│   │   ├── hooks/          # Custom hooks React
│   │   ├── context/        # Estado global (AuthContext, EmpresaContext)
│   │   └── utils/          # Formatadores e validadores
│   ├── public/
│   └── vite.config.js
│
└── README.md
```
 
---
 
## Política de Branches
 
O projeto adota o seguinte modelo de branches:
 
| Branch | Descrição |
|---|---|
| `main` | Versão estável e entregável. Recebe merge apenas via PR aprovado pelo QA |
| `develop` | Branch de integração. Todo desenvolvimento é integrado aqui primeiro |
| `feature/<nome>` | Nova funcionalidade (ex: `feature/cadastro-usuario`) |
| `fix/<nome>` | Correção de bug (ex: `fix/validacao-cnpj`) |
| `refactor/<nome>` | Refatoração sem nova feature (ex: `refactor/dtos-backend`) |
 
### Regras
- **Nunca** commitar diretamente na `main` ou `develop`
- Todo merge exige **Pull Request** com ao menos uma aprovação
- Branches temporárias (`feature/`, `fix/`, `refactor/`) são excluídas após o merge
- O par de QA revisa o PR antes de qualquer merge na `develop`
---
 
## Política de Issues e Commits
 
### Padrão de Commits (Conventional Commits)
 
```
feat      → nova funcionalidade
fix       → correção de bug
docs      → mudança em documentação
style     → formatação sem mudança de lógica
refactor  → refatoração sem nova feature e sem bug fix
test      → adição ou correção de testes
chore     → configuração e manutenção
perf      → melhoria de performance
ci        → mudanças no pipeline CI/CD
build     → mudanças que afetam o build
```
 
**Exemplos:**
```
feat: adiciona endpoint de cadastro de usuário
fix: corrige validação de CNPJ duplicado
chore: atualiza dependências no requirements.txt
test: adiciona teste de login com credenciais inválidas
```
 
### Regras de Commit
- Mensagem no **imperativo** — "adiciona", "corrige", "atualiza"
- Sempre em **português** no corpo da mensagem
- Prefixo sempre em **inglês**
### Padrão de Issues
 
Cada issue deve conter:
- **Título** claro e objetivo
- **Tipo** via label: `user-story`, `refactor`, `bug`, `chore`
- **Camada** via label: `backend`, `frontend`, `banco-de-dados`
- **Lista de tarefas** com checkboxes
- **Critérios de aceitação** (para user stories)
- **Referência à branch** que resolve a issue
---
 
## Time
 
**Equipe Parnas — MDS 2026.1 — UnB FGA**
 
| Membro | Papel |
|---|---|
| Alan Semil · João Pedro · Gabriel Cardone · Igor Dantas | Backend |
| Anna Júlia · Júlia Amanda · João Marcos · Cibelle | Frontend |
| Eduardo Dal Pizzol · Maria Eduarda | Arquitetura de Banco de Dados |
| Daniel Filipe · Matheus Moretti | Qualidade e Testes (QA) |
