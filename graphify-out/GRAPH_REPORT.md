# Graph Report - aulas-tribunal-do-juri  (2026-05-13)

## Corpus Check
- 13 files · ~74,890 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 188 nodes · 420 edges · 7 communities detected
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e1df9124`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `build_topico.py` - 30 edges
2. `parse_markdown()` - 24 edges
3. `parse_markdown()` - 23 edges
4. `parse_markdown()` - 21 edges
5. `clean_md_title()` - 16 edges
6. `generate_index_page()` - 16 edges
7. `clean_md_title()` - 15 edges
8. `clean_md_title()` - 14 edges
9. `main()` - 14 edges
10. `main()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `render_copilot_agent_cta()` --calls--> `safe_href()`  [INFERRED]
  scripts/html_gen/renderer.py → scripts/html_gen/utils.py
- `main()` --calls--> `replace_between()`  [INFERRED]
  scripts/html_gen/cli.py → scripts/html_gen/utils.py
- `render_topics_menu()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py
- `Regra absoluta: o HTML não pode perder conteúdo relevante do markdown.     Faz v` --rationale_for--> `validate_content_preservation()`  [EXTRACTED]
  gera_html.py → scripts/gera_html.py

## Communities (7 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (38): classify_critical_paragraph(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), is_strategic_paragraph(), assign_unique_icons(), pick_agent_icon() (+30 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (42): apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc(), extract_agent_access_url() (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.23
Nodes (31): build_topico.py, apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc() (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (20): generate_index_page(), main(), parse_args(), Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation., Parse command-line arguments for the HTML generator., Generate landing page with index.template.html, Generate landing page with index.template.html (+12 more)

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (14): build_html(), discover_markdown_files(), get_project_root(), main(), print_header(), print_summary(), Imprime sumário final, Imprime sumário final (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.14
Nodes (14): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html (+6 more)

### Community 6 - "Community 6"
Cohesion: 0.23
Nodes (11): generate_cards_html(), main(), parse_index_md(), Gera HTML dos cards a partir dos tópicos, Replace conteúdo entre dois marcadores, Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Parse index.md e extrai: título, metadados, tópicos (+3 more)

## Knowledge Gaps
- **52 isolated node(s):** `Retorna a raiz do projeto (onde está conteudo/ e html/)`, `Descobre todos os .md em conteudo/ e ordena logicamente`, `Executa gera_html.py para um arquivo markdown     Retorna True se bem-sucedido,`, `Imprime cabeçalho visual`, `Imprime sumário final` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `parse_markdown()` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `main()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `generate_index_page()` connect `Community 5` to `Community 1`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `parse_markdown()` (e.g. with `main()` and `is_page_comment_line()`) actually correct?**
  _`parse_markdown()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Retorna a raiz do projeto (onde está conteudo/ e html/)`, `Descobre todos os .md em conteudo/ e ordena logicamente`, `Executa gera_html.py para um arquivo markdown     Retorna True se bem-sucedido,` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._