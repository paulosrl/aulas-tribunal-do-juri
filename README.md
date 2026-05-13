# Aulas: IA Aplicada ao Tribunal do Júri

Repositório do material em HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário**. O projeto converte conteúdos em Markdown para páginas HTML com layout padronizado, menu lateral consistente, tema claro/escuro e navegação entre tópicos.

**Publicação**: [https://paulosrl.github.io/aulas-tribunal-do-juri/](https://paulosrl.github.io/aulas-tribunal-do-juri/)

---

## 📁 Estrutura do Projeto

```text
.
├── conteudo/              # Fontes Markdown
│   ├── index.md           # Landing page (fonte)
│   ├── 1.md a 5.md        # Conteúdo dos tópicos
├── templates/             # Templates HTML com marcadores AUTO
│   ├── index.template.html    # Template da landing page
│   └── topico.template.html   # Template dos tópicos (com sidebar)
├── scripts/               # Geradores Markdown → HTML
│   ├── gera_index.py      # Gera html/index.html a partir de conteudo/index.md
│   └── gera_html.py       # Gera páginas de tópicos (html/1.html a 5.html)
├── html/                  # Saída final (publicada no GitHub Pages)
│   ├── index.html         # Landing page
│   ├── 1.html a 5.html    # Páginas de tópicos
│   └── logo.png           # Logo (inserida como data URI nas páginas)
├── graphify-out/          # Grafo de conhecimento (gerado por graphify)
│   ├── graph.html         # Visualização interativa do grafo
│   └── GRAPH_REPORT.md    # Relatório de análise do grafo
├── CLAUDE.md              # Instruções ao Claude Code (detalhes de build)
├── CODEX.md               # Guia de integração com Codex
├── GEMINI.md              # Guia de integração com Gemini
├── AGENTS.md              # Documentação de agentes (graphify)
└── README.md              # Este arquivo
```

---

## 📄 Sistema de Geração

O projeto possui **dois geradores paralelos** para dois tipos de layout diferentes:

### 1. Landing Page (`gera_index.py`)

Gera `html/index.html` a partir de `conteudo/index.md` com **layout de cards** (grid 2 colunas).

**Formato do `conteudo/index.md`**:

```markdown
# Título Principal

**site:** ciia.mppa.mp.br
**subtítulo:** Descrição ou chamada para ação
**rodapé:** MPPA — CIIA

***

## Tópico 1 | Título Visível | 1.html
Descrição breve do tópico.

## Tópico 2 | Outro Título | 2.html
Descrição breve.

[... adicione até 6 tópicos ...]
```

**Regras**:

- `H1` = título da página
- Metadados em `**chave:** valor` antes da primeira seção
- `H2` com formato `## Tag | Título | link.html`
- Descrição em linha imediatamente após o H2
- Separadores `***` entre tópicos (opcional)

**Comando para regenerar**:

```bash
python3 scripts/gera_index.py conteudo/index.md html/index.html --template templates/index.template.html
```

### 2. Páginas de Tópicos (`gera_html.py`)

Gera `html/N.html` a partir de `conteudo/N.md` com **layout de sidebar + conteúdo**, atribuindo ícones automaticamente baseado em palavras-chave e aplicando regras de formatação avançada (alertas críticos, parágrafos estratégicos).

**Comando para regenerar** (exemplo para tópico 1):

```bash
python3 scripts/gera_html.py conteudo/1.md html/1.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --menu-icon "fa-graduation-cap"
```

---

## 🚀 Como Editar e Regenerar

### Editar Conteúdo

1. Abra o arquivo desejado em `conteudo/`:
   - `conteudo/index.md` — landing page
   - `conteudo/1.md` a `5.md` — tópicos

2. Edite em Markdown (títulos, listas, tabelas, etc.)

3. Salve o arquivo

### Regenerar uma Página

**Landing page**:

```bash
python3 scripts/gera_index.py conteudo/index.md html/index.html --template templates/index.template.html
```

**Tópico 1**:

```bash
python3 scripts/gera_html.py conteudo/1.md html/1.html --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --menu-icon "fa-graduation-cap"
```

**Tópico 2**:
```bash
python3 scripts/gera_html.py conteudo/2.md html/2.html --template templates/topico.template.html \
  --page-title "Engenharia de Prompts – Aplicada ao Ministério Público" \
  --menu-icon "fa-lightbulb"
```

**Tópico 3**:
```bash
python3 scripts/gera_html.py conteudo/3.md html/3.html --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --menu-icon "fa-gavel"
```

**Tópico 4**:
```bash
python3 scripts/gera_html.py conteudo/4.md html/4.html --template templates/topico.template.html \
  --page-title "Segurança, Compliance e Regulamentação de IA" \
  --menu-icon "fa-shield-halved"
```

**Tópico 5**:
```bash
python3 scripts/gera_html.py conteudo/5.md html/5.html --template templates/topico.template.html \
  --page-title "Estudos de Caso e Simulações Práticas" \
  --menu-icon "fa-microscope"
```

### Regenerar Tudo

```bash
# Landing page
python3 scripts/gera_index.py conteudo/index.md html/index.html --template templates/index.template.html

# Tópicos
python3 scripts/gera_html.py conteudo/1.md html/1.html --template templates/topico.template.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" --menu-icon "fa-graduation-cap"
python3 scripts/gera_html.py conteudo/2.md html/2.html --template templates/topico.template.html --page-title "Engenharia de Prompts – Aplicada ao Ministério Público" --menu-icon "fa-lightbulb"
python3 scripts/gera_html.py conteudo/3.md html/3.html --template templates/topico.template.html --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" --menu-icon "fa-gavel"
python3 scripts/gera_html.py conteudo/4.md html/4.html --template templates/topico.template.html --page-title "Segurança, Compliance e Regulamentação de IA" --menu-icon "fa-shield-halved"
python3 scripts/gera_html.py conteudo/5.md html/5.html --template templates/topico.template.html --page-title "Estudos de Caso e Simulações Práticas" --menu-icon "fa-microscope"
```

---

## 🎨 Recursos de Markdown Suportados

### Formatação Básica
- `**texto em negrito**` → `<strong>`
- `*texto em itálico*` → `<em>`
- `` `código inline` `` → `<code>`

### Links
- `[texto do link](url)` → `<a href="url">texto do link</a>`
- Links para claude.ai são preservados automaticamente

### Headings
- `# H1` — Título principal (cartão de abertura)
- `## H2` — Seções principais (cards no tópico)
- `### H3` — Subseções

### Listas
- Listas não-ordenadas: `- item`
- Listas ordenadas: `1. item`, `2. item`

### Tabelas

```markdown
| Coluna 1 | Coluna 2 |
|----------|----------|
| Dado     | Valor    |
```

### Caixas de Alerta (estilo Obsidian)

```markdown
> [!WARNING] Título do Alerta
> Conteúdo do alerta vai aqui
```

Tipos suportados: `WARNING`, `CRITICAL`, `NOTE`, `INFO`

### Parágrafos Estratégicos
Parágrafos contendo palavras-chave como "estratégia", "validação", "protocolo" recebem estilo especial (texto discreto).

### Alertas Críticos
Parágrafos mencionando "LGPD", "sigilo judicial" ou "proibido" são automaticamente envolvidos em caixas de alerta vermelho.

---

## 🎯 Ícones

### Ícones de Tópicos
Cada tópico tem um ícone Font Awesome 6 (padrão do template):
- Tópico 1: `fa-graduation-cap` (chapéu de formatura)
- Tópico 2: `fa-lightbulb` (lâmpada)
- Tópico 3: `fa-gavel` (martelo)
- Tópico 4: `fa-shield-halved` (escudo)
- Tópico 5: `fa-microscope` (microscópio)

### Ícones de Seções e Itens

O gerador atribui ícones automaticamente baseado em palavras-chave:

**Atribuição inteligente** (`assign_unique_icons()`):
- Mapeia palavras-chave em português para ícones semânticos
- Garante que nenhum card receba o mesmo ícone do pool (sem duplicatas)
- Volta ao pool de fallback se o ícone preferido já está em uso

**Exemplos de regras**:
- "introdução", "guia" → `fa-book-open`
- "segurança", "privacidade" → `fa-shield-halved`
- "juríd", "lei" → `fa-gavel`
- "contexto", "memória" → `fa-window-maximize`
- Contém URL → `fa-link` (ciano)
- E mais (consulte `scripts/gera_html.py` para lista completa)

**Pool de fallback**: 20 ícones genéricos quando a regra preferida não se aplica

### Ícones da Landing Page
A landing page usa 6 ícones SVG hardcoded em sequência:
1. Checkmark
2. Edit
3. Layers
4. Grid
5. Bookmark
6. Star

---

## 🌙 Tema Claro/Escuro

- **Padrão inicial**: Tema claro
- **Persistência**: A escolha é salva em `localStorage`
- **Botão**: `🌓 TEMA` no canto superior direito
- **Variáveis CSS**: Definidas em `:root` e `body.dark-mode`

---

## 🔧 Detalhes de Implementação

### Gerador de Tópicos (`gera_html.py`)

O pipeline implementa:

1. **Parse de Markdown** — Extrai H1, H2/H3, listas, tabelas, blockquotes
2. **Atribuição de Ícones** — Regras baseadas em palavras-chave + pool de fallback
3. **Classificação de Conteúdo** — Detecta alertas críticos e parágrafos estratégicos
4. **Processamento Inline** — Converte Markdown para HTML preservando links
5. **Injeção em Template** — Insere conteúdo entre marcadores `<!-- AUTO:* -->`
6. **Regras Globais** — Ajusta título, logo, paths

### Gerador de Landing Page (`gera_index.py`)

1. **Parse de Metadados** — Extrai site, subtítulo, rodapé
2. **Parse de Tópicos** — Lê H2 com pipes e descrições
3. **Geração de Cards** — Cria elementos `<a class="card">` com ícones SVG
4. **Injeção em Template** — Insere entre `<!-- AUTO:CARDS:* -->`

### Remocimento de Referências de Origem
A função `strip_source_references()` remove referências a SharePoint/Copilot **sem remover** links para claude.ai (usa negative lookahead).

---

## 📊 Páginas Geradas

| Página | Arquivo | Ícone | Descrição |
|--------|---------|-------|-----------|
| Landing | `html/index.html` | — | Entrada com cards dos 5 tópicos |
| Tópico 1 | `html/1.html` | 🎓 `fa-graduation-cap` | Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário |
| Tópico 2 | `html/2.html` | 💡 `fa-lightbulb` | Engenharia de Prompts – Aplicada ao Ministério Público |
| Tópico 3 | `html/3.html` | ⚖️ `fa-gavel` | Agentes de IA e Sistemas Autônomos |
| Tópico 4 | `html/4.html` | 🛡️ `fa-shield-halved` | Segurança, Compliance e Regulamentação de IA |
| Tópico 5 | `html/5.html` | 🔬 `fa-microscope` | Estudos de Caso e Simulações Práticas |

---

## 🚢 Publicação

### Local
Abra `html/index.html` em um navegador para testar localmente.

### GitHub Pages
As alterações em `html/` são publicadas automaticamente no repositório configurado para GitHub Pages.

**Processo**:
```bash
# Edite conteúdo em conteudo/
# Regenere os HTMLs (comandos acima)
git add conteudo/ html/ templates/ scripts/
git commit -m "Atualiza conteúdo: [descrição breve]"
git push origin main
```

---

## 📚 Documentação Complementar

### Guias de Integração com Assistentes de IA

- **[CLAUDE.md](CLAUDE.md)** — Instruções detalhadas ao Claude Code (estrutura de build, pipeline de geração, sistema de ícones)
- **[CODEX.md](CODEX.md)** — Guia de integração com Codeium Codex
- **[GEMINI.md](GEMINI.md)** — Guia de integração com Google Gemini

### Grafo de Conhecimento

- **[AGENTS.md](AGENTS.md)** — Documentação de agentes e graphify
- **[graphify-out/](graphify-out/)** — Artefatos gerados pelo graphify:
  - `graph.html` — Visualização interativa do grafo de conhecimento
  - `GRAPH_REPORT.md` — Relatório de análise semântica do projeto

---

## 📝 Notas

- **Template de tópico**: 231KB com CSS completo + Font Awesome 6 embutido
- **Logo**: Convertida para base64 data URI automaticamente
- **Compatibilidade**: Responsivo (mobile-first com breakpoint 860px)
- **Encoding**: UTF-8 (suporta português completo)
- **Segurança**: HTML escapeado para prevenir XSS; validações de arquivo em tempo de build
- **Sistema de Ícones**: Atribuição automática de ícones Font Awesome por palavras-chave + pool de fallback (sem duplicatas)
- **Alertas Críticos**: Parágrafos mencionando LGPD, sigilo judicial ou conteúdo proibido são destacados automaticamente
