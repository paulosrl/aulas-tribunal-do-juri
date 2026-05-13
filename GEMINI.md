# GEMINI.md

Guia de trabalho do Gemini neste repositório.

## Estado Atual do Projeto

- Gerador principal: `scripts/gera_html.py`
- Fontes: `conteudo/*.md`
- Saídas: `html/*.html`
- Template de tópicos: `templates/topico.template.html`
- Template de landing: `templates/index.template.html`

## Build

### Landing

```bash
python3 scripts/gera_html.py conteudo/index.md html/index.html
```

### Tópico

```bash
python3 scripts/gera_html.py conteudo/N.md html/N.html \
  --template templates/topico.template.html \
  --page-title "<titulo>" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

### Favoritos

```bash
python3 scripts/gera_html.py conteudo/favoritos.md html/favoritos.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Favoritos" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

### NotebookLM

```bash
python3 scripts/gera_html.py conteudo/notebooklm.md html/notebooklm.html \
  --template templates/topico.template.html \
  --page-title "NotebookLM no Tribunal do Júri" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

## Regras Importantes

- Não remover marcadores `<!-- AUTO:* -->` dos templates.
- Menu lateral padrão tem 7 itens, incluindo `Favoritos` e `NotebookLM`.
- Botão de agente Copilot é detectado por linha `Acesse o agente: ...`.
- Ícone do botão Copilot usa `copilot.png` e é embutido no CSS.

## Graphify

Siga o `AGENTS.md`:
- ler `graphify-out/GRAPH_REPORT.md` para contexto arquitetural
- após mudar código Python, rodar `graphify update .`
