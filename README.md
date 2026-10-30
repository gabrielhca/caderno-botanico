# Caderno Botânico

Diário fotográfico e controle de cultivo de plantas. Aplicação desktop **offline-first** para acompanhar cada planta ao longo do tempo, com uma cadeia de fotos datadas por espécime, organizada em cadernos (um por ambiente de cultivo).

> **Status: planejamento.** Ainda não há código. Este repositório começa pela documentação e pelo fluxo de especificação (Spec-Driven Development com OpenSpec).

## Objetivo do projeto

- componentização de interface com Qt Quick/QML;
- integração Qt/Python (QObject, Signals, Slots, Properties, Model/View);
- fluxo SDD com OpenSpec e gerenciamento de contexto para LLMs;
- automação de qualidade e entrega (CI/CD).

## Stack

- Python
- PySide6 / QML
- SQLite
- pytest

Arquitetura em camadas: `UI → Services → Domain / Repositories`, com o `Storage` implementando os Repositories. Detalhes em [`docs/project.md`](docs/project.md).

## Estrutura do repositório

```text
.
├── README.md
├── docs/
│   ├── project.md                # contexto global (enviado no início de toda sessão com a IA)
│   ├── historias-de-usuario.md   # histórias da Fase 1 (US01 a US12)
│   ├── mapa-de-capacidades.md    # capacidades OpenSpec e plano de changes
│   └── guia_de_contexto.md       # como fornecer contexto à IA em cada etapa
└── openspec/
    └── config.yaml               # resumo do project.md usado pelo OpenSpec
```

O comando `openspec init` cria o restante de `openspec/` (specs, changes e arquivos da ferramenta de IA escolhida). Esses arquivos são gerados pelo fluxo e não devem ser editados à mão, exceto o `config.yaml`.

## Como trabalhar

O fluxo de cada história de usuário é:

```text
história → explore → proposal → specs + design → tasks → apply
```

1. Escolha a próxima change em [`docs/mapa-de-capacidades.md`](docs/mapa-de-capacidades.md).
2. Siga o [`docs/guia_de_contexto.md`](docs/guia_de_contexto.md) para decidir o que enviar à IA em cada etapa.
3. Sempre que o `docs/project.md` mudar, atualize o `context` do `openspec/config.yaml` no mesmo commit.

## Fases

- **Fase 1 (em andamento):** caderno, locais e opções configuráveis, espécimes, fotos, campos de registro e pacote (.zip).
- **Fase 2 (sem histórias ainda):** registro diário, clima e cálculo da próxima rega, quarentena, radar de ação imediata e filtros.
