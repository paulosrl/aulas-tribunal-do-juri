# Graph Report - aulas-tribunal-do-juri  (2026-05-14)

## Corpus Check
- 14 files · ~80,381 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 219 nodes · 464 edges · 8 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a6a011ca`
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
2. `parse_markdown()` - 24 edges
3. `parse_markdown()` - 23 edges
4. `parse_markdown()` - 21 edges
5. `main()` - 18 edges
6. `clean_md_title()` - 16 edges
7. `generate_index_page()` - 16 edges
8. `clean_md_title()` - 15 edges
9. `clean_md_title()` - 14 edges
10. `main()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `replace_between()`  [INFERRED]
  html_gen/cli.py → scripts/html_gen/utils.py
- `apply_global_page_rules()` --calls--> `esc()`  [INFERRED]
  html_gen/postprocessor.py → scripts/html_gen/utils.py
- `main()` --calls--> `assign_unique_icons()`  [INFERRED]
  html_gen/cli.py → scripts/html_gen/icons.py
- `generate_index_page()` --calls--> `esc()`  [INFERRED]
  html_gen/cli.py → scripts/html_gen/utils.py
- `generate_index_page()` --calls--> `safe_href()`  [INFERRED]
  html_gen/cli.py → scripts/html_gen/utils.py

## Communities (8 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (44): classify_critical_paragraph(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), is_strategic_paragraph(), assign_unique_icons(), pick_agent_icon() (+36 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (42): apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc(), extract_agent_access_url() (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.23
Nodes (31): build_topico.py, apply_global_page_rules(), assign_unique_icons(), Card, classify_critical_paragraph(), clean_md_title(), derive_page_card_title(), esc() (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (23): build_html(), discover_markdown_files(), get_project_root(), main(), parse_args(), print_header(), print_summary(), Imprime sumário final (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (21): _card_has_meaningful_content(), generate_index_page(), main(), parse_args(), Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation., Main entry point: orchestrates parsing, rendering, and validation. (+13 more)

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
- **64 isolated node(s):** `Retorna a raiz do projeto (onde está conteudo/ e html/)`, `Descobre todos os .md em conteudo/ e ordena logicamente`, `Executa gera_html.py para um arquivo markdown     Retorna True se bem-sucedido,`, `Imprime cabeçalho visual`, `Imprime sumário final` (+59 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `parse_markdown()` connect `Community 0` to `Community 4`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `main()` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `generate_index_page()` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `parse_markdown()` (e.g. with `main()` and `is_page_comment_line()`) actually correct?**
  _`parse_markdown()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `main()` (e.g. with `parse_markdown()` and `assign_unique_icons()`) actually correct?**
  _`main()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Retorna a raiz do projeto (onde está conteudo/ e html/)`, `Descobre todos os .md em conteudo/ e ordena logicamente`, `Executa gera_html.py para um arquivo markdown     Retorna True se bem-sucedido,` to the rest of the system?**
  _64 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._