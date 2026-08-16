---
title: Components
description: Use cards, callouts, badges, steps, API parameters, file trees, tabs, captions, and FAQ details in Static Docs Markdown.
badge: Components
status: beta
order: 3
---

# Components

Static Docs includes lightweight Markdown directives for common documentation patterns. Use these when plain Markdown needs more structure without writing HTML.

## Cards

Use cards to create a quick entry point to related pages or sections.

Write:

```md
:::cards
::card title="Configuration" description="Configure site.toml." href="/configuration/"
::card title="Deploy" description="Deploy with GitHub Actions." href="/deployment/"
:::
```

You get:

:::cards
::card title="Callouts" description="Highlight notes, warnings, errors, success messages, and ideas." href="#callouts"
::card title="Badges" description="Label versions, status, and feature states inline with your docs." href="#badges"
::card title="Steps" description="Guide readers through ordered workflows with clear milestones." href="#steps"
::card title="API parameters" description="Document function and endpoint inputs in a compact table." href="#api-parameters"
::card title="File trees" description="Show project structure with collapsible folders." href="#file-trees"
::card title="Tabs" description="Switch between commands, package managers, or framework examples." href="#tabs"
::card title="Captions" description="Add descriptive captions to code blocks and other block elements." href="#captions"
::card title="FAQ" description="Create collapsible question and answer sections." href="#faq"
:::

## Callouts

Use callouts to draw attention to notes, warnings, success states, and errors.

Write:

```md
:::callout type="note" title="Note"
Directive content is rendered safely through Static Docs' Markdown renderer.
:::
```

You get:

:::callout type="warning" title="Escaped by default"
Directive content is rendered safely through Static Docs' Markdown renderer.
:::

:::callout type="note" title="Note"
Directive content is rendered safely through Static Docs' Markdown renderer.
:::

:::callout type="success" title="Reusable syntax"
The same directive syntax works across every Markdown page.
:::

:::callout type="info" title="Reusable syntax"
The same directive syntax works across every Markdown page.
:::

:::callout type="danger" title="Reusable syntax"
The same directive syntax works across every Markdown page.
:::

## Badges

Use badges to mark feature maturity, package support, or small metadata near headings and examples.

Write:

```md
:::badges
::badge label="New" type="success"
::badge label="Beta" type="warning"
::badge label="CLI" type="info"
::badge label="Deprecated" type="danger"
:::
```

You get:

:::badges
::badge label="New" type="success"
::badge label="Beta" type="warning"
::badge label="CLI" type="info"
::badge label="Deprecated" type="danger"
:::

## Steps

Use steps when readers need to complete a workflow in order. Each `::step` becomes one numbered item, and the body text can include Markdown like inline code or links.

Write:

```md
:::steps
::step title="Create a site"
Run `static-docs init docs-site` to scaffold content and configuration.
::step title="Preview locally"
Run `static-docs preview --config site.toml` while you edit Markdown.
::step title="Build for production"
Run `static-docs build --config site.toml` to generate static HTML.
:::
```

You get:

:::steps
::step title="Create a site"
Run `static-docs init docs-site` to scaffold content and configuration.
::step title="Preview locally"
Run `static-docs preview --config site.toml` while you edit Markdown.
::step title="Build for production"
Run `static-docs build --config site.toml` to generate static HTML.
:::

## API parameters

Use API parameter tables to document function arguments, endpoint inputs, CLI options, or configuration keys.

Write:

```md
:::params
::param name="config" type="Path | str" required="yes" description="Path to the `site.toml` configuration file."
::param name="output_dir" type="Path | str" description="Optional directory for generated static files."
::param name="live_reload" type="bool" description="Injects the preview reload script during local development."
:::
```

You get:

:::params
::param name="config" type="Path | str" required="yes" description="Path to the `site.toml` configuration file."
::param name="output_dir" type="Path | str" description="Optional directory for generated static files."
::param name="live_reload" type="bool" description="Injects the preview reload script during local development."
:::

## File trees

Use file trees to show project layout. Folders end with `/`, and indentation controls nesting.

Write:

```md
:::files
content/
    _meta.js
    contact.md
    index.mdx
    about/
        _meta.js
        legal.md
        index.mdx
:::
```

You get:

:::files
content/
    _meta.js
    contact.md
    index.mdx
    about/
        _meta.js
        legal.md
        index.mdx
:::

## Tabs

Use tabs to show equivalent instructions for package managers, frameworks, or operating systems.

Write:

```md
:::tabs
::tab title="pip"
Install with `pip install static-docs`.
::tab title="editable"
Clone the repository and run `pip install -e .`.
:::
```

You get:

:::tabs
::tab title="pip"
Install with `pip install static-docs`.
::tab title="editable"
Clone the repository and run `pip install -e .`.
:::

## Captions

Use captions to describe code blocks, tables, images, or other block elements.

Write:

````md
```python
from staticnest import build_site

build_site("site.toml")
```

/// caption
Build a Static Docs site from a config file.
///
````

You get:

```python
from staticnest import build_site

build_site("site.toml")
```

/// caption
Build a Static Docs site from a config file.
///

## FAQ

Use details blocks for FAQs and optional explanations that should not take over the page.

Write:

```md
/// details | Can I use collapsible FAQ items?
Yes. Static Docs enables `pymdownx.blocks.details`, so Markdown authors can create accessible collapsible sections.
///
```

You get:

/// details | Can I use collapsible FAQ items?
Yes. Static Docs enables `pymdownx.blocks.details`, so Markdown authors can create accessible collapsible sections.
///

/// details | Can details contain Markdown?
Yes. You can include **formatted text**, links, lists, and inline code like `static-docs preview` inside a details block.
///
