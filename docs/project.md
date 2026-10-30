# Caderno Botânico

**Diário fotográfico e controle de cultivo de plantas**

> Contexto global do projeto. Este arquivo é enviado no início de **toda** sessão de trabalho (explore, proposal, specs, design, tasks e apply). Trate-o como fonte de verdade sobre o que é o projeto e quais regras não podem ser quebradas.
>

## 1. Visão Geral

Aplicação desktop **offline-first** para acompanhar plantas ao longo do tempo. A unidade central é o **espécime** (uma planta individual): cada um tem identidade, estado atual e uma cadeia de fotos datadas. As plantas são organizadas em **cadernos**, e cada caderno representa um ambiente de cultivo (ex.: horta, jardim, área interna, mini-estufa).

Locais de cultivo, listas de opções (estágios, estados de saúde) e campos extras de registro são definidos pelo usuário, nunca fixados no código. Espécime, caderno, local e foto são entidades fixas do domínio.

## 2. Papéis

Existe um único papel: o **jardineiro**, que usa a aplicação sozinho, em uma máquina local. Não há identificação de usuário, perfis nem fluxo de aprovação.

## 3. Fluxo de Dados

1. **Configuração:** o jardineiro cria um caderno, define seus locais de cultivo, as listas de opções e os campos extras de registro.
2. **Cadastro e acompanhamento:** cadastra espécimes e adiciona fotos datadas à cadeia de cada um.
3. **Pacote:** exporta um caderno completo (dados e fotos) em um **Pacote (.zip)** para backup ou transporte, e pode abri-lo novamente.

> Fora da Fase 1 (ainda sem histórias): registro diário de rega e inspeção, cálculo da próxima rega com clima, protocolo de quarentena, radar de ação imediata e filtros combinados.

## 4. Stack Tecnológica

- **Linguagem:** Python
- **Interface gráfica:** PySide6 / QML
- **Banco de dados:** SQLite (local, um único arquivo com todos os cadernos)
- **Testes:** pytest

## 5. Arquitetura em Camadas

- **UI:** componentes visuais em QML e controladores PySide6. Apenas apresenta dados e captura ações do usuário.
- **Services:** orquestram os casos de uso e fazem a ponte entre a UI e o Domain.
- **Domain:** modelos de negócio, entidades e validações puras, sem dependência de PySide6, SQLite ou sistema de arquivos.
- **Repositories:** interfaces de acesso a dados.
- **Storage:** implementação concreta dos Repositories em SQLite e a manipulação de arquivos, incluindo fotos em disco e a leitura e escrita de pacotes ZIP e JSON.

**Direção das dependências:** UI → Services → Domain e Repositories. O Storage implementa os Repositories. O Domain não depende de nenhuma outra camada.

**Entidades principais (Fase 1):** Caderno, Local de cultivo (com recebe chuva e exposição ao sol), Espécime (espécie, variedade, número, estágio, local, situação), Foto de espécime (data, caminho relativo), Opção configurável (listas de estágios e de saúde), Campo de registro (definido pelo usuário) e Pacote.

## 6. Contratos de Dados

- **Pacote (.zip):** contém um `manifest.json` (versão do formato, caderno, locais, espécimes, opções, campos e metadados das fotos) e a pasta `fotos/` com os arquivos de imagem.
- **Datas:** formato ISO 8601 nos arquivos JSON.
- **Caminhos de foto:** sempre relativos à pasta de dados da aplicação, nunca absolutos.

Nenhuma mudança nesses contratos deve ser feita sem atualizar a spec correspondente.

## 7. Regras Invioláveis

1. **Offline-first:** o sistema não pode depender de internet, APIs em nuvem, CDNs ou telemetria em nenhuma funcionalidade.
2. **Isolamento de banco de dados:** somente a camada Storage acessa o SQLite. A UI e os Services NUNCA o acessam diretamente; toda persistência passa obrigatoriamente pelos Repositories.
3. **Isolamento de regras:** regras de negócio não ficam na UI. Ficam no Domain e são orquestradas pelos Services.
4. **Domínio fixo, listas configuráveis:** as entidades (Caderno, Local, Espécime, Foto) são fixas no código. As listas de opções (estágios, estados de saúde) e os campos extras de registro vêm da configuração do usuário. Nunca escreva no código um estágio, um estado de saúde ou um campo extra específico.
5. **Espécime nunca é apagado por perda:** uma planta perdida ou descartada é arquivada, mantendo seu histórico e suas fotos.
6. **Fotos em disco:** o banco guarda apenas o caminho relativo da foto, nunca o conteúdo da imagem.
7. **Idioma:** todos os artefatos (documentação OpenSpec, comentários, docstrings, mensagens de erro e textos da interface) em Português (PT-BR). Identificadores de código (nomes de classes, funções e arquivos) seguem a convenção Python (PEP 8) em inglês.
8. **Contexto limitado:** se faltar informação, liste os arquivos de que precisa e por quê, em vez de supor o conteúdo de arquivos que não foram enviados. Dúvidas de negócio devem ser registradas como 'Questões em aberto', sem inventar requisitos.
