from __future__ import annotations

from dataclasses import dataclass
from html import escape
import re

from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


HEADING_SLUG_RE = re.compile(r"[^a-z0-9]+")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")

_formatter = HtmlFormatter(nowrap=True)


@dataclass
class Heading:
    level: int
    text: str
    slug: str


@dataclass
class RenderedPage:
    html: str
    headings: list[Heading]
    title: str
    summary: str


def slugify(value: str) -> str:
    slug = HEADING_SLUG_RE.sub("-", value.lower()).strip("-")
    return slug or "section"


def render_inline(text: str) -> str:
    escaped = escape(text)
    escaped = LINK_RE.sub(lambda m: f'<a href="{escape(m.group(2), quote=True)}">{m.group(1)}</a>', escaped)
    escaped = INLINE_CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", escaped)
    escaped = BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", escaped)
    escaped = ITALIC_RE.sub(lambda m: f"<em>{m.group(1)}</em>", escaped)
    return escaped


def summarize(lines: list[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            if len(stripped) <= 180:
                return stripped
            trimmed = stripped[:177].rsplit(" ", 1)[0].rstrip(" ,.")
            return f"{trimmed}..."
    return ""


def highlight_code(language: str, code: str) -> str:
    lang = language.strip().lower()
    if not lang:
        return escape(code)
    try:
        lexer = get_lexer_by_name(lang, stripnl=False)
        return pygments_highlight(code, lexer, _formatter).rstrip("\n")
    except ClassNotFound:
        return escape(code)


def render_code_block(language: str, code_lines: list[str]) -> str:
    raw_code = "\n".join(code_lines)
    code_html = highlight_code(language, raw_code)
    language_value = language.strip()
    language_class = f' class="language-{escape(language_value, quote=True)}"' if language_value else ""
    language_badge = escape(language_value) if language_value else "text"
    return (
        '<div class="code-block">'
        '<div class="code-block-header">'
        f'<span class="code-block-language">{language_badge}</span>'
        '<button class="code-copy-button" type="button" data-code-copy>Copy</button>'
        "</div>"
        f'<pre class="highlight"><code{language_class}>{code_html}</code></pre>'
        "</div>"
    )


def render_markdown(text: str) -> RenderedPage:
    lines = text.splitlines()
    headings: list[Heading] = []
    blocks: list[str] = []
    paragraph: list[str] = []
    list_buffer: list[str] = []
    list_kind: str | None = None
    in_code = False
    code_language = ""
    code_lines: list[str] = []
    title = "Untitled"
    primary_heading_rendered = False
    slug_counts: dict[str, int] = {}

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{render_inline(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_buffer, list_kind
        if list_buffer and list_kind:
            inner = "".join(f"<li>{render_inline(item)}</li>" for item in list_buffer)
            blocks.append(f"<{list_kind}>{inner}</{list_kind}>")
        list_buffer = []
        list_kind = None

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code:
                blocks.append(render_code_block(code_language, code_lines))
                code_lines = []
                code_language = ""
                in_code = False
            else:
                in_code = True
                code_language = stripped.removeprefix("```").strip()
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        if stripped == "---":
            flush_paragraph()
            flush_list()
            blocks.append("<hr />")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<blockquote>{render_inline(stripped[2:])}</blockquote>")
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            flush_list()
            level = len(heading_match.group(1))
            text_value = heading_match.group(2).strip()
            base_slug = slugify(text_value)
            count = slug_counts.get(base_slug, 0)
            slug_counts[base_slug] = count + 1
            slug = base_slug if count == 0 else f"{base_slug}-{count}"
            headings.append(Heading(level=level, text=text_value, slug=slug))
            if title == "Untitled" and level == 1:
                title = text_value
                if not primary_heading_rendered:
                    primary_heading_rendered = True
                    continue
            blocks.append(f'<h{level} id="{slug}">{render_inline(text_value)}</h{level}>')
            continue

        unordered_match = re.match(r"^[-*]\s+(.*)$", stripped)
        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if unordered_match:
            flush_paragraph()
            if list_kind not in (None, "ul"):
                flush_list()
            list_kind = "ul"
            list_buffer.append(unordered_match.group(1))
            continue
        if ordered_match:
            flush_paragraph()
            if list_kind not in (None, "ol"):
                flush_list()
            list_kind = "ol"
            list_buffer.append(ordered_match.group(1))
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_list()

    if in_code:
        blocks.append(render_code_block(code_language, code_lines))

    return RenderedPage(
        html="\n".join(blocks),
        headings=headings,
        title=title,
        summary=summarize(lines),
    )
