import hashlib
from pathlib import Path

from gachit.domain.entity import Mode, Sha, Tree, TreeLeaf
from gachit.io.database import DataBase, ObjectHeader


class TreeSerializer:
    @classmethod
    def deserialize(cls, data: bytes, db: DataBase) -> Tree:
        """Deserialize tree object from bytes data.

        Args:
            data (bytes): tree data.

        Returns:
            Tree: deserialized tree object.
        """
        pos = 0
        length = len(data)
        root_tree = Tree()
        while pos < length:
            leaf, pos = cls.__parse_one_tree(data, pos)
            if leaf.mode == Mode.DIRECTORY:
                _, sub_tree_body = db.read_object(leaf.sha)
                sub_tree = TreeSerializer.deserialize(sub_tree_body, db)
                root_tree.entries[leaf.path.name] = sub_tree
            else:
                root_tree.add_entry(leaf)
        return root_tree

    @classmethod
    def serialize(cls, tree: Tree) -> bytes:
        ret = b""
        for entry in sorted(tree.entries.values(), key=cls.__tree_leaf_sort_key):
            if isinstance(entry, Tree):
                mode = Mode.DIRECTORY
                data_body = TreeSerializer.serialize(entry)
                header = ObjectHeader(Tree, len(data_body))
                written_data = header.value + data_body
                sha = Sha(hashlib.sha1(written_data).hexdigest())
                name = entry.path.name

            elif isinstance(entry, TreeLeaf):
                mode = Mode(entry.mode)
                sha = entry.sha
                name = entry.path.name
            else:
                raise ValueError(f"Unknown entry type: {type(entry)}")
            ret += (
                mode.value.encode("ascii")
                + b" "
                + name.encode("ascii")
                + b"\x00"
                + (int(sha.value, 16)).to_bytes(20, byteorder="big")
            )
        return ret

    @classmethod
    def __tree_leaf_sort_key(cls, entry: TreeLeaf | Tree) -> str:
        if isinstance(entry, TreeLeaf):
            return str(entry.path)
        # We have to distinguish directories from files.
        # We can do this by adding a slash to the end of the directory name.
        return str(entry.path) + "/"

    @classmethod
    def __parse_one_tree(cls, data: bytes, pos: int) -> tuple[TreeLeaf, int]:
        """Parse one tree entry from data.

        Args:
            data (bytes): tree data.
            pos (int): current position.

        Returns:
            tuple[TreeLeaf, int]: tree entry and next position.
        """
        mode_end = data.find(b" ", pos)
        mode = Mode(data[pos:mode_end].decode("ascii"))
        name_end = data.find(b"\x00", mode_end)
        name = data[mode_end + 1 : name_end].decode("ascii")
        sha = Sha(data[name_end + 1 : name_end + 21].hex())
        return TreeLeaf(mode, Path(name), sha), name_end + 21
