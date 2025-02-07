from pathlib import Path

from gachit.domain.entity import Sha, Tree
from gachit.io.serializer import TreeSerializer

from .db import DataBase
from .object_header import ObjectHeader


class TreeIO:
    def __init__(self, git_dir: Path) -> None:
        self.db = DataBase(git_dir)

    def get(self, sha: Sha) -> Tree:
        header, data = self.db.read_object(sha)
        if header.object_type != Tree:
            raise ValueError(f"Invalid object type: {header.object_type}")
        return TreeSerializer.deserialize(data, self.db)

    def write(self, tree: Tree) -> Sha:
        for entry in tree.entries.values():
            # save sub tree recursively
            if isinstance(entry, Tree):
                self.write(entry)
        tree_data = TreeSerializer.serialize(tree)
        header = ObjectHeader(Tree, len(tree_data))
        return self.db.write_object(
            header, tree_data, raise_on_exist=False
        )  # skip if already exists sub tree
