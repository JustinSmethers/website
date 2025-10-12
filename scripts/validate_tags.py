#!/usr/bin/env python3
"""Validate that every blog post declares only approved tags."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from blog.tagging import ALLOWED_TAGS, normalize_and_validate_tags


def extract_front_matter(markdown_path: Path) -> dict:
    content = markdown_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def validate_markdown_file(markdown_path: Path) -> List[str]:
    metadata = extract_front_matter(markdown_path)
    _, invalid = normalize_and_validate_tags(metadata.get("tags"))
    if invalid:
        return [
            f"{markdown_path}: unsupported tag '{tag}'. Allowed tags: {', '.join(ALLOWED_TAGS)}"
            for tag in sorted(set(invalid))
        ]
    return []


def discover_markdown_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from sorted(path.rglob("*.md"))
        elif path.suffix == ".md":
            yield path


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("blog_posts")],
        help="Directories or markdown files to validate. Defaults to 'blog_posts'.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    markdown_files = list(discover_markdown_files(args.paths))
    errors: List[str] = []
    for markdown_path in markdown_files:
        errors.extend(validate_markdown_file(markdown_path))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
