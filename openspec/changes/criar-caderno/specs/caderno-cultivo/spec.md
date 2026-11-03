## ADDED Requirements

### Requirement: Criar caderno
O sistema DEVE permitir que o jardineiro crie um caderno informando um nome obrigatório e uma descrição opcional, e DEVE registrar automaticamente a data de criação.

#### Scenario: Criar caderno com nome e descrição
- **WHEN** o jardineiro informa o nome "Horta dos fundos" e a descrição "Hortaliças e legumes" e confirma
- **THEN** o caderno passa a existir com esse nome e essa descrição
- **AND** a data de criação fica registrada automaticamente

#### Scenario: Criar caderno apenas com nome
- **WHEN** o jardineiro informa o nome "Jardim da frente", deixa a descrição em branco e confirma
- **THEN** o caderno é criado com a descrição vazia

#### Scenario: Nome vazio é rejeitado
- **WHEN** o jardineiro deixa o nome em branco, ou só com espaços, e confirma
- **THEN** o caderno não é criado
- **AND** o sistema informa, em português, que o nome é obrigatório

### Requirement: Limite de tamanho do nome
O sistema DEVE rejeitar nomes de caderno com mais de 80 caracteres, desconsiderando os espaços no início e no fim.

#### Scenario: Nome acima do limite
- **WHEN** o jardineiro informa um nome com 81 caracteres e confirma
- **THEN** o caderno não é criado
- **AND** o sistema informa que o nome excede o tamanho máximo

#### Scenario: Nome exatamente no limite
- **WHEN** o jardineiro informa um nome com 80 caracteres e confirma
- **THEN** o caderno é criado

### Requirement: Nome único entre cadernos
O sistema DEVE garantir que dois cadernos não tenham o mesmo nome, comparando sem diferenciar maiúsculas de minúsculas e desconsiderando os espaços no início e no fim.

#### Scenario: Nome já existente
- **GIVEN** existe um caderno chamado "Horta"
- **WHEN** o jardineiro tenta criar outro caderno chamado "Horta"
- **THEN** o novo caderno não é criado
- **AND** o sistema informa que já existe um caderno com esse nome

#### Scenario: Nome já existente com outra caixa ou espaços
- **GIVEN** existe um caderno chamado "Horta"
- **WHEN** o jardineiro tenta criar um caderno chamado "  hORTA "
- **THEN** o novo caderno não é criado
- **AND** o sistema informa que já existe um caderno com esse nome

### Requirement: Editar caderno
O sistema DEVE permitir alterar o nome e a descrição de um caderno existente, mantendo a data de criação original e respeitando as mesmas regras de nome da criação.

#### Scenario: Alterar a descrição
- **GIVEN** existe um caderno chamado "Horta"
- **WHEN** o jardineiro altera apenas a descrição e confirma
- **THEN** a nova descrição é salva
- **AND** o nome e a data de criação permanecem os mesmos

#### Scenario: Salvar sem alterar o nome não gera conflito
- **GIVEN** existe um caderno chamado "Horta"
- **WHEN** o jardineiro abre a edição e confirma sem mudar o nome
- **THEN** o sistema não acusa nome duplicado

#### Scenario: Renomear para o nome de outro caderno
- **GIVEN** existem os cadernos "Horta" e "Jardim"
- **WHEN** o jardineiro tenta renomear "Jardim" para "horta"
- **THEN** a alteração não é salva
- **AND** o sistema informa que já existe um caderno com esse nome

### Requirement: Listar cadernos
O sistema DEVE exibir todos os cadernos existentes, com nome, descrição e data de criação, em ordem alfabética do nome sem diferenciar maiúsculas de minúsculas.

#### Scenario: Lista com vários cadernos
- **GIVEN** existem os cadernos "Varanda", "horta" e "Jardim"
- **WHEN** o jardineiro abre a lista de cadernos
- **THEN** os cadernos aparecem na ordem "horta", "Jardim", "Varanda"

#### Scenario: Nenhum caderno existente
- **GIVEN** não existe nenhum caderno
- **WHEN** o jardineiro abre a lista de cadernos
- **THEN** o sistema mostra a lista vazia e permite criar o primeiro caderno

### Requirement: Cancelar criação ou edição
O sistema DEVE permitir cancelar a criação ou a edição de um caderno, sem salvar nenhuma alteração.

#### Scenario: Cancelar a criação
- **WHEN** o jardineiro preenche o formulário de novo caderno e cancela
- **THEN** nenhum caderno é criado

#### Scenario: Cancelar a edição
- **GIVEN** existe um caderno chamado "Horta"
- **WHEN** o jardineiro altera o nome no formulário e cancela
- **THEN** o caderno continua com o nome "Horta"

### Requirement: Persistência local
O sistema DEVE manter os cadernos salvos entre execuções do aplicativo, sem depender de internet.

#### Scenario: Cadernos permanecem após reabrir
- **GIVEN** o jardineiro criou o caderno "Horta" e fechou o aplicativo
- **WHEN** o jardineiro abre o aplicativo novamente, sem conexão com a internet
- **THEN** o caderno "Horta" aparece na lista
