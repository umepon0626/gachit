from gachit.domain.entity import Blob, Commit, TreeShallow


def cat_file_presentation(data: Blob | TreeShallow | Commit) -> None:
    if isinstance(data, Blob):
        print(data.data.decode("ascii"))
    elif isinstance(data, TreeShallow):
        print(format_tree(data))
    else:
        raise ValueError(f"Unknown data type: {data}")


def format_tree(tree: TreeShallow) -> str:
    return "\n".join(
        f"{entry.mode.value} {entry.mode.object_type} {entry.sha.value} {name}"
        for name, entry in tree.entries.items()
    )
