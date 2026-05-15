# Graph Report - aulas-tribunal-do-juri  (2026-05-15)

## Corpus Check
- 14 files · ~87,923 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 238 nodes · 492 edges · 8 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1d018250`
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
- [[_COMMUNITY_Community 7|Community 7]]

## God Nodes (most connected - your core abstractions)
1. `build_topico.py` - 30 edges
2. `parse_markdown()` - 25 edges
3. `parse_markdown()` - 23 edges
4. `main()` - 22 edges
5. `parse_markdown()` - 21 edges
6. `clean_md_title()` - 16 edges
7. `generate_index_page()` - 16 edges
8. `clean_md_title()` - 15 edges
9. `clean_md_title()` - 14 edges
10. `main()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Imprime cabeçalho visual` --rationale_for--> `print_header()`  [EXTRACTED]
  build_all.py → scripts/build_all.py
- `Imprime sumário final` --rationale_for--> `print_summary()`  [EXTRACTED]
  build_all.py → scripts/build_all.py
- `render_copilot_agent_cta()` --calls--> `safe_href()`  [INFERRED]
  scripts/html_gen/renderer.py → scripts/html_gen/utils.py
- `main()` --calls--> `replace_between()`  [INFERRED]
  scripts/html_gen/cli.py → scripts/html_gen/utils.py
- `Convert markdown inline formatting to HTML.` --rationale_for--> `inline_md()`  [EXTRACTED]
  html_gen/renderer.py → scripts/html_gen/renderer.py

## Communities (8 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (38): classify_critical_paragraph(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), is_strategic_paragraph(), assign_unique_icons(), pick_agent_icon() (+30 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (42): apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc(), extract_agent_access_url() (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (37): append_generation_log(), _card_has_meaningful_content(), generate_index_page(), main(), parse_args(), Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation. (+29 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (32): build_html(), build_page_title(), discover_markdown_files(), extract_h1_from_markdown(), get_project_root(), main(), parse_args(), print_header() (+24 more)

### Community 4 - "Community 4"
Cohesion: 0.23
Nodes (31): build_topico.py, apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc() (+23 more)

### Community 5 - "Community 5"
Cohesion: 0.23
Nodes (12): add_class(), apply_pattern(), insert_lock_icon_in_card_title(), lock_attrs(), main(), parse_args(), patch_match(), process_file() (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (14): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.23
Nodes (11): generate_cards_html(), main(), parse_index_md(), Gera HTML dos cards a partir dos tópicos, Replace conteúdo entre dois marcadores, Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Parse index.md e extrai: título, metadados, tópicos (+3 more)

## Knowledge Gaps
- **79 isolated node(s):** `Extrai o primeiro H1 do arquivo markdown.     Retorna texto sem '#' e espaços ex`, `Constrói o título completo da página.     Padrão: "Inteligência Artificial Aplic`, `Retorna a raiz do projeto (onde está conteudo/ e html/)`, `Descobre todos os .md em conteudo/ e ordena logicamente`, `Executa gera_html.py para um arquivo markdown     Retorna True se bem-sucedido,` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `parse_markdown()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `generate_index_page()` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `parse_markdown()` (e.g. with `main()` and `is_page_comment_line()`) actually correct?**
  _`parse_markdown()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `main()` (e.g. with `parse_markdown()` and `assign_unique_icons()`) actually correct?**
  _`main()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Extrai o primeiro H1 do arquivo markdown.     Retorna texto sem '#' e espaços ex`, `Constrói o título completo da página.     Padrão: "Inteligência Artificial Aplic`, `Retorna a raiz do projeto (onde está conteudo/ e html/)` to the rest of the system?**
  _79 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._