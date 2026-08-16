---
title: Search, SEO, and LLM Files
description: Static Docs generates search indexes, SEO files, and LLM-friendly text exports at build time.
order: 6
---

# Search, SEO, and LLM Files

## Search

Run:

```bash
static-docs build --config site.toml
```

You get:

:::files
dist/
    assets/
        search-index.json
:::

The search bar reads `assets/search-index.json` in the browser. Results include page matches and heading matches, so searching `API parameters` can open `/components/#api-parameters`.

The generated `404.html` page also includes a search box that reads the same index. If a reader lands on an old or missing URL, they can search directly from the error page.

Keyboard shortcuts:

:::params
::param name="/" type="shortcut" description="Focus the search input."
::param name="Cmd/Ctrl K" type="shortcut" description="Focus the search input."
:::

## SEO

Build output includes:

:::files
dist/
    sitemap.xml
    robots.txt
    index.html
:::

Each page includes:

- canonical URL
- OpenGraph title, description, URL, site name
- Twitter summary card metadata

Set `site_url` for production URLs:

```toml
site_url = "https://docs.example.com"
base_url = "/"
```

## LLM files

Build output includes:

:::files
dist/
    llms.txt
    llms-full.txt
    llms-pages/
        index.md
        components.md
:::

Use these files when AI tools need to read the documentation without scraping HTML.

:::callout type="note" title="Why this helps"
`llms.txt` gives tools a compact page index, while `llms-full.txt` gives them the complete docs content in one text file.
:::
