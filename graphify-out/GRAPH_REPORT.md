# Graph Report - aulas-tribunal-do-juri  (2026-05-13)

## Corpus Check
- 2 files · ~49,177 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 79 nodes · 229 edges · 9 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `90ebe9d0`
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
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `build_topico.py` - 30 edges
2. `parse_markdown()` - 22 edges
3. `parse_markdown()` - 21 edges
4. `clean_md_title()` - 15 edges
5. `clean_md_title()` - 15 edges
6. `main()` - 13 edges
7. `main()` - 13 edges
8. `esc()` - 8 edges
9. `derive_page_card_title()` - 8 edges
10. `render_cards()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `pick_agent_icon()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 6 → community 5_
- `parse_markdown()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 6 → community 1_
- `extract_h1_title()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 7 → community 5_
- `parse_markdown()` --calls--> `parse_authors_line()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 5 → community 1_
- `parse_markdown()` --calls--> `pick_icon()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 7 → community 1_

## Communities (9 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.27
Nodes (14): build_topico.py, apply_global_page_rules(), assign_unique_icons(), Card, esc(), extract_h1_title(), main(), normalize_data_uri() (+6 more)

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (11): Card, derive_page_card_title(), extract_agent_access_url(), file_to_data_uri(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line() (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.53
Nodes (8): derive_page_card_title(), file_to_data_uri(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), parse_markdown(), split_key_value_item()

### Community 3 - "Community 3"
Cohesion: 0.31
Nodes (9): classify_critical_paragraph(), clean_md_title(), inline_md(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_item_icon(), render_cards() (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.36
Nodes (7): generate_cards_html(), main(), parse_index_md(), Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Gera HTML dos cards a partir dos tópicos, replace_between()

### Community 5 - "Community 5"
Cohesion: 0.36
Nodes (8): classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_item_icon(), render_cards(), strip_leading_number()

### Community 6 - "Community 6"
Cohesion: 0.32
Nodes (8): apply_global_page_rules(), esc(), inline_md(), parse_agent_block(), pick_agent_icon(), render_menu_from_labels(), render_topics_accordion(), render_topics_menu()

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (7): assign_unique_icons(), extract_h1_title(), main(), parse_args(), pick_icon(), replace_between(), validate_completeness()

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (3): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html

## Knowledge Gaps
- **5 isolated node(s):** `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores`, `Generate landing page with index.template.html`, `Generate landing page with index.template.html`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_topico.py` connect `Community 0` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `parse_markdown()` connect `Community 1` to `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `generate_index_page()` connect `Community 8` to `Community 1`, `Community 7`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._