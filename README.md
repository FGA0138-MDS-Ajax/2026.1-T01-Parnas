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
- PostgreSQL rodando localmente
### 1. Backend
 
```bash
cd backend
 
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows
 
# Instalar dependências
pip install -r requirements.txt
 
# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais do PostgreSQL
 
# Aplicar migrações e subir o servidor
flask db upgrade
flask run
```
 
O backend estará disponível em `http://localhost:5000`.
 
### 2. Frontend
 
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
 
Copie o arquivo `.env.example` para `.env` na pasta `backend/` e preencha:
 
```env
DATABASE_URL=postgresql://usuario:senha@localhost/credfab
JWT_SECRET_KEY=sua_chave_secreta
FLASK_ENV=development
FLASK_APP=run.py
```
 
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
