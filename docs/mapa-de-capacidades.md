# Mapa de Capacidades e Plano de Changes

> **Status: PROPOSTA.**
> Como cada feature é especificada em uma conversa isolada do Claude, este mapa é o que
> mantém o vocabulário consistente entre conversas. Ele vai para o conhecimento do
> projeto no Claude e é citado no `openspec/config.yaml`.

## Capacidades (specs permanentes em `openspec/specs/<capacidade>/spec.md`)

Uma **capacidade** é um comportamento durável do sistema. Ela não é uma tarefa. Ela acumula
requisitos ao longo de várias changes.

| Capacidade | O que cobre | Histórias |
|---|---|---|
| `caderno-cultivo` | Criar, editar e listar cadernos (nome único) | US01, US02 |
| `locais-cultivo` | Locais do caderno, com chuva e exposição ao sol | US08 |
| `opcoes-configuraveis` | Listas de estágios e de estados de saúde | US09 |
| `especimes` | Cadastrar e arquivar plantas | US03, US04 |
| `fotos-especime` | Adicionar, remover e ver a cadeia cronológica de fotos | US05, US06, US07 |
| `campos-registro` | Campos extras definidos pelo usuário para o diário | US10 |
| `pacote-caderno` | Exportar e abrir o pacote .zip de um caderno | US11, US12 |

## Plano de changes

Regra de fatiamento: **uma change entrega de 1 a 4 histórias da mesma capacidade e
termina em um comportamento testável.** Se o Explore revelar que a change ficou
grande, divida-a antes da proposta.

| # | Change (nome kebab-case) | Histórias | Depende de |
|---|---|---|---|
| 1 | `criar-caderno` | US01, US02 | - |
| 2 | `configurar-locais-opcoes` | US08, US09 | 1 |
| 3 | `gerenciar-especimes` | US03, US04 | 2 |
| 4 | `gerenciar-fotos` | US05, US06, US07 | 3 |
| 5 | `configurar-campos-registro` | US10 | 3 |
| 6 | `exportar-abrir-pacote` | US11, US12 | 4, 5 |

## Fase 2 (sem histórias ainda)

Registro diário (rega, inspeção, tratamento), clima vigente e cálculo da próxima rega,
protocolo de quarentena, radar de ação imediata e filtros combinados.
