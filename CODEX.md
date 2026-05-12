# CODEX.md

Este arquivo fornece orientação ao Codex ao trabalhar com código neste repositório.

## Visão Geral do Projeto

**Tribunal do Júri - Curso de IA**: Plataforma educacional em português que ensina profissionais do Direito como usar IA em processos judiciais e investigações. O conteúdo aborda engenharia de prompt, gestão de contexto e prevenção de alucinações em contextos jurídicos.

## Sistema de Build

### Gerando HTML a partir de Markdown

O projeto usa um sistema Python customizado para converter conteúdo de cursos em Markdown para páginas HTML estilizadas com menus e navegação dinâmica.

**Script de build principal**: `scripts/build_topico.py`

**Uso básico**:
```bash
python3 scripts/build_topico.py conteudo/topico1.md html/topico1.html \
  --template templates/topico.template.html \
  --page-title "Título da Sua Página" \
  --menu-icon "fa-list-ol"
```

**Parâmetros obrigatórios**:
- `input_md`: Arquivo Markdown de origem (ex: `conteudo/topico1.md`)
- `output_html`: Localização do arquivo HTML de saída (ex: `html/topico1.html`)

**Parâmetros opcionais**:
- `--template`: Template HTML com marcadores AUTO (padrão: `templates/topico.template.html`)
- `--page-title`: Título da página na tag `<title>`
- `--menu-icon`: Ícone Font Awesome para itens do menu
- `--menu-md`: Arquivo de definição do menu (padrão: `menu.md`)

**Exemplo com todas as opções**:
```bash
python3 scripts/build_topico.py \
  conteudo/topico1.md \
  html/topico1.html \
  --template templates/topico.template.html \
  --page-title "Engenharia de Contexto para IA Jurídica" \
  --menu-icon "fa-book-open" \
  --menu-md menu.md
```

## Arquitetura do Projeto

### Estrutura de Diretórios

```
.
├── conteudo/              # Arquivos Markdown com conteúdo do curso
│   └── topico1.md         # Material do curso em formato Markdown
├── templates/             # Templates HTML com marcadores AUTO
│   └── topico.template.html  # Template principal (231KB, contém estilos + marcadores)
├── scripts/               # Scripts de build e automação
│   └── build_topico.py    # Conversor Markdown → HTML
├── html/                  # Diretório de saída com HTMLs gerados
└── AGENTS.md              # Menção ao grafo de conhecimento graphify
```

### Arquitetura do Pipeline de Build

O script `build_topico.py` implementa um pipeline sofisticado de conversão Markdown → HTML:

1. **Análise de Markdown** (`parse_markdown()`):
   - Extrai H1 como card de abertura
   - Converte H2/H3 para seções de cards
   - Analisa listas (ordenadas e não-ordenadas)
   - Processa tabelas com sintaxe pipe
   - Detecta blockquotes e caixas de alerta (estilo Obsidian: `> [!WARNING]`)
   - Extrai parágrafos e agrupa inteligentemente

2. **Atribuição de Ícones**:
   - **Regras baseadas em palavras-chave** (array `ICON_RULES`): Mapeia palavras-chave (em português) para ícones Font Awesome
   - Exemplos: "introdução" → `fa-book-open`, "segurança" → `fa-shield-halved`, "juríd" → `fa-gavel`
   - **Deduplicação inteligente** (`assign_unique_icons()`): Garante que nenhum card receba o mesmo ícone do pool
   - Volta ao `ICON_POOL` se o ícone preferido já está em uso

3. **Classificação de Conteúdo**:
   - **Alertas críticos** (`classify_critical_paragraph()`): Parágrafos mencionando LGPD, sigilo judicial ou conteúdo proibido são envolvidos em caixas `alert-critical`
   - **Parágrafos estratégicos** (`is_strategic_paragraph()`): Conteúdo sobre estratégia, validação, boas práticas recebe estilo `text-discreet`

4. **Processamento de Markdown Inline** (`inline_md()`):
   - Escapa entidades HTML
   - Converte `**texto**` → `<strong>texto</strong>`
   - Converte `*texto*` → `<em>texto</em>`
   - Converte `` `código` `` → `<code>código</code>`
   - Processa caracteres especiais escapados

5. **Injeção de Template** (`replace_between()`):
   - Procura por marcadores especiais no template HTML:
     - `<!-- AUTO:MENU:AULA1:START -->` ... `<!-- AUTO:MENU:AULA1:END -->` → Injeta menu de tópicos
     - `<!-- AUTO:CONTENT:START -->` ... `<!-- AUTO:CONTENT:END -->` → Injeta conteúdo principal
     - `<!-- AUTO:MENU:TOPICOS:START -->` ... `<!-- AUTO:MENU:TOPICOS:END -->` → Injeta navegação entre tópicos

6. **Regras Globais de Página** (`apply_global_page_rules()`):
   - Substitui tag `<title>` com o título fornecido
   - Atualiza títulos do menu em versões mobile e desktop
   - Injeta logo a partir de `logo.png` (converte para base64 data URI)
   - Corrige caminhos relativos para links da homepage

### Fluxo de Dados

```
topico1.md (Markdown)
    ↓
parse_markdown() → List[Card]
    ↓
assign_unique_icons() → card_icons: List[str]
    ↓
render_cards() → Seções HTML de conteúdo
render_menu() → Menu HTML de navegação
    ↓
replace_between() no template → Insere conteúdo + menu
    ↓
apply_global_page_rules() → HTML final com título + logo
    ↓
topico1.html (Saída HTML)
```

### Estruturas de Dados Principais

**Card** (dataclass):
- `title`: Título da seção (string)
- `level`: Nível de heading (1 ou 2)
- `blocks`: Lista de blocos de conteúdo HTML (parágrafos, listas, tabelas, alertas)

Cada card representa uma seção principal do curso. Cards são renderizados como `<section class="caor-card">` com ícones dinâmicos.

### Sintaxe Markdown Customizada

O parser reconhece recursos Markdown estendidos:

**Caixas de alerta** (estilo Obsidian):
```markdown
> [!WARNING] Título Customizado
> Conteúdo do alerta vai aqui
```

**Itens de lista chave-valor** (para conteúdo estruturado):
```markdown
- **Label:** Descrição
- ⚖️ **Atividade-Fim:** Conteúdo de atividade
```

**Tabelas**: Sintaxe pipe padrão (normalizada automaticamente para desajustes de coluna)

**Parágrafos estratégicos**: Detectados por palavras-chave como "estratégia", "validação", "protocolo" — estilizados com opacidade reduzida

**Alertas críticos**: Parágrafos mencionando "LGPD", "sigilo judicial", "proibido" — envolvidos em caixas de alerta com estilo `alert-critical`

## Detalhes Importantes de Implementação

### Sistema de Pool de Ícones

Dois níveis de seleção de ícones:

1. **Regras de palavras-chave** (correspondência semântica):
   - 13 grupos de regras cobrindo conceitos jurídicos
   - Correspondência de padrão em texto de título limpo e em minúsculas
   - Exemplos: "contexto" ou "memória" → `fa-window-maximize`

2. **Pool de fallback** (20 ícones genéricos):
   - Usado quando o ícone preferido já está atribuído
   - Garante variedade visual entre seções

### Normalização de Títulos

A função `clean_md_title()`:
- Remove espaços em branco no início e fim
- Remove marcadores de `**negrito**` envolventes
- Converte caracteres escapados (`\-` → `-`)
- Colapsa espaços em branco
- Usada em todo o código para rótulos de menu consistentes

### Segurança HTML

A função `esc()` usa `html.escape()` com `quote=True` para prevenir XSS ao renderizar títulos e conteúdo.

## Integração com Graphify

Este projeto tem um grafo de conhecimento graphify (`graphify-out/`). Para perguntas sobre arquitetura entre módulos, use:
```bash
graphify query "como X se relaciona com Y"
graphify path "modulo-a" "modulo-b"
graphify explain "nome-conceito"
```

Veja `AGENTS.md` para regras de graphify.

## Tarefas Comuns de Desenvolvimento

### Adicionar uma nova seção do curso

1. Crie ou edite `conteudo/topicN.md` com seu material de curso
2. Execute o script de build para gerar `html/topicN.html`
3. Certifique-se de que `logo.png` existe no diretório `html/` (será convertido para base64 automaticamente)

### Atualizar estilos do template

O arquivo template (`templates/topico.template.html`) tem 231KB e contém:
- CSS completo com suporte a dark mode
- Integração da biblioteca de ícones Font Awesome
- Layout responsivo (sidebar + conteúdo principal)
- Variáveis de esquema de cores em `:root`

**Importante**: Sempre preserve os marcadores AUTO ao editar templates:
- `<!-- AUTO:MENU:AULA1:START -->` ... `<!-- AUTO:MENU:AULA1:END -->`
- `<!-- AUTO:CONTENT:START -->` ... `<!-- AUTO:CONTENT:END -->`
- `<!-- AUTO:MENU:TOPICOS:START -->` ... `<!-- AUTO:MENU:TOPICOS:END -->`

### Adicionar regras Markdown customizadas

Estenda a análise em `build_topico.py`:
- Adicione regras de palavras-chave ao `ICON_RULES` para novos mapeamentos de ícones
- Estenda `classify_critical_paragraph()` para novos tipos de alerta
- Adicione lógica de detecção em `is_strategic_paragraph()` para regras de estilo
- Modifique `pick_item_icon()` para regras de ícones específicos de itens de lista

## Testes e Validação

O script inclui validação integrada:
- Verificações de existência de arquivo (template, Markdown de entrada, logo)
- Validação de marcadores em templates (lança `ValueError` se marcadores não encontrados)
- Remoção de card de intro vazio (se houver apenas uma seção)

Para testar um build:
```bash
python3 scripts/build_topico.py conteudo/topico1.md /tmp/test.html
# Verifique o HTML de saída no navegador
```

## Notas de Performance

- O algoritmo de atribuição de ícones garante que não há ícones duplicados enquanto respeita preferências de palavras-chave
- A análise de tabelas normaliza automaticamente comprimentos de linhas para segurança
- A renderização inline de HTML é feita em uma única passagem
- Todas as operações de I/O de arquivo usam codificação UTF-8 (caracteres em português suportados)
