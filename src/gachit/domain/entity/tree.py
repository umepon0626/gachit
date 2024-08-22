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

    def __post__init__(self) -> None:
        self.__validate_mode(self.mode)

    def __validate_mode(self, mode: Mode) -> None:
        if mode not in [Mode.FILE, Mode.EXECUTABLE]:
            raise ValueError(f"Invalid mode: {mode}")


@dataclass
class Tree:
    """Tree

    Args:
        directory (Path | None): Directory path. If the tree is for the root,
        it should be None.

        entries (list[TreeLeaf | Tree]): Entries

    Raises:
        ValueError: If the key of entries contains "/".
    """

    format: ClassVar[str] = "tree"
    directory: Path
    entries: list[Union[TreeLeaf, "Tree"]] = field(default_factory=list)

    def add_entry(self, entry: TreeLeaf) -> None:
        """Add entry to tree

        Args:
            entry (TreeLeaf): Entry to add
        """
        relative_path = entry.path.relative_to(self.directory)
        if len(relative_path.parts) == 1:
            self.entries.append(entry)
        elif len(relative_path.parts) > 1:
            # Find existing tree
            for e in self.entries:
                if (
                    isinstance(e, self.__class__)
                    and e.directory.name == relative_path.parts[0]
                ):
                    e.add_entry(entry=entry)
                    return
            # If not found, create a new tree
            tree = self.__class__(directory=self.directory / relative_path.parts[0])
            tree.add_entry(entry=entry)
            self.entries.append(tree)
        else:
            raise ValueError(f"Invalid path: {entry.path}")
