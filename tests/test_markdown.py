from __future__ import annotations

import unittest

from staticnest.markdown import (
    Heading,
    RenderedPage,
    highlight_code,
    render_code_block,
    render_inline,
    render_markdown,
    slugify,
    summarize,
)


class SlugifyTests(unittest.TestCase):
    def test_lowercase_words(self) -> None:
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_special_characters_replaced(self) -> None:
        self.assertEqual(slugify("Getting Started!"), "getting-started")

    def test_numbers_preserved(self) -> None:
        self.assertEqual(slugify("Step 1: Setup"), "step-1-setup")

    def test_empty_string_returns_section(self) -> None:
        self.assertEqual(slugify(""), "section")

    def test_only_special_chars_returns_section(self) -> None:
        self.assertEqual(slugify("!!!"), "section")

    def test_leading_trailing_hyphens_stripped(self) -> None:
        self.assertEqual(slugify("-Title-"), "title")


class RenderInlineTests(unittest.TestCase):
    def test_plain_text_passthrough(self) -> None:
        self.assertEqual(render_inline("hello world"), "hello world")

    def test_link_rendered(self) -> None:
        result = render_inline("[Click me](https://example.com)")
        self.assertIn('<a href="https://example.com">Click me</a>', result)

    def test_inline_code(self) -> None:
        result = render_inline("run `pip install` now")
        self.assertIn("<code>pip install</code>", result)

    def test_bold(self) -> None:
        result = render_inline("this is **bold** text")
        self.assertIn("<strong>bold</strong>", result)

    def test_italic(self) -> None:
        result = render_inline("this is *italic* text")
        self.assertIn("<em>italic</em>", result)

    def test_html_characters_escaped(self) -> None:
        result = render_inline("a < b & c > d")
        self.assertIn("&lt;", result)
        self.assertIn("&amp;", result)
        self.assertIn("&gt;", result)

    def test_combined_formatting(self) -> None:
        result = render_inline("**bold** and `code`")
        self.assertIn("<strong>bold</strong>", result)
        self.assertIn("<code>code</code>", result)


class SummarizeTests(unittest.TestCase):
    def test_returns_first_non_heading_line(self) -> None:
        lines = ["# Title", "", "This is a description."]
        self.assertEqual(summarize(lines), "This is a description.")

    def test_skips_headings(self) -> None:
        lines = ["# Heading", "## Sub", "Some content"]
        self.assertEqual(summarize(lines), "Some content")

    def test_truncates_long_lines(self) -> None:
        long_line = "word " * 50  # > 180 chars
        result = summarize([long_line])
        self.assertTrue(result.endswith("..."))
        self.assertLessEqual(len(result), 180)

    def test_empty_lines_skipped(self) -> None:
        lines = ["", "   ", "First paragraph."]
        self.assertEqual(summarize(lines), "First paragraph.")

    def test_empty_returns_empty_string(self) -> None:
        self.assertEqual(summarize([]), "")

    def test_only_headings_returns_empty(self) -> None:
        self.assertEqual(summarize(["# Heading", "## Sub"]), "")


class HighlightCodeTests(unittest.TestCase):
    def test_python_produces_spans(self) -> None:
        result = highlight_code("python", "def foo(): pass")
        self.assertIn("<span", result)

    def test_bash_produces_spans(self) -> None:
        result = highlight_code("bash", "echo hello")
        self.assertIn("<span", result)

    def test_yaml_produces_spans(self) -> None:
        result = highlight_code("yaml", "key: value")
        self.assertIn("<span", result)

    def test_toml_produces_spans(self) -> None:
        result = highlight_code("toml", 'name = "staticnest"')
        self.assertIn("<span", result)

    def test_json_produces_spans(self) -> None:
        result = highlight_code("json", '{"key": true}')
        self.assertIn("<span", result)

    def test_sh_alias_produces_spans(self) -> None:
        result = highlight_code("sh", "echo hello")
        self.assertIn("<span", result)

    def test_py_alias_produces_spans(self) -> None:
        result = highlight_code("py", "return x")
        self.assertIn("<span", result)

    def test_unknown_language_returns_escaped(self) -> None:
        result = highlight_code("unknown-xyz", "<b>bold</b>")
        self.assertIn("&lt;b&gt;", result)
        self.assertNotIn("<b>", result)

    def test_empty_language_returns_escaped(self) -> None:
        result = highlight_code("", "<b>bold</b>")
        self.assertIn("&lt;b&gt;", result)
        self.assertNotIn("<b>", result)

    def test_multiline_code_preserved(self) -> None:
        result = highlight_code("python", "def foo():\n    return 1")
        self.assertIn("\n", result)

    def test_html_not_injected(self) -> None:
        result = highlight_code("python", 'x = "<script>"')
        self.assertNotIn("<script>", result)


class RenderCodeBlockTests(unittest.TestCase):
    def test_contains_code_block_wrapper(self) -> None:
        result = render_code_block("python", ["x = 1"])
        self.assertIn('class="code-block"', result)

    def test_contains_copy_button(self) -> None:
        result = render_code_block("python", ["x = 1"])
        self.assertIn("data-code-copy", result)

    def test_language_badge_shown(self) -> None:
        result = render_code_block("bash", ["echo hi"])
        self.assertIn("bash", result)

    def test_empty_language_shows_text_badge(self) -> None:
        result = render_code_block("", ["some text"])
        self.assertIn(">text<", result)

    def test_language_class_on_code_element(self) -> None:
        result = render_code_block("python", ["x = 1"])
        self.assertIn('class="language-python"', result)

    def test_multiline_code_preserved(self) -> None:
        result = render_code_block("python", ["a = 1", "b = 2"])
        self.assertIn("\n", result)

    def test_pre_has_highlight_class(self) -> None:
        result = render_code_block("python", ["x = 1"])
        self.assertIn('class="highlight"', result)


class RenderMarkdownTests(unittest.TestCase):
    def test_code_fence_title_is_rendered(self) -> None:
        page = render_markdown('```python title="app.py"\nx = 1\n```')
        self.assertIn('class="code-block-title">app.py</span>', page.html)

    def test_code_fence_highlight_lines_are_preserved(self) -> None:
        page = render_markdown('```python hl_lines="1"\nx = 1\n```')
        self.assertIn('class="hll"', page.html)

    def test_h1_extracted_as_title(self) -> None:
        page = render_markdown("# Hello World\n\nSome text.")
        self.assertEqual(page.title, "Hello World")

    def test_h1_not_in_html_output(self) -> None:
        page = render_markdown("# Hello World\n\nSome text.")
        self.assertNotIn("<h1", page.html)

    def test_headings_in_list(self) -> None:
        page = render_markdown("# Title\n\n## Section\n\nText")
        slugs = [h.slug for h in page.headings]
        self.assertIn("section", slugs)

    def test_paragraph_rendered(self) -> None:
        page = render_markdown("Just a paragraph.")
        self.assertIn("<p>", page.html)

    def test_unordered_list(self) -> None:
        page = render_markdown("- item one\n- item two")
        self.assertIn("<ul>", page.html)
        self.assertIn("<li>", page.html)

    def test_ordered_list(self) -> None:
        page = render_markdown("1. first\n2. second")
        self.assertIn("<ol>", page.html)

    def test_blockquote(self) -> None:
        page = render_markdown("> This is a quote")
        self.assertIn("<blockquote>", page.html)

    def test_horizontal_rule(self) -> None:
        page = render_markdown("---")
        self.assertIn("<hr />", page.html)

    def test_fenced_code_block(self) -> None:
        page = render_markdown("```python\nx = 1\n```")
        self.assertIn("code-block", page.html)

    def test_mermaid_fence_renders_mermaid_block(self) -> None:
        page = render_markdown("```mermaid\ngraph TD;\nA-->B;\n```")
        self.assertIn('class="mermaid-block"', page.html)
        self.assertIn('class="mermaid"', page.html)
        self.assertIn("graph TD;", page.html)
        self.assertNotIn("code-block", page.html)

    def test_summary_extracted(self) -> None:
        page = render_markdown("# Title\n\nThis is the summary sentence.")
        self.assertEqual(page.summary, "This is the summary sentence.")

    def test_untitled_when_no_h1(self) -> None:
        page = render_markdown("Just text, no heading.")
        self.assertEqual(page.title, "Untitled")

    def test_inline_link_in_paragraph(self) -> None:
        page = render_markdown("See [docs](https://example.com) for info.")
        self.assertIn('<a href="https://example.com">', page.html)

    def test_unclosed_code_block_still_renders(self) -> None:
        page = render_markdown("```python\nx = 1\n")
        self.assertIn("code-block", page.html)

    def test_returns_rendered_page_type(self) -> None:
        page = render_markdown("# Title\n")
        self.assertIsInstance(page, RenderedPage)

    def test_toc_only_includes_h2_and_h3(self) -> None:
        page = render_markdown("# H1\n\n## H2\n\n### H3\n\n#### H4")
        h2 = next((h for h in page.headings if h.level == 2), None)
        h3 = next((h for h in page.headings if h.level == 3), None)
        h4 = next((h for h in page.headings if h.level == 4), None)
        self.assertIsNotNone(h2)
        self.assertIsNotNone(h3)
        self.assertIsNotNone(h4)

    def test_h2_appears_in_html(self) -> None:
        page = render_markdown("# Title\n\n## Sub-section\n\nText")
        self.assertIn("<h2", page.html)

    def test_heading_copy_anchor_is_added(self) -> None:
        page = render_markdown("# Title\n\n## Sub-section\n\nText")
        self.assertIn('class="heading-with-anchor"', page.html)
        self.assertIn('data-heading-anchor="sub-section"', page.html)
        self.assertIn('aria-label="Copy section link"', page.html)

    def test_badges_directive_renders_badges(self) -> None:
        page = render_markdown(':::badges\n::badge label="Beta" type="warning"\n:::')
        self.assertIn('class="badges"', page.html)
        self.assertIn('class="badge badge-warning"', page.html)
        self.assertIn("Beta", page.html)

    def test_staticnest_directive_inside_code_fence_stays_code(self) -> None:
        page = render_markdown(
            '```md\n:::cards\n::card title="Configuration" description="Configure site.toml."\n:::\n```'
        )
        self.assertIn("code-block", page.html)
        self.assertIn(":::cards", page.html)
        self.assertNotIn('&lt;div class="cards"', page.html)

    def test_staticnest_directive_inside_four_backtick_fence_stays_code(self) -> None:
        page = render_markdown(
            "````md\n"
            "## create_client\n\n"
            "```python\n"
            "create_client(project: str) -> StaticnestClient\n"
            "```\n\n"
            ":::params\n"
            '::param name="project" description="Project name."\n'
            ":::\n"
            "````"
        )
        self.assertIn("code-block", page.html)
        self.assertIn(":::params", page.html)
        self.assertNotIn('&lt;div class="params"', page.html)
        self.assertNotIn('class="params"', page.html)

    def test_steps_directive_renders_ordered_steps(self) -> None:
        page = render_markdown(':::steps\n::step title="Install"\nRun `pip install staticnest-cli`.\n:::')
        self.assertIn('class="steps"', page.html)
        self.assertIn('class="step-marker">1</span>', page.html)
        self.assertIn("Install", page.html)

    def test_params_directive_renders_api_table(self) -> None:
        page = render_markdown(
            ':::params\n::param name="config" type="Path | str" required="yes" description="Path to `site.toml`."\n:::'
        )
        self.assertIn('class="params"', page.html)
        self.assertIn("<th>Parameter</th>", page.html)
        self.assertIn("<code>config</code>", page.html)
        self.assertIn('class="param-required">Required</span>', page.html)

    def test_note_callout_keeps_note_variant(self) -> None:
        page = render_markdown(':::callout type="note" title="Note"\nPurple callout.\n:::')
        self.assertIn("callout-note", page.html)
        self.assertIn("admonition note", page.html)
        self.assertIn('class="callout-icon"', page.html)

    def test_files_directive_renders_collapsible_tree(self) -> None:
        page = render_markdown(":::files\ncontent/\n    index.md\n    about/\n        index.md\n:::")
        self.assertIn('class="files file-tree"', page.html)
        self.assertIn('<details class="file-tree-folder"', page.html)
        self.assertIn('<summary class="file-tree-row file-tree-folder-row"', page.html)
        self.assertIn('class="file-tree-row file-tree-file-row"', page.html)


if __name__ == "__main__":
    unittest.main()
