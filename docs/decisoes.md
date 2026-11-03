# Registro de Decisõess

## Decisões tomadas

| Tema | Decisão | Motivo |
|---|---|---|
| Stack | Python, PySide6/QML, SQLite, pytest | Mesma stack do projeto da equipe, para dominar as ferramentas |
| Caderno | Vários cadernos, um por ambiente; nome único; sem campo "local" | Cada ambiente tem dinâmicas e cuidados próprios |
| Locais de cultivo | Ficam dentro do caderno, com chuva e exposição ao sol (US08) | Um mesmo ambiente pode ter áreas com luz diferente |
| Banco | Um único SQLite com todos os cadernos; fotos em disco | Visão global na Fase 2 e mover plantas entre cadernos |
| Python | 3.14, ambiente com `venv` e `pip`, layout `src/` | Simplicidade; PySide6 6.11 suporta 3.14 |
| CI inicial | Só Ruff e pytest, em Pull Requests para develop e main | PySide6 e qmllint entram quando houver QML para checar |
| Estrutura inicial | Feita fora do OpenSpec (branch `feature/estrutura-inicial`) | Esqueleto e CI não são uma capacidade do sistema |
| Escopo | Fase 1 enxuta; radar, motor de rega e quarentena ficam para a Fase 2 | Evitar que o projeto de estudo vire uma segunda tarefa gigante |
| Fluxo de Git | `feature/*` nasce da `develop` e volta por Pull Request com CI verde; `develop` vai para `main` nas versões estáveis | Fluxo definido na reunião da equipe |
| `criar-caderno` | Descrição opcional; nome com até 80 caracteres e único sem diferenciar caixa; lista em ordem alfabética | Premissas confirmadas |


## Decisões adiadas

- Formato exato do `manifest.json` do pacote (change `exportar-abrir-pacote`).
- Confirmação final do banco único no `design.md` da change 1.
- Regras 5 e 6 do `project.md` (espécime arquivado e fotos em disco): confirmar.
- Nome único: diferenciar maiúsculas de minúsculas? Tamanho máximo do nome? Descrição obrigatória?
- Excluir caderno (fora da change 1).
- `integration.yml` (quando houver testes de integração) e `release.yml` (quando houver app executável).
- Como gerar o aplicativo para Windows e Linux.
- PySide6 e qmllint no CI.
- Proteção das branches `develop` e `main` no GitHub.
- Aprofundar componentização QML (a interface da `criar-caderno` é mínima de propósito).
- Revisar o `ci.yml` linha a linha e fazer `integration.yml`, `release.yml`, build e proteção de branches.
