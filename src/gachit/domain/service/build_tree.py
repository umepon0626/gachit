from gachit.domain.entity import Index, Mode, Tree, TreeLeaf
from gachit.io.database import DataBase


def build_tree_from_index(index: Index, db: DataBase) -> Tree:
    root_tree = Tree(db.git_dir.parent)
    for entry in index.entries:
        root_tree.add_entry(
            TreeLeaf(Mode.FILE, db.git_dir.parent / entry.path, entry.sha)
        )
    return root_tree
