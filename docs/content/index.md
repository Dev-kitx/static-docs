---
title: Static Docs
description: Build polished documentation sites from Markdown with a pure-Python CLI.
badge: Docs
status: beta
---

# Static Docs

Static Docs builds documentation sites from Markdown using a Python-only workflow. You write pages in `content/`, configure navigation with `navigation.yml`, and build static HTML into `dist/`.

:::cards
::card title="Getting started" description="Install Static Docs, scaffold a site, preview locally, and build static HTML." href="/static-docs/getting-started/"
::card title="Components" description="Use callouts, cards, tabs, file trees, steps, badges, parameters, details, captions, and Mermaid." href="/static-docs/components/"
::card title="API docs" description="Generate API reference pages from Python files and docstrings." href="/static-docs/api-docs/"
::card title="Deploy" description="Publish to GitHub Pages with a GitHub Actions workflow." href="/static-docs/deployment/"
:::

## What you get

:::steps
::step title="Markdown authoring"
Write normal Markdown plus Static Docs directives for docs components.
::step title="Built-in docs theme"
Get a sidebar, top navigation, right-side table of contents, search, dark mode, and polished code blocks.
::step title="Production outputs"
Generate HTML, search index, SEO files, and LLM-friendly docs files.
:::

## Build this documentation

```bash
static-docs build --config docs/site.toml
```

The output is written to:

:::files
docs/
    dist/
        index.html
        sitemap.xml
        robots.txt
        llms.txt
        assets/
            search-index.json
:::

