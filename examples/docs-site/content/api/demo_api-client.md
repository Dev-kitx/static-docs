---
title: demo_api.client
description: API reference for demo_api.client.
badge: API
---

# demo_api.client

## Classes

### StaticDocsClient

```python title="line 4"
class StaticDocsClient
```

Client for publishing Static Docs documentation.

:::params
::param name="project" type="" description="Project name displayed in generated docs."
::param name="base_url" type="" description="Public base URL for generated pages."
:::

#### StaticDocsClient.build

```python title="line 16"
build(self, clean: bool = True) -> str
```

Build the documentation site.

:::params
::param name="clean" type="bool" description="Remove stale output before building."
:::

:::callout type="info" title="Returns"
Path to the generated output directory.
:::

:::callout type="warning" title="Raises"
ValueError: If the project name is empty.
:::

## Functions

### create_client

```python title="line 33"
create_client(project: str, base_url: str = '/') -> StaticDocsClient
```

Create a configured Static Docs client.

:::params
::param name="project" type="str" description="Project name displayed in generated docs."
::param name="base_url" type="str" description="Public base URL for generated pages."
:::

:::callout type="info" title="Returns"
Configured client instance.
:::
