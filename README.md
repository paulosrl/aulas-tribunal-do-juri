# Aulas: IA Aplicada ao Tribunal do Júri

Repositório do material em HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário**.

O projeto converte conteúdo Markdown em páginas HTML com:
- landing page em cards
- páginas de tópicos com sidebar
- menu lateral unificado com 7 itens (inclui **Favoritos** e **NotebookLM**)
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
│   ├── favoritos.md
│   └── notebooklm.md
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
│   └── notebooklm.html
├── graphify-out/
├── AGENTS.md
├── CLAUDE.md
├── CODEX.md
├── GEMINI.md
└── README.md
```

---

## Build Automático (Recomendado)

Para regenerar **todos** os arquivos HTML de uma vez:

```bash
python3 scripts/build_all.py
```

Este script:

- Descobre automaticamente todos os `.md` em `conteudo/`
- Aplica configurações de página-título e template apropriadas
- Gera um relatório com sucesso/falha de cada arquivo
- Mantém ordem lógica: `index.md` → tópicos 1-5 → favoritos → notebooklm

---

## Build Manual (Por Arquivo)

Se precisar gerar um arquivo isoladamente, use `scripts/gera_html.py`:

**Landing:**

```bash
python3 scripts/gera_html.py conteudo/index.md html/index.html
```

**Tópico (exemplo):**

```bash
python3 scripts/gera_html.py conteudo/3.md html/3.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

**Favoritos / NotebookLM:**

```bash
python3 scripts/gera_html.py conteudo/favoritos.md html/favoritos.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Favoritos" \
  --menu-md conteudo/index.md \
  --section-mode semantic
```

---

## Arquitetura

### Estrutura de Módulos

O gerador está organizado em `scripts/html_gen/` com responsabilidades claras:

- **`cli.py`**: Interface de linha de comando (parse de argumentos, orquestração)
- **`parser.py`**: Parse de markdown → HTML intermediário
- **`renderer.py`**: Renderização em templates
- **`postprocessor.py`**: Processamento pós-geração (injeção de menu, regras globais)
- **`classifier.py`**: Detecção de tipos de linha (marcadores, comentários, etc)
- **`icons.py`**: Mapeamento automático de ícones
- **`validation.py`**: Validação de integridade de conteúdo
- **`constants.py`**: Constantes globais (regras de ícones, pools, etc)
- **`models.py`**: Estruturas de dados
- **`utils.py`**: Funções utilitárias

Para detalhes, veja [scripts/html_gen/README.md](scripts/html_gen/README.md).

### Pipeline Geral

```text
conteudo/*.md
    ↓
[parse_markdown]
    ↓
[apply_global_rules]
    ↓
[assign_icons]
    ↓
[render_templates]
    ↓
html/*.html
```

---

## Regras Visíveis no HTML Gerado

- Sidebar com navegação unificada para **1 a 5**, **Favoritos** e **NotebookLM**.
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
