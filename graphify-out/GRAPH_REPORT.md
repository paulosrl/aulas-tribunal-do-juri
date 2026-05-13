# Graph Report - aulas-tribunal-do-juri  (2026-05-13)

## Corpus Check
- 2 files · ~55,381 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 83 nodes · 236 edges · 9 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `230ba1f1`
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
2. `parse_markdown()` - 23 edges
3. `parse_markdown()` - 21 edges
4. `clean_md_title()` - 15 edges
5. `clean_md_title()` - 15 edges
6. `main()` - 13 edges
7. `main()` - 13 edges
8. `esc()` - 9 edges
9. `derive_page_card_title()` - 8 edges
10. `render_cards()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `pick_agent_icon()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 7 → community 3_
- `parse_markdown()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 7 → community 4_
- `render_topics_accordion()` --calls--> `esc()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 7 → community 1_
- `extract_h1_title()` --calls--> `clean_md_title()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 1 → community 3_
- `parse_markdown()` --calls--> `parse_authors_line()`  [EXTRACTED]
  gera_html.py → gera_html.py  _Bridges community 3 → community 4_

## Communities (9 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.32
Nodes (12): apply_global_page_rules(), assign_unique_icons(), esc(), extract_h1_title(), inline_md(), main(), normalize_data_uri(), parse_args() (+4 more)

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (9): apply_global_page_rules(), assign_unique_icons(), extract_h1_title(), file_to_data_uri(), main(), parse_args(), render_topics_accordion(), replace_between() (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.42
Nodes (11): build_topico.py, Card, derive_page_card_title(), file_to_data_uri(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line() (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.31
Nodes (10): classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_icon(), pick_item_icon(), render_cards() (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (10): Card, derive_page_card_title(), extract_agent_access_url(), is_ocr_comment_line(), is_page_comment_line(), is_page_marker_line(), is_separator_line(), parse_markdown() (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.36
Nodes (7): generate_cards_html(), main(), parse_index_md(), Replace conteúdo entre dois marcadores, Parse index.md e extrai: título, metadados, tópicos, Gera HTML dos cards a partir dos tópicos, replace_between()

### Community 6 - "Community 6"
Cohesion: 0.36
Nodes (8): classify_critical_paragraph(), clean_md_title(), is_strategic_paragraph(), parse_authors_line(), parse_menu_md(), pick_item_icon(), render_cards(), strip_leading_number()

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (6): esc(), inline_md(), parse_agent_block(), pick_agent_icon(), render_copilot_agent_cta(), render_topics_menu()

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (6): generate_index_page(), Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html, Generate landing page with index.template.html

## Knowledge Gaps
- **8 isolated node(s):** `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores`, `Generate landing page with index.template.html`, `Generate landing page with index.template.html` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generate_index_page()` connect `Community 8` to `Community 1`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `build_topico.py` connect `Community 2` to `Community 0`, `Community 6`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `parse_markdown()` connect `Community 4` to `Community 1`, `Community 3`, `Community 7`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `Parse index.md e extrai: título, metadados, tópicos`, `Gera HTML dos cards a partir dos tópicos`, `Replace conteúdo entre dois marcadores` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._