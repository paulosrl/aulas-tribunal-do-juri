# Análise do Codebase - 2026-05-14

## Resumo Executivo

- Estado: ativo e consistente com geração atual.
- Escopo analisado: scripts Python, templates, conteúdo markdown e HTML gerado.
- Fonte arquitetural: `graphify-out/GRAPH_REPORT.md` (build `2026-05-14`).

## Estrutura Atual

```text
aulas-tribunal-do-juri/
├── conteudo/                 # 8 arquivos markdown (index + 1..7)
├── templates/                # index.template.html e topico.template.html
├── scripts/
│   ├── build_all.py
│   ├── gera_html.py          # wrapper de 7 linhas
│   ├── lock_menu_items.py
│   └── html_gen/             # pipeline modularizado
├── html/                     # páginas geradas
└── graphify-out/
```

## Métricas de Código (linhas)

- `scripts/gera_html.py`: 7
- `scripts/html_gen/parser.py`: 860
- `scripts/html_gen/postprocessor.py`: 417
- `scripts/html_gen/renderer.py`: 254
- `scripts/html_gen/cli.py`: 191
- `scripts/html_gen/validation.py`: 170
- `scripts/html_gen/*` total: 2.293

## Arquitetura de Geração

Entrada de build:
- `python3 scripts/build_all.py`
- `python3 scripts/gera_html.py ...`

Fluxo:
1. `html_gen.cli`: parse de args e roteamento.
2. `html_gen.parser`: markdown para `Card`.
3. `html_gen.icons`: ícones únicos e consistentes.
4. `html_gen.renderer`: conteúdo e menu/sumário.
5. `html_gen.postprocessor`: ajustes visuais globais, CSS/JS e CTAs.
6. `html_gen.validation`: completude e preservação de conteúdo.

## Script de Lock/Unlock

Arquivo: `scripts/lock_menu_items.py`

- Atua em `html/index.html` e `html/1..7.html`.
- Modos: lock, unlock e dry-run.
- Remove/injeta bloqueio em itens de menu e cards por número de tópico.
- Estado atual: fluxo idempotente sem duplicar cadeado ao reaplicar operação.

## Estado Visual Relevante

- Tema claro:
  - itens de menu em `#8A1F3A`
  - subitens em `#8A1F3A`
- Tema escuro:
  - títulos principais e links destacados em `#fbd246`
  - subitens em branco
- Ícones dos subitens preservam cores originais (não forçados para branco).

## Graphify (estado atual)

Dados de `graphify-out/GRAPH_REPORT.md`:
- 219 nós
- 464 arestas
- 8 comunidades
- God node principal listado: `build_topico.py` (legado de nomenclatura do grafo)

Observação:
- O relatório inclui nomes legados, mas o pipeline real executado está em `scripts/html_gen/*`.

## Riscos Técnicos

- `parser.py` e `postprocessor.py` concentram boa parte da complexidade.
- Regras de CSS injetadas no template e no pós-processador exigem sincronização para evitar regressão visual.
- Mudanças de estrutura no menu exigem validação em todas as páginas (`1..7` e `index`).

## Rotina Recomendada de Validação

1. `python3 scripts/build_all.py`
2. Comparar hashes de `html/*.html` antes/depois quando necessário.
3. Testar lock/unlock:
   - `python3 scripts/lock_menu_items.py --items 4 5 7`
   - `python3 scripts/lock_menu_items.py --items 4 5 7 --unlock`
4. Atualizar grafo após mudanças em Python:
   - `graphify update .`
