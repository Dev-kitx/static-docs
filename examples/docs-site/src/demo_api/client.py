"""Small API surface used to demonstrate generated Static Docs API docs."""


class StaticDocsClient:
    """Client for publishing Static Docs documentation.

    Args:
        project: Project name displayed in generated docs.
        base_url: Public base URL for generated pages.
    """

    def __init__(self, project: str, base_url: str = "/") -> None:
        self.project = project
        self.base_url = base_url

    def build(self, clean: bool = True) -> str:
        """Build the documentation site.

        Args:
            clean: Remove stale output before building.

        Returns:
            Path to the generated output directory.

        Raises:
            ValueError: If the project name is empty.
        """
        if not self.project:
            raise ValueError("project is required")
        return "dist"


def create_client(project: str, base_url: str = "/") -> StaticDocsClient:
    """Create a configured Static Docs client.

    Args:
        project: Project name displayed in generated docs.
        base_url: Public base URL for generated pages.

    Returns:
        Configured client instance.
    """
    return StaticDocsClient(project=project, base_url=base_url)

