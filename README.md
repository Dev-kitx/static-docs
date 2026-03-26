# Staticnest

> A pure-Python static site generator for polished documentation sites — strong typography, left sidebar navigation, right table of contents, client-side full-text search, and live reload in dev mode.

[![PyPI](https://img.shields.io/pypi/v/staticnest-cli)](https://pypi.org/project/staticnest-cli/)
[![Python](https://img.shields.io/pypi/pyversions/staticnest-cli)](https://pypi.org/project/staticnest-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Features

- **Zero runtime dependencies** — pure Python, no Node, no build system
- **TOML-based configuration** — single `site.toml` controls everything
- **YAML navigation** — explicit sidebar order, nested groups, top-bar links
- **Front matter** — YAML (`---`) or TOML (`+++`) blocks for title, summary, draft, order, and template overrides
- **Syntax highlighting** — Pygments-powered with the `xcode` style
- **Table of contents** — auto-generated per page, scroll-synced right panel
- **Client-side search** — full-text index baked into each page at build time
- **Live reload dev server** — watches content and config files, pushes reload via polling
- **GitHub Pages deploy** — one command builds and force-pushes to `gh-pages`
- **Theme overrides** — drop custom CSS/JS or a full HTML template into `theme/`

---

## Installation

### From PyPI

```bash
pip install staticnest-cli
```

### From source (local / contributor)

```bash
git clone https://github.com/Dev-kitx/staticnest-cli.git
cd staticnest-cli
pip install -e .
```

The `-e` flag installs in editable mode — changes to `src/staticnest/` are reflected immediately without reinstalling. The `staticnest` command is available as soon as this completes.

---

## Quick start

```bash
# 1. Scaffold a new project
staticnest init my-docs

# 2. Preview with live reload
staticnest preview --config my-docs/site.toml

# 3. Build for production
staticnest build --config my-docs/site.toml
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

## CLI reference

All commands follow the pattern:

```
staticnest <command> [options]
```

### `init`

Scaffold a new project directory.

```bash
staticnest init [path]
```

| Argument | Default | Description |
|---|---|---|
| `path` | `.` | Directory to initialise. Created if it does not exist. |

### `build`

Build the site to `output_dir` (configured in `site.toml`).

```bash
staticnest build --config <path/to/site.toml>
```

| Flag | Default | Description |
|---|---|---|
| `--config` | `site.toml` | Path to the site configuration file. |

### `preview` / `serve`

Start a local dev server with live reload. Both names are equivalent.

```bash
staticnest preview --config <path/to/site.toml> [--host HOST] [--port PORT]
```

| Flag | Default | Description |
|---|---|---|
| `--config` | `site.toml` | Path to the site configuration file. |
| `--host` | `127.0.0.1` | Network interface to bind. |
| `--port` | `8000` | Port to listen on. |

### `publish`

Copy the built output to a publish destination.

```bash
staticnest publish --config <path/to/site.toml> [--destination DIR]
```

| Flag | Default | Description |
|---|---|---|
| `--config` | `site.toml` | Path to the site configuration file. |
| `--destination` | `output_dir` from config | Override the target directory for this run. |

### `gh-deploy`

Build, add GitHub Pages artifacts (`.nojekyll`, `404.html`), and force-push to a deploy branch.

```bash
staticnest gh-deploy --config <path/to/site.toml> [--remote REMOTE] [--branch BRANCH] [--message MSG]
```

| Flag | Default | Description |
|---|---|---|
| `--config` | `site.toml` | Path to the site configuration file. |
| `--remote` | `origin` | Git remote to push to. |
| `--branch` | `gh-pages` | Branch to force-push the output to. |
| `--message` | `Deploy staticnest site` | Commit message for the deploy commit. |

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
name = "nest"
# Optional: enable theme overrides from a local directory
# dir = "theme"

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

| Field | Description |
|---|---|
| `title` | Page `<title>` and `<h1>` (overrides first `#` heading). |
| `nav_title` | Shorter label used only in the sidebar. |
| `order` | Integer sort key within a navigation group. |
| `summary` | Used in `<meta description>` and search results. |
| `template` | Select an alternate template from `theme/templates/`. |
| `draft` | Set `true` to exclude from the build output. |

---

## Theme overrides

The built-in `nest` theme requires no local files. To customise:

```toml
[theme]
name = "nest"
dir  = "theme"
```

When `dir` is set the generator will:

- copy `theme/assets/*` into `dist/assets/`
- auto-load `theme/assets/custom.css` after the built-in stylesheet
- auto-load `theme/assets/custom.js` after the built-in script
- use `theme/templates/page.html` as the outer HTML shell
- use `template: <name>.html` front matter to select other templates

---

## Repository layout

```text
staticnest-cli/
├── src/staticnest/      # package source
│   ├── cli.py           # argparse entry point
│   ├── site.py          # build / publish / deploy orchestration
│   ├── markdown.py      # Markdown → HTML renderer (Pygments-backed)
│   ├── theme.py         # CSS, JS, and HTML template
│   ├── devserver.py     # live-reload HTTP server
│   └── scaffold.py      # init command scaffolding
├── examples/docs-site/  # built-in example site
│   ├── content/
│   ├── navigation.yml
│   └── site.toml
├── tests/               # pytest test suite
├── pyproject.toml
└── README.md
```

---

## Local development

### Run the example site

```bash
staticnest preview --config examples/docs-site/site.toml
```

Open `http://127.0.0.1:8000` in your browser. The server rebuilds and reloads automatically when you save a file.

### Run tests

```bash
pip install pytest
pytest
```

---

## Releasing

Releases are fully automated via [Release Please](https://github.com/googleapis/release-please) and [Trusted Publishing](https://docs.pypi.org/trusted-publishers/). Merging a Release Please PR bumps the version and triggers the PyPI publish workflow automatically — no manual wheel building needed.

To verify a release artifact locally before publishing, maintainers can build with:

```bash
pip install build
pyproject-build
```

> **Note:** `build.py` in the project root is a legacy shim that shadows `python -m build`. Use `pyproject-build` until it is removed.

---

## License

MIT — see [LICENSE](LICENSE).
