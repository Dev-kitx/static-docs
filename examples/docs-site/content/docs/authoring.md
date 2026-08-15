---
title: Authoring
summary: Write Markdown pages with front matter, headings, links, lists, and code blocks.
order: 4
status: deprecated
hide_toc: false
hide_sidebar: false
---

# Authoring

Static Docs pages are Markdown files with optional front matter.

## Page metadata

```yaml
---
title: Architecture
description: Explains the rendering pipeline.
badge: Guide
status: beta
hide_toc: false
hide_sidebar: false
order: 4
---
```

Use `status: new`, `status: beta`, or `status: deprecated` to show a status badge beside the page title.

Use headings to generate the right side table of contents.

```mermaid
graph TD;
subgraph AA [Consumers]
A[Mobile app];
B[Web app];
C[Node.js client];
end
subgraph BB [Services]
E[REST API];
F[GraphQL API];
G[SOAP API];
end
Z[GraphQL API];
A --> Z;
B --> Z;
C --> Z;
Z --> E;
Z --> F;
Z --> G;
```
