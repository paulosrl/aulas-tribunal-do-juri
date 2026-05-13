from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List
from .constants import ICON_RULES, ICON_POOL, AGENT_HEADER_PAT, TOPIC_NAV_ITEMS, NUMBERED_TOPIC_PAGES


@dataclass
class Card:
    title: str
    level: int = 2
    blocks: List[str] = field(default_factory=list)


# Re-export constants
__all__ = [
    "Card",
    "ICON_RULES",
    "ICON_POOL",
    "AGENT_HEADER_PAT",
    "TOPIC_NAV_ITEMS",
    "NUMBERED_TOPIC_PAGES",
]
