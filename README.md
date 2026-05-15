# Aulas: IA Aplicada ao Tribunal do Júri

Repositório de geração de páginas HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri**.

Publicação: <https://paulosrl.github.io/aulas-tribunal-do-juri/>

## Objetivo

Transformar conteúdo autoral em Markdown (`conteudo/*.md`) em páginas HTML estáticas, com:
- navegação lateral padronizada;
- identidade visual consistente (tema claro/escuro);
- validações de completude e preservação de conteúdo;
- saída pronta para publicação em GitHub Pages.

## Estrutura do Projeto

```text
.
├── conteudo/                  # Fonte em markdown (index + tópicos 1..7)
├── templates/                 # Templates HTML base
├── scripts/
│   ├── build_all.py           # Build completo
│   ├── gera_html.py           # Wrapper CLI do gerador
│   ├── lock_menu_items.py     # Lock/unlock de tópicos no HTML pronto
│   └── html_gen/              # Pipeline principal Markdown -> HTML
├── html/                      # Saída gerada
├── graphify-out/              # Grafo de conhecimento do codebase
└── loggerador.md              # Log de geração por página (data/hash)
```

## Arquitetura de Geração

Entrada principal: `scripts/gera_html.py` (encaminha para `html_gen.cli.main`).

Fluxo real:
1. `html_gen/cli.py`: parsing de argumentos, roteamento (landing vs tópico) e orquestração.
2. `html_gen/parser.py`: parsing Markdown para estrutura de `Card` com blocos HTML.
3. `html_gen/icons.py`: escolha e deduplicação de ícones.
4. `html_gen/renderer.py`: render de seções, cards, menu lateral e acordeão de tópicos.
5. `html_gen/postprocessor.py`: injeção de CSS/JS, logo em data URI e ajustes globais finais.
6. `html_gen/validation.py`: validação de completude e preservação textual.
7. `html_gen/cli.py`: append no `loggerador.md` (página, timestamp, SHA-256).

## Comandos de Uso

Build completo:

```bash
python3 scripts/build_all.py
```

Build de uma página:

```bash
python3 scripts/gera_html.py conteudo/3.md html/3.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Agentes no Júri" \
  --section-mode semantic
```

Travar/destravar tópicos (menu + cards):

```bash
python3 scripts/lock_menu_items.py --items 4 5 6
python3 scripts/lock_menu_items.py --items 4 5 6 --unlock
python3 scripts/lock_menu_items.py --items 4 5 6 --dry-run
```

## Qualidade e Verificação

Checklist recomendado antes de release:

```bash
python3 -m py_compile scripts/build_all.py scripts/gera_html.py scripts/lock_menu_items.py scripts/html_gen/*.py
python3 scripts/build_all.py
python3 scripts/lock_menu_items.py --items 4 5 6 --dry-run
python3 scripts/lock_menu_items.py --items 4 5 6 --unlock --dry-run
```

## Rotina de Testes (Completa)

Execute nesta ordem:

```bash
# 1) Sanidade de sintaxe Python
python3 -m py_compile scripts/build_all.py scripts/gera_html.py scripts/lock_menu_items.py scripts/html_gen/*.py

# 2) Build completo (index + tópicos)
python3 scripts/build_all.py

# 3) Teste funcional do lock (sem alterar arquivos)
python3 scripts/lock_menu_items.py --items 4 5 6 --dry-run

# 4) Teste funcional do unlock (sem alterar arquivos)
python3 scripts/lock_menu_items.py --items 4 5 6 --unlock --dry-run

# 5) Atualização do grafo de código após mudanças
graphify update .
```

Critérios de aprovação:
- nenhum erro no `py_compile`;
- build com `8/8` páginas geradas;
- lock `dry-run` reportando itens travados esperados;
- unlock `dry-run` sem erro;
- `graphify update .` concluído com atualização de `graphify-out/*`.

## Status de Prontidão para Versão 1.0 (2026-05-15)

Validações executadas nesta revisão:
- `py_compile` em todos os scripts principais e `scripts/html_gen/*.py`: **OK**
- `python3 scripts/build_all.py` com 8/8 páginas (`index` + `1..7`): **OK**
- `lock_menu_items.py` em `--dry-run` (lock/unlock): **OK**

Conclusão atual:
- O projeto está **funcional e estável** para release **v1.0** do ponto de vista de geração.
- Não foram identificadas falhas bloqueantes de execução no pipeline.

Hardening concluído nesta revisão:
- removida duplicação de chamada de `apply_global_page_rules()` em `html_gen/cli.py`;
- centralizada a data institucional em `COURSE_DATE_LABEL` (`html_gen/constants.py`) e atualizada para 2026;
- removida duplicação de `inline_md`, mantendo implementação única em `html_gen/utils.py`.

## Observações Operacionais

- `index.html` na raiz redireciona para `html/index.html`.
- Landing embute `logo.png` e `mppa.png` como data URI quando presentes.
- O CTA “Acessar Agente Copilot” é gerado no parser e estilizado no pós-processamento.

## Graphify

Regras do projeto:
- usar `graphify-out/GRAPH_REPORT.md` para visão arquitetural;
- após alterar arquivos de código, executar:

```bash
graphify update .
```

## Documentos Relacionados

- `AGENTS.md`
- `CHANGELOG.md`
- `CODEBASE_ANALYSIS.md`
- `scripts/html_gen/README.md`
- `loggerador.md`
