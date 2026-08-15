---
title: Configuration
summary: Configure site metadata, navigation, theme options, and links.
order: 2
---

# Configuration

Static Docs reads site settings from `site.toml` and sidebar/header structure from `navigation.yml`.

## Project files

:::files
my-docs/
├── site.toml
├── navigation.yml
└── content/
    └── index.md
:::

## Theme

Static Docs ships with one built-in docs theme:

```toml
[theme]
name = "static-docs"
```

## API docs

Generate API reference pages from Python docstrings:

```toml
[api_docs]
enabled = true
source = "src/my_package"
output = "content/api"
package = "my_package"
title = "API Reference"
```

You can also generate them manually:

```bash
static-docs api generate --source src/my_package --output content/api --package my_package
```

The example site includes a tiny package in `examples/docs-site/src/demo_api`; running the normal build generates the API pages under `content/api`.
