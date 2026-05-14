from __future__ import annotations

import re


MENU_START = "<!-- AUTO:MENU:AULA1:START -->"
MENU_END = "<!-- AUTO:MENU:AULA1:END -->"
CONTENT_START = "<!-- AUTO:CONTENT:START -->"
CONTENT_END = "<!-- AUTO:CONTENT:END -->"
TOPICS_START = "<!-- AUTO:MENU:TOPICOS:START -->"
TOPICS_END = "<!-- AUTO:MENU:TOPICOS:END -->"

ICON_RULES = [
    (("introdu", "funda", "base", "conceito"), "fa-book-open"),
    (("contexto", "memória", "memoria", "janela", "token"), "fa-window-maximize"),
    (("engenharia", "pilar", "método", "metodo", "protocolo"), "fa-pencil-ruler"),
    (("alucina", "risco", "erro", "falha", "ponto cego"), "fa-exclamation-triangle"),
    (("segurança", "seguranca", "lgpd", "sigilo", "compliance"), "fa-shield-halved"),
    (("promotor", "júri", "juri", "juríd", "jurid"), "fa-gavel"),
    (("dados", "prova", "laudo", "documento", "autos"), "fa-database"),
    (("análise", "analise", "investiga", "diagnóstico", "diagnostico"), "fa-search"),
    (("checklist", "validação", "validacao", "verificação", "verificacao"), "fa-check-circle"),
    (("estratégia", "estrategia", "plano", "tática", "tatica"), "fa-bullseye"),
    (("fluxo", "processo", "pipeline", "etapa"), "fa-sync"),
    (("conclus", "síntese", "sintese", "resumo"), "fa-star"),
    (("alerta", "atenção", "atencao"), "fa-exclamation-circle"),
]

ICON_POOL = [
    "fa-book-open",
    "fa-window-maximize",
    "fa-pencil-ruler",
    "fa-exclamation-triangle",
    "fa-shield-halved",
    "fa-gavel",
    "fa-database",
    "fa-search",
    "fa-check-circle",
    "fa-bullseye",
    "fa-sync",
    "fa-star",
    "fa-brain",
    "fa-microscope",
    "fa-balance-scale",
    "fa-chart-line",
    "fa-handshake",
    "fa-fingerprint",
    "fa-network-wired",
    "fa-rocket",
]

AGENT_HEADER_PAT = re.compile(
    r"^\*\*(\d+)\\?\.\*\*[\s\t]+\*\*([^*]+)\*\*"
)

TOPIC_NAV_ITEMS: list[tuple[str, str, str]] = [
    ("Abertura", "1.html", "fa-book-open"),
    ("Engenharia de Prompts", "2.html", "fa-window-maximize"),
    ("Agentes no Júri", "3.html", "fa-gavel"),
    ("Elementos Gráficos no Júri", "4.html", "fa-chart-line"),
    ("NotebookLM no Júri", "5.html", "fa-pencil-ruler"),
    ("Favoritos", "6.html", "fa-star"),
    ("Notebooklm - Guia e Dicas", "7.html", "fa-brain"),
]

NUMBERED_TOPIC_PAGES = {item[1] for item in TOPIC_NAV_ITEMS}
