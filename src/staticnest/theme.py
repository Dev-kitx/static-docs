from __future__ import annotations

import json
from html import escape

from pygments.formatters import HtmlFormatter


THEME_ALIASES = {
    "staticnest": "static-docs",
    "static-docs": "static-docs",
}


THEME_PRESETS = {
    "static-docs": {
        "accent": "#2563eb",
        "bg": "#ffffff",
        "surface": "#ffffff",
        "surface_alt": "#fafafa",
        "border": "#e5e7eb",
        "text": "#111827",
        "muted": "#6b7280",
        "muted_soft": "#9ca3af",
        "active_bg": "#eff6ff",
        "active_text": "#2563eb",
        "code_bg": "#f8fafc",
        "quote_bg": "#ecfdf5",
        "quote_border": "#22c55e",
    },
}


BASE_CSS = r"""
:root {
  --accent: {{ accent }};
  --bg: {{ bg }};
  --surface: {{ surface }};
  --surface-alt: {{ surface_alt }};
  --border: {{ border }};
  --text: {{ text }};
  --muted: {{ muted }};
  --muted-soft: {{ muted_soft }};
  --active-bg: {{ active_bg }};
  --active-text: {{ active_text }};
  --code-bg: {{ code_bg }};
  --quote-bg: {{ quote_bg }};
  --quote-border: {{ quote_border }};
  --topbar-height: 60px;
  --sidebar-width: 300px;
  --toc-width: 280px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Inter", "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
}

a {
  color: inherit;
  text-decoration: none;
}

code, pre {
  font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 40;
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 1.15rem;
  height: var(--topbar-height);
  padding: 0 1.25rem;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(8px);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.86rem;
  font-weight: 700;
}

.brand-label {
  display: inline-block;
  font-size: 1rem;
  background: linear-gradient(120deg, var(--accent) 0%, color-mix(in srgb, var(--accent) 60%, white) 50%, var(--accent) 100%);
  background-size: 200% auto;
  background-position: right center;
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  transition: background-position 0.5s ease-in-out;
}

.brand:hover .brand-label {
  background-position: left center;
}

.brand-mark {
  width: 1.1rem;
  height: 1.1rem;
  border-radius: 0.3rem;
  border: 2px solid var(--text);
  transform: rotate(45deg);
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1.1rem;
  min-width: 0;
}

.top-nav-link {
  color: var(--muted);
  font-size: 0.88rem;
  font-weight: 500;
}

.top-nav-link.active {
  color: var(--text);
  font-weight: 600;
}

.top-nav-group {
  position: relative;
}

.top-nav-group summary {
  list-style: none;
  cursor: pointer;
}

.top-nav-group summary::-webkit-details-marker {
  display: none;
}

.top-nav-menu {
  position: absolute;
  top: calc(100% + 0.55rem);
  left: 0;
  min-width: 12rem;
  padding: 0.4rem;
  border: 1px solid var(--border);
  border-radius: 0.8rem;
  background: var(--surface);
  box-shadow: 0 10px 32px rgba(17, 24, 39, 0.08);
}

.top-nav-menu-link {
  display: block;
  padding: 0.55rem 0.7rem;
  border-radius: 0.55rem;
  color: var(--muted);
  font-size: 0.86rem;
}

.top-nav-menu-link:hover {
  background: var(--surface-alt);
  color: var(--text);
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  justify-content: flex-end;
  min-width: 0;
}

.search-shell {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  min-width: 280px;
  padding: 0.42rem 0.68rem;
  border: 1px solid var(--border);
  border-radius: 0.65rem;
  background: var(--surface-alt);
}

.search-shell input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  font: inherit;
  color: var(--text);
  font-size: 0.9rem;
}

.search-kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.7rem;
  height: 1.35rem;
  padding: 0 0.3rem;
  border: 1px solid var(--border);
  border-radius: 0.45rem;
  color: var(--muted);
  font-size: 0.72rem;
}

.icon-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.86rem;
  overflow: hidden;
}

.icon-link-image {
  width: 1.05rem;
  height: 1.05rem;
  object-fit: contain;
}

.layout {
  display: grid;
  grid-template-columns: var(--sidebar-width) minmax(0, 1fr) var(--toc-width);
  min-height: calc(100vh - var(--topbar-height));
}

.sidebar {
  position: sticky;
  top: var(--topbar-height);
  height: calc(100vh - var(--topbar-height));
  overflow: auto;
  padding: 1rem 0.9rem 1.75rem 1.35rem;
  border-right: 1px solid var(--border);
  background: var(--surface);
}

.sidebar-title {
  margin: 0 0 0.8rem;
  color: var(--muted-soft);
  font-size: 0.76rem;
  font-weight: 600;
}

.nav-tree,
.toc-list {
  display: grid;
  gap: 0.15rem;
}

.nav-group-label {
  margin-top: 0.9rem;
  margin-bottom: 0.35rem;
  color: #374151;
  font-size: 0.9rem;
  font-weight: 600;
}

.nav-children {
  display: grid;
  gap: 0.15rem;
}

.nav-depth-1 { margin-left: 0.4rem; }
.nav-depth-2 { margin-left: 1rem; }

.nav-link {
  display: block;
  padding: 0.52rem 0.72rem;
  border-radius: 0.55rem;
  color: #4b5563;
  font-size: 0.9rem;
}

.nav-link:hover {
  background: #f9fafb;
}

.nav-link.active {
  background: var(--active-bg);
  color: var(--active-text);
  font-weight: 600;
}

.content-shell {
  padding: 1.4rem 2.35rem 3.5rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  margin-bottom: 0.85rem;
  color: var(--muted);
  font-size: 0.84rem;
}

.breadcrumb-sep {
  color: var(--muted-soft);
}

.article-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.75rem;
}

.copy-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  color: #374151;
  font: inherit;
  cursor: pointer;
  font-size: 0.88rem;
}

.article-shell h1 {
  margin: 0 0 1.25rem;
  font-size: clamp(1.75rem, 3.15vw, 2.55rem);
  line-height: 1.05;
  letter-spacing: -0.05em;
}

.article-shell h2 {
  margin-top: 2.5rem;
  margin-bottom: 0.85rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border);
  font-size: 1.18rem;
  letter-spacing: -0.03em;
}

.article-shell h3 {
  margin-top: 1.7rem;
  margin-bottom: 0.65rem;
  font-size: 0.98rem;
}

.article-shell p,
.article-shell li,
.article-shell blockquote {
  color: #374151;
  font-size: 0.96rem;
  line-height: 1.8;
}

.article-shell ul,
.article-shell ol {
  padding-left: 1.5rem;
}

.article-shell pre {
  overflow: auto;
  margin: 0;
  padding: 1rem 1.1rem;
  border-top: 1px solid var(--border);
  background: var(--code-bg);
}

.article-shell code {
  padding: 0.16rem 0.35rem;
  border-radius: 0.35rem;
  background: #f3f4f6;
  font-size: 0.92em;
}

.article-shell pre code {
  padding: 0;
  background: transparent;
  color: #1f2937;
}

.code-block {
  margin: 1.25rem 0;
  border: 1px solid var(--border);
  border-radius: 0.85rem;
  overflow: hidden;
  background: var(--code-bg);
}

.code-block-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.7rem 0.95rem;
  background: var(--surface);
}

.code-block-language {
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.code-copy-button {
  border: 1px solid var(--border);
  border-radius: 0.55rem;
  background: var(--surface);
  color: #374151;
  padding: 0.4rem 0.65rem;
  font: inherit;
  font-size: 0.85rem;
  cursor: pointer;
}


.article-shell blockquote {
  margin: 1.5rem 0;
  padding: 1rem 1.2rem;
  border: 1px solid var(--quote-border);
  border-radius: 0.9rem;
  background: var(--quote-bg);
}

.pager {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

.pager-link {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem 1.1rem;
  border: 1px solid var(--border);
  border-radius: 0.85rem;
  background: var(--surface);
}

.pager-link.next {
  text-align: right;
}

.pager-label {
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.toc {
  position: sticky;
  top: var(--topbar-height);
  height: calc(100vh - var(--topbar-height));
  overflow: auto;
  padding: 1.7rem 1.35rem 1.8rem 1.1rem;
  border-left: 1px solid var(--border);
  background: var(--surface);
}

.toc-title {
  margin: 0 0 1rem;
  font-size: 0.84rem;
  font-weight: 700;
}

.toc-link {
  display: block;
  padding: 0.26rem 0.5rem;
  border-left: 2px solid transparent;
  color: var(--muted);
  font-size: 0.88rem;
}

.toc-link.active {
  border-left-color: var(--active-text);
  color: var(--active-text);
  font-weight: 600;
}

.toc-level-3 {
  margin-left: 0.85rem;
}

.toc-meta {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.toc-meta a {
  display: block;
  margin-top: 0.6rem;
  color: var(--muted);
  font-size: 0.86rem;
}

.search-wrapper {
  position: relative;
}

.search-results {
  display: none;
  position: absolute;
  top: calc(100% + 0.4rem);
  left: 0;
  right: 0;
  z-index: 50;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  background: var(--surface);
  box-shadow: 0 10px 32px rgba(17, 24, 39, 0.12);
}

.search-results.visible {
  display: block;
}

.search-result {
  display: block;
  padding: 0.85rem 0.95rem;
}

.search-result + .search-result {
  border-top: 1px solid var(--border);
}

.search-result-title {
  display: block;
  font-weight: 600;
}

.search-result-copy {
  display: block;
  margin-top: 0.22rem;
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.55;
}

.menu-toggle {
  display: none;
}

.not-found-shell {
  display: grid;
  gap: 0.9rem;
  max-width: 34rem;
  padding: 4rem 0 2rem;
}

.not-found-eyebrow {
  margin: 0;
  color: var(--accent);
  font-size: 0.86rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.not-found-shell h1 {
  margin: 0;
  font-size: clamp(2rem, 3vw, 2.75rem);
}

.not-found-shell p:last-of-type {
  margin: 0;
  color: var(--muted);
  font-size: 1rem;
}

.not-found-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.4rem;
}

.not-found-search {
  position: relative;
  display: grid;
  gap: 0.5rem;
  margin-top: 0.4rem;
}

.not-found-search input {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 0.85rem;
  background: var(--surface);
  color: var(--text);
  padding: 0.8rem 0.9rem;
  font: inherit;
}

.not-found-search-results {
  display: grid;
  gap: 0.25rem;
}

.not-found-empty {
  color: var(--muted);
  font-size: 0.9rem;
}

.not-found-link {
  display: inline-flex;
  align-items: center;
  padding: 0.7rem 0.95rem;
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  color: var(--text);
  font-size: 0.92rem;
  font-weight: 600;
}

.not-found-link.primary {
  border-color: var(--accent);
  background: var(--accent);
  color: #ffffff;
}

@media (max-width: 1200px) {
  .layout {
    grid-template-columns: 280px minmax(0, 1fr);
  }

  .toc {
    display: none;
  }
}

@media (max-width: 920px) {
  .topbar {
    grid-template-columns: auto 1fr;
    gap: 0.8rem;
    padding: 0 1rem;
  }

  .search-shell {
    min-width: 0;
  }

  .layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: var(--topbar-height);
    z-index: 30;
    width: min(320px, 90vw);
    transform: translateX(-101%);
    transition: transform 180ms ease;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .content-shell {
    padding: 1.25rem 1rem 3rem;
  }

  .menu-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.2rem;
    height: 2.2rem;
    border: 1px solid var(--border);
    border-radius: 0.65rem;
    background: var(--surface);
  }
}
"""


BASE_JS = r"""
const searchInput = document.querySelector('[data-search-input]');
const searchResults = document.querySelector('[data-search-results]');
const notFoundSearchInput = document.querySelector('[data-not-found-search]');
const notFoundSearchResults = document.querySelector('[data-not-found-results]');
const sidebar = document.querySelector('[data-sidebar]');
const menuToggle = document.querySelector('[data-menu-toggle]');
const copyButton = document.querySelector('[data-copy-link]');
const tocLinks = [...document.querySelectorAll('.toc-link')];
const sections = tocLinks
  .map((link) => document.querySelector(link.getAttribute('href')))
  .filter(Boolean);

if (menuToggle && sidebar) {
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
}

if (copyButton) {
  copyButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      copyButton.querySelector('span').textContent = 'Copied';
      window.setTimeout(() => {
        copyButton.querySelector('span').textContent = 'Copy page';
      }, 1200);
    } catch (_error) {
      copyButton.querySelector('span').textContent = 'Copy failed';
    }
  });
}

document.querySelectorAll('[data-code-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const block = button.closest('.code-block');
    const code = block ? block.querySelector('code') : null;
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code.textContent || '');
      button.dataset.copied = 'true';
      button.setAttribute('aria-label', 'Copied');
      window.setTimeout(() => {
        delete button.dataset.copied;
        button.setAttribute('aria-label', 'Copy code');
      }, 1200);
    } catch (_error) {
      button.setAttribute('aria-label', 'Copy failed');
    }
  });
});

let pages = [];
const inlineIndex = document.querySelector('#search-index');
if (inlineIndex) {
  try { pages = JSON.parse(inlineIndex.textContent); } catch (_e) {}
}
fetch(`${base_url}assets/search-index.json`, { cache: 'no-store' })
  .then((response) => response.ok ? response.json() : [])
  .then((index) => { if (Array.isArray(index)) pages = index; })
  .catch(() => {});

const searchMatches = (query) => {
  const normalized = query.trim().toLowerCase();
  if (!normalized) return [];
  return pages
    .map((page) => {
      const title = (page.title || '').toLowerCase();
      const summary = (page.summary || '').toLowerCase();
      const excerpt = (page.excerpt || '').toLowerCase();
      const headings = (page.headings || []).join(' ').toLowerCase();
      const content = (page.content || '').toLowerCase();
      let score = 0;
      if (title === normalized) score += 20;
      if (title.includes(normalized)) score += 10;
      if (summary.includes(normalized)) score += 6;
      if (excerpt.includes(normalized)) score += 5;
      if (headings.includes(normalized)) score += 4;
      if (content.includes(normalized)) score += 2;
      if (page.kind === 'heading' && headings.includes(normalized)) score += 8;
      return { ...page, score };
    })
    .filter((page) => page.score > 0)
    .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title))
    .slice(0, 8);
};

const resultHtml = (page) => `
  <a class="search-result" href="${page.url}">
    <span class="search-result-title">${page.title}</span>
    <span class="search-result-copy">${page.excerpt || page.summary || ''}</span>
  </a>
`;

if (searchInput && searchResults) {
  const renderMatches = (matches) => {
    searchResults.innerHTML = matches.map(resultHtml).join('');
    searchResults.classList.toggle('visible', matches.length > 0);
  };

  const focusSearch = () => {
    searchInput.focus();
    searchInput.select();
  };

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLowerCase();
    if (!query) {
      searchResults.classList.remove('visible');
      searchResults.innerHTML = '';
      return;
    }

    renderMatches(searchMatches(query));
  });

  document.addEventListener('keydown', (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      focusSearch();
    }
    if (event.key === '/' && document.activeElement !== searchInput && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName || '')) {
      event.preventDefault();
      focusSearch();
    }
  });

  document.addEventListener('click', (event) => {
    if (!searchResults.contains(event.target) && event.target !== searchInput) {
      searchResults.classList.remove('visible');
    }
  });
}

if (notFoundSearchInput && notFoundSearchResults) {
  notFoundSearchInput.addEventListener('input', () => {
    const matches = searchMatches(notFoundSearchInput.value);
    notFoundSearchResults.innerHTML = matches.length
      ? matches.map(resultHtml).join('')
      : '<p class="not-found-empty">No matches yet.</p>';
  });
}

if (sections.length) {
  function updateActiveToc() {
    const readingLine = 80;
    const atBottom = window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4;

    let active = sections[0].id;
    if (atBottom) {
      // At the bottom of the page: activate the last section
      active = sections[sections.length - 1].id;
    } else {
      // Pick the heading closest to the reading line
      let minDist = Infinity;
      sections.forEach((section) => {
        const dist = Math.abs(section.getBoundingClientRect().top - readingLine);
        if (dist < minDist) {
          minDist = dist;
          active = section.id;
        }
      });
    }

    tocLinks.forEach((link) => {
      link.classList.toggle('active', link.getAttribute('href') === `#${active}`);
    });
  }
  window.addEventListener('scroll', updateActiveToc, { passive: true });
  document.addEventListener('scroll', updateActiveToc, { passive: true });
  window.addEventListener('resize', updateActiveToc, { passive: true });
  requestAnimationFrame(updateActiveToc);
}
"""


LIVE_RELOAD_JS = r"""
(function() {
  const endpoint = "{{ live_reload_path }}";
  let version = null;
  async function check() {
    try {
      const response = await fetch(endpoint, { cache: 'no-store' });
      const payload = await response.json();
      if (version && version !== payload.version) {
        window.location.reload();
        return;
      }
      version = payload.version;
    } catch (_error) {}
  }
  setInterval(check, 1000);
  check();
})();
"""


DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ title }}</title>
    <meta name="description" content="{{ description_text }}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{{ current_url }}assets/site.css" />
    {{ custom_css_tag }}
  </head>
  <body>
    <header class="topbar">
      <div class="topbar-left">
        <button class="menu-toggle" type="button" data-menu-toggle>≡</button>
        <a class="brand" href="{{ current_url }}">
          <span class="brand-mark"></span>
          <span class="brand-label">{{ brand_name }}</span>
        </a>
      </div>
      <div class="topbar-actions">
        <nav class="top-nav">{{ top_nav_html }}</nav>
        <div class="search-wrapper">
          <label class="search-shell">
            <input type="search" placeholder="Search documentation..." data-search-input />
            <span class="search-kbd">K</span>
          </label>
          <div class="search-results" data-search-results></div>
        </div>
        {{ header_action_html }}
      </div>
    </header>
    <main class="layout">
      <aside class="sidebar" data-sidebar>
        <p class="sidebar-title">Documentation</p>
        <nav class="nav-tree">{{ nav_html }}</nav>
      </aside>
      <section class="content-shell">
        <div class="breadcrumbs">{{ breadcrumbs_html }}</div>
        <div class="article-toolbar">
          <button class="copy-link" type="button" data-copy-link><span>Copy page</span></button>
        </div>
        <article class="article-shell">
          {{ page_heading_html }}
          {{ article_html }}
          {{ pager_html }}
        </article>
      </section>
      <aside class="toc">
        <p class="toc-title">On This Page</p>
        <nav class="toc-list">{{ toc_html }}</nav>
        <div class="toc-meta">
          <a href="{{ feedback_url }}">Question? Give us feedback</a>
          <a href="{{ github_url }}">Edit this page on GitHub</a>
        </div>
      </aside>
    </main>
    <script id="search-index" type="application/json">{{ search_json }}</script>
    <script>{{ base_js }}</script>
    {{ custom_js_tag }}
    {{ live_reload_tag }}
  </body>
</html>
"""


NOT_FOUND_ARTICLE_HTML = """
<div class="not-found-shell">
  <p class="not-found-eyebrow">404</p>
  <h1>Page not found</h1>
  <p>The page you requested does not exist or may have moved.</p>
  <label class="not-found-search">
    <span class="sr-only">Search documentation</span>
    <input type="search" placeholder="Search documentation..." data-not-found-search />
    <div class="not-found-search-results" data-not-found-results></div>
  </label>
  <div class="not-found-actions">
    <a class="not-found-link primary" href="{{ current_url }}">Go home</a>
    <a class="not-found-link" href="{{ current_url }}docs/getting-started/">Open getting started</a>
  </div>
</div>
"""


STATICNEST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <script>const base_url = "{{ current_url }}";</script>
    <script>
      const storageKey = "theme";
      const getThemePreference = () => localStorage.getItem(storageKey) || "light";
      const syncThemeControls = (theme) => {
        document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
          const isDark = theme === "dark";
          button.setAttribute("aria-checked", String(isDark));
          button.setAttribute("title", isDark ? "Switch to light theme" : "Switch to dark theme");
        });
      };
      const applyTheme = (theme) => {
        document.documentElement.classList.toggle("dark", theme === "dark");
        syncThemeControls(theme);
      };
      applyTheme(getThemePreference());
      function onThemeSwitch() {
        const next = document.documentElement.classList.contains("dark") ? "light" : "dark";
        localStorage.setItem(storageKey, next);
        applyTheme(next);
      }
      function toggleLayout() {}
      function onMobileMenuButtonClick(event) {
        const body = document.getElementById("inner-body");
        body?.classList.toggle("mobile-sidebar-open");
        event.currentTarget?.setAttribute("data-state", body?.classList.contains("mobile-sidebar-open") ? "open" : "closed");
      }
      function deferSetActiveTocLink(href) {
        requestAnimationFrame(() => {
          document.querySelectorAll("#toc a").forEach((link) => {
            link.dataset.active = String(link.getAttribute("href") === href);
          });
        });
      }
      const toc = { observer: { observe() {} } };
      document.addEventListener("DOMContentLoaded", () => applyTheme(getThemePreference()));
    </script>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ title }}</title>
    <meta name="description" content="{{ description_text }}" />
    <link rel="canonical" href="{{ canonical_url }}" />
    <meta property="og:type" content="{{ og_type }}" />
    <meta property="og:title" content="{{ title }}" />
    <meta property="og:description" content="{{ description_text }}" />
    <meta property="og:url" content="{{ canonical_url }}" />
    <meta property="og:site_name" content="{{ brand_name }}" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{{ title }}" />
    <meta name="twitter:description" content="{{ description_text }}" />
    <link href="{{ current_url }}assets/img/favicon.ico" rel="icon" />
    <link href="{{ current_url }}assets/css/base.css" rel="stylesheet" />
    <link href="{{ current_url }}assets/css/geist.css" rel="stylesheet" />
    <style>
      :root { --theme-accent: {{ theme_accent }}; }
      .mobile-sidebar-open [data-slot="sidebar"] { display: flex; position: fixed; inset: var(--header-height) auto 0 0; z-index: 60; width: min(80vw, 280px); background: var(--background); padding-left: 1rem; }
      .staticnest-search { width: 8.5rem; }
      .staticnest-search-results { display: none; position: absolute; top: calc(100% + .4rem); right: 0; z-index: 90; width: min(28rem, 80vw); max-height: 24rem; overflow: auto; padding: .35rem; border: 1px solid var(--border); border-radius: .75rem; background: var(--popover); color: var(--popover-foreground); box-shadow: 0 20px 50px rgba(0, 0, 0, .14); }
      .staticnest-search-results.visible { display: grid; gap: .15rem; }
      .staticnest-search-results .search-result { display: grid; gap: .15rem; padding: .65rem .7rem; border-radius: .55rem; text-decoration: none; }
      .staticnest-search-results .search-result:hover { background: var(--accent); }
      .staticnest-search-results .search-result-title { color: var(--foreground); font-size: .9rem; font-weight: 600; }
      .staticnest-search-results .search-result-copy { color: var(--muted-foreground); font-size: .78rem; line-height: 1.35; }
      .top-nav { display: none; align-items: center; gap: .25rem; }
      .top-nav-link { appearance: none; display: inline-flex; align-items: center; height: 2rem; padding-inline: .75rem; border: 0; border-radius: .5rem; background: transparent; color: var(--muted-foreground); font-size: .875rem; font-weight: 500; transition: color .15s ease, background-color .15s ease; cursor: pointer; }
      .top-nav-link:hover { background: var(--accent); color: var(--accent-foreground); }
      .top-nav-group { position: relative; }
      .top-nav-menu { display: none; position: absolute; top: calc(100% + .35rem); left: 0; z-index: 80; min-width: 12rem; padding: .35rem; border: 1px solid var(--border); border-radius: .75rem; background: var(--popover); color: var(--popover-foreground); box-shadow: 0 16px 40px rgba(0, 0, 0, .12); }
      .top-nav-group[data-open="true"] .top-nav-menu { display: block; }
      .top-nav-menu-link { display: block; padding: .5rem .65rem; border-radius: .5rem; color: var(--muted-foreground); font-size: .875rem; white-space: nowrap; }
      .top-nav-menu-link:hover { background: var(--accent); color: var(--accent-foreground); }
      .icon-link { display: inline-flex; align-items: center; justify-content: center; width: 2rem; height: 2rem; border-radius: .5rem; color: var(--foreground); transition: background-color .15s ease; overflow: hidden; }
      .icon-link:hover { background: var(--accent); }
      .icon-link-image { width: 1.1rem; height: 1.1rem; object-fit: contain; }
      .theme-toggle { appearance: none; display: inline-flex; align-items: center; width: 2.35rem; height: 1.35rem; padding: .15rem; border: 1px solid var(--border); border-radius: 999px; background: var(--muted); color: var(--foreground); cursor: pointer; transition: background-color .15s ease, border-color .15s ease; }
      .theme-toggle:hover { background: var(--accent); }
      .theme-toggle:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
      .theme-toggle-thumb { width: .95rem; height: .95rem; border-radius: 999px; background: var(--background); box-shadow: 0 1px 2px rgba(0, 0, 0, .18); transform: translateX(0); transition: transform .18s ease, background-color .18s ease; }
      .dark .theme-toggle { background: var(--primary); border-color: var(--primary); }
      .dark .theme-toggle-thumb { background: var(--primary-foreground); transform: translateX(1rem); }
      @media (min-width: 768px) { .top-nav { display: flex; } .staticnest-search { width: 12rem; } }
      .code-block { margin-block: 1.5rem; overflow: hidden; border: 0; border-radius: 1rem; background: #f7f7f8; color: #1f2937; }
      .code-block-header { display: flex; align-items: center; justify-content: space-between; padding: 1.15rem 1.25rem .45rem; color: #6b7280; font-size: .9rem; background: transparent; }
      .code-block-meta { display: inline-flex; align-items: center; gap: .6rem; min-width: 0; }
      .code-block-language { opacity: .95; }
      .code-block-title { color: #1f2937; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .code-copy-button { appearance: none; display: inline-flex; align-items: center; justify-content: center; width: 1.5rem; height: 1.5rem; margin: 0; padding: 0; border: 0 !important; border-radius: 0; background: transparent !important; box-shadow: none !important; color: #111827; cursor: pointer; outline: 0; pointer-events: auto; }
      .code-copy-button:hover,
      .code-copy-button:focus,
      .code-copy-button:focus-visible,
      .code-copy-button:active,
      .code-copy-button[data-copied="true"] { background: transparent !important; box-shadow: none !important; outline: 0; }
      .code-copy-button svg { width: 1.08rem; height: 1.08rem; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
      .code-check-icon { display: none; }
      .code-copy-button[data-copied="true"] .code-copy-icon { display: none; }
      .code-copy-button[data-copied="true"] .code-check-icon { display: block; }
      .code-block .codehilite { margin: 0; background: transparent; }
      .code-block pre { margin: 0; padding: .85rem 1.25rem 1.45rem; overflow: auto; background: transparent !important; }
      .code-block code { border: 0 !important; background: transparent !important; color: inherit; padding: 0; }
      .code-block .hll { display: block; margin-inline: -1.25rem; padding-inline: 1.25rem; background: color-mix(in oklab, #1f6feb 12%, transparent); }
      .codehilite { color: #1f2937; }
      .codehilite .c, .codehilite .c1, .codehilite .cm, .codehilite .cp, .codehilite .cpf { color: #6b7280; font-style: italic; }
      .codehilite .k, .codehilite .kd, .codehilite .kn, .codehilite .kp, .codehilite .kr, .codehilite .kt { color: #dc2626; }
      .codehilite .ow { color: #7c3aed; }
      .codehilite .n, .codehilite .nx, .codehilite .nv, .codehilite .vi, .codehilite .vm { color: #7c3aed; }
      .codehilite .nf, .codehilite .fm { color: #075bc2; }
      .codehilite .nb, .codehilite .bp { color: #9a3412; }
      .codehilite .s, .codehilite .s1, .codehilite .s2, .codehilite .sa, .codehilite .sb, .codehilite .sc, .codehilite .sd, .codehilite .se, .codehilite .sh, .codehilite .si, .codehilite .sx, .codehilite .sr, .codehilite .ss, .codehilite .dl { color: #075bc2; }
      .codehilite .m, .codehilite .mi, .codehilite .mf, .codehilite .mh, .codehilite .mo, .codehilite .il { color: #075bc2; }
      .codehilite .o { color: #15803d; }
      .codehilite .p, .codehilite .pm { color: #1f2937; }
      .codehilite .nt { color: #166534; }
      .codehilite .na { color: #075bc2; }
      .codehilite .l, .codehilite .l-Scalar, .codehilite .l-Scalar-Plain { color: #9a3412; }
      .dark .code-block { background: #0b1118; color: #d6dee8; }
      .dark .code-block-header { color: #9aa4b2; }
      .dark .code-block-title { color: #f8fafc; }
      .dark .code-copy-button { color: #f8fafc; }
      .dark .code-block .hll { background: color-mix(in oklab, #79c0ff 16%, transparent); }
      .dark .code-copy-button:hover,
      .dark .code-copy-button:focus,
      .dark .code-copy-button:focus-visible,
      .dark .code-copy-button:active,
      .dark .code-copy-button[data-copied="true"] { background: transparent !important; box-shadow: none !important; outline: 0; }
      .dark .codehilite { color: #d6dee8; }
      .dark .codehilite .c, .dark .codehilite .c1, .dark .codehilite .cm, .dark .codehilite .cp, .dark .codehilite .cpf { color: #8b98a9; font-style: italic; }
      .dark .codehilite .k, .dark .codehilite .kd, .dark .codehilite .kn, .dark .codehilite .kp, .dark .codehilite .kr, .dark .codehilite .kt { color: #ff7b72; }
      .dark .codehilite .ow { color: #d2a8ff; }
      .dark .codehilite .n, .dark .codehilite .nx, .dark .codehilite .nv, .dark .codehilite .vi, .dark .codehilite .vm { color: #d2a8ff; }
      .dark .codehilite .nf, .dark .codehilite .fm { color: #79c0ff; }
      .dark .codehilite .nb, .dark .codehilite .bp { color: #ffa657; }
      .dark .codehilite .s, .dark .codehilite .s1, .dark .codehilite .s2, .dark .codehilite .sa, .dark .codehilite .sb, .dark .codehilite .sc, .dark .codehilite .sd, .dark .codehilite .se, .dark .codehilite .sh, .dark .codehilite .si, .dark .codehilite .sx, .dark .codehilite .sr, .dark .codehilite .ss, .dark .codehilite .dl { color: #a5d6ff; }
      .dark .codehilite .m, .dark .codehilite .mi, .dark .codehilite .mf, .dark .codehilite .mh, .dark .codehilite .mo, .dark .codehilite .il { color: #79c0ff; }
      .dark .codehilite .o { color: #7ee787; }
      .dark .codehilite .p, .dark .codehilite .pm { color: #d6dee8; }
      .dark .codehilite .nt { color: #7ee787; }
      .dark .codehilite .na { color: #79c0ff; }
      .dark .codehilite .l, .dark .codehilite .l-Scalar, .dark .codehilite .l-Scalar-Plain { color: #ffa657; }
      .mermaid-block { margin-block: 1.5rem; overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); padding: 1rem; }
      .mermaid { display: flex; justify-content: center; min-width: max-content; }
      .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 1rem; margin-block: 1.25rem; }
      .card { border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem; background: var(--card); color: var(--card-foreground); }
      .card-title { margin: 0 0 .35rem; font-weight: 600; }
      .card-description { color: var(--muted-foreground); font-size: .9rem; }
      .badges { display: flex; flex-wrap: wrap; gap: .5rem; margin-block: 1rem; }
      .badge { display: inline-flex; align-items: center; width: fit-content; border: 1px solid var(--border); border-radius: 999px; padding: .18rem .6rem; background: color-mix(in oklab, var(--muted) 70%, transparent); color: var(--foreground); font-size: .78rem; font-weight: 600; line-height: 1.4; }
      .badge-info { border-color: color-mix(in oklab, var(--theme-accent) 38%, var(--border)); color: var(--theme-accent); background: color-mix(in oklab, var(--theme-accent) 10%, transparent); }
      .badge-success { border-color: color-mix(in oklab, #16a34a 40%, var(--border)); color: #15803d; background: color-mix(in oklab, #16a34a 10%, transparent); }
      .badge-warning { border-color: color-mix(in oklab, #d97706 42%, var(--border)); color: #b45309; background: color-mix(in oklab, #d97706 11%, transparent); }
      .badge-danger { border-color: color-mix(in oklab, #dc2626 42%, var(--border)); color: #b91c1c; background: color-mix(in oklab, #dc2626 10%, transparent); }
      .dark .badge-success { color: #4ade80; }
      .dark .badge-warning { color: #fbbf24; }
      .dark .badge-danger { color: #f87171; }
      .page-meta { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; margin-top: .15rem; }
      .page-badge, .page-status { display: inline-flex; align-items: center; width: fit-content; border: 1px solid var(--border); border-radius: 999px; padding: .16rem .55rem; font-size: .75rem; font-weight: 650; line-height: 1.35; }
      .page-badge { background: color-mix(in oklab, var(--muted) 70%, transparent); color: var(--foreground); }
      .page-status-new { border-color: color-mix(in oklab, #16a34a 40%, var(--border)); color: #15803d; background: color-mix(in oklab, #16a34a 10%, transparent); }
      .page-status-beta { border-color: color-mix(in oklab, #d97706 42%, var(--border)); color: #b45309; background: color-mix(in oklab, #d97706 11%, transparent); }
      .page-status-deprecated { border-color: color-mix(in oklab, #dc2626 42%, var(--border)); color: #b91c1c; background: color-mix(in oklab, #dc2626 10%, transparent); }
      .dark .page-status-new { color: #4ade80; }
      .dark .page-status-beta { color: #fbbf24; }
      .dark .page-status-deprecated { color: #f87171; }
      .steps { list-style: none; margin: 1.5rem 0; padding: 0; }
      .step { position: relative; margin-left: .65rem; padding: 0 0 1.25rem 2rem; border-left: 1px solid var(--border); }
      .step:last-child { border-left-color: transparent; padding-bottom: 0; }
      .step-marker { position: absolute; left: -.65rem; top: .05rem; display: inline-flex; width: 1.3rem; height: 1.3rem; align-items: center; justify-content: center; border-radius: 999px; border: 1px solid var(--border); background: var(--background); color: var(--muted-foreground); font-size: .72rem; font-weight: 700; line-height: 1; }
      .step-title { margin: 0 0 .25rem; font-size: 1rem; font-weight: 650; line-height: 1.35; }
      .step-description { margin: 0; color: var(--muted-foreground); }
      .params { margin-block: 1.25rem; overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); }
      .params table { width: 100%; border-collapse: collapse; margin: 0; font-size: .9rem; }
      .params th, .params td { padding: .8rem .95rem; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
      .params th { color: var(--muted-foreground); font-size: .78rem; font-weight: 650; text-transform: uppercase; letter-spacing: .02em; }
      .params tbody tr:last-child td { border-bottom: 0; }
      .params code { white-space: nowrap; }
      .param-required, .param-optional { display: inline-flex; border-radius: 999px; padding: .12rem .5rem; font-size: .72rem; font-weight: 650; line-height: 1.35; }
      .param-required { color: #b91c1c; background: color-mix(in oklab, #dc2626 10%, transparent); }
      .param-optional { color: var(--muted-foreground); background: color-mix(in oklab, var(--muted) 70%, transparent); }
      .dark .param-required { color: #f87171; }
      .callout, .files { margin-block: 1.25rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); padding: 1rem; }
      .callout { display: flex; gap: .85rem; align-items: flex-start; }
      .callout-icon { display: inline-flex; width: 1.25rem; height: 1.25rem; flex: 0 0 auto; margin-top: .08rem; color: var(--theme-accent); }
      .callout-icon svg { width: 1.25rem; height: 1.25rem; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
      .callout-title { font-weight: 600; }
      .callout-description { color: var(--muted-foreground); }
      .callout-info { border-color: color-mix(in oklab, #1f6feb 55%, var(--border)); background: color-mix(in oklab, #1f6feb 10%, var(--card)); color: #1f6feb; }
      .callout-info .callout-icon { color: #1f6feb; }
      .callout-info .callout-title,
      .callout-info .callout-description { color: #1f6feb; }
      .callout-warning { border-color: color-mix(in oklab, #9a6700 58%, var(--border)); background: color-mix(in oklab, #bf8700 10%, var(--card)); color: #9a6700; }
      .callout-warning .callout-icon { color: #9a6700; }
      .callout-warning .callout-title,
      .callout-warning .callout-description { color: #9a6700; }
      .callout-success { border-color: color-mix(in oklab, #1a7f37 58%, var(--border)); background: color-mix(in oklab, #1a7f37 10%, var(--card)); color: #1a7f37; }
      .callout-success .callout-icon { color: #1a7f37; }
      .callout-success .callout-title,
      .callout-success .callout-description { color: #1a7f37; }
      .callout-danger { border-color: color-mix(in oklab, #cf222e 58%, var(--border)); background: color-mix(in oklab, #cf222e 10%, var(--card)); color: #cf222e; }
      .callout-danger .callout-icon { color: #cf222e; }
      .callout-danger .callout-title,
      .callout-danger .callout-description { color: #cf222e; }
      .callout-note { border-color: #8b5cf6 !important; background: #eadcff !important; color: var(--foreground); }
      .callout-note .callout-icon { color: #8250df; }
      .callout-note .callout-title,
      .callout-note .callout-description { color: var(--foreground); }
      .dark .callout-info { border-color: #1f6feb; background: color-mix(in oklab, #1f6feb 22%, transparent); }
      .dark .callout-info .callout-icon,
      .dark .callout-info .callout-title,
      .dark .callout-info .callout-description { color: #58a6ff; }
      .dark .callout-warning { border-color: #9a6700; background: color-mix(in oklab, #9a6700 20%, transparent); }
      .dark .callout-warning .callout-icon,
      .dark .callout-warning .callout-title,
      .dark .callout-warning .callout-description { color: #d29922; }
      .dark .callout-success { border-color: #238636; background: color-mix(in oklab, #238636 24%, transparent); }
      .dark .callout-success .callout-icon,
      .dark .callout-success .callout-title,
      .dark .callout-success .callout-description { color: #3fb950; }
      .dark .callout-danger { border-color: #da3633; background: color-mix(in oklab, #da3633 24%, transparent); }
      .dark .callout-danger .callout-icon,
      .dark .callout-danger .callout-title,
      .dark .callout-danger .callout-description { color: #f85149; }
      .dark .callout-note { border-color: #a371f7 !important; background: color-mix(in oklab, #a371f7 24%, transparent) !important; }
      .dark .callout-note .callout-icon { color: #a371f7; }
      .dark .callout-note .callout-title,
      .dark .callout-note .callout-description { color: #d8b9ff; }
      .files { width: fit-content; min-width: 16rem; padding: .9rem 1rem; border-radius: .75rem; }
      .file-tree { color: var(--foreground); }
      .file-tree-folder { margin: 0; }
      .file-tree-folder,
      .file-tree-folder[open],
      .file-tree-children { border: 0 !important; background: transparent !important; box-shadow: none !important; padding: 0 !important; }
      .file-tree-folder,
      .file-tree-children,
      .file-tree-row { margin: 0 !important; }
      .file-tree .file-tree-folder > summary,
      .file-tree .file-tree-folder[open] > summary { list-style: none; cursor: pointer; margin: 0 !important; margin-bottom: 0 !important; padding: .18rem 0 .18rem calc(var(--file-depth) * 1.15rem) !important; }
      .file-tree .file-tree-folder + .file-tree-folder,
      .file-tree .file-tree-file-row + .file-tree-folder { margin-top: 0 !important; }
      .file-tree-folder > summary::-webkit-details-marker { display: none; }
      .file-tree-row { display: flex; align-items: center; gap: .6rem; min-height: 1.75rem; padding-block: .18rem; padding-left: calc(var(--file-depth) * 1.15rem); color: var(--foreground); font-family: var(--font-sans); font-size: .95rem; line-height: 1.35; }
      .file-tree-row:hover { color: var(--theme-accent); }
      .file-tree-icon { display: inline-flex; width: 1rem; height: 1rem; flex: 0 0 auto; color: currentColor; background-color: currentColor; }
      .file-tree-folder-icon { -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.5l-2-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2Z'/%3E%3C/svg%3E") center / contain no-repeat; mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.5l-2-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2Z'/%3E%3C/svg%3E") center / contain no-repeat; }
      .file-tree-file-icon { -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/%3E%3Cpath d='M14 2v4a2 2 0 0 0 2 2h4'/%3E%3Cpath d='M10 13h4'/%3E%3Cpath d='M10 17h4'/%3E%3C/svg%3E") center / contain no-repeat; mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/%3E%3Cpath d='M14 2v4a2 2 0 0 0 2 2h4'/%3E%3Cpath d='M10 13h4'/%3E%3Cpath d='M10 17h4'/%3E%3C/svg%3E") center / contain no-repeat; }
      .tabs { margin-block: 1.25rem; overflow: hidden; padding: 0; border: 0; border-radius: 0; background: transparent; }
      .tabs-list { display: flex; gap: 2rem; align-items: flex-end; border-bottom: 1px solid var(--border); padding-inline: 0; background: transparent; }
      .tabs-trigger { appearance: none; position: relative; border: 0 !important; border-bottom: 3px solid transparent !important; border-radius: 0 !important; background: transparent !important; color: var(--muted-foreground) !important; padding: .45rem .65rem .55rem !important; font-size: .95rem; font-weight: 600; line-height: 1.15; cursor: pointer; }
      .tabs-trigger.active { color: var(--foreground) !important; border-bottom-color: var(--foreground) !important; }
      .tabs-trigger.active::before { content: ""; position: absolute; inset: .15rem .35rem auto; height: calc(100% - .7rem); z-index: -1; border-radius: .65rem; background: color-mix(in oklab, var(--muted) 65%, transparent); }
      .tabs-panel { margin-top: 1.25rem; padding: 1.1rem 1.25rem; border-radius: .8rem; background: color-mix(in oklab, var(--muted) 45%, transparent); }
      .tabs-panel[hidden] { display: none; }
      .toc-snake-list { --snake-y: .35rem; --snake-height: 1.2rem; position: relative; display: flex; flex-direction: column; gap: .48rem; padding-left: 2.1rem; }
      .toc-snake-rail { position: absolute; left: .65rem; top: .35rem; bottom: .35rem; width: 1px; border-radius: 999px; background: var(--border); }
      .toc-snake-indicator { position: absolute; left: .65rem; top: var(--snake-y); width: 1px; height: var(--snake-height); border-radius: 999px; background: var(--theme-accent); transform: translateY(0); transition: top .22s ease, height .22s ease; }
      .toc-snake-indicator::after { content: ""; position: absolute; left: 50%; bottom: 0; width: .4rem; height: .4rem; border-radius: 999px; background: var(--theme-accent); transform: translate(-50%, 50%); }
      .toc-snake-list[data-direction="up"] .toc-snake-indicator::after { top: 0; bottom: auto; transform: translate(-50%, -50%); }
      .toc-snake-list[data-direction="down"] .toc-snake-indicator::after { top: auto; bottom: 0; transform: translate(-50%, 50%); }
      .staticnest-toc-link { display: block; line-height: 1.25rem; }
      .staticnest-toc-link[data-active="true"] { color: var(--theme-accent) !important; font-weight: 600; }
      .toc-snake-list:not(:has(.staticnest-toc-link)) .toc-snake-rail,
      .toc-snake-list:not(:has(.staticnest-toc-link)) .toc-snake-indicator { display: none; }
      .heading-with-anchor { position: relative; display: flex; align-items: center; gap: .45rem; scroll-margin-top: calc(var(--header-height) + 1.25rem); }
      .heading-anchor { appearance: none; display: inline-flex; width: 1.35rem; height: 1.35rem; align-items: center; justify-content: center; border: 0; border-radius: .4rem; background: transparent; color: var(--muted-foreground); opacity: 0; cursor: pointer; transition: opacity .15s ease, color .15s ease, background-color .15s ease; }
      .heading-with-anchor:hover .heading-anchor, .heading-anchor:focus-visible, .heading-anchor[data-copied="true"] { opacity: 1; }
      .heading-anchor:hover { background: var(--muted); color: var(--foreground); }
      .heading-anchor svg { width: .9rem; height: .9rem; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
      .heading-anchor[data-copied="true"] { color: var(--theme-accent); }
    </style>
  </head>
  <body class="text-foreground group/body overscroll-none font-sans antialiased [--footer-height:calc(var(--spacing)*14)] [--header-height:calc(var(--spacing)*14)] xl:[--footer-height:calc(var(--spacing)*24)] theme-default">
    <div class="bg-background relative z-10 flex min-h-svh flex-col" id="inner-body">
      <header class="bg-background sticky top-0 z-50 w-full" view-transition-name="header">
        <div class="container-wrapper 3xl:fixed:px-0 px-6">
          <div class="3xl:fixed:container flex h-(--header-height) items-center gap-2 **:data-[slot=separator]:!h-4">
            <button id="menu-button" data-slot="popover-trigger" onclick="onMobileMenuButtonClick(event)"
              class="group whitespace-nowrap rounded-md text-sm font-medium transition-all hover:text-accent-foreground px-4 py-2 has-[&gt;svg]:px-3 extend-touch-target h-8 touch-manipulation items-center justify-start gap-2.5 !p-0 hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 active:bg-transparent dark:hover:bg-transparent flex lg:hidden"
              type="button" aria-haspopup="dialog" aria-expanded="false" data-state="closed">
              <div class="relative flex h-8 w-4 items-center justify-center">
                <div class="relative size-4">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="0" x2="16" y1="5" y2="5"></line>
                    <line x1="0" x2="16" y1="11" y2="11"></line>
                  </svg>
                </div>
                <span class="sr-only">Toggle Menu</span>
              </div>
              <span class="flex h-8 items-center text-lg leading-none font-medium">Menu</span>
            </button>
            <a data-slot="button" class="items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all hover:bg-accent hover:text-accent-foreground hidden h-8 lg:flex" href="{{ current_url }}">
              <span class="size-8 flex flex-row justify-center items-center">
                <svg class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
              </span>
              <h1 class="pr-2">{{ brand_name }}</h1>
            </a>
            <div class="ml-auto flex items-center gap-2 md:flex-1 md:justify-end">
              <nav class="top-nav">{{ top_nav_html }}</nav>
              <label class="relative block">
                <span class="sr-only">Search</span>
                <input class="staticnest-search h-8 rounded-md border border-input bg-background px-3 text-sm" type="search" placeholder="Search..." data-search-input />
                <div class="staticnest-search-results" data-search-results></div>
              </label>
              <div data-orientation="vertical" role="none" data-slot="separator" class="bg-border shrink-0 data-[orientation=vertical]:h-full data-[orientation=vertical]:w-px"></div>
              {{ header_action_html }}
              <button class="theme-toggle" type="button" role="switch" aria-checked="false" data-theme-toggle title="Toggle theme" onclick="onThemeSwitch(event)">
                <span class="theme-toggle-thumb" aria-hidden="true"></span>
                <span class="sr-only">Toggle theme</span>
              </button>
            </div>
          </div>
        </div>
      </header>
      <main class="flex flex-1 flex-col">
        <div class="container-wrapper flex flex-1 flex-col px-2">
          <div class="group/sidebar-wrapper has-data-[variant=inset]:bg-sidebar flex w-full 3xl:fixed:container 3xl:fixed:px-3 min-h-min flex-1 items-start px-0 [--sidebar-width:220px] [--top-spacing:0] lg:grid lg:grid-cols-[var(--sidebar-width)_minmax(0,1fr)] lg:[--sidebar-width:240px] lg:[--top-spacing:calc(var(--spacing)*4)]" data-slot="sidebar-wrapper" style="--sidebar-width:calc(var(--spacing) * 72);--sidebar-width-icon:3rem;{{ sidebar_grid_style }}">
            {{ sidebar_html }}
            <div class="h-full w-full">
              <div class="flex items-stretch text-[1.05rem] sm:text-[15px] xl:w-full" data-slot="docs">
                <div class="flex min-w-0 flex-1 flex-col">
                  <div class="h-(--top-spacing) shrink-0"></div>
                  <article class="w-full" view-transition-name="page">
                    <div class="flex flex-col gap-2">
                      <div class="flex flex-col gap-2">
                        <div id="page-header" class="flex items-start justify-between">
                          <h1 class="scroll-m-20 text-4xl font-semibold tracking-tight sm:text-3xl xl:text-4xl">{{ page_title }}</h1>
                          <div class="flex items-center gap-2 pt-1.5">
                            <button data-slot="button" class="inline-flex items-center justify-center rounded-md text-sm font-medium bg-secondary text-secondary-foreground hover:bg-secondary/80 px-3 h-8 shadow-none" type="button" data-copy-link><span>Copy</span></button>
                          </div>
                        </div>
                        {{ page_meta_html }}
                        <p id="summary" class="text-muted-foreground text-[1.05rem] text-balance sm:text-base">{{ page_summary }}</p>
                      </div>
                    </div>
                    <div class="typography w-full flex-1 *:data-[slot=alert]:first:mt-0">{{ article_html }}</div>
                  </article>
                  {{ pager_html }}
                </div>
                {{ toc_sidebar_html }}
              </div>
            </div>
          </div>
        </div>
      </main>
      <footer view-transition-name="footer" class="group-has-[.section-soft]/body:bg-surface/40 3xl:fixed:bg-transparent dark:bg-transparent">
        <div class="container-wrapper px-4 xl:px-6">
          <div class="flex h-(--footer-height) items-center justify-between"></div>
        </div>
      </footer>
    </div>
    <script>{{ base_js }}</script>
    <script>
      document.querySelectorAll('.tabs').forEach((tabs) => {
        const triggers = Array.from(tabs.querySelectorAll('.tabs-trigger'));
        const panels = Array.from(tabs.querySelectorAll('.tabs-panel'));
        triggers.forEach((trigger) => {
          trigger.addEventListener('click', () => {
            const target = trigger.dataset.tabTarget;
            triggers.forEach((item) => item.classList.toggle('active', item === trigger));
            panels.forEach((panel) => {
              const active = panel.id === target;
              panel.classList.toggle('active', active);
              panel.hidden = !active;
            });
          });
        });
      });
      const topNavGroups = Array.from(document.querySelectorAll('.top-nav-group'));
      const closeTopNavGroups = () => {
        topNavGroups.forEach((group) => {
          group.dataset.open = 'false';
          group.querySelector('[data-top-nav-trigger]')?.setAttribute('aria-expanded', 'false');
        });
      };
      topNavGroups.forEach((group) => {
        const trigger = group.querySelector('[data-top-nav-trigger]');
        trigger?.addEventListener('click', (event) => {
          event.stopPropagation();
          const willOpen = group.dataset.open !== 'true';
          closeTopNavGroups();
          group.dataset.open = String(willOpen);
          trigger.setAttribute('aria-expanded', String(willOpen));
        });
      });
      document.addEventListener('click', closeTopNavGroups);
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') closeTopNavGroups();
      });
      document.querySelectorAll('[data-heading-anchor]').forEach((button) => {
        button.addEventListener('click', async (event) => {
          event.preventDefault();
          event.stopPropagation();
          const sectionId = button.dataset.headingAnchor;
          if (!sectionId) return;
          const url = `${window.location.origin}${window.location.pathname}#${sectionId}`;
          try {
            await navigator.clipboard.writeText(url);
            button.dataset.copied = 'true';
            button.setAttribute('aria-label', 'Copied section link');
            window.setTimeout(() => {
              delete button.dataset.copied;
              button.setAttribute('aria-label', 'Copy section link');
            }, 1200);
          } catch (_error) {
            window.location.hash = sectionId;
          }
        });
      });
      const tocSnake = document.querySelector('[data-toc-snake]');
      if (tocSnake) {
        const tocLinks = Array.from(tocSnake.querySelectorAll('.staticnest-toc-link'));
        const headingTargets = tocLinks
          .map((link) => document.querySelector(link.getAttribute('href')))
          .filter(Boolean);
        let lastScrollY = window.scrollY;
        let activeTocLink = null;
        let settleSnakeTimer = 0;
        let dragUntil = 0;
        const syncTocSnake = () => {
          if (!tocLinks.length || !headingTargets.length) return;
          const currentScrollY = window.scrollY;
          if (currentScrollY !== lastScrollY) {
            tocSnake.dataset.direction = currentScrollY < lastScrollY ? 'up' : 'down';
            lastScrollY = currentScrollY;
          } else if (!tocSnake.dataset.direction) {
            tocSnake.dataset.direction = 'down';
          }
          let activeId = headingTargets[0].id;
          if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) {
            activeId = headingTargets[headingTargets.length - 1].id;
          } else {
            let closestDistance = Infinity;
            headingTargets.forEach((heading) => {
              const distance = Math.abs(heading.getBoundingClientRect().top - 96);
              if (distance < closestDistance) {
                closestDistance = distance;
                activeId = heading.id;
              }
            });
          }
          const activeLink = tocLinks.find((link) => link.getAttribute('href') === `#${activeId}`) || tocLinks[0];
          tocLinks.forEach((link) => link.dataset.active = String(link === activeLink));
          const listRect = tocSnake.getBoundingClientRect();
          const linkRect = activeLink.getBoundingClientRect();
          const nextY = linkRect.top - listRect.top + 2;
          const nextHeight = Math.max(18, linkRect.height - 4);
          const previousLink = activeTocLink;
          const activeChanged = previousLink && previousLink !== activeLink;
          if (activeChanged) {
            window.clearTimeout(settleSnakeTimer);
            const previousRect = previousLink.getBoundingClientRect();
            const previousY = previousRect.top - listRect.top + 2;
            const previousHeight = Math.max(18, previousRect.height - 4);
            const movingUp = nextY < previousY;
            tocSnake.dataset.direction = movingUp ? 'up' : 'down';
            const dragY = movingUp ? nextY : previousY;
            const dragHeight = movingUp
              ? previousY - nextY + previousHeight
              : nextY - previousY + nextHeight;
            tocSnake.style.setProperty('--snake-y', `${dragY}px`);
            tocSnake.style.setProperty('--snake-height', `${dragHeight}px`);
            dragUntil = Date.now() + 420;
            settleSnakeTimer = window.setTimeout(() => {
              if (activeTocLink === activeLink) {
                tocSnake.style.setProperty('--snake-y', `${nextY}px`);
                tocSnake.style.setProperty('--snake-height', `${nextHeight}px`);
              }
            }, 420);
          } else {
            if (Date.now() >= dragUntil) {
              tocSnake.style.setProperty('--snake-y', `${nextY}px`);
              tocSnake.style.setProperty('--snake-height', `${nextHeight}px`);
            }
          }
          activeTocLink = activeLink;
        };
        tocLinks.forEach((link) => link.addEventListener('click', () => requestAnimationFrame(syncTocSnake)));
        window.addEventListener('scroll', syncTocSnake, { passive: true });
        window.addEventListener('resize', syncTocSnake, { passive: true });
        requestAnimationFrame(syncTocSnake);
      }
    </script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({
        startOnLoad: true,
        securityLevel: "strict",
        theme: document.documentElement.classList.contains("dark") ? "dark" : "default"
      });
    </script>
    {{ live_reload_tag }}
  </body>
</html>
"""


def normalize_theme_name(name: str | None) -> str | None:
    if name is None:
        return None
    return THEME_ALIASES.get(name, name)


def get_theme_preset(name: str | None, accent: str | None = None) -> dict[str, str] | dict[str, dict[str, str]]:
    if name is None:
        return THEME_PRESETS
    normalized_name = normalize_theme_name(name)
    if normalized_name not in THEME_PRESETS:
        raise ValueError("Unknown theme. Static Docs supports 'static-docs'.")
    preset = dict(THEME_PRESETS[normalized_name])
    if accent:
        preset["accent"] = accent
        preset["active_text"] = accent
    return preset


def get_pygments_css(style: str = "xcode") -> str:
    return HtmlFormatter(style=style).get_style_defs("pre.highlight")


def render_css(theme_tokens: dict[str, str], pygments_style: str = "xcode") -> str:
    rendered = BASE_CSS
    for key, value in theme_tokens.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    rendered += "\n" + get_pygments_css(pygments_style)
    return rendered


def replace_tokens(template: str, context: dict[str, str]) -> str:
    rendered = template
    for key in [
        "title",
        "description_text",
        "canonical_url",
        "og_type",
        "current_url",
        "brand_name",
        "github_url",
        "feedback_url",
        "edit_url",
        "edit_link_html",
        "header_action_html",
        "breadcrumbs_html",
        "page_title",
        "page_summary",
        "page_meta_html",
        "page_heading_html",
        "sidebar_grid_style",
        "custom_css_tag",
        "custom_js_tag",
        "live_reload_tag",
        "top_nav_html",
        "nav_html",
        "sidebar_html",
        "pager_html",
        "toc_html",
        "toc_sidebar_html",
        "search_json",
        "base_js",
        "article_html",
        "theme_accent",
    ]:
        rendered = rendered.replace(f"{{{{ {key} }}}}", context.get(key, ""))
    return rendered


def render_staticnest_page(
    *,
    site_title: str,
    brand_name: str,
    description: str,
    page_title: str,
    page_summary: str,
    page_badge: str = "",
    page_status: str = "",
    nav_html: str,
    toc_html: str,
    hide_sidebar: bool = False,
    hide_toc: bool = False,
    article_html: str,
    pager_html: str,
    top_nav_html: str,
    header_action_html: str,
    current_url: str,
    github_url: str,
    feedback_url: str,
    edit_url: str = "",
    canonical_url: str = "",
    live_reload: bool,
    live_reload_path: str,
) -> str:
    title = escape(f"{page_title} | {site_title}")
    description_text = escape(page_summary or description)
    canonical = canonical_url or current_url
    meta_items = []
    if page_badge:
        meta_items.append(f'<span class="page-badge">{escape(page_badge)}</span>')
    normalized_status = page_status.strip().lower()
    if normalized_status in {"new", "beta", "deprecated"}:
        meta_items.append(
            f'<span class="page-status page-status-{normalized_status}">{escape(normalized_status.title())}</span>'
        )
    page_meta_html = f'<div class="page-meta">{"".join(meta_items)}</div>' if meta_items else ""
    sidebar_html = "" if hide_sidebar else (
        '<div class="w-(--sidebar-width) flex-col text-sidebar-foreground sticky top-[calc(var(--header-height)+0.6rem)] z-30 hidden h-[calc(100svh-10rem)] overscroll-none bg-transparent [--sidebar-menu-width:--spacing(56)] lg:flex" data-slot="sidebar">'
        '<div class="h-9"></div>'
        '<div class="absolute top-8 z-10 h-8 w-(--sidebar-menu-width) shrink-0 bg-gradient-to-b from-background via-background/80 to-background/50 blur-xs"></div>'
        '<div class="absolute top-12 right-2 bottom-0 hidden h-full w-px bg-gradient-to-b from-transparent via-border to-transparent lg:flex"></div>'
        '<div class="flex min-h-0 flex-1 flex-col gap-2 overflow-auto group-data-[collapsible=icon]:overflow-hidden mx-auto no-scrollbar w-(--sidebar-menu-width) overflow-x-hidden px-2" data-sidebar="content" data-slot="sidebar-content" view-transition-name="sidebar">'
        '<div data-slot="sidebar-group" data-sidebar="group" class="relative flex w-full min-w-0 flex-col p-2 pt-6">'
        '<div data-slot="sidebar-group-content" data-sidebar="group-content" class="w-full text-sm">'
        f'<ul data-slot="sidebar-menu" data-sidebar="menu" class="flex w-full min-w-0 flex-col gap-0.5">{nav_html}</ul>'
        '</div></div><div class="sticky -bottom-1 z-10 h-16 shrink-0 bg-gradient-to-t from-background via-background/80 to-background/50 blur-xs"></div></div></div>'
    )
    toc_fallback_html = '<span class="text-muted-foreground text-[0.8rem]">No headings</span>'
    toc_sidebar_html = "" if hide_toc else (
        '<div class="sticky top-[calc(var(--header-height)+1px)] ml-auto hidden h-[calc(100svh-var(--header-height)-var(--footer-height))] w-72 flex-col gap-4 overflow-hidden overscroll-none pb-8 xl:flex">'
        '<div class="h-(--top-spacing) shrink-0"></div>'
        '<div id="toc" view-transition-name="toc" class="no-scrollbar overflow-y-auto px-8">'
        '<div class="flex flex-col gap-2 p-4 pt-0 text-sm">'
        '<p class="text-muted-foreground bg-background sticky top-0 h-6 text-xs">On This Page</p>'
        '<div class="toc-snake-list" data-toc-snake>'
        '<span class="toc-snake-rail" aria-hidden="true"></span>'
        '<span class="toc-snake-indicator" aria-hidden="true"></span>'
        f'{toc_html or toc_fallback_html}'
        '</div>'
        '<div class="mt-8 flex flex-col gap-3 border-t border-border pt-6 text-muted-foreground">'
        f'<a class="block hover:text-foreground" href="{escape(feedback_url, quote=True)}">Question? Give us feedback</a>'
        f'{"<a class=\"block hover:text-foreground\" href=\"" + escape(edit_url, quote=True) + "\">Edit this page on GitHub</a>" if edit_url else ""}'
        '</div></div><div class="h-12"></div></div></div>'
    )
    live_reload_tag = ""
    if live_reload:
        live_reload_tag = f"<script>{LIVE_RELOAD_JS.replace('{{ live_reload_path }}', live_reload_path)}</script>"
    return replace_tokens(
        STATICNEST_TEMPLATE,
        {
            "title": title,
            "description_text": description_text,
            "canonical_url": escape(canonical, quote=True),
            "og_type": "website",
            "current_url": escape(current_url, quote=True),
            "brand_name": escape(brand_name),
            "github_url": escape(github_url, quote=True),
            "page_title": escape(page_title),
            "page_summary": escape(page_summary),
            "page_meta_html": page_meta_html,
            "sidebar_grid_style": "grid-template-columns:minmax(0,1fr);" if hide_sidebar else "",
            "article_html": article_html,
            "pager_html": pager_html,
            "nav_html": nav_html,
            "sidebar_html": sidebar_html,
            "toc_html": toc_html or '<span class="text-muted-foreground text-[0.8rem]">No headings</span>',
            "toc_sidebar_html": toc_sidebar_html,
            "base_js": BASE_JS,
            "live_reload_tag": live_reload_tag,
            "theme_accent": "oklch(62.3% 0.214 259.815)",
            "feedback_url": escape(feedback_url, quote=True),
            "edit_url": escape(edit_url, quote=True),
            "edit_link_html": (
                f'<a href="{escape(edit_url, quote=True)}">Edit this page on GitHub</a>' if edit_url else ""
            ),
            "header_action_html": header_action_html,
            "breadcrumbs_html": "",
            "custom_css_tag": "",
            "custom_js_tag": "",
            "top_nav_html": top_nav_html,
            "search_json": "[]",
        },
    )


def render_page(
    *,
    site_title: str,
    brand_name: str,
    description: str,
    tagline: str,
    github_url: str,
    feedback_url: str,
    header_action_html: str,
    page_title: str,
    page_summary: str,
    nav_html: str,
    top_nav_html: str,
    toc_html: str,
    article_html: str,
    current_url: str,
    search_index: list[dict[str, str]],
    template_override: str | None,
    has_custom_css: bool,
    has_custom_js: bool,
    live_reload: bool,
    live_reload_path: str,
    breadcrumbs_html: str,
    pager_html: str,
) -> str:
    template = template_override or DEFAULT_TEMPLATE
    title = escape(f"{page_title} | {site_title}")
    description_text = escape(page_summary or description)
    page_heading_html = f"<h1>{escape(page_title)}</h1>" if page_title else ""
    search_json = json.dumps(search_index).replace("</", "<\\/")
    custom_css_tag = f'<link rel="stylesheet" href="{current_url}assets/custom.css" />' if has_custom_css else ""
    custom_js_tag = f'<script src="{current_url}assets/custom.js"></script>' if has_custom_js else ""
    live_reload_tag = ""
    if live_reload:
        live_reload_tag = f"<script>{LIVE_RELOAD_JS.replace('{{ live_reload_path }}', live_reload_path)}</script>"
    toc_markup = toc_html or '<p class="toc-link">No headings on this page.</p>'
    return replace_tokens(
        template,
        {
            "title": title,
            "description_text": description_text,
            "current_url": escape(current_url, quote=True),
            "brand_name": escape(brand_name),
            "github_url": escape(github_url, quote=True),
            "feedback_url": escape(feedback_url, quote=True),
            "header_action_html": header_action_html,
            "top_nav_html": top_nav_html,
            "nav_html": nav_html,
            "breadcrumbs_html": breadcrumbs_html,
            "page_title": escape(page_title),
            "page_summary": escape(page_summary),
            "page_heading_html": page_heading_html,
            "article_html": article_html,
            "pager_html": pager_html,
            "toc_html": toc_markup,
            "search_json": search_json,
            "base_js": BASE_JS,
            "custom_css_tag": custom_css_tag,
            "custom_js_tag": custom_js_tag,
            "live_reload_tag": live_reload_tag,
        },
    )


def render_not_found_page(
    *,
    site_title: str,
    brand_name: str,
    description: str,
    github_url: str,
    feedback_url: str,
    header_action_html: str,
    top_nav_html: str,
    nav_html: str,
    current_url: str,
    search_index: list[dict[str, str]],
    has_custom_css: bool,
    has_custom_js: bool,
    live_reload: bool,
    live_reload_path: str,
) -> str:
    article_html = NOT_FOUND_ARTICLE_HTML.replace("{{ current_url }}", escape(current_url, quote=True))
    return render_page(
        site_title=site_title,
        brand_name=brand_name,
        description=description,
        tagline="",
        github_url=github_url,
        feedback_url=feedback_url,
        header_action_html=header_action_html,
        page_title="",
        page_summary="The requested page could not be found.",
        nav_html=nav_html,
        top_nav_html=top_nav_html,
        toc_html="",
        article_html=article_html,
        current_url=current_url,
        search_index=search_index,
        template_override=None,
        has_custom_css=has_custom_css,
        has_custom_js=has_custom_js,
        live_reload=live_reload,
        live_reload_path=live_reload_path,
        breadcrumbs_html='<a href="/">Documentation</a><span class="breadcrumb-sep">›</span><strong>404</strong>',
        pager_html="",
    )
