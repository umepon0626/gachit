from pathlib import Path

from gachit.domain.entity import Index, Mode, Tree, TreeLeaf
from gachit.io.database import DataBase


def build_tree_from_index(index: Index, db: DataBase) -> Tree:
    root_tree = Tree(Path("."))
    for entry in index.entries:
        root_tree.add_entry(TreeLeaf(Mode.FILE, Path(entry.path), entry.sha))
    return root_tree
