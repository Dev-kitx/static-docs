---
title: Getting Started
description: Install Static Docs, create a docs project, preview locally, and build for production.
order: 1
---

# Getting Started

## Installation

Install Static Docs from PyPI:

```bash
pip install static-docs
```

For local development inside this repository:

```bash
pip install -e .
```

## Quick start

Scaffold a project, preview it with live reload, then build production output:

```bash
# 1. Scaffold a new project
static-docs init my-docs

# 2. Preview with live reload
static-docs preview --config my-docs/site.toml

# 3. Build for production
static-docs build --config my-docs/site.toml
```

You can pass either the config file or the project directory:

```bash
static-docs preview --config my-docs
```

When `--config` points at a directory, Static Docs reads `site.toml` inside that directory.

## Scaffolded files

```bash
static-docs init my-docs
```

You get:

:::files
my-docs/
    site.toml
    navigation.yml
    content/
        index.md
:::

## Build output

```bash
static-docs build --config my-docs/site.toml
```

You get:

:::files
my-docs/
    dist/
        index.html
        404.html
        sitemap.xml
        robots.txt
        llms.txt
        llms-full.txt
        assets/
            search-index.json
:::
