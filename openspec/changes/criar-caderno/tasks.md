# Tasks

## 1. Dependências e CI com Qt

- [x] 1.1 Adicionar o PySide6 às dependências do `pyproject.toml` e verificar que `pip install -e ".[dev]"` conclui e `python -c "import PySide6"` funciona
- [x] 1.2 Ajustar o `ci.yml` para rodar com Qt sem tela (`QT_QPA_PLATFORM=offscreen` e pacotes do sistema, se necessários) e verificar que o CI de um Pull Request fica verde

## 2. Domain

- [x] 2.1 Criar a entidade `Caderno`, o cálculo do nome normalizado, a validação de nome (obrigatório, até 80 caracteres) e as exceções `NomeInvalidoError` e `NomeDuplicadoError`, com testes em `tests/domain/` cobrindo os cenários de nome vazio, só espaços, 80 e 81 caracteres e normalização por caixa e espaços
- [x] 2.2 Rodar `pytest` e verificar que `tests/test_arquitetura.py` continua passando (Domain sem PySide6 e sem sqlite3)

## 3. Repositories e Services

- [x] 3.1 Definir a interface `CadernoRepository` e criar um repositório falso em memória para os testes, verificando que ele satisfaz a interface
- [x] 3.2 Implementar `CadernoService` (criar, editar, listar) com testes cobrindo nome duplicado na criação, edição sem mudar o nome, renomear para nome de outro caderno, descrição opcional e ordenação alfabética sem diferenciar caixa

## 4. Storage

- [x] 4.1 Implementar a criação do esquema SQLite (tabela `cadernos`, `UNIQUE` em `nome_normalizado`, `PRAGMA user_version`) e verificar com um teste que o esquema é criado em um banco `:memory:`
- [x] 4.2 Implementar `SqliteCadernoRepository` e verificar com testes que salvar, atualizar, listar e a checagem de nome funcionam, e que uma violação de `UNIQUE` vira `NomeDuplicadoError`
- [x] 4.3 Verificar com um teste usando arquivo temporário que os cadernos continuam disponíveis após fechar e reabrir a conexão (cenário de persistência local)

## 5. Ponte Qt na UI

- [x] 5.1 Implementar `CadernoListModel` (`QAbstractListModel` com os papéis `id`, `nome`, `descricao` e `criadoEm`) e verificar com testes de `rowCount`, `data` e `roleNames`
- [x] 5.2 Implementar `CadernoController` (property do modelo, slots `criar` e `editar`, signals de sucesso e erro) e verificar com testes que erros do Domain viram mensagens em português e que o modelo é recarregado após criar e editar

## 6. Interface QML e montagem

- [ ] 6.1 Criar a tela QML (lista de cadernos e formulário com Salvar e Cancelar) e o módulo de entrada que monta banco, repositório, service e controller; verificar executando o aplicativo e criando, editando e cancelando um caderno
- [ ] 6.2 Rodar `pyside6-qmllint` nos arquivos QML e verificar que não há erros

## 7. Verificação final

- [ ] 7.1 Percorrer manualmente os cenários do `specs/caderno-cultivo/spec.md` no aplicativo e verificar que todos se comportam como descrito
- [ ] 7.2 Rodar `openspec validate criar-caderno`, `ruff check .`, `ruff format --check .` e `pytest`, e verificar que passam
- [ ] 7.3 Atualizar o `README.md` (árvore do repositório e como executar) e verificar que as instruções funcionam a partir de um clone limpo

## Workflow follow-up

- Abrir o Pull Request de `feature/criar-caderno` para `develop` e aguardar o CI verde.
- Arquivar a change depois do merge (`/opsx:archive`).
