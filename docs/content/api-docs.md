---
title: API Docs
description: Generate API reference pages from Python source files and docstrings.
order: 5
---

# API Docs

Static Docs can generate Markdown API reference pages from Python source files.

Generated pages group classes, methods, and functions, include signatures, fill parameter types from annotations when possible, and render docstring params, returns, and raises as Static Docs components.

## Install optional parser

```bash
pip install "static-docs[api]"
```

Static Docs uses `docstring-parser` when installed. Without it, Static Docs falls back to a small built-in parser.

## Configure API docs

Add this to `site.toml`:

```toml
[api_docs]
enabled = true
source = "src/my_package"
output = "content/api"
package = "my_package"
title = "API Reference"
```

Then run:

```bash
static-docs build --config site.toml
```

You get:

:::files
content/
    api/
        index.md
        my_package-client.md
        my_package-config.md
dist/
    api/
        index.html
        my_package-client/
            index.html
:::

## Manual generation

```bash
static-docs api generate \
  --source src/my_package \
  --output content/api \
  --package my_package \
  --title "API Reference"
```

## Python input

```python
def create_client(project: str, base_url: str = "/") -> StaticDocsClient:
    """Create a configured Static Docs client.

    Args:
        project: Project name displayed in generated docs.
        base_url: Public base URL for generated pages.

    Returns:
        Configured client instance.
    """
```

## Generated Markdown

````md
## Functions

### create_client

```python title="line 1"
create_client(project: str, base_url: str = '/') -> StaticDocsClient
```

:::params
::param name="project" type="str" description="Project name displayed in generated docs."
::param name="base_url" type="str" description="Public base URL for generated pages."
:::

:::callout type="info" title="Returns"
Configured client instance.
:::
````

:::callout type="warning" title="Generated files"
Files under `content/api/` are generated. Edit Python docstrings, not generated Markdown.
:::
