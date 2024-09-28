from dataclasses import dataclass, field
from pathlib import Path

from .sha import Sha


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
    blob_diffs: dict[Path, BlobDiff] = field(default_factory=dict)
    # path to BlobDiff

    # TODO: Implement setter, getter for blob_diffs
