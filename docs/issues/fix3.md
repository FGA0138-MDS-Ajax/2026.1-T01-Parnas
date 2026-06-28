## Descrição técnica
Tarefa técnica de qualidade (refatoração/correção). Diversas integrações entre models, services e schemas apresentam inconsistências acumuladas ao longo das Sprints anteriores. É necessário revisar e consolidar antes de avançar com novas funcionalidades.

## Rastreabilidade
- **Requisito(s):** — (transversal)
- **Cenário:** Transversal (CEN-00 a CEN-04)
- **Sprint:** 10
- **Prioridade:** Should
- **Tipo:** refactor / fix (backend)
- **Funcionalidade do produto:** Transversal

## Tarefas
- [ ] Revisar todos os relacionamentos SQLAlchemy (`back_populates`, `cascade`) entre Empresa, Usuario, UsuarioEmpresa, Categoria, Transacao, Conta, Simulacao e Documento
- [ ] Garantir que todos os endpoints usam os schemas Marshmallow criados na refatoração de DTOs ([task5](task5.md))
- [ ] Revisar se o `id_empresa` usado em todos os services vem do token JWT / empresa ativa, e não de parâmetros do frontend
- [ ] Testar manualmente o fluxo completo: cadastro → login → seleção de empresa → criação de categoria → criação de conta → quitação → geração de transação → exibição no dashboard
- [ ] Corrigir erros encontrados durante o teste de fluxo completo
- [ ] Atualizar testes do Pytest e Vitest para refletir as correções

## Critérios de conclusão
- [ ] Relacionamentos SQLAlchemy revisados e consistentes
- [ ] Todos os endpoints passando pelos schemas Marshmallow
- [ ] Fluxo completo executado sem erros
- [ ] Suíte de testes verde após as correções

## Critérios de teste
- [ ] Reexecução completa da suíte (Pytest / Vitest)
- [ ] Cobertura mínima mantida

## Definição de Done
- [ ] Código revisado em pair programming
- [ ] PR aberto de `fix/3-integracao-classes` para `develop`
- [ ] PR revisado pelo par de QA antes do merge na `develop`

## Branch
`fix/3-integracao-classes`
