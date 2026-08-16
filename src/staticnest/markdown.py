from __future__ import annotations

from dataclasses import dataclass
from html import escape, unescape
import re

import markdown
from pymdownx import emoji
from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


HEADING_SLUG_RE = re.compile(r"[^a-z0-9]+")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
CARD_ATTR_RE = re.compile(r'(\w+)="([^"]*)"')
CODEHILITE_BLOCK_RE = re.compile(
    r'<div class="(?P<class>[^"]*\bcodehilite\b[^"]*)">(?P<body>\s*(?:<span class="filename">.*?</span>\s*)?<pre>.*?</pre>\s*)</div>',
    re.DOTALL,
)
CODE_INNER_RE = re.compile(r"<code[^>]*>(?P<code>.*?)</code>", re.DOTALL)
FILENAME_RE = re.compile(r'<span class="filename">(?P<name>.*?)</span>', re.DOTALL)
HTML_TAG_RE = re.compile(r"<[^>]+>")
HEADING_HTML_RE = re.compile(r'<h(?P<level>[2-6]) id="(?P<id>[^"]+)">(?P<body>.*?)</h(?P=level)>', re.DOTALL)
FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>.*)$")

_formatter = HtmlFormatter(nowrap=True)

MARKDOWN_EXTENSIONS = [
    "abbr",
    "admonition",
    "attr_list",
    "def_list",
    "footnotes",
    "md_in_html",
    "tables",
    "toc",
    "pymdownx.details",
    "pymdownx.emoji",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.superfences",
    "pymdownx.blocks.caption",
    "pymdownx.blocks.details",
    "pymdownx.blocks.tab",
    "pymdownx.tasklist",
    "pymdownx.tilde",
]

MARKDOWN_EXTENSION_CONFIGS = {
    "toc": {
        "slugify": lambda value, _separator: slugify(value),
        "separator": "-",
    },
    "pymdownx.highlight": {
        "use_pygments": True,
        "css_class": "codehilite",
        "pygments_lang_class": True,
    },
    "pymdownx.superfences": {
        "preserve_tabs": True,
    },
    "pymdownx.tasklist": {
        "custom_checkbox": True,
    },
    "pymdownx.emoji": {
        "emoji_index": emoji.gemoji,
        "emoji_generator": emoji.to_alt,
    },
}


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


def parse_fence(line: str) -> tuple[str, str] | None:
    match = FENCE_RE.match(line.strip())
    if not match:
        return None
    return match.group("fence"), match.group("info").strip()


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
        if stripped.startswith((":::", "::")):
            continue
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
    if language.strip().lower() == "mermaid":
        return render_mermaid_block(raw_code)
    code_html = highlight_code(language, raw_code)
    language_value = language.strip()
    language_class = f' class="language-{escape(language_value, quote=True)}"' if language_value else ""
    language_badge = escape(language_value) if language_value else "text"
    return (
        '<div class="code-block">'
        '<div class="code-block-header">'
        f'<span class="code-block-language">{language_badge}</span>'
        '<button class="code-copy-button" type="button" data-code-copy aria-label="Copy code">'
        '<svg class="code-copy-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="11" height="11" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1"></path></svg>'
        '<svg class="code-check-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>'
        "</button>"
        "</div>"
        f'<div class="codehilite"><pre class="highlight"><code{language_class}>{code_html}</code></pre></div>'
        "</div>"
    )


def render_code_block_shell(language: str, codehilite_html: str, title: str = "") -> str:
    if language.strip().lower() == "mermaid":
        return render_mermaid_block(extract_code_text(codehilite_html))
    language_badge = escape(language or "text")
    title_html = f'<span class="code-block-title">{title}</span>' if title else ""
    return (
        '<div class="code-block">'
        '<div class="code-block-header">'
        f'<span class="code-block-meta"><span class="code-block-language">{language_badge}</span>{title_html}</span>'
        '<button class="code-copy-button" type="button" data-code-copy aria-label="Copy code">'
        '<svg class="code-copy-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="11" height="11" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1"></path></svg>'
        '<svg class="code-check-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>'
        "</button>"
        "</div>"
        f"{codehilite_html}"
        "</div>"
    )


def extract_code_text(html: str) -> str:
    match = CODE_INNER_RE.search(html)
    code_html = match.group("code") if match else html
    return unescape(HTML_TAG_RE.sub("", code_html)).strip()


def render_mermaid_block(code: str) -> str:
    return f'<div class="mermaid-block"><div class="mermaid">{escape(code.strip())}</div></div>'


def wrap_codehilite_blocks(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        class_value = match.group("class")
        body = match.group("body")
        language_match = re.search(r"\blanguage-([^\s\"]+)", class_value)
        language = language_match.group(1) if language_match else "text"
        filename_match = FILENAME_RE.search(body)
        filename = unescape(HTML_TAG_RE.sub("", filename_match.group("name"))) if filename_match else ""
        body = FILENAME_RE.sub("", body)
        return render_code_block_shell(
            language,
            f'<div class="{class_value}">{body}</div>',
            escape(filename),
        )

    return CODEHILITE_BLOCK_RE.sub(replace, html)


def add_heading_copy_links(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        level = match.group("level")
        heading_id = match.group("id")
        body = match.group("body")
        escaped_id = escape(heading_id, quote=True)
        return (
            f'<h{level} id="{escaped_id}" class="heading-with-anchor">{body}'
            f'<button class="heading-anchor" type="button" data-heading-anchor="{escaped_id}" '
            'aria-label="Copy section link" title="Copy section link">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>'
            "</button>"
            f"</h{level}>"
        )

    return HEADING_HTML_RE.sub(replace, html)


def close_unclosed_fence(text: str) -> str:
    open_fence: str | None = None
    for line in text.splitlines():
        fence_info = parse_fence(line)
        if not fence_info:
            continue
        fence, info = fence_info
        if open_fence is None:
            open_fence = fence
        elif not info and fence == open_fence:
            open_fence = None
    if open_fence is None:
        return text
    return f"{text}\n{open_fence}"


def parse_card_attrs(value: str) -> dict[str, str]:
    return {match.group(1): match.group(2) for match in CARD_ATTR_RE.finditer(value)}


def render_card(attrs: dict[str, str], body_lines: list[str] | None = None) -> str:
    body_lines = body_lines or []
    title = attrs.get("title", "").strip()
    href = attrs.get("href", "").strip()
    icon = attrs.get("icon", "").strip()
    description = attrs.get("description", "").strip()
    body = " ".join(line.strip() for line in body_lines if line.strip()).strip()
    tag = "a" if href else "div"
    href_attr = f' href="{escape(href, quote=True)}"' if href else ""
    target_attr = ' target="_blank" rel="noreferrer"' if href.startswith(("http://", "https://")) else ""
    icon_html = f'<span class="card-icon">{render_inline(icon)}</span>' if icon else ""
    title_html = f'<h3 class="card-title">{render_inline(title)}</h3>' if title else ""
    description_text = description or body
    description_html = f'<p class="card-description">{render_inline(description_text)}</p>' if description_text else ""
    return f'<{tag} class="card"{href_attr}{target_attr}>{icon_html}{title_html}{description_html}</{tag}>'


def render_cards(lines: list[str]) -> str:
    cards = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("::card"):
            cards.append(render_card(parse_card_attrs(stripped.removeprefix("::card").strip())))
    return f'<div class="cards">{"".join(cards)}</div>'


def render_badge(attrs: dict[str, str]) -> str:
    label = attrs.get("label", "").strip()
    tone = attrs.get("tone", attrs.get("type", "default")).strip().lower()
    if tone not in {"default", "info", "success", "warning", "danger"}:
        tone = "default"
    if not label:
        return ""
    return f'<span class="badge badge-{tone}">{render_inline(label)}</span>'


def render_badges(lines: list[str]) -> str:
    badges = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("::badge"):
            badges.append(render_badge(parse_card_attrs(stripped.removeprefix("::badge").strip())))
    return f'<div class="badges">{"".join(badges)}</div>'


def render_rich_text(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip()).strip()
    return render_inline(text) if text else ""


CALLOUT_ICONS = {
    "info": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>',
    "note": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 15a4 4 0 0 1-4 4H7l-4 4V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"></path><path d="M12 7v5"></path><path d="M12 16h.01"></path></svg>',
    "success": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M8.5 14.5A6 6 0 1 1 15.5 14.5c-.9.7-1.5 1.7-1.5 2.5h-4c0-.8-.6-1.8-1.5-2.5z"></path></svg>',
    "warning": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><path d="M12 9v4"></path><path d="M12 17h.01"></path></svg>',
    "danger": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 3 7v6c0 5 3.8 9 9 9s9-4 9-9V7l-9-5z"></path><path d="M12 8v5"></path><path d="M12 17h.01"></path></svg>',
}


def render_callout(attrs: dict[str, str], body_lines: list[str]) -> str:
    callout_type = attrs.get("type", "info").strip().lower()
    if callout_type in {"error", "danger"}:
        callout_type = "danger"
    elif callout_type == "warn":
        callout_type = "warning"
    elif callout_type not in {"info", "note", "warning", "success"}:
        callout_type = "info"
    title = attrs.get("title", "").strip()
    title_html = f'<p class="callout-title admonition-title">{render_inline(title)}</p>' if title else ""
    body_html = render_rich_text(body_lines)
    description_html = f'<p class="callout-description">{body_html}</p>' if body_html else ""
    icon_html = f'<span class="callout-icon">{CALLOUT_ICONS[callout_type]}</span>'
    return (
        f'<div class="callout callout-{callout_type} admonition {callout_type}">'
        f"{icon_html}"
        f'<div class="callout-content">{title_html}{description_html}</div>'
        "</div>"
    )


def render_files(lines: list[str]) -> str:
    rows: list[str] = []
    previous_depth = 0
    open_folders = 0

    def close_to_depth(depth: int) -> None:
        nonlocal open_folders, previous_depth
        while open_folders > depth:
            rows.append("</div></details>")
            open_folders -= 1
        previous_depth = depth

    for line in lines:
        raw = line.rstrip()
        if not raw.strip():
            continue
        marker_index = max(raw.find("├──"), raw.find("└──"))
        if marker_index >= 0:
            depth = marker_index // 4
            name = raw[marker_index + 3 :].strip()
        else:
            leading_spaces = len(raw) - len(raw.lstrip(" "))
            depth = leading_spaces // 4
            name = raw.strip()

        is_folder = name.endswith("/")
        display_name = name.rstrip("/")
        if is_folder:
            close_to_depth(depth)
            open_attr = " open" if depth == 0 else ""
            rows.append(
                f'<details class="file-tree-folder" data-depth="{depth}"{open_attr}>'
                f'<summary class="file-tree-row file-tree-folder-row" style="--file-depth:{depth}">'
                '<span class="file-tree-icon file-tree-folder-icon" aria-hidden="true"></span>'
                f'<span>{escape(display_name)}</span></summary><div class="file-tree-children">'
            )
            open_folders += 1
            previous_depth = depth + 1
        else:
            close_to_depth(min(depth, open_folders))
            rows.append(
                f'<div class="file-tree-row file-tree-file-row" style="--file-depth:{depth}">'
                '<span class="file-tree-icon file-tree-file-icon" aria-hidden="true"></span>'
                f'<span>{escape(display_name)}</span></div>'
            )
            previous_depth = depth

    close_to_depth(0)
    return f'<div class="files file-tree">{"".join(rows)}</div>'


def render_tabs(tabs: list[tuple[str, list[str]]]) -> str:
    if not tabs:
        return ""
    tab_seed = "-".join(title for title, _lines in tabs)
    tab_id = f"tabs-{sum(ord(char) for char in tab_seed)}"
    triggers = []
    panels = []
    for index, (title, lines) in enumerate(tabs):
        tab_name = escape(title or f"Tab {index + 1}")
        active = " active" if index == 0 else ""
        hidden = "" if index == 0 else " hidden"
        triggers.append(
            f'<button class="tabs-trigger{active}" type="button" data-tab-target="{tab_id}-{index}">{tab_name}</button>'
        )
        panels.append(
            f'<div class="tabs-panel{active}" id="{tab_id}-{index}"{hidden}>{render_rich_text(lines)}</div>'
        )
    return f'<div class="tabs"><div class="tabs-list">{"".join(triggers)}</div>{"".join(panels)}</div>'


def render_steps(steps: list[tuple[str, list[str]]]) -> str:
    if not steps:
        return ""
    rows = []
    for index, (title, lines) in enumerate(steps, start=1):
        title_html = f'<h3 class="step-title">{render_inline(title)}</h3>' if title else ""
        body_html = f'<p class="step-description">{render_rich_text(lines)}</p>' if render_rich_text(lines) else ""
        rows.append(
            f'<li class="step"><span class="step-marker">{index}</span>'
            f'<div class="step-content">{title_html}{body_html}</div></li>'
        )
    return f'<ol class="steps">{"".join(rows)}</ol>'


def render_params(lines: list[str]) -> str:
    rows = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("::param"):
            continue
        attrs = parse_card_attrs(stripped.removeprefix("::param").strip())
        name = attrs.get("name", "").strip()
        param_type = attrs.get("type", "").strip()
        required = attrs.get("required", "").strip().lower() in {"1", "true", "yes", "required"}
        description = attrs.get("description", "").strip()
        if not name:
            continue
        required_html = '<span class="param-required">Required</span>' if required else '<span class="param-optional">Optional</span>'
        rows.append(
            "<tr>"
            f'<td><code>{escape(name)}</code></td>'
            f'<td>{f"<code>{escape(param_type)}</code>" if param_type else ""}</td>'
            f"<td>{required_html}</td>"
            f"<td>{render_inline(description)}</td>"
            "</tr>"
        )
    if not rows:
        return ""
    return (
        '<div class="params"><table><thead><tr>'
        "<th>Parameter</th><th>Type</th><th>Status</th><th>Description</th>"
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def extract_headings(lines: list[str]) -> tuple[list[Heading], str, int | None]:
    headings: list[Heading] = []
    title = "Untitled"
    first_h1_index: int | None = None
    slug_counts: dict[str, int] = {}
    open_fence: str | None = None

    for index, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        fence_info = parse_fence(stripped)
        if fence_info:
            fence, info = fence_info
            if open_fence is None:
                open_fence = fence
            elif not info and fence == open_fence:
                open_fence = None
            continue
        if open_fence is not None:
            continue
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if not heading_match:
            continue
        level = len(heading_match.group(1))
        text_value = heading_match.group(2).strip()
        base_slug = slugify(text_value)
        count = slug_counts.get(base_slug, 0)
        slug_counts[base_slug] = count + 1
        slug = base_slug if count == 0 else f"{base_slug}-{count}"
        headings.append(Heading(level=level, text=text_value, slug=slug))
        if title == "Untitled" and level == 1:
            title = text_value
            first_h1_index = index

    return headings, title, first_h1_index


def preprocess_staticnest_blocks(lines: list[str], first_h1_index: int | None) -> str:
    output: list[str] = []
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        stripped = raw_line.strip()

        if index == first_h1_index:
            index += 1
            continue

        fence_info = parse_fence(stripped)
        if fence_info and fence_info[1].lower() != "mermaid":
            fence = fence_info[0]
            output.append(raw_line)
            index += 1
            while index < len(lines):
                output.append(lines[index])
                if lines[index].strip() == fence:
                    index += 1
                    break
                index += 1
            continue

        if fence_info and fence_info[1].lower() == "mermaid":
            fence = fence_info[0]
            mermaid_lines: list[str] = []
            index += 1
            while index < len(lines) and lines[index].strip() != fence:
                mermaid_lines.append(lines[index])
                index += 1
            output.extend(["", render_mermaid_block("\n".join(mermaid_lines)), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped == ":::cards":
            directive_lines: list[str] = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                directive_lines.append(lines[index])
                index += 1
            output.extend(["", render_cards(directive_lines), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped == ":::badges":
            directive_lines = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                directive_lines.append(lines[index])
                index += 1
            output.extend(["", render_badges(directive_lines), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped.startswith(":::callout"):
            attrs = parse_card_attrs(stripped.removeprefix(":::callout").strip())
            directive_lines = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                directive_lines.append(lines[index])
                index += 1
            output.extend(["", render_callout(attrs, directive_lines), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped == ":::files":
            directive_lines = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                directive_lines.append(lines[index])
                index += 1
            output.extend(["", render_files(directive_lines), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped == ":::steps":
            steps: list[tuple[str, list[str]]] = []
            current_title = ""
            current_lines: list[str] = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                step_line = lines[index].strip()
                if step_line.startswith("::step"):
                    if current_title or current_lines:
                        steps.append((current_title, current_lines))
                    current_title = parse_card_attrs(step_line.removeprefix("::step").strip()).get("title", "")
                    current_lines = []
                else:
                    current_lines.append(lines[index])
                index += 1
            if current_title or current_lines:
                steps.append((current_title, current_lines))
            output.extend(["", render_steps(steps), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped == ":::params":
            directive_lines = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                directive_lines.append(lines[index])
                index += 1
            output.extend(["", render_params(directive_lines), ""])
            if index < len(lines):
                index += 1
            continue

        if stripped == ":::tabs":
            tabs: list[tuple[str, list[str]]] = []
            current_title = ""
            current_lines: list[str] = []
            index += 1
            while index < len(lines) and lines[index].strip() != ":::":
                tab_line = lines[index].strip()
                if tab_line.startswith("::tab"):
                    if current_title or current_lines:
                        tabs.append((current_title, current_lines))
                    current_title = parse_card_attrs(tab_line.removeprefix("::tab").strip()).get("title", "")
                    current_lines = []
                else:
                    current_lines.append(lines[index])
                index += 1
            if current_title or current_lines:
                tabs.append((current_title, current_lines))
            output.extend(["", render_tabs(tabs), ""])
            if index < len(lines):
                index += 1
            continue

        output.append(raw_line)
        index += 1

    return "\n".join(output)


def render_markdown_with_pymdown(text: str) -> str:
    md = markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        output_format="html5",
    )
    rendered = md.convert(close_unclosed_fence(text))
    return add_heading_copy_links(wrap_codehilite_blocks(rendered)).replace("<hr>", "<hr />")


def render_markdown(text: str) -> RenderedPage:
    lines = text.splitlines()
    headings, title, first_h1_index = extract_headings(lines)
    body = preprocess_staticnest_blocks(lines, first_h1_index)
    html = render_markdown_with_pymdown(body)
    return RenderedPage(
        html=html,
        headings=headings,
        title=title,
        summary=summarize(lines),
    )
