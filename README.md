# Aulas: IA Aplicada ao Tribunal do Júri

Repositório do material em HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário**.

O projeto converte conteúdo Markdown em páginas HTML com:
- landing page em cards
- páginas de tópicos com sidebar
- menu lateral unificado com 6 itens (inclui **6. Favoritos**)
- tema claro/escuro
- ícones e estilos automáticos

**Publicação**: <https://paulosrl.github.io/aulas-tribunal-do-juri/>

---

## Estrutura do Projeto

```text
.
├── conteudo/
│   ├── index.md
│   ├── 1.md ... 5.md
│   └── favoritos.md
├── templates/
│   ├── index.template.html
│   └── topico.template.html
├── scripts/
│   ├── gera_html.py
│   └── gera_index.py
├── html/
│   ├── index.html
│   ├── 1.html ... 5.html
│   ├── favoritos.html
│   ├── logo.png
│   └── copilot.png
├── graphify-out/
├── AGENTS.md
├── CLAUDE.md
├── CODEX.md
├── GEMINI.md
└── README.md
```

---

## Build Atual (Fonte da Verdade)

O gerador principal do codebase é **`scripts/gera_html.py`**.

Ele gera:
- páginas de tópico (`1.html` a `5.html`)
- página `favoritos.html`
- `index.html` (modo landing, quando `output_html` é `index.html`)

### Comandos

Landing:

```bash
python3 scripts/gera_html.py conteudo/index.md html/index.html
```

Tópico (exemplo):

```bash
python3 scripts/gera_html.py conteudo/3.md html/3.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

Favoritos:

```bash
python3 scripts/gera_html.py conteudo/favoritos.md html/favoritos.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Favoritos" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

Regenerar tudo:

```bash
python3 scripts/gera_html.py conteudo/index.md html/index.html
python3 scripts/gera_html.py conteudo/1.md html/1.html --template templates/topico.template.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" --menu-md conteudo/index.md --section-mode semantic
python3 scripts/gera_html.py conteudo/2.md html/2.html --template templates/topico.template.html --page-title "Engenharia de Prompts – Aplicada ao Ministério Público" --menu-md conteudo/index.md --section-mode semantic
python3 scripts/gera_html.py conteudo/3.md html/3.html --template templates/topico.template.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" --menu-md conteudo/index.md --section-mode semantic
python3 scripts/gera_html.py conteudo/4.md html/4.html --template templates/topico.template.html --page-title "Segurança, Compliance e Regulamentação de IA" --menu-md conteudo/index.md --section-mode semantic
python3 scripts/gera_html.py conteudo/5.md html/5.html --template templates/topico.template.html --page-title "Estudos de Caso e Simulações Práticas" --menu-md conteudo/index.md --section-mode semantic
python3 scripts/gera_html.py conteudo/favoritos.md html/favoritos.html --template templates/topico.template.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Favoritos" --menu-md conteudo/index.md --section-mode semantic
```

> `scripts/gera_index.py` ainda existe, mas o fluxo principal atual está centralizado em `gera_html.py`.

---

## Regras Visíveis no HTML Gerado

- Sidebar com tópicos principais numerados de **1 a 6**.
- Item **Favoritos** aparece como `6. Favoritos` no menu lateral.
- Página de favoritos deixa de ficar bloqueada quando `html/favoritos.html` existe.
- Botões “Acessar Agente Copilot” são gerados a partir de linhas `Acesse o agente: ...` e posicionados antes de `Funcionalidades principais`.
- Ícone desses botões usa `copilot.png` (embutido como data URI no CSS).

---

## Markdown Suportado

- `#`, `##`, `###`
- listas `-` e `1.`
- tabelas pipe
- blockquote e alerta estilo `> [!WARNING]`
- links markdown e URLs diretas
- imagem local markdown `![alt](arquivo)` (remota é bloqueada)

---

## Publicação

```bash
git add conteudo/ html/ scripts/ templates/ README.md CLAUDE.md CODEX.md GEMINI.md
git commit -m "Atualiza docs e páginas geradas"
git push origin main
```

---

## Documentação Relacionada

- [AGENTS.md](AGENTS.md)
- [CLAUDE.md](CLAUDE.md)
- [CODEX.md](CODEX.md)
- [GEMINI.md](GEMINI.md)
