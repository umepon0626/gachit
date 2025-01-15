from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Union

from .mode import Mode
from .sha import Sha


@dataclass
class TreeLeaf:
    """Tree leaf

    Args:
        mode (Mode): Entry mode
        path (Path): Full path
        sha (str): Entry SHA
    """

    mode: Mode
    path: Path
    sha: Sha


@dataclass
class TreeShallow:
    """Tree shallow. This holds only the top level of the tree.

    Args:
        path (Path): Directory path.
    """

    format: ClassVar[str] = "tree"
    entries: dict[str, TreeLeaf] = field(default_factory=dict)


@dataclass
class Tree:
    """Tree

    Args:
        path (Path): Directory path.
        entries (list[TreeLeaf | Tree]): Entries

    Raises:
        ValueError: If the key of entries contains "/".
    """

    format: ClassVar[str] = "tree"
    path: Path = field(default=Path("."))
    entries: dict[str, Union[TreeLeaf, "Tree"]] = field(default_factory=dict)

    def add_entry(self, entry: TreeLeaf) -> None:
        """Add entry to tree

        Args:
            entry (TreeLeaf): Entry to add
        """
        relative_path = entry.path.relative_to(self.path)
        if len(relative_path.parts) == 1:
            self.entries[relative_path.parts[0]] = entry
        elif len(relative_path.parts) > 1:
            # Find existing tree
            leaf = self.entries.get(relative_path.parts[0], None)
            if (
                isinstance(leaf, self.__class__)
                and leaf.path.name == relative_path.parts[0]
            ):
                leaf.add_entry(entry=entry)
                return
            # If not found, create a new tree
            tree = self.__class__(path=self.path / relative_path.parts[0])
            tree.add_entry(entry=entry)
            self.entries[relative_path.parts[0]] = tree
        else:
            raise ValueError(f"Invalid path: {entry.path}")

    def find_entry(self, path: Path) -> Union[TreeLeaf, None]:
        """Find entry by path

        Args:
            path (Path): Path to find

        Returns:
            Union[TreeLeaf, None]: Found entry or None
        """
        relative_path = path.relative_to(self.path)
        if len(relative_path.parts) == 1:
            entry = self.entries.get(relative_path.parts[0], None)
            if isinstance(entry, TreeLeaf):
                return entry
        elif len(relative_path.parts) > 1:
            entry = self.entries.get(relative_path.parts[0] + "/", None)
            if isinstance(entry, self.__class__):
                return entry.find_entry(path=path)
        return None
