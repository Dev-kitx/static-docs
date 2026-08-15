from __future__ import annotations

from pathlib import Path


DEFAULT_SITE_TOML = """title = "My Docs"
tagline = "Documentation built with Static Docs"
description = "A polished documentation site powered by Static Docs."
base_url = "/"
content_dir = "content"
output_dir = "dist"
nav_file = "navigation.yml"

[brand]
name = "My Docs"
accent = "#2563eb"

[links]
github = "https://github.com/"

[theme]
name = "static-docs"
"""


DEFAULT_NAVIGATION_YML = """- title: Overview
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
- issues:
    title: Issues
    link: https://github.com/your-org/your-repo/issues
"""


DEFAULT_INDEX_MD = """# Welcome

Static Docs gives you a clean docs shell with built-in navigation, search, and a right-side table of contents.

## Start here

- Edit `site.toml` to set your project title and links.
- Update `navigation.yml` to control sidebar order.
- Add pages under `content/`.
"""


DEFAULT_GETTING_STARTED_MD = """# Getting Started

Use the CLI to preview and build your documentation site.

## Preview locally

```bash
static-docs preview
```

## Build the site

```bash
static-docs build
```
"""


DEFAULT_CONFIGURATION_MD = """# Configuration

Static Docs reads your site settings from `site.toml`.

## Theme

```toml
[theme]
name = "static-docs"
```

## Navigation

Set `nav_file = "navigation.yml"` and manage sidebar order, top navigation, and the top-right GitHub logo there.
"""


def init_project(target_dir: Path) -> Path:
    target_dir = target_dir.resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    files_to_write = {
        target_dir / "site.toml": DEFAULT_SITE_TOML,
        target_dir / "navigation.yml": DEFAULT_NAVIGATION_YML,
        target_dir / "content" / "index.md": DEFAULT_INDEX_MD,
        target_dir / "content" / "docs" / "getting-started.md": DEFAULT_GETTING_STARTED_MD,
        target_dir / "content" / "docs" / "configuration.md": DEFAULT_CONFIGURATION_MD,
    }

    existing = [path for path in files_to_write if path.exists()]
    if existing:
        existing_paths = ", ".join(sorted(path.relative_to(target_dir).as_posix() for path in existing))
        raise ValueError(f"Refusing to overwrite existing files: {existing_paths}")

    for path, content in files_to_write.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    return target_dir
