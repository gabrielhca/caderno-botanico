## Why

O jardineiro cuida de plantas em ambientes diferentes (horta, jardim, área interna, mini-estufa), cada um com dinâmicas e cuidados próprios. O sistema ainda não tem nenhum conceito que represente esses ambientes. Antes de cadastrar locais, espécimes ou fotos, é preciso existir o **caderno**, que é o contêiner de tudo isso e a unidade exportada no pacote.

## What Changes

- Criar um caderno informando **nome** (obrigatório) e **descrição** (opcional) (US01, US02).
- Registrar automaticamente a **data de criação** do caderno.
- Garantir que o **nome seja único** entre os cadernos, sem diferenciar maiúsculas de minúsculas.
- **Editar** o nome e a descrição de um caderno existente (US02).
- **Listar** os cadernos existentes para o usuário escolher em qual trabalhar.
- Permitir **cancelar** a criação ou a edição sem salvar.
- Manter os cadernos salvos entre execuções do aplicativo, sem depender de internet.

## Capabilities

### New Capabilities

- `caderno-cultivo`: criar, editar e listar cadernos de cultivo, com nome único.

### Modified Capabilities

Nenhuma.

## Impact

- Primeira entidade, primeiro repositório, primeiro serviço e primeira tela do projeto.
- Introduz o SQLite local e a dependência do PySide6 (o CI precisará ser ajustado para rodar com Qt).
- Serve de base para as changes seguintes (`configurar-locais-opcoes`, `gerenciar-especimes` e demais), que dependem de um caderno existente.

## Out of Scope

- Excluir caderno.
- Locais de cultivo, espécimes, fotos, campos de registro, exportação e abertura de pacote.
- Qualquer campo de "local" no próprio caderno (os locais ficam dentro do caderno, na change `configurar-locais-opcoes`).

## Premissas adotadas (a confirmar)

- A descrição é opcional.
- O nome tem no máximo 80 caracteres.
- A lista de cadernos é exibida em ordem alfabética do nome.
