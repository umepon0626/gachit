from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .sha import Sha
from .tree import Tree


class DiffType(Enum):
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    UNTRACKED = "untracked"
    NO_CHANGE = "no_change"


@dataclass
class BlobDiff:
    path: Path
    # TODO: make before and after private
    before: Sha | None
    after: Sha | None

    def __post_init__(self) -> None:
        if self.before is None and self.after is None:
            raise ValueError("Both before and after are None.")
        if self.before == self.after:
            raise ValueError("Both before and after are the same.")


@dataclass
class TreeDiff:
    before: Tree
    after: Tree
    blob_diffs: dict[Path, BlobDiff] = field(default_factory=dict)
    # path to BlobDiff

    # TODO: Implement setter, getter for blob_diffs
