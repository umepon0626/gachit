import hashlib
from dataclasses import dataclass

from gachit.domain.entity import Mode, Sha, Tree, TreeLeaf
from gachit.io.database import DataBase
from gachit.io.database.object_header import ObjectHeader


@dataclass
class TreeLeafData:
    mode: Mode
    name: str
    sha: Sha


class TreeSerializer:
    @staticmethod
    def deserialize(data: bytes, db: DataBase) -> Tree:
        """Deserialize tree object from bytes data.

        Args:
            data (bytes): tree data.

        Returns:
            Tree: deserialized tree object.
        """
        pos = 0
        length = len(data)
        root_tree = Tree(db.git_dir.parent)
        while pos < length:
            leaf, pos = parse_one_tree(data, pos)
            if leaf.mode == Mode.DIRECTORY:
                _, sub_tree_body = db.read_object(leaf.sha)
                sub_tree = TreeSerializer.deserialize(sub_tree_body, db)
                root_tree.entries.append(sub_tree)
            else:
                root_tree.add_entry(
                    TreeLeaf(leaf.mode, db.git_dir.parent / leaf.name, leaf.sha)
                )
        return root_tree

    @staticmethod
    def serialize(tree: Tree) -> bytes:
        ret = b""
        for entry in sorted(tree.entries, key=tree_leaf_sort_key):
            if isinstance(entry, Tree):
                mode = Mode.DIRECTORY
                data_body = TreeSerializer.serialize(entry)
                header = ObjectHeader(Tree, len(data_body))
                written_data = header.value + data_body
                sha = Sha(hashlib.sha1(written_data).hexdigest())
                name = entry.directory.name

            elif isinstance(entry, TreeLeaf):
                mode = Mode(entry.mode)
                sha = entry.sha
                name = entry.path.name
            else:
                raise ValueError(f"Unknown entry type: {type(entry)}")
            ret += (
                mode.value.encode("ascii")
                + name.encode("ascii")
                + b"\x00"
                + (int(sha.value, 16)).to_bytes(20, byteorder="big")
            )
        return ret


def tree_leaf_sort_key(entry: TreeLeaf | Tree) -> str:
    if isinstance(entry, TreeLeaf):
        return str(entry.path)
    # We have to distinguish directories from files.
    # We can do this by adding a slash to the end of the directory name.
    return str(entry.directory) + "/"


def parse_one_tree(data: bytes, pos: int) -> tuple[TreeLeafData, int]:
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
    name = data[mode_end:name_end].decode("ascii")
    sha = Sha(data[name_end + 1 : name_end + 21].hex())
    return TreeLeafData(mode, name, sha), name_end + 21
