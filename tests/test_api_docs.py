from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from staticnest.api_docs import ApiDocsOptions, generate_api_docs


class GenerateApiDocsTests(unittest.TestCase):
    def test_generates_module_page_from_python_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src" / "example"
            source.mkdir(parents=True)
            (source / "tools.py").write_text(
                'def greet(name: str, excited: bool = False) -> str:\n'
                '    """Create a greeting.\n\n'
                '    Args:\n'
                '        name: Person to greet.\n'
                '        excited: Whether to add emphasis.\n'
                '    """\n'
                '    return name\n'
            )

            generated = generate_api_docs(
                ApiDocsOptions(source=source, output=root / "content" / "api", package="example")
            )

            page = root / "content" / "api" / "example-tools.md"
            self.assertIn(page.resolve(), generated)
            self.assertTrue((root / "content" / "api" / "index.md").exists())
            self.assertIn(
                "Browse generated API documentation for 1 Python module.",
                (root / "content" / "api" / "index.md").read_text(),
            )
            content = page.read_text()
            self.assertIn("# example.tools", content)
            self.assertIn("## Functions", content)
            self.assertIn("### greet", content)
            self.assertNotIn("\nAPI reference for example.tools.\n\n##", content)
            self.assertIn("greet(name: str, excited: bool = False) -> str", content)
            self.assertIn('::param name="name"', content)
            self.assertIn('type="str"', content)
            self.assertIn('```python title="line 1"', content)

    def test_groups_classes_and_methods(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src"
            source.mkdir()
            (source / "client.py").write_text(
                'class Client:\n'
                '    """HTTP client."""\n\n'
                '    def request(self, path: str) -> str:\n'
                '        """Send a request."""\n'
                '        return path\n'
            )

            generate_api_docs(ApiDocsOptions(source=source, output=root / "api"))

            content = (root / "api" / "client.md").read_text()
            self.assertIn("## Classes", content)
            self.assertIn("### Client", content)
            self.assertIn("#### Client.request", content)

    def test_skips_private_objects_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src"
            source.mkdir()
            (source / "mod.py").write_text('def _hidden():\n    """Hidden."""\n')

            generate_api_docs(ApiDocsOptions(source=source, output=root / "api"))

            self.assertNotIn("_hidden", (root / "api" / "index.md").read_text())


if __name__ == "__main__":
    unittest.main()
