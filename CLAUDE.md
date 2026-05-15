# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Memória operacional curta do projeto.

## Estado Atual

- Entrada de conteúdo: `conteudo/index.md` e `conteudo/1.md` ... `conteudo/7.md`.
- Saídas: `html/index.html` e `html/1.html` ... `html/7.html`.
- Templates: `templates/index.template.html` e `templates/topico.template.html`.
- Pipeline principal: `scripts/html_gen/*` (via `scripts/gera_html.py`).
- Log de geração: `loggerador.md` (página, data/hora e SHA-256).
- Sem testes automatizados (cobertura de testes = 0%).

## Arquitetura do Pipeline

O fluxo de geração HTML segue esta sequência:

1. **parser.py**: Converte markdown em estrutura `Card` (seções/blocos hierárquicos)
2. **icons.py**: Seleciona e decoduplica ícones Font Awesome para cada card
3. **renderer.py**: Renderiza conteúdo HTML, menu lateral e sumário
4. **postprocessor.py**: Aplica CSS/JS globais, tema claro/escuro e ajustes finais
5. **validation.py**: Valida completude e preservação de conteúdo vs. original

**Entrada principal:** `scripts/gera_html.py` (wrapper CLI que orquestra `html_gen.cli.main`)

**Orchestração:** `scripts/build_all.py` descobre todos os markdowns em `conteudo/` e executa build paralelo

## Estrutura de Dados

Cada página é modelada como lista de `Card` (em `html_gen/models.py`):

- `title`: Título da seção (H2/H3)
- `blocks`: Lista de conteúdos (parágrafos, listas, etc.)
- `icon`: Ícone Font Awesome atribuído
- `collapsed`: Flag para trava de menu

## Comandos de Trabalho

Build completo (todas as páginas):

```bash
python3 scripts/build_all.py
```

Build unitário (uma página):

```bash
python3 scripts/gera_html.py conteudo/N.md html/N.html \
  --template templates/topico.template.html \
  --page-title "<titulo>" \
  --section-mode semantic
```

Travar/destravar itens de menu:

```bash
# Travar tópicos 4, 5, 7
python3 scripts/lock_menu_items.py --items 4 5 7

# Destravar tópicos
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock

# Teste seco (sem alteração)
python3 scripts/lock_menu_items.py --items 4 5 7 --dry-run
```

Consultar log de geração:

```bash
# Primeiras 40 linhas
sed -n '1,40p' loggerador.md
```

Verificar sintaxe Python:

```bash
python3 -m py_compile scripts/build_all.py scripts/gera_html.py scripts/lock_menu_items.py scripts/html_gen/*.py
```

## Regra de Títulos (CRÍTICA)

**Todos os títulos das páginas seguem este padrão:**

```text
Inteligência Artificial Aplicada ao Tribunal do Júri — <Tópico>
```

**Exemplo:**

- `1.html`: "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário"
- `2.html`: "Inteligência Artificial Aplicada ao Tribunal do Júri — Engenharia de Prompts"
- `3.html`: "Inteligência Artificial Aplicada ao Tribunal do Júri — Fluxo nos Crimes Dolosos"

**Como funciona:**

1. `build_all.py` extrai o H1 (primeira linha `# ...`) de cada arquivo markdown
2. Usa a função `build_page_title()` para montar o título padrão
3. Passa automaticamente via `--page-title` ao gerador
4. **Não é necessário editar manualmente** — a regra é aplicada automaticamente

**Mapeamento de tópicos (PAGE_TOPICS):**

Em `scripts/build_all.py`, cada arquivo tem seu tópico definido:

```python
PAGE_TOPICS = {
    '1.md': 'Do Inquérito ao Plenário',
    '2.md': 'Engenharia de Prompts',
    '3.md': 'Fluxo nos Crimes Dolosos',
    '4.md': 'Elementos Gráficos no Tribunal do Júri',
    '5.md': 'NotebookLM',
    '6.md': 'Sites Abertos',
    '7.md': 'Apresentação',
}
```

Se precisar mudar o tópico de uma página, edite `PAGE_TOPICS` em `build_all.py`, não o arquivo markdown.

## Regras Visuais (Tema Claro/Escuro)

**Tema claro (`prefers-color-scheme: light`):**

- Menu principal: `#8A1F3A` (marrom/burgundy)
- Subitens: `#8A1F3A`

**Tema escuro (`prefers-color-scheme: dark`):**

- Destaques principais (títulos, links): `#fbd246` (amarelo)
- Subitens: branco
- Ícones: mantêm paleta própria (não herdam cores forçadas)

Cores definidas em:

- Template: `templates/topico.template.html` (CSS inline)
- Pós-processamento: `scripts/html_gen/postprocessor.py` (ajustes globais)

## Regras de Segurança de Edição

1. **Preservar marcadores AUTO** — Nunca remover `<!-- AUTO:* -->` dos templates (usados para injeção de conteúdo gerado)
2. **Sincronizar estilo** — Mudanças de CSS/cores devem ser feitas em AMBOS:
   - `templates/topico.template.html` (template)
   - `scripts/html_gen/postprocessor.py` (pós-processamento dinâmico)
3. **Graphify após Python** — Após alterar código Python:

   ```bash
   graphify update .
   ```

4. **Validação sempre** — Sempre rodar `python3 scripts/build_all.py` após mudanças para validar

## Validação e Debugging

**Validações automáticas (em `html_gen/validation.py`):**

- `validate_completeness()`: Verifica se todo o conteúdo foi processado
- `validate_content_preservation()`: Confirma que nenhum texto foi perdido na transformação

**Rastrear erros através do pipeline:**

1. Verificar saída do parser: adicionar `print(cards)` em `cli.py:main()` após `parse_markdown()`
2. Verificar atribuição de ícones: `assign_unique_icons(cards)`
3. Verificar renderização: `render_cards(cards)`
4. Verificar pós-processamento: `apply_global_page_rules(html_content)`

## Funcionalidades Especiais

**Landing page (index.html):**

- Redirecionador que aponta para `html/index.html`
- `logo.png` e `mppa.png` são embarcados como data URIs quando disponíveis
- CTA "Acessar Agente Copilot" é convertido para botão estilizado em pós-processamento

**Log de geração (`loggerador.md`):**

- Registra cada página gerada com data/hora e hash SHA-256
- Útil para rastreabilidade e detecção de mudanças
- Alimentado automaticamente por `cli.py:append_generation_log()`

## Pente-fino Rápido (Checklist antes de Commit)

```bash
# 1. Validar sintaxe Python
python3 -m py_compile scripts/build_all.py scripts/gera_html.py scripts/lock_menu_items.py scripts/html_gen/*.py

# 2. Build completo
python3 scripts/build_all.py

# 3. Testes de lock (secos)
python3 scripts/lock_menu_items.py --items 4 5 7 --dry-run
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock --dry-run

# 4. Atualizar graphify
graphify update .
```

## Documentação Relacionada

- `README.md` — Visão geral e exemplos de uso
- `scripts/html_gen/README.md` — Detalhes dos módulos do pipeline
- `loggerador.md` — Log de geração das páginas
- `CODEX.md` / `AGENTS.md` / `GEMINI.md` — Documentação adicional
