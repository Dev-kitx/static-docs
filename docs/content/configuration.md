---
title: Configuration
description: Configure site metadata, paths, navigation, branding, API docs, and theme settings.
order: 2
---

# Configuration

Static Docs reads `site.toml`. Paths are resolved relative to the config file.

## Minimal config

```toml
title = "My Docs"
tagline = "Python documentation without a frontend build step"
description = "Documentation for my project."
site_url = "https://example.com/docs"
base_url = "/docs/"
content_dir = "content"
output_dir = "dist"
nav_file = "navigation.yml"

[brand]
name = "My Project"
accent = "#f46e00"

[links]
github = "https://github.com/acme/my-project"

[repo]
url = "https://github.com/acme/my-project"
branch = "main"
docs_dir = "docs/content"

[theme]
name = "static-docs"
```

## Site fields

:::params
::param name="title" type="string" required="yes" description="Site title used in metadata and page chrome."
::param name="tagline" type="string" description="Short supporting text used by some pages and metadata."
::param name="description" type="string" description="Fallback meta description when a page does not define its own."
::param name="content_dir" type="path" required="yes" description="Directory containing Markdown source pages."
::param name="output_dir" type="path" required="yes" description="Directory where Static Docs writes HTML and assets."
::param name="nav_file" type="path" description="YAML file used for sidebar, top nav, GitHub link, and feedback link."
::param name="site_url" type="URL" description="Public production URL used for canonical URLs, sitemap.xml, and robots.txt."
::param name="base_url" type="path or URL" description="Base path used by generated links and assets."
:::

## Edit links

Use `[repo]` to show an "Edit this page on GitHub" link in the right-side panel.

```toml
[repo]
url = "https://github.com/acme/my-project"
branch = "main"
docs_dir = "docs/content"
```

:::params
::param name="url" type="URL" description="Repository URL used to build edit links."
::param name="branch" type="string" description="Branch used in GitHub edit URLs. Defaults to `main`."
::param name="docs_dir" type="path" description="Path from the repository root to the Markdown content directory."
:::

## Navigation

Navigation lives in `navigation.yml` by default.

```yaml
- title: Overview
  page: index.md

- title: Guides
  items:
    - page: getting-started.md
    - page: configuration.md

- navigation-bar:
    github:
      title: GitHub
      link: https://github.com/acme/my-project
      logo: https://github.githubassets.com/favicons/favicon.svg
    resources:
      title: Resources
      items:
        - name: PyPI
          link: https://pypi.org/project/static-docs/
- issues:
    title: Issues
    link: https://github.com/acme/my-project/issues
```

Each sidebar item supports `title`, `page`, `url`, `items`, and `order`.

## Navigation result

- Sidebar entries come from `title`, `page`, and nested `items`.
- Top navigation entries come from `navigation-bar`.
- The GitHub icon comes from `navigation-bar.github`.
- The right-side feedback link comes from `issues.link`.

## Page metadata

Page-level metadata belongs in Markdown front matter. Use it for titles, sidebar labels, descriptions, badges, page status, drafts, and per-page layout options.

See [Authoring](authoring/) for the full front matter reference.

## Theme overrides

The built-in theme is `static-docs` and requires no local files:

```toml
[theme]
name = "static-docs"
```

To add project-specific CSS, JavaScript, or templates, point `theme.dir` at a local directory:

```toml
[theme]
name = "static-docs"
dir = "theme"
```

When `dir` is set, Static Docs will:

- copy `theme/assets/*` into `dist/assets/`
- load `theme/assets/custom.css` after the built-in stylesheet when it exists
- load `theme/assets/custom.js` after the built-in script when it exists
- use `theme/templates/page.html` as the default outer HTML shell when it exists
- use `template: <name>.html` front matter to select another template from `theme/templates/`
