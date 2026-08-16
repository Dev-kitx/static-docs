from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from staticnest.api_docs import ApiDocsOptions, generate_api_docs
from staticnest.devserver import serve_site
from staticnest.scaffold import init_project
from staticnest.site import DeployOptions, build_site, gh_deploy_site, publish_site


def _get_version() -> str:
    try:
        return version("static-docs")
    except PackageNotFoundError:
        try:
            return version("staticnest-cli")
        except PackageNotFoundError:
            return "dev"


def _print_version() -> None:
    ver = _get_version()
    print()
    print("  ◆  s t a t i c")
    print("  ███╗   ██╗███████╗███████╗████████╗")
    print("  ████╗  ██║██╔════╝██╔════╝╚══██╔══╝")
    print("  ██╔██╗ ██║█████╗  ███████╗   ██║   ")
    print("  ██║╚██╗██║██╔══╝  ╚════██║   ██║   ")
    print("  ██║ ╚████║███████╗███████║   ██║   ")
    print("  ╚═╝  ╚═══╝╚══════╝╚══════╝   ╚═╝   ")
    print()
    print(f"  version {ver}  ·  Pure-Python docs builder")
    print("  " + "─" * 40)
    print()


def resolve_config_path(config: str) -> Path:
    path = Path(config).resolve()
    if path.is_dir():
        path = path / "site.toml"
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="static-docs",
        description="Build a static documentation site with the Static Docs theme.",
    )
    parser.add_argument(
        "-V", "--version",
        action="store_true",
        help="Show version and exit.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="build",
        choices=["build", "serve", "preview", "publish", "gh-deploy", "init", "api"],
        help="Command to run.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project directory for the init command.",
    )
    parser.add_argument(
        "--config",
        default="site.toml",
        help="Path to the site configuration file or project directory.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host interface for serve mode.")
    parser.add_argument("--port", default=8000, type=int, help="Port for serve mode.")
    parser.add_argument(
        "--destination",
        help="Publish destination directory for the publish command.",
    )
    parser.add_argument("--remote", default="origin", help="Git remote for gh-deploy.")
    parser.add_argument("--branch", default="gh-pages", help="Git branch for gh-deploy.")
    parser.add_argument("--source", default="src", help="Python source path for api generate.")
    parser.add_argument("--output", default="content/api", help="Output directory for generated API Markdown.")
    parser.add_argument("--package", default="", help="Package prefix for generated API module names.")
    parser.add_argument("--title", default="API Reference", help="Title for generated API docs.")
    parser.add_argument("--include-private", action="store_true", help="Include private Python objects in API docs.")
    parser.add_argument("--include-init", action="store_true", help="Include __init__.py modules in API docs.")
    parser.add_argument(
        "--message",
        default="Deploy static-docs site",
        help="Git commit message for gh-deploy.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        _print_version()
        return 0

    if args.command == "init":
        try:
            project_dir = init_project(Path(args.path))
        except ValueError as exc:
            parser.exit(1, f"Error: {exc}\n")
        print(f"Initialized Static Docs project in {project_dir}")
        return 0

    if args.command == "api":
        if args.path != "generate":
            parser.exit(1, "Error: api command currently supports only: static-docs api generate\n")
        generated = generate_api_docs(
            ApiDocsOptions(
                source=Path(args.source),
                output=Path(args.output),
                package=args.package,
                title=args.title,
                include_private=args.include_private,
                include_init=args.include_init,
            )
        )
        print(f"Generated {len(generated)} API docs pages in {Path(args.output).resolve()}")
        return 0

    config_path = resolve_config_path(args.config)

    if args.command == "build":
        build_site(config_path)
        print(f"Built site from {config_path}")
    elif args.command in {"serve", "preview"}:
        serve_site(config_path, host=args.host, port=args.port)
    elif args.command == "publish":
        destination = Path(args.destination).resolve() if args.destination else None
        published_to = publish_site(config_path, destination=destination)
        print(f"Published site to {published_to}")
    elif args.command == "gh-deploy":
        deployed_to = gh_deploy_site(
            config_path,
            DeployOptions(remote=args.remote, branch=args.branch, message=args.message),
        )
        print(f"Deployed site to {deployed_to}")

    return 0
