# Package html_gen

Módulos extraídos e reorganizados do script principal `gera_html.py`.

## Estrutura

```
html_gen/
├── __init__.py          # Export da API pública
├── constants.py         # Constantes globais (ICON_RULES, ICON_POOL, etc)
├── utils.py             # Funções utilitárias (clean_md_title)
├── models.py            # Dataclasses e re-exports de constantes
├── classifier.py        # Funções de classificação de linhas markdown
└── icons.py             # Funções de seleção e atribuição de ícones
```

## Módulos

### constants.py
Define constantes globais reutilizáveis:
- `ICON_RULES`: Tuplas (keywords, icon) para mapeamento automático de ícones
- `ICON_POOL`: Lista de 20 ícones FontAwesome disponíveis
- `AGENT_HEADER_PAT`: Regex para detectar cabeçalhos de agentes
- `TOPIC_NAV_ITEMS`: Itens de navegação lateral
- `NUMBERED_TOPIC_PAGES`: Conjunto de nomes de páginas numeradas

### utils.py
Utilitários de processamento de texto:
- `clean_md_title(text)`: Normaliza títulos markdown (remove **, escapes, espaços)

### models.py
Define estruturas de dados:
- `Card`: Dataclass com `title`, `level`, `blocks`

### classifier.py
Funções de classificação e detecção:
- `is_page_marker_line()`: Detecta marcadores de página
- `is_page_comment_line()`: Detecta comentários HTML de paginação
- `is_separator_line()`: Detecta separadores markdown
- `is_ocr_comment_line()`: Detecta comentários de OCR
- `classify_critical_paragraph()`: Identifica parágrafos críticos
- `is_strategic_paragraph()`: Detecta parágrafos estratégicos

### icons.py
Funções de mapeamento de ícones:
- `pick_agent_icon(name)`: Mapeia nome de agente para ícone
- `pick_icon(title, fallback)`: Mapeia título para ícone usando ICON_RULES
- `pick_item_icon(text)`: Mapeia item de lista para ícone
- `assign_unique_icons(cards, fallback)`: Deduplica ícones em cards

## Uso

```python
from scripts.html_gen import Card, pick_icon, is_page_marker_line

# Criar um card
card = Card(title="Introdução", level=2, blocks=["<p>Conteúdo</p>"])

# Escolher um ícone baseado no título
icon = pick_icon("Introdução")  # Retorna "fa-book-open"

# Verificar se uma linha é marcador de página
if is_page_marker_line(line):
    print("Marcador de página detectado")
```

## Importações

Todas as funções e classes estão disponíveis no `__init__.py`:

```python
# Importação centralizada
from scripts.html_gen import (
    Card,
    clean_md_title,
    pick_icon,
    pick_item_icon,
    assign_unique_icons,
    is_page_marker_line,
    classify_critical_paragraph,
)
```
