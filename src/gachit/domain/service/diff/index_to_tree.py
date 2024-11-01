from pathlib import Path

from gachit.domain.entity import Index, Tree
from gachit.domain.entity.diff import DiffType


class IndexToTreeDiffService:
    def __init__(self, index: Index, tree: Tree) -> None:
        self.index = index
        self.tree = tree

    def check_one(self, full_path: Path) -> DiffType | None:
        tree_leaf = self.tree.find_entry(full_path)
        index_entry = self.index.find_entry(str(full_path))
        if tree_leaf is None and index_entry is None:
            return None

        if tree_leaf is None:
            return DiffType.ADDED

        if index_entry is None:
            return DiffType.DELETED

        if tree_leaf.sha != index_entry.sha:
            return DiffType.MODIFIED

        return DiffType.NO_CHANGE
