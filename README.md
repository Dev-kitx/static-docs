# Static Docs

> A pure-Python static site generator for polished documentation sites — strong typography, left sidebar navigation, right table of contents, client-side full-text search, and live reload in dev mode.

[![PyPI](https://img.shields.io/pypi/v/static-docs?style=for-the-badge&labelColor=2d3748&color=ffd166)](https://pypi.org/project/static-docs/)
[![Python](https://img.shields.io/pypi/pyversions/static-docs?style=for-the-badge&labelColor=023047&color=8ecae6)](https://pypi.org/project/static-docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-95d5b2?style=for-the-badge&labelColor=1b4332)](LICENSE)

[![Pure Python](https://img.shields.io/badge/Pure%20Python-no%20node-ffd166?style=for-the-badge&labelColor=2d3748)](https://pypi.org/project/static-docs/)
[![Markdown Powered](https://img.shields.io/badge/Markdown-powered-8ecae6?style=for-the-badge&labelColor=023047)](#features)
[![Static Output](https://img.shields.io/badge/Static%20HTML-fast%20docs-95d5b2?style=for-the-badge&labelColor=1b4332)](#quick-start)
[![Docs Theme](https://img.shields.io/badge/Docs%20Theme-built--in-ffafcc?style=for-the-badge&labelColor=5a189a)](#features)

---

## Features

- **Python-only runtime** — no Node or frontend build step
- **TOML-based configuration** — single `site.toml` controls everything
- **YAML navigation** — explicit sidebar order, nested groups, top-bar links
- **Front matter** — YAML (`---`) or TOML (`+++`) blocks for title, summary, draft, order, and template overrides
- **Pymdown-powered Markdown** — Python-Markdown plus `pymdown-extensions` for richer Markdown behavior
- **Syntax highlighting** — Pygments-powered fenced code blocks
- **Table of contents** — auto-generated per page, scroll-synced right panel
- **Client-side search** — full-text index baked into each page at build time
- **Live reload dev server** — watches content and config files, pushes reload via polling
- **GitHub Pages deploy** — one command builds and force-pushes to `gh-pages`
- **Theme overrides** — drop custom CSS/JS or a full HTML template into `theme/`

---

## Installation

### From PyPI

```bash
pip install static-docs
```

### From source (local / contributor)

```bash
git clone https://github.com/Dev-kitx/static-docs.git
cd static-docs
uv sync --locked --extra dev
```

The project uses `uv.lock` for repeatable contributor and CI installs. The `static-docs` command is available through `uv run static-docs`.

---

## Quick start

```bash
# 1. Scaffold a new project
static-docs init my-docs

# 2. Preview with live reload
static-docs preview --config my-docs/site.toml

# 3. Build for production
static-docs build --config my-docs/site.toml
```

The scaffolded directory contains:

```text
my-docs/
├── site.toml        # site-wide config
├── navigation.yml   # sidebar + top-bar nav
└── content/
    └── index.md     # home page
```

---

## Project documentation

This repository includes a full Static Docs documentation site under `docs/`.

```bash
static-docs build --config docs/site.toml
```

The docs source explains configuration, authoring, components, API docs generation, search, SEO, LLM files, and GitHub Actions deployment.

---

## CLI reference

All commands follow the pattern:

```
static-docs <command> [options]
```

### `init`

Scaffold a new project directory.

```bash
static-docs init [path]
```

| Argument | Default | Description                                           |
| -------- | ------- | ----------------------------------------------------- |
| `path`   | `.`     | Directory to initialise. Created if it does not exist. |

### `build`

Build the site to `output_dir` (configured in `site.toml`).

```bash
static-docs build --config <path/to/site.toml>
```

| Flag       | Default     | Description                          |
| ---------- | ----------- | ------------------------------------ |
| `--config` | `site.toml` | Path to the site configuration file. |

### `preview` / `serve`

Start a local dev server with live reload. Both names are equivalent.

```bash
static-docs preview --config <path/to/site.toml> [--host HOST] [--port PORT]
```

| Flag       | Default     | Description                          |
| ---------- | ----------- | ------------------------------------ |
| `--config` | `site.toml` | Path to the site configuration file. |
| `--host`   | `127.0.0.1` | Network interface to bind.           |
| `--port`   | `8000`      | Port to listen on.                   |

### `publish`

Copy the built output to a publish destination.

```bash
static-docs publish --config <path/to/site.toml> [--destination DIR]
```

| Flag            | Default                  | Description                                 |
| --------------- | ------------------------ | ------------------------------------------- |
| `--config`      | `site.toml`              | Path to the site configuration file.        |
| `--destination` | `output_dir` from config | Override the target directory for this run. |

### `gh-deploy`

Build, add GitHub Pages artifacts (`.nojekyll`, `404.html`), and force-push to a deploy branch.

```bash
static-docs gh-deploy --config <path/to/site.toml> [--remote REMOTE] [--branch BRANCH] [--message MSG]
```

| Flag        | Default                   | Description                           |
| ----------- | ------------------------- | ------------------------------------- |
| `--config`  | `site.toml`               | Path to the site configuration file.  |
| `--remote`  | `origin`                  | Git remote to push to.                |
| `--branch`  | `gh-pages`                | Branch to force-push the output to.   |
| `--message` | `Deploy static-docs site` | Commit message for the deploy commit. |

---

## Configuration (`site.toml`)

```toml
[site]
title       = "My Docs"
description = "Documentation for My Project"
base_url    = "https://your-org.github.io/your-repo/"
output_dir  = "dist"

[brand]
name = "My Project"

[theme]
name = "static-docs"

[nav]
file = "navigation.yml"
```

---

## Navigation (`navigation.yml`)

```yaml
- title: Overview
  page: index.md

- title: Guides
  items:
    - page: docs/getting-started.md
    - page: docs/configuration.md

- navigation-bar:
    github:
      title: GitHub
      link: https://github.com/your-org/your-repo
      logo: https://github.githubassets.com/favicons/favicon.svg
    resources:
      title: Resources
      items:
        - name: Release notes
          link: https://example.com/releases

- issues:
    title: Issues
    link: https://github.com/your-org/your-repo/issues
```

Each nav item supports: `title`, `page`, `url`, `items`, `order`.

- `navigation-bar.github` renders as a dedicated icon link in the top-right header.
- Other `navigation-bar` entries render to the left of the search bar.
- `issues.link` populates the "Give us feedback" link in the right-side TOC panel.

---

## Front matter

YAML (`---`) or TOML (`+++`) at the top of any `.md` file:

```md
---
title: Architecture
nav_title: System Design
order: 4
summary: Explains the pipeline and page rendering model.
template: page.html
draft: false
---
```

| Field       | Description                                                |
| ----------- | ---------------------------------------------------------- |
| `title`     | Page `<title>` and `<h1>` (overrides first `#` heading).   |
| `nav_title` | Shorter label used only in the sidebar.                    |
| `order`     | Integer sort key within a navigation group.                |
| `summary`   | Used in `<meta description>` and search results.           |
| `template`  | Select an alternate template from `theme/templates/`.      |
| `draft`     | Set `true` to exclude from the build output.               |

---

## Theme

Static Docs includes one built-in docs theme:

```toml
[theme]
name = "static-docs"
```

---

## Repository layout

```text
static-docs/
├── src/staticnest/      # package source
│   ├── cli.py           # argparse entry point
│   ├── site.py          # build / publish / deploy orchestration
│   ├── markdown.py      # Python-Markdown/pymdown renderer
│   ├── theme.py         # CSS, JS, and HTML template
│   ├── devserver.py     # live-reload HTTP server
│   └── scaffold.py      # init command scaffolding
├── docs/                # documentation site source
│   ├── content/
│   ├── navigation.yml
│   └── site.toml
├── tests/               # pytest test suite
├── uv.lock              # locked development and CI dependencies
├── pyproject.toml
└── README.md
```

---

## Local development

### Run the documentation site

```bash
uv run static-docs preview --config docs/site.toml
```

Open `http://127.0.0.1:8000` in your browser. The server rebuilds and reloads automatically when you save a file.

### Run tests

```bash
uv sync --locked --extra dev
uv run pytest
```

---

## Releasing

Releases are automated through the shared Dev-kitx release workflow and PyPI Trusted Publishing. Publishing a GitHub Release triggers the PyPI workflow automatically.

To verify a release artifact locally before publishing, maintainers can build with:

```bash
uv sync --locked --extra dev
uv build
```

---

## License

MIT — see [LICENSE](LICENSE).
