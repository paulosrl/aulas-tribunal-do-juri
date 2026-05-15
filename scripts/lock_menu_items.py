#!/usr/bin/env python3
"""Trava/destrava itens de menu e cards por número de tópico."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Optional, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES: List[Path] = [
    ROOT / "html/index.html",
    ROOT / "html/1.html",
    ROOT / "html/2.html",
    ROOT / "html/3.html",
    ROOT / "html/4.html",
    ROOT / "html/5.html",
    ROOT / "html/6.html",
    ROOT / "html/7.html",
]

LOCK_ICON = '<span class="codex-lock-emoji" aria-hidden="true">🔒</span> <i class="fas fa-lock codex-lock-icon" aria-hidden="true"></i>'

A_CARD_RE = re.compile(r"<a\b([^>]*)class=\"([^\"]*\bcard\b[^\"]*)\"([^>]*)>(.*?)</a>", re.DOTALL)
A_MENU_RE = re.compile(r"<a\b([^>]*)class=\"([^\"]*\bnav-l\b[^\"]*\bnav-topic-header\b[^\"]*)\"([^>]*)>(.*?)</a>", re.DOTALL)
SPAN_MENU_RE = re.compile(
    r"<span\b([^>]*)class=\"([^\"]*\bnav-l\b[^\"]*\bnav-topic-header\b[^\"]*)\"([^>]*)>"
    r"(.*?<span[^>]*class=\"[^\"]*\bnav-topic-num\b[^\"]*\"[^>]*>.*?</span>.*?"
    r"<i[^>]*class=\"[^\"]*\bnav-topic-chevron\b[^\"]*\"[^>]*></i>"
    r"(?:\s*<span class=\"codex-lock-emoji\" aria-hidden=\"true\">🔒</span>\s*"
    r"<i class=\"fas fa-lock codex-lock-icon\" aria-hidden=\"true\"></i>)?\s*)"
    r"</span>",
    re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Trava/destrava itens de menu e cards por número.")
    p.add_argument("--items", nargs="+", type=int, required=True)
    p.add_argument("--unlock", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--files", nargs="*")
    return p.parse_args()


def resolve_files(files_arg: Optional[Sequence[str]]) -> List[Path]:
    if not files_arg:
        return DEFAULT_FILES
    out = []
    for item in files_arg:
        p = Path(item)
        if not p.is_absolute():
            p = ROOT / p
        out.append(p.resolve())
    return out


def get_topic_num(html_fragment: str) -> Optional[int]:
    m_title = re.search(r"Tópico\s*(\d+)\s*\|", html_fragment, flags=re.IGNORECASE)
    if m_title:
        return int(m_title.group(1))
    m_num = re.search(r"<span[^>]*class=\"[^\"]*nav-topic-num[^\"]*\"[^>]*>\s*(\d+)\.", html_fragment)
    if m_num:
        return int(m_num.group(1))
    return None


def has_class(class_attr: str, cls: str) -> bool:
    return cls in class_attr.split()


def add_class(class_attr: str, cls: str) -> str:
    classes = class_attr.split()
    if cls not in classes:
        classes.append(cls)
    return " ".join(classes)


def remove_class(class_attr: str, cls: str) -> str:
    classes = [c for c in class_attr.split() if c != cls]
    return " ".join(classes)


def strip_lock_icon(inner_html: str) -> str:
    inner_html = re.sub(
        r"\s*<span class=\"codex-lock-emoji\" aria-hidden=\"true\">🔒</span>\s*<i class=\"fas fa-lock codex-lock-icon\" aria-hidden=\"true\"></i>",
        "",
        inner_html,
    )
    inner_html = re.sub(
        r"\s*<span class=\"codex-lock-emoji\" aria-hidden=\"true\">🔒</span>",
        "",
        inner_html,
    )
    inner_html = re.sub(
        r"\s*<i class=\"fas fa-lock codex-lock-icon\" aria-hidden=\"true\"></i>",
        "",
        inner_html,
    )
    return inner_html


def insert_lock_icon_in_card_title(inner_html: str) -> str:
    if "codex-lock-emoji" in inner_html:
        return inner_html
    if "codex-lock-icon" in inner_html:
        return inner_html.replace(
            '<i class="fas fa-lock codex-lock-icon" aria-hidden="true"></i>',
            LOCK_ICON,
            1,
        )
    return re.sub(
        r"(<div[^>]*class=\"[^\"]*title-row[^\"]*\"[^>]*>.*?</h2>)",
        r"\1 " + LOCK_ICON,
        inner_html,
        count=1,
        flags=re.DOTALL,
    )


def lock_attrs(tag_text: str) -> Tuple[str, bool]:
    changed = False

    m_class = re.search(r'class=\"([^\"]*)\"', tag_text)
    if m_class:
        old = m_class.group(1)
        new = add_class(old, "nav-locked")
        if new != old:
            tag_text = tag_text.replace(f'class="{old}"', f'class="{new}"', 1)
            changed = True

    if "aria-disabled=\"true\"" not in tag_text:
        tag_text = tag_text[:-1] + ' aria-disabled="true">'
        changed = True

    if "tabindex=\"-1\"" not in tag_text:
        tag_text = tag_text[:-1] + ' tabindex="-1">'
        changed = True

    if tag_text.startswith("<a"):
        m_href = re.search(r'\shref=\"([^\"]*)\"', tag_text)
        if m_href:
            href = m_href.group(1)
            if "data-href=" not in tag_text:
                tag_text = tag_text[:-1] + f' data-href="{href}">'
            tag_text = re.sub(r'\shref=\"[^\"]*\"', "", tag_text, count=1)
            changed = True

    return tag_text, changed


def unlock_attrs(tag_text: str) -> Tuple[str, bool]:
    changed = False

    m_class = re.search(r'class=\"([^\"]*)\"', tag_text)
    if m_class:
        old = m_class.group(1)
        new = remove_class(old, "nav-locked")
        if new != old:
            tag_text = tag_text.replace(f'class="{old}"', f'class="{new}"', 1)
            changed = True

    for patt in [r'\saria-disabled=\"true\"', r'\stabindex=\"-1\"']:
        new_tag = re.sub(patt, "", tag_text)
        if new_tag != tag_text:
            tag_text = new_tag
            changed = True

    if tag_text.startswith("<a"):
        m_data = re.search(r'\sdata-href=\"([^\"]*)\"', tag_text)
        has_href = re.search(r'\shref=\"([^\"]*)\"', tag_text) is not None
        if m_data and not has_href:
            href = m_data.group(1)
            tag_text = tag_text[:-1] + f' href="{href}">'
            changed = True
        new_tag = re.sub(r'\sdata-href=\"[^\"]*\"', "", tag_text)
        if new_tag != tag_text:
            tag_text = new_tag
            changed = True

    return tag_text, changed


def patch_match(full_match: str, unlock: bool) -> Tuple[str, bool]:
    tag_start = re.match(r"<(a|span)\b[^>]*>", full_match, flags=re.DOTALL)
    if not tag_start:
        return full_match, False
    start_tag = tag_start.group(0)
    end_tag = "</a>" if full_match.endswith("</a>") else "</span>"
    inner = full_match[len(start_tag):-len(end_tag)]

    changed = False
    if unlock:
        new_tag, c1 = unlock_attrs(start_tag)
        new_inner = strip_lock_icon(inner)
        c2 = new_inner != inner
        changed = c1 or c2
        return f"{new_tag}{new_inner}{end_tag}", changed

    new_tag, c1 = lock_attrs(start_tag)
    new_inner = inner
    if "codex-lock-icon" not in inner:
        if re.search(r'class=\"[^\"]*\bcard\b[^\"]*\"', start_tag):
            injected = insert_lock_icon_in_card_title(inner)
            new_inner = injected if injected != inner else (inner + " " + LOCK_ICON)
        else:
            if "nav-topic-chevron" in inner:
                new_inner = re.sub(
                    r"(\s*<i[^>]*class=\"[^\"]*\bnav-topic-chevron\b[^\"]*\"[^>]*></i>)",
                    " " + LOCK_ICON + r"\1",
                    inner,
                    count=1,
                )
            else:
                new_inner = inner + " " + LOCK_ICON
        changed = True
    elif "codex-lock-emoji" not in inner:
        new_inner = inner.replace(
            '<i class="fas fa-lock codex-lock-icon" aria-hidden="true"></i>',
            LOCK_ICON,
            1,
        )
        if new_inner != inner:
            changed = True
    changed = changed or c1
    return f"{new_tag}{new_inner}{end_tag}", changed


def apply_pattern(content: str, pattern: re.Pattern, items: Set[int], unlock: bool) -> Tuple[str, int]:
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        full = m.group(0)
        num = get_topic_num(full)
        if num is None or num not in items:
            return full
        new_full, changed = patch_match(full, unlock)
        if changed:
            changes += 1
        return new_full

    new_content = pattern.sub(repl, content)
    return new_content, changes


def process_file(path: Path, items: Set[int], unlock: bool, dry_run: bool) -> Tuple[int, int, bool]:
    if not path.exists():
        return 0, 0, False

    original = path.read_text(encoding="utf-8")
    content = original

    total_changed = 0
    for pattern in (A_CARD_RE, A_MENU_RE, SPAN_MENU_RE):
        content, ch = apply_pattern(content, pattern, items, unlock)
        total_changed += ch

    file_changed = content != original
    if file_changed and not dry_run:
        path.write_text(content, encoding="utf-8")

    return (0, total_changed, file_changed) if unlock else (total_changed, 0, file_changed)


def main() -> int:
    args = parse_args()
    items = set(args.items)
    files = resolve_files(args.files)

    mode = "UNLOCK" if args.unlock else "LOCK"

    total_locked = 0
    total_unlocked = 0
    touched = 0

    for fp in files:
        locked, unlocked, changed = process_file(fp, items, args.unlock, args.dry_run)
        total_locked += locked
        total_unlocked += unlocked
        if changed:
            touched += 1

    blocked_items = sorted(items) if not args.unlock else []
    unblocked_items = sorted(items) if args.unlock else []
    print(
        f"Resumo: modo={mode}, dry_run={args.dry_run}, "
        f"arquivos_alterados={touched}, itens_travados={total_locked}, itens_destravados={total_unlocked}, "
        f"itens_bloqueados={blocked_items}, itens_desbloqueados={unblocked_items}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
