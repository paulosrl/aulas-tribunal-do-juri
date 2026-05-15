# html_gen

Pacote principal de transformação `Markdown -> HTML` das páginas de tópico.

## Módulos

- `cli.py`: ponto de entrada da pipeline.
- `parser.py`: parsing de markdown e montagem de seções/cards.
- `renderer.py`: render de conteúdo e navegação.
- `postprocessor.py`: ajustes finais de HTML/CSS/JS e componentes visuais.
- `validation.py`: validações de completude e preservação de texto.
- `icons.py`: seleção e deduplicação de ícones.
- `classifier.py`: heurísticas para classificação de linhas/blocos.
- `utils.py`: escaping, replace entre marcadores e helpers.
- `constants.py`: marcadores e constantes compartilhadas.
- `models.py`: dataclasses (`Card`).

## Fluxo

1. `parse_markdown()`
2. remoção de cards vazios
3. `assign_unique_icons()`
4. `render_cards()` e render do menu/sumário
5. `apply_global_page_rules()`
6. `validate_completeness()` e `validate_content_preservation()`

## Observações

- `scripts/gera_html.py` é wrapper fino para `html_gen.cli.main`.
- As regras visuais críticas ficam em `templates/topico.template.html` e `postprocessor.py`.
- Alterações de estilo devem manter template e pós-processador alinhados.
- `cli.py` registra cada página gerada em `loggerador.md` com data/hora e hash SHA-256.
