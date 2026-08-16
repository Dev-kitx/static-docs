from __future__ import annotations

import ast
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any


@dataclass
class ApiDocsOptions:
    source: Path
    output: Path
    package: str = ""
    title: str = "API Reference"
    include_private: bool = False
    include_init: bool = False
    group_by: str = "module"


@dataclass
class ParsedParam:
    name: str
    description: str = ""
    type_name: str = ""


@dataclass
class ParsedDocstring:
    short_description: str = ""
    long_description: str = ""
    params: list[ParsedParam] | None = None
    returns: str = ""
    raises: list[str] | None = None


@dataclass
class ApiObject:
    name: str
    kind: str
    signature: str
    docstring: ParsedDocstring
    lineno: int


def is_public_name(name: str, include_private: bool) -> bool:
    return include_private or not name.startswith("_")


def annotation_to_string(node: ast.AST | None) -> str:
    if node is None:
        return ""
    return ast.unparse(node)


def default_to_string(node: ast.AST | None) -> str:
    if node is None:
        return ""
    return ast.unparse(node)


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args: list[str] = []
    positional = list(node.args.posonlyargs) + list(node.args.args)
    defaults: list[ast.AST | None] = [None] * (len(positional) - len(node.args.defaults)) + list(node.args.defaults)
    for arg, default in zip(positional, defaults):
        part = arg.arg
        annotation = annotation_to_string(arg.annotation)
        if annotation:
            part += f": {annotation}"
        default_value = default_to_string(default)
        if default_value:
            part += f" = {default_value}"
        args.append(part)

    if node.args.vararg:
        vararg = f"*{node.args.vararg.arg}"
        annotation = annotation_to_string(node.args.vararg.annotation)
        if annotation:
            vararg += f": {annotation}"
        args.append(vararg)
    elif node.args.kwonlyargs:
        args.append("*")

    for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
        part = arg.arg
        annotation = annotation_to_string(arg.annotation)
        if annotation:
            part += f": {annotation}"
        default_value = default_to_string(default)
        if default_value:
            part += f" = {default_value}"
        args.append(part)

    if node.args.kwarg:
        kwarg = f"**{node.args.kwarg.arg}"
        annotation = annotation_to_string(node.args.kwarg.annotation)
        if annotation:
            kwarg += f": {annotation}"
        args.append(kwarg)

    returns = annotation_to_string(node.returns)
    suffix = f" -> {returns}" if returns else ""
    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
    return f"{prefix}{node.name}({', '.join(args)}){suffix}"


def function_param_types(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, str]:
    params: dict[str, str] = {}
    for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]:
        if arg.arg in {"self", "cls"}:
            continue
        annotation = annotation_to_string(arg.annotation)
        if annotation:
            params[arg.arg] = annotation
    if node.args.vararg:
        annotation = annotation_to_string(node.args.vararg.annotation)
        if annotation:
            params[node.args.vararg.arg] = annotation
    if node.args.kwarg:
        annotation = annotation_to_string(node.args.kwarg.annotation)
        if annotation:
            params[node.args.kwarg.arg] = annotation
    return params


def merge_annotation_types(docstring: ParsedDocstring, annotations: dict[str, str]) -> ParsedDocstring:
    params = list(docstring.params or [])
    seen = {param.name for param in params}
    merged = [
        ParsedParam(
            name=param.name,
            description=param.description,
            type_name=param.type_name or annotations.get(param.name, ""),
        )
        for param in params
    ]
    for name, type_name in annotations.items():
        if name not in seen:
            merged.append(ParsedParam(name=name, type_name=type_name, description=""))
    return ParsedDocstring(
        short_description=docstring.short_description,
        long_description=docstring.long_description,
        params=merged,
        returns=docstring.returns,
        raises=docstring.raises,
    )


def parse_docstring_fallback(value: str) -> ParsedDocstring:
    lines = [line.rstrip() for line in value.strip().splitlines()]
    short = lines[0].strip() if lines else ""
    long_lines: list[str] = []
    params: list[ParsedParam] = []
    raises: list[str] = []
    returns = ""
    section = ""
    for line in lines[1:]:
        stripped = line.strip()
        lower = stripped.lower().rstrip(":")
        if lower in {"args", "arguments", "parameters", "returns", "raises"}:
            section = lower
            continue
        if stripped.startswith(":param"):
            parts = stripped.removeprefix(":param").strip().split(":", 1)
            left = parts[0].strip().split()
            name = left[-1] if left else ""
            type_name = " ".join(left[:-1])
            description = parts[1].strip() if len(parts) > 1 else ""
            if name:
                params.append(ParsedParam(name=name, type_name=type_name, description=description))
            continue
        if stripped.startswith(":returns:") or stripped.startswith(":return:"):
            returns = stripped.split(":", 2)[-1].strip()
            continue
        if stripped.startswith(":raises"):
            raises.append(stripped.split(":", 2)[-1].strip())
            continue
        if section in {"args", "arguments", "parameters"} and ":" in stripped:
            name_part, description = stripped.split(":", 1)
            name_tokens = name_part.strip().split()
            name = name_tokens[0].strip()
            type_name = " ".join(name_tokens[1:]).strip("()")
            if name:
                params.append(ParsedParam(name=name, type_name=type_name, description=description.strip()))
            continue
        if section == "returns" and stripped:
            returns = stripped
            continue
        if section == "raises" and stripped:
            raises.append(stripped)
            continue
        if stripped:
            long_lines.append(stripped)
    return ParsedDocstring(short_description=short, long_description="\n".join(long_lines), params=params, returns=returns, raises=raises)


def parse_docstring(value: str) -> ParsedDocstring:
    try:
        from docstring_parser import parse as parse_external
    except ImportError:
        return parse_docstring_fallback(value)

    parsed: Any = parse_external(value)
    params = [
        ParsedParam(
            name=param.arg_name or "",
            description=param.description or "",
            type_name=param.type_name or "",
        )
        for param in getattr(parsed, "params", [])
        if getattr(param, "arg_name", "")
    ]
    raises = [
        " ".join(part for part in [getattr(item, "type_name", ""), getattr(item, "description", "")] if part)
        for item in getattr(parsed, "raises", [])
    ]
    returns_obj = getattr(parsed, "returns", None)
    returns = getattr(returns_obj, "description", "") if returns_obj else ""
    return ParsedDocstring(
        short_description=getattr(parsed, "short_description", "") or "",
        long_description=getattr(parsed, "long_description", "") or "",
        params=params,
        returns=returns or "",
        raises=[item for item in raises if item],
    )


def module_name_for(path: Path, source: Path, package: str) -> str:
    relative = path.relative_to(source).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    prefix = [package] if package else []
    return ".".join(prefix + parts)


def collect_api_objects(path: Path, include_private: bool) -> list[ApiObject]:
    tree = ast.parse(path.read_text(), filename=str(path))
    objects: list[ApiObject] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and is_public_name(node.name, include_private):
            docstring = merge_annotation_types(parse_docstring(ast.get_docstring(node) or ""), function_param_types(node))
            objects.append(
                ApiObject(
                    name=node.name,
                    kind="function",
                    signature=function_signature(node),
                    docstring=docstring,
                    lineno=node.lineno,
                )
            )
        elif isinstance(node, ast.ClassDef) and is_public_name(node.name, include_private):
            objects.append(
                ApiObject(
                    name=node.name,
                    kind="class",
                    signature=f"class {node.name}",
                    docstring=parse_docstring(ast.get_docstring(node) or ""),
                    lineno=node.lineno,
                )
            )
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and is_public_name(child.name, include_private):
                    docstring = merge_annotation_types(parse_docstring(ast.get_docstring(child) or ""), function_param_types(child))
                    objects.append(
                        ApiObject(
                            name=f"{node.name}.{child.name}",
                            kind="method",
                            signature=function_signature(child),
                            docstring=docstring,
                            lineno=child.lineno,
                        )
                    )
    return objects


def should_include_file(path: Path, include_init: bool) -> bool:
    if path.name == "__init__.py" and not include_init:
        return False
    return path.suffix == ".py"


def render_param_rows(obj: ApiObject) -> str:
    params = obj.docstring.params or []
    if not params:
        return ""
    lines = ["", ":::params"]
    for param in params:
        type_name = param.type_name or ""
        description = param.description or ""
        lines.append(
            f'::param name="{escape(param.name, quote=True)}" type="{escape(type_name, quote=True)}" '
            f'description="{escape(description, quote=True)}"'
        )
    lines.append(":::")
    return "\n".join(lines)


def render_api_object(obj: ApiObject, level: int = 2) -> str:
    heading_level = "#" * level
    chunks = [f"{heading_level} {obj.name}", "", f"```python title=\"line {obj.lineno}\"\n{obj.signature}\n```"]
    if obj.docstring.short_description:
        chunks.extend(["", obj.docstring.short_description])
    if obj.docstring.long_description:
        chunks.extend(["", obj.docstring.long_description])
    params = render_param_rows(obj)
    if params:
        chunks.append(params)
    if obj.docstring.returns:
        chunks.extend(["", ":::callout type=\"info\" title=\"Returns\"", obj.docstring.returns, ":::"])
    for raised in obj.docstring.raises or []:
        chunks.extend(["", ":::callout type=\"warning\" title=\"Raises\"", raised, ":::"])
    return "\n".join(chunks)


def render_module_page(module_name: str, objects: list[ApiObject]) -> str:
    summary = f"API reference for {module_name}."
    sorted_objects = sorted(objects, key=lambda item: (item.lineno, item.name))
    classes = [obj for obj in sorted_objects if obj.kind == "class"]
    functions = [obj for obj in sorted_objects if obj.kind == "function"]
    methods_by_class: dict[str, list[ApiObject]] = {}
    for obj in sorted_objects:
        if obj.kind == "method":
            class_name = obj.name.split(".", 1)[0]
            methods_by_class.setdefault(class_name, []).append(obj)
    chunks = [
        "---",
        f"title: {module_name}",
        f"description: {summary}",
        "badge: API",
        "---",
        "",
        f"# {module_name}",
    ]
    if classes:
        chunks.extend(["", "## Classes"])
        for obj in classes:
            chunks.extend(["", render_api_object(obj, level=3)])
            for method in methods_by_class.get(obj.name, []):
                chunks.extend(["", render_api_object(method, level=4)])
    if functions:
        chunks.extend(["", "## Functions"])
        for obj in functions:
            chunks.extend(["", render_api_object(obj, level=3)])
    return "\n".join(chunks).rstrip() + "\n"


def render_index_page(title: str, modules: list[str]) -> str:
    module_count = len(modules)
    module_label = "module" if module_count == 1 else "modules"
    description = f"Browse generated API documentation for {module_count} Python {module_label}."
    chunks = [
        "---",
        f"title: {title}",
        f"description: {description}",
        "badge: API",
        "---",
        "",
        f"# {title}",
        "",
        description,
        "",
        ":::cards",
    ]
    for module in modules:
        href = f"./{module.replace('.', '-')}/"
        chunks.append(f'::card title="{escape(module, quote=True)}" description="API reference for {escape(module, quote=True)}." href="{href}"')
    chunks.extend([":::", ""])
    return "\n".join(chunks)


def generate_api_docs(options: ApiDocsOptions) -> list[Path]:
    source = options.source.resolve()
    output = options.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []
    modules: list[str] = []

    for path in sorted(source.rglob("*.py") if source.is_dir() else [source]):
        if not should_include_file(path, options.include_init):
            continue
        objects = collect_api_objects(path, options.include_private)
        if not objects:
            continue
        module_name = module_name_for(path, source if source.is_dir() else source.parent, options.package)
        modules.append(module_name)
        page_name = f"{module_name.replace('.', '-')}.md"
        page_path = output / page_name
        page_path.write_text(render_module_page(module_name, objects))
        generated.append(page_path)

    index_path = output / "index.md"
    index_path.write_text(render_index_page(options.title, modules))
    generated.insert(0, index_path)
    return generated
