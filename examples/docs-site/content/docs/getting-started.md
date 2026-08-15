---
title: Getting Started
nav_title: Getting Started
order: 1
summary: Create a project, understand the generated files, and start the local preview loop.
---

## Getting Started

Example getting started page.

1. Clone the repo

   ```bash
   git clone https://github.com/github_username/repo_name.git
   ```

2. Install NPM packages

   ```bash
   npm install
   ```

3. Change git remote url to avoid accidental pushes to base project

   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

### Python code block Example

```python
def fibonacci(n):
    """Prints a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()

# Example usage:
fibonacci(10)
```
