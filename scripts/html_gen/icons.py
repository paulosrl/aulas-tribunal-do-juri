from __future__ import annotations

from typing import List
from .constants import ICON_RULES, ICON_POOL
from .utils import clean_md_title


def pick_agent_icon(name: str) -> str:
    name_lower = clean_md_title(name).lower()
    if any(k in name_lower for k in ("investiga", "analista")):
        return "fa-search"
    if any(k in name_lower for k in ("denúncia", "denuncia")):
        return "fa-gavel"
    if any(k in name_lower for k in ("diligência", "diligencia")):
        return "fa-tasks"
    if "arquivamento" in name_lower:
        return "fa-database"
    if any(k in name_lower for k in ("prisão", "prisao", "revogação", "revogacao")):
        return "fa-lock"
    if any(k in name_lower for k in ("laudo", "pericial")):
        return "fa-microscope"
    if any(k in name_lower for k in ("depoimento", "incoerência", "incoerencia")):
        return "fa-eye-slash"
    if any(k in name_lower for k in ("tese", "defensiva", "antecipação", "antecipacao")):
        return "fa-shield-halved"
    if any(k in name_lower for k in ("firac", "jurídica", "juridica")):
        return "fa-balance-scale"
    if any(k in name_lower for k in ("audiência", "audiencia", "perguntas")):
        return "fa-calendar-alt"
    if any(k in name_lower for k in ("cross", "interrogatório", "interrogatorio")):
        return "fa-user-tie"
    if any(k in name_lower for k in ("advogado", "diabo")):
        return "fa-user-secret"
    if any(k in name_lower for k in ("alegação", "alegacao", "memorial")):
        return "fa-tasks"
    if "embargo" in name_lower:
        return "fa-exclamation-circle"
    if any(k in name_lower for k in ("razões", "razoes", "recursal")):
        return "fa-level-up-alt"
    if any(k in name_lower for k in ("contrarrazões", "contrarrazoes")):
        return "fa-users-slash"
    if "roteiro" in name_lower:
        return "fa-list-ol"
    if any(k in name_lower for k in ("sustentação", "sustentacao", "oral")):
        return "fa-play-circle"
    if any(k in name_lower for k in ("quesitação", "quesitacao", "quesito")):
        return "fa-check-circle"
    if "dashboard" in name_lower:
        return "fa-chart-line"
    return "fa-bolt"


def pick_icon(title: str, fallback: str = "fa-list-ol") -> str:
    t = clean_md_title(title).lower()
    for keywords, icon in ICON_RULES:
        if any(k in t for k in keywords):
            return icon
    return fallback


def pick_item_icon(text: str) -> str:
    # Se o item contém uma URL, usa ícone de link externo
    if "http" in text.lower() or "claude.ai" in text.lower():
        return "fa-link"

    t = clean_md_title(text).lower()
    rules = [
        (("promotor", "juiz", "decid"), "fa-gavel"),
        (("performance", "desempenho", "velocidade"), "fa-rocket"),
        (("curadoria", "seleção", "selecao"), "fa-bolt"),
        (("segurança", "seguranca", "lgpd", "sigilo"), "fa-shield-halved"),
        (("risco", "erro", "falha", "alucina"), "fa-exclamation-triangle"),
        (("verificar", "validar", "chec", "auditoria"), "fa-check-circle"),
        (("dados", "prova", "laudo", "autos"), "fa-database"),
        (("estratégia", "estrategia", "plano", "tática", "tatica"), "fa-bullseye"),
        (("contexto", "janela", "memória", "memoria", "token"), "fa-window-maximize"),
        (("processamento", "operacional", "organização", "organizacao"), "fa-cog"),
    ]
    for keywords, icon in rules:
        if any(k in t for k in keywords):
            return icon
    return "fa-check-circle"


def assign_unique_icons(cards: List, fallback: str) -> List[str]:
    used: set[str] = set()
    assigned: List[str] = []
    for card in cards:
        preferred = pick_icon(card.title, fallback)
        if preferred not in used:
            selected = preferred
        else:
            selected = next((icon for icon in ICON_POOL if icon not in used), fallback)
        assigned.append(selected)
        used.add(selected)
    return assigned
