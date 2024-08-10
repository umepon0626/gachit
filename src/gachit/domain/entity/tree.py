from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from .sha import Sha


class TreeEntryMode(StrEnum):
    FILE = "100644"
    EXECUTABLE = "100755"
    DIRECTORY = "040000"
    SYMLINK = "120000"
    SUBMODULE = "160000"


@dataclass
class TreeEntry:
    """Tree entry

    Args:
        mode (TreeEntryMode): Entry mode
        name (str): Entry name, not full path.
        sha (str): Entry SHA
    """

    mode: TreeEntryMode
    name: str
    sha: Sha


@dataclass
class Tree:
    format: ClassVar[str] = "tree"
    entries: list[TreeEntry]
