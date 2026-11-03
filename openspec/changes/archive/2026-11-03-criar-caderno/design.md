## Context

Primeira change com código de negócio: o projeto só tem o esqueleto em camadas e o CI mínimo. Motivação e escopo estão em `proposal.md`; o comportamento está em `specs/caderno-cultivo/spec.md`. Valem as regras do `docs/project.md` (offline-first, só o Storage acessa o SQLite, regras de negócio no Domain, textos em PT-BR).

## Goals / Non-Goals

**Goals**
- Entregar a primeira fatia vertical completa (UI, Services, Domain, Repositories, Storage) de ponta a ponta.
- Servir de base de estudo para a integração Qt/Python (QObject, Signals, Slots, Properties, `QAbstractListModel`).

**Non-Goals**
- Migrações de banco e exclusão de caderno.
- Visual refinado: a interface QML é mínima nesta change.

## Decisions

### 1. Banco único em SQLite, com a unicidade garantida em dois níveis
Um arquivo SQLite guarda todos os cadernos. A tabela `cadernos` tem `id` (inteiro, autoincremento), `nome`, `nome_normalizado` (`UNIQUE`), `descricao` e `criado_em` (texto ISO 8601, em UTC).
O Domain calcula o `nome_normalizado` com `strip()` e `casefold()`. O Service confere duplicidade antes de salvar, e a restrição `UNIQUE` do banco é a rede de segurança contra corrida ou falha de lógica.
- *Alternativa descartada:* `COLLATE NOCASE` do SQLite, porque só ignora maiúsculas de letras ASCII ("Ágata" e "ágata" seriam nomes diferentes).

### 2. Regras no Domain
O Domain tem a entidade `Caderno`, as validações de nome (obrigatório, até 80 caracteres após `strip()`) e as exceções de negócio: `NomeInvalidoError` e `NomeDuplicadoError`. Sem PySide6, sem `sqlite3`.

### 3. Repositório como interface, injetada no Service
A camada Repositories define `CadernoRepository` (salvar, atualizar, buscar por id, listar e verificar se um nome existe, podendo excluir o próprio caderno da checagem para o caso de edição). O Storage entrega `SqliteCadernoRepository`. O Service recebe o repositório pelo construtor.
Isso permite testar o Service com um repositório falso em memória, e o Storage com SQLite em `:memory:` e em arquivo temporário.

### 4. Services sem Qt
`CadernoService` (criar, editar, listar) é Python puro. Toda a ponte com o Qt fica na camada UI. Assim os serviços são testáveis sem interface e as regras não vazam para a UI.

### 5. Ponte Qt na UI (base de estudo do Aluno 3)
- `CadernoListModel`, um `QAbstractListModel` com papéis `id`, `nome`, `descricao` e `criadoEm`.
- `CadernoController`, um `QObject` que o QML usa: expõe o modelo como *property*, tem *slots* `criar` e `editar`, e *signals* para sucesso e para erro de validação (com mensagem em português).
- O controlador traduz as exceções do Domain em mensagens para a tela e recarrega o modelo após cada alteração.
- *Alternativa descartada:* expor os objetos do Domain direto ao QML, porque acoplaria a UI às entidades.

### 5b. Ponto de montagem
Um módulo de entrada monta as peças (caminho do banco, repositório, service, controller) e carrega o QML. O caminho do banco é decidido ali e injetado no Storage, que não depende de Qt.

### 6. Interface QML mínima
Uma tela com a lista de cadernos e um formulário (nome e descrição) para criar e editar, com botões Salvar e Cancelar. Sem componentização elaborada: isso é trabalho do Aluno 2.

## Risks / Trade-offs

- **PySide6 no CI** → o runner do GitHub pode não ter as bibliotecas gráficas; mitigar com `QT_QPA_PLATFORM=offscreen` e, se preciso, instalar pacotes do sistema. Tratado no primeiro grupo de tarefas.
- **`casefold()` não resolve toda equivalência de texto** (ex.: acentos decompostos) → aceitável por ora; revisitar se surgir um caso real.
- **Ordenação alfabética** com `casefold()` não segue a ordem de dicionário do português para todos os casos → aceitável; trocar por ordenação por *locale* só se incomodar.
- **Sem versionamento do esquema do banco** → registrar a versão com `PRAGMA user_version` já na criação do banco, para facilitar migrações futuras.

## Open Questions

- O limite de 80 caracteres e a ordem alfabética são premissas do proposal; mudá-los só altera constantes e a consulta de listagem.
