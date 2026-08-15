---
title: CLI Reference
description: Static Docs command line commands, arguments, and flags.
order: 2
---

# CLI Reference

All commands follow this pattern:

```bash
static-docs <command> [options]
```

`--config` accepts either a `site.toml` file or a project directory containing `site.toml`.

## init

Scaffold a new project directory.

```bash
static-docs init [path]
```

:::params
::param name="path" type="argument" description="Directory to initialize. Defaults to the current directory."
:::

## build

Build the site to `output_dir` from `site.toml`.

```bash
static-docs build --config <path/to/site.toml>
```

:::params
::param name="--config" type="flag" description="Path to `site.toml` or a project directory. Defaults to `site.toml`."
:::

## preview

Start the local development server with live reload.

```bash
static-docs preview --config <path/to/site.toml> --host 127.0.0.1 --port 8000
```

`serve` is an alias for `preview`.

:::params
::param name="--config" type="flag" description="Path to `site.toml` or a project directory. Defaults to `site.toml`."
::param name="--host" type="flag" description="Network interface to bind. Defaults to `127.0.0.1`."
::param name="--port" type="flag" description="Port to listen on. Defaults to `8000`."
:::

## publish

Build the site and copy the output to a destination directory.

```bash
static-docs publish --config <path/to/site.toml> --destination ./release
```

:::params
::param name="--config" type="flag" description="Path to `site.toml` or a project directory. Defaults to `site.toml`."
::param name="--destination" type="flag" description="Optional destination directory. Defaults to the configured `output_dir`."
:::

## gh-deploy

Build the site, add GitHub Pages artifacts, and force-push the output to a deploy branch.

```bash
static-docs gh-deploy --config <path/to/site.toml> --remote origin --branch gh-pages
```

:::params
::param name="--config" type="flag" description="Path to `site.toml` or a project directory. Defaults to `site.toml`."
::param name="--remote" type="flag" description="Git remote to push to. Defaults to `origin`."
::param name="--branch" type="flag" description="Branch to force-push generated output to. Defaults to `gh-pages`."
::param name="--message" type="flag" description="Commit message for the deploy commit. Defaults to `Deploy static-docs site`."
:::

## api generate

Generate Markdown API reference pages from Python source files.

```bash
static-docs api generate --source src --output content/api --package my_package
```

:::params
::param name="--source" type="flag" description="Python source directory. Defaults to `src`."
::param name="--output" type="flag" description="Directory where generated Markdown pages are written. Defaults to `content/api`."
::param name="--package" type="flag" description="Optional package prefix for generated module names."
::param name="--title" type="flag" description="Title for the generated API index page. Defaults to `API Reference`."
::param name="--include-private" type="flag" description="Include private Python objects."
::param name="--include-init" type="flag" description="Include `__init__.py` modules."
:::
