---
title: Deployment
description: Deploy Static Docs docs to GitHub Pages with GitHub Actions or the gh-deploy command.
order: 7
---

# Deployment

Static Docs supports local build output, copying builds to a release directory, GitHub Actions, and direct `gh-pages` deployment.

## Build locally

Generate static output into `output_dir`:

```bash
static-docs build --config docs/site.toml
```

You get:

:::files
docs/
    dist/
        index.html
        404.html
        .nojekyll
        sitemap.xml
        robots.txt
:::

## Publish

`publish` builds the site and copies the generated output to a destination directory.

```bash
static-docs publish --config docs/site.toml
```

Override the destination for one run:

```bash
static-docs publish --config docs/site.toml --destination ./release
```

## GitHub Actions

Create `#!yaml .github/workflows/docs.yml`:

```yaml
name: Deploy docs

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Install uv
        uses: astral-sh/setup-uv@21d5da3bc3126fc3b5b182828c8772282a6b694d # v8
        with:
          enable-cache: true
          python-version: "3.12"

      - name: Install dependencies
        run: uv sync --locked --extra dev

      - name: Build docs
        run: uv run static-docs build --config docs/site.toml

      - uses: actions/configure-pages@v6

      - uses: actions/upload-pages-artifact@v4
        with:
          path: docs/dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

## Configure GitHub Pages

In the repository settings:

1. Open **Settings**.
2. Open **Pages**.
3. Set **Source** to **GitHub Actions**.
4. Push to `main`.

## Alternative: deploy branch

```bash
static-docs gh-deploy --config docs/site.toml --branch gh-pages
```

Use this if you prefer publishing a `gh-pages` branch instead of the official Pages artifact workflow.

`gh-deploy` builds the site, adds GitHub Pages artifacts, commits the output, and force-pushes to the deploy branch.

:::callout type="warning" title="Repository access"
`gh-deploy` expects a Git repository, a configured remote, and permission to push to the target branch.
:::

Optional flags:

:::params
::param name="--remote" type="flag" description="Git remote to push to. Defaults to `origin`."
::param name="--branch" type="flag" description="Deploy branch. Defaults to `gh-pages`."
::param name="--message" type="flag" description="Commit message for the deploy commit."
:::
