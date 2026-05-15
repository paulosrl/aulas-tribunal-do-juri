# Aulas: IA Aplicada ao Tribunal do Júri

Repositório de geração de páginas HTML da trilha **Inteligência Artificial Aplicada ao Tribunal do Júri**.

Publicação: <https://paulosrl.github.io/aulas-tribunal-do-juri/>

## Visão Geral

O projeto converte arquivos Markdown em:
- `html/index.html` (landing page)
- `html/1.html` ... `html/7.html` (páginas de tópicos)

A geração aplica automaticamente:
- layout e estilos a partir de templates
- menu lateral unificado de tópicos
- tema claro/escuro
- regras visuais e componentes (ex.: CTA de agente Copilot)
- validações de completude e preservação de conteúdo

## Estrutura

```text
.
├── conteudo/
│   ├── index.md
│   └── 1.md ... 7.md
├── templates/
│   ├── index.template.html
│   └── topico.template.html
├── scripts/
│   ├── build_all.py
│   ├── gera_html.py
│   ├── lock_menu_items.py
│   └── html_gen/
├── html/
│   ├── index.html
│   └── 1.html ... 7.html
├── graphify-out/
└── README.md
```

## Como Gerar

### Build completo (recomendado)

```bash
python3 scripts/build_all.py
```

Opções:

```bash
python3 scripts/build_all.py --help
python3 scripts/build_all.py --timeout 45
```

Comportamento:
- descobre automaticamente `conteudo/*.md`
- ordena em `index.md`, depois páginas numéricas
- gera saída em `html/`
- mostra sumário final com sucesso/falha por arquivo

### Build por arquivo

Landing:

```bash
python3 scripts/gera_html.py conteudo/index.md html/index.html
```

Tópico:

```bash
python3 scripts/gera_html.py conteudo/3.md html/3.html \
  --template templates/topico.template.html \
  --page-title "Inteligência Artificial Aplicada ao Tribunal do Júri — Do Inquérito ao Plenário" \
  --section-mode semantic
```

## Pipeline de Geração (real)

Entrada principal: `scripts/gera_html.py` (wrapper de `html_gen.cli.main`).

Fluxo:
1. `cli.py`: parse de argumentos e roteamento (landing vs tópico)
2. `parser.py`: markdown -> estrutura `Card` e blocos HTML
3. `cli.py`: remoção automática de seções vazias (cards sem conteúdo útil)
4. `icons.py`: atribuição de ícones únicos
5. `renderer.py`: render de cards e navegação interna
6. `postprocessor.py`: regras globais de página, CSS/JS e injeções finais
7. `validation.py`: completude + preservação de conteúdo
8. gravação do HTML final

## Scripts Python

### `scripts/build_all.py`
Orquestra o build de todos os markdowns em `conteudo/`.

### `scripts/gera_html.py`
Wrapper CLI para o módulo gerador `scripts/html_gen/cli.py`.

### `scripts/lock_menu_items.py`
Trava/destrava itens de menu e cards por número de tópico.

Exemplos:

```bash
python3 scripts/lock_menu_items.py --items 4 5 7
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock
python3 scripts/lock_menu_items.py --items 4 5 7 --dry-run
```

Observação: o script é idempotente no fluxo normal (executar lock ou unlock repetidamente não duplica alterações).

## `scripts/html_gen/`

Módulo principal do gerador:
- `cli.py`: orquestração
- `parser.py`: parse de markdown
- `renderer.py`: render em HTML
- `postprocessor.py`: regras globais pós-render
- `validation.py`: validações de segurança de conteúdo
- `icons.py`: mapeamento de ícones
- `classifier.py`: heurísticas de classificação de linhas
- `utils.py`: utilitários
- `constants.py`: constantes
- `models.py`: `Card` e tipos

## Comportamentos Importantes

- `index.html` na raiz do repositório é redirecionador para `html/index.html`.
- A landing (`html/index.html`) embute logos quando `html/logo.png` e `html/mppa.png` existem.
- Em páginas de tópico, links de CTA de agente Copilot são convertidos para botão estilizado.
- No build atual, seções vazias são descartadas automaticamente para evitar cards sem conteúdo.

## Publicação

```bash
git add conteudo/ html/ scripts/ templates/ README.md
git commit -m "Atualiza conteúdo e páginas geradas"
git push origin main
```

## Documentos Relacionados

- `AGENTS.md`
- `CLAUDE.md`
- `CODEX.md`
- `GEMINI.md`
- `scripts/html_gen/README.md`
