from pathlib import Path

import click

from gachit.presentation import cat_file_presentation
from gachit.usecase import add_use_case, cat_file_use_case


@click.group()
def main() -> int:
    return 0


@main.command()
@click.argument("sha", type=str, required=True)
def cat_file(sha: str) -> int:
    entity = cat_file_use_case(sha_str=sha)
    cat_file_presentation(data=entity)
    return 0


@main.command()
@click.argument("path", type=Path, required=True)
def add(path: Path) -> int:
    add_use_case(path)
    return 0
