# Aulas: IA Aplicada ao Tribunal do Júri

Repositório de geração de páginas HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri**.

Publicação: <https://paulosrl.github.io/aulas-tribunal-do-juri/>

## Visão Geral

O projeto converte `conteudo/*.md` em:
- `html/index.html` (landing)
- `html/1.html` ... `html/7.html` (tópicos)

O pipeline aplica templates, navegação lateral, tema claro/escuro, componentes visuais e validações de conteúdo automaticamente.

## Estrutura

```text
.
├── conteudo/
├── templates/
├── scripts/
│   ├── build_all.py
│   ├── gera_html.py
│   ├── lock_menu_items.py
│   └── html_gen/
├── html/
└── graphify-out/
```

## Geração

Build completo:

```bash
python3 scripts/build_all.py
```

Build de um arquivo:

```bash
python3 scripts/gera_html.py conteudo/3.md html/3.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --section-mode semantic
```

## Pipeline Real (scripts/html_gen)

Entrada: `scripts/gera_html.py` (wrapper fino para `html_gen.cli.main`).

1. `cli.py`: argumentos e roteamento (landing x tópico)
2. `parser.py`: markdown para estrutura `Card`
3. `cli.py`: remoção de seções vazias
4. `icons.py`: deduplicação e atribuição de ícones
5. `renderer.py`: HTML de conteúdo + menu/sumário
6. `postprocessor.py`: CSS/JS e ajustes globais finais
7. `validation.py`: completude e preservação de conteúdo

## Scripts

- `scripts/build_all.py`: orquestra build de todos os markdowns.
- `scripts/gera_html.py`: ponto de entrada CLI do gerador.
- `scripts/lock_menu_items.py`: trava/destrava itens de menu/cards por tópico.

Exemplos do lock:

```bash
python3 scripts/lock_menu_items.py --items 4 5 7
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock
python3 scripts/lock_menu_items.py --items 4 5 7 --dry-run
```

## Regras de Estilo em Uso

- Tema claro: texto de menu em `#8A1F3A`.
- Tema escuro: títulos principais do menu e links destacados em `#fbd246`.
- Subitens do menu:
  - tema claro em `#8A1F3A`
  - tema escuro em branco
- Ícones mantêm paleta própria (não herdam cor forçada dos subitens).

## Observações

- `index.html` na raiz é redirecionador para `html/index.html`.
- Landing embute `html/logo.png` e `html/mppa.png` como data URI quando disponíveis.
- CTA “Acessar Agente Copilot” é convertido para botão estilizado no pós-processamento.

## Graphify

Após alterar código Python:

```bash
graphify update .
```

## Documentos Relacionados

- `AGENTS.md`
- `CODEX.md`
- `CLAUDE.md`
- `GEMINI.md`
- `CODEBASE_ANALYSIS.md`
- `scripts/html_gen/README.md`
