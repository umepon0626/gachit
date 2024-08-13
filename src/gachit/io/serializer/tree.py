from gachit.domain.entity import Sha, Tree, TreeEntry, TreeEntryMode


class TreeSerializer:
    @classmethod
    def deserialize(cls: type, data: bytes) -> Tree:
        """Deserialize tree object from bytes data.

        Args:
            data (bytes): tree data.

        Returns:
            Tree: deserialized tree object.
        """
        pos = 0
        length = len(data)
        tree_entries: list[TreeEntry] = []
        while pos < length:
            leaf, pos = parse_one_tree(data, pos)
            tree_entries.append(leaf)
        return Tree(tree_entries)

    @classmethod
    def serialize(cls: type, tree: Tree) -> bytes:
        ret = b""
        for entry in sorted(tree.entries, key=tree_leaf_sort_key):
            ret += (
                entry.mode.value.encode("ascii")
                + b" "
                + entry.name.encode("ascii")
                + b"\x00"
                + (int(entry.sha.value, 16)).to_bytes(20, byteorder="big")
            )
        return ret


def tree_leaf_sort_key(entry: TreeEntry) -> str:
    if entry.mode == TreeEntryMode.FILE or entry.mode == TreeEntryMode.EXECUTABLE:
        return entry.name
    return entry.name + "/"


def parse_one_tree(data: bytes, pos: int) -> tuple[TreeEntry, int]:
    """Parse one tree entry from data.

    Args:
        data (bytes): tree data.
        pos (int): current position.

    Returns:
        tuple[TreeEntry, int]: tree entry and next position.
    """
    mode_end = data.find(b" ", pos)
    mode = TreeEntryMode(data[pos:mode_end].decode("ascii"))
    name_end = data.find(b"\x00", mode_end)
    name = data[mode_end:name_end].decode("ascii")
    sha = Sha(data[name_end + 1 : name_end + 21].hex())
    return TreeEntry(mode, name, sha), name_end + 21
