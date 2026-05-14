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
│   ├── 6.md
│   └── 7.md
├── templates/
│   ├── index.template.html
│   └── topico.template.html
├── scripts/
│   ├── build_all.py
│   ├── gera_html.py (wrapper)
│   ├── lock_menu_items.py
│   └── html_gen/ (módulo principal)
├── html/
│   ├── index.html
│   ├── 1.html ... 5.html
│   ├── 6.html
│   └── 7.html
├── graphify-out/
├── AGENTS.md
├── CLAUDE.md
├── CODEX.md
├── GEMINI.md
└── README.md
```

---

## Arquivos Python: Função e Uso

### Scripts executáveis (`scripts/`)

| Arquivo | Função | Como usar |
|---|---|---|
| `scripts/build_all.py` | Orquestra build completo: descobre `conteudo/*.md`, ordena (`index`, tópicos numéricos, extras), chama o gerador e imprime sumário de sucesso/falha. | `python3 scripts/build_all.py` |
| `scripts/gera_html.py` | Wrapper de entrada para o módulo `html_gen`; delega para `html_gen.cli.main()`. | `python3 scripts/gera_html.py <input.md> <output.html> [--template ... --page-title ... --section-mode semantic\|page]` |
| `scripts/lock_menu_items.py` | Trava/destrava cards e itens de menu por número de tópico nos HTMLs gerados, incluindo modo simulação (`--dry-run`). | Travar: `python3 scripts/lock_menu_items.py --items 4 5 7`  •  Destravar: `python3 scripts/lock_menu_items.py --items 4 5 7 --unlock` |

### Módulo principal (`scripts/html_gen/`)

| Arquivo | Função | Como usar |
|---|---|---|
| `scripts/html_gen/cli.py` | CLI principal do gerador: parse de argumentos, escolha de fluxo (landing vs tópico), parse, renderização, pós-processamento e validações. | Uso indireto via `scripts/gera_html.py` ou direto: `python3 -m html_gen.cli ...` (com `PYTHONPATH` ajustado para `scripts/`). |
| `scripts/html_gen/parser.py` | Converte Markdown em `List[Card]`; interpreta headings, listas, tabelas, blockquotes, alertas, blocos de agente e imagens locais em data URI. | Uso interno por import em `cli.py`. |
| `scripts/html_gen/renderer.py` | Renderiza cards HTML, submenu interno e acordeão lateral de tópicos. | Uso interno por import em `cli.py`. |
| `scripts/html_gen/postprocessor.py` | Regras globais após render: título, logo/ícones embutidos, CSS/JS injetados e ajustes finais de navegação/layout. | Uso interno por import em `cli.py`. |
| `scripts/html_gen/validation.py` | Valida completude e preservação de conteúdo entre Markdown e HTML final; lança erro em perda relevante. | Uso interno por import em `cli.py`. |
| `scripts/html_gen/icons.py` | Seleção e distribuição de ícones (cards, itens e agentes), com regras semânticas e prevenção de duplicação. | Uso interno por import em `parser.py`, `renderer.py` e `cli.py`. |
| `scripts/html_gen/classifier.py` | Classificadores de linhas e conteúdo: marcadores de página, comentários OCR, separadores e heurísticas de parágrafo estratégico/crítico. | Uso interno por import em `parser.py`. |
| `scripts/html_gen/utils.py` | Utilitários transversais: escape HTML, sanitização de `href`, markdown inline, limpeza de títulos, data URI e substituição entre marcadores. | Uso interno por import em múltiplos módulos. |
| `scripts/html_gen/constants.py` | Constantes centrais: marcadores `AUTO`, regras/pool de ícones, regex de cabeçalho de agente e itens do menu lateral. | Uso interno por import em múltiplos módulos. |
| `scripts/html_gen/models.py` | Modelo `Card` (`dataclass`) e re-export de constantes usadas no pacote. | Uso interno por import em parser/render. |
| `scripts/html_gen/__init__.py` | Ponto de exportação do pacote `html_gen` (`__all__`) para facilitar imports externos. | Uso por import (`from html_gen import ...`) quando necessário. |

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
- Mantém ordem lógica: `index.md` → tópicos `1.md` a `7.md`

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
  --section-mode semantic
```

**Favoritos (Tópico 6):**

```bash
python3 scripts/gera_html.py conteudo/6.md html/6.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Favoritos" \
  --section-mode semantic
```

**Guia NotebookLM (Tópico 7):**

```bash
python3 scripts/gera_html.py conteudo/7.md html/7.html \
  --template templates/topico.template.html \
  --page-title "NotebookLM no Tribunal do Júri" \
  --section-mode semantic
```

---

## Travar/Destravar Itens de Menu (Script)

Foi adicionado o utilitário:

- `scripts/lock_menu_items.py`

Ele permite **travar** e **destravar** itens de navegação por número de tópico (ex.: `4 5 7`), atuando em:

- `html/index.html` (cards/menu de acesso da landing)
- menus laterais dos arquivos:
  - `html/1.html`
  - `html/2.html`
  - `html/3.html`
  - `html/4.html`
  - `html/5.html`
  - `html/6.html`
  - `html/7.html`

### Comandos

**Travar itens 4, 5 e 7:**

```bash
python3 scripts/lock_menu_items.py --items 4 5 7
```

**Destravar itens 4, 5 e 7:**

```bash
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock
```

**Simular sem gravar (`dry-run`):**

```bash
python3 scripts/lock_menu_items.py --items 4 5 7 --dry-run
```

**Limitar a arquivos específicos:**

```bash
python3 scripts/lock_menu_items.py --items 7 --files html/index.html html/1.html
```

### O que o script altera ao travar

- adiciona classe `nav-locked`
- remove `href` (guardando em `data-href`)
- adiciona `aria-disabled="true"` e `tabindex="-1"`
- adiciona cadeado visual (`🔒` + ícone `fa-lock`)

### O que o script faz ao destravar

- remove `nav-locked`
- restaura `href` a partir de `data-href`
- remove `aria-disabled`, `tabindex` e `data-href`
- remove o cadeado injetado

### Observações

- O `index.html` da raiz do repositório é apenas redirecionador para `html/index.html`.
- O script é idempotente para uso normal (não deve duplicar lock em fluxos de lock/unlock).

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

### Pipeline Detalhado

O processamento de cada arquivo markdown segue 6 etapas:

#### **1️⃣ Orquestração (cli.py)**

- Parse argumentos de linha de comando
- Determina tipo de página: landing (`index.html`) ou tópico
- Carrega template apropriado
- Valida caminhos de entrada/saída

**Entrada**: argumentos do shell

**Saída**: configurações validadas para próxima etapa

---

#### **2️⃣ Parse de Markdown (parser.py)**

Converte markdown bruto em HTML estruturado.

**O que faz:**

- Converte `#`, `##`, `###` em `<h1>`, `<h2>`, `<h3>`
- Processa listas (`-`, `1.`)
- Renderiza tabelas pipe (`| coluna |`)
- Transforma blockquotes e alertas (`> [!WARNING]`)
- Preserva links markdown `[texto](url)` e URLs diretas
- Detecta blocos de agentes (`Acesse o agente: ...`)
- **Remove**: marcadores de página, comentários OCR, referências automáticas de SharePoint

**Conecta com:**

- `classifier.py` — para filtrar linhas não relevantes
- `constants.py` — para padrões de detecção

**Entrada**: Conteúdo markdown bruto

**Saída**: HTML intermediário com blocos estruturados

---

#### **3️⃣ Atribuição de Ícones (icons.py)**

Mapeia títulos de blocos para ícones Font Awesome 6 de forma automática.

**O que faz:**

- Lê título de cada bloco (ex: "Introdução", "Segurança")
- Consulta `ICON_RULES` em `constants.py` para encontrar melhor match
- Evita duplicação: se ícone já foi usado, escolhe alternativo de `ICON_POOL`
- Injeta class CSS `fa-icon-name` no HTML

**Exemplos de mapeamento:**

- "Introdução" → `fa-book-open`
- "Segurança" → `fa-shield-halved`
- "Análise" → `fa-search`

**Entrada**: HTML com blocos (sem ícones)

**Saída**: HTML com classes de ícones FA6 adicionadas

---

#### **4️⃣ Renderização em Template (renderer.py)**

Injeta conteúdo HTML no template apropriado.

**Para landing page** (`index.html`):

- Extrai tópicos de `conteudo/index.md`
- Gera cards com título, descrição, ícone
- Renderiza grid de 7 tópicos (1-5, Favoritos, NotebookLM)

**Para tópicos** (`1.html` a `5.html`, `6.html`, `7.html`):

- Injeta conteúdo entre `<!-- AUTO:CONTENT:START -->` e `<!-- AUTO:CONTENT:END -->`
- Preserva estrutura de template

**Entrada**: HTML processado + template

**Saída**: HTML com conteúdo injetado em template

---

#### **5️⃣ Pós-processamento (postprocessor.py)**

Injeção de menu sidebar e aplicação de regras globais.

**O que faz:**

- Renderiza menu lateral fixo a partir de `TOPIC_NAV_ITEMS` do gerador
- Renderiza sidebar com 7 itens fixos: Início, Tópicos (1-5), Favoritos, NotebookLM
- Injeta menu entre `<!-- AUTO:MENU:TOPICOS:START -->` e `<!-- AUTO:MENU:TOPICOS:END -->`
- Aplica regras CSS/JavaScript globais (tema claro/escuro, responsive)
- Escapa HTML especial e sanitiza URLs (previne XSS)

**Entrada**: HTML com placeholder de menu

**Saída**: HTML final com sidebar injetada

---

#### **6️⃣ Validação (validation.py)**

Verifica integridade do conteúdo antes de salvar.

**O que faz:**

- Compara contagem de linhas/parágrafos: markdown vs HTML
- Verifica se URLs foram preservadas
- Alerta se houver discrepâncias suspeitas
- Garante que nenhum conteúdo foi perdido silenciosamente

**Entrada**: Markdown original + HTML final

**Saída**: logs de validação no stdout; em perda relevante, erro (`ValueError`) interrompendo a geração

---

### Pipeline Visual

```text
conteudo/N.md
    ↓
[1. cli.py] — Parse CLI, valida caminhos
    ↓
[2. parser.py] — Markdown → HTML, filtra linhas, detecta agentes
    ↓
[3. icons.py] — Mapeia títulos → ícones FA6, evita duplicação
    ↓
[4. renderer.py] — Injeta em template (landing ou tópico)
    ↓
[5. postprocessor.py] — Injeção de sidebar, escaping, regras globais
    ↓
[6. validation.py] — Verifica integridade conteúdo
    ↓
html/N.html
```

---

## Regras Visíveis no HTML Gerado

- Sidebar com navegação unificada para **1 a 5**, **Favoritos** e **NotebookLM**.
- Página de favoritos deixa de ficar bloqueada quando `html/6.html` existe.
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
