# Caderno Botânico

Diário fotográfico e controle de cultivo de plantas. Aplicação desktop **offline-first** para acompanhar cada planta ao longo do tempo, com uma cadeia de fotos datadas por espécime, organizada em cadernos (um por ambiente de cultivo).

> **Status:** Fase 1 em andamento. Já é possível criar, editar e listar cadernos (change `criar-caderno`). Locais de cultivo, espécimes, fotos e pacotes ainda não foram implementados.

## Objetivo do projeto

Projeto pessoal de estudo e portfólio, desenvolvido em paralelo a um projeto de equipe. Ele usa a mesma stack e a mesma arquitetura em camadas, mas com um domínio diferente, para praticar:

- componentização de interface com Qt Quick/QML;
- integração Qt/Python (QObject, Signals, Slots, Properties, Model/View);
- fluxo SDD com OpenSpec e gerenciamento de contexto para LLMs;
- automação de qualidade e entrega (CI/CD).

## Stack

- Python 3.14
- PySide6 / QML
- SQLite
- pytest e Ruff

Arquitetura em camadas: `UI → Services → Domain / Repositories`, com o `Storage` implementando os Repositories. Detalhes em [`docs/project.md`](docs/project.md).

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

python -m caderno_botanico
```

O banco fica na pasta de dados do usuário (no Linux, `~/.local/share/caderno-botanico/`). Para usar outro arquivo, por exemplo em testes manuais:

```bash
CADERNO_BOTANICO_DB=/tmp/teste.db python -m caderno_botanico
```

## Qualidade

```bash
ruff check .
ruff format --check .
pyside6-qmllint src/caderno_botanico/ui/qml/*.qml
pytest
```

O mesmo conjunto roda no GitHub Actions a cada Pull Request (`.github/workflows/ci.yml`).

## Estrutura do repositório

```text
.
├── README.md
├── pyproject.toml
├── .github/workflows/ci.yml        # CI: Ruff, qmllint e pytest
├── docs/
│   ├── project.md                  # contexto global (enviado no início de toda sessão com a IA)
│   ├── historias-de-usuario.md     # histórias da Fase 1 (US01 a US12)
│   ├── mapa-de-capacidades.md      # capacidades OpenSpec e plano de changes
│   ├── guia_de_contexto.md         # como fornecer contexto à IA em cada etapa
│   └── decisoes.md                 # registro de decisões
├── openspec/
│   ├── config.yaml                 # resumo do project.md usado pelo OpenSpec
│   ├── specs/                      # comportamentos já entregues (por capacidade)
│   └── changes/                    # changes em andamento e arquivadas
├── src/caderno_botanico/
│   ├── app.py                      # ponto de montagem das camadas
│   ├── domain/                     # entidades e regras de negócio
│   ├── repositories/               # interfaces de acesso a dados
│   ├── services/                   # casos de uso
│   ├── storage/                    # SQLite
│   └── ui/                         # controladores Qt e telas QML
└── tests/                          # testes por camada
```

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
