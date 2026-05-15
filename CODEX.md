# CODEX.md

Memória operacional curta do projeto.

## Estado Atual

- Entrada de conteúdo: `conteudo/index.md` e `conteudo/1.md` ... `conteudo/7.md`.
- Saídas: `html/index.html` e `html/1.html` ... `html/7.html`.
- Templates: `templates/index.template.html` e `templates/topico.template.html`.
- Pipeline principal: `scripts/html_gen/*` (via `scripts/gera_html.py`).
- Log de geração: `loggerador.md` (página, data/hora e SHA-256).

## Comandos de Trabalho

Build completo:

```bash
python3 scripts/build_all.py
```

Build unitário:

```bash
python3 scripts/gera_html.py conteudo/N.md html/N.html --template templates/topico.template.html --page-title "<titulo>" --section-mode semantic
```

Lock/unlock de menu:

```bash
python3 scripts/lock_menu_items.py --items 4 5 7
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock
```

Conferir log:

```bash
sed -n '1,40p' loggerador.md
```

## Regras Visuais Atuais

- Tema claro: menu em `#8A1F3A`.
- Tema escuro: destaques principais em `#fbd246`.
- Subitens:
  - claro em `#8A1F3A`
  - escuro em branco
- Ícones dos subitens mantêm paleta própria.

## Regras de Segurança de Edição

- Não remover marcadores `<!-- AUTO:* -->` dos templates.
- Sincronizar mudanças de estilo entre template e `postprocessor.py`.
- Após alterar Python: `graphify update .`.

## Pente-fino Rápido

```bash
python3 -m py_compile scripts/build_all.py scripts/gera_html.py scripts/lock_menu_items.py scripts/html_gen/*.py
python3 scripts/build_all.py
python3 scripts/lock_menu_items.py --items 4 5 7 --dry-run
python3 scripts/lock_menu_items.py --items 4 5 7 --unlock --dry-run
```
