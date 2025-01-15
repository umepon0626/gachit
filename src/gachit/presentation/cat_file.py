from gachit.domain.entity import Blob, Commit, TreeShallow


def cat_file_presentation(data: Blob | TreeShallow | Commit) -> None:
    if isinstance(data, Blob):
        print(data.data.decode("ascii"))
    elif isinstance(data, TreeShallow):
        print(format_tree(data))
    elif isinstance(data, Commit):
        print(format_commit(data))
    else:
        raise ValueError(f"Unknown data type: {data}")


def format_tree(tree: TreeShallow) -> str:
    return "\n".join(
        f"{entry.mode.value} {entry.mode.object_type} {entry.sha.value} {name}"
        for name, entry in tree.entries.items()
    )


def format_commit(commit: Commit) -> str:
    formatted_str = f"tree {commit.tree.value}\n"
    for parent in commit.parents:
        formatted_str += f"parent {parent.value}\n"
    formatted_str += f"author {commit.author.name} <{commit.author.email}> "
    formatted_str += f"{commit.created_at.timestamp()} +0900\n"
    formatted_str += f"committer {commit.committer.name} <{commit.committer.email}> "
    formatted_str += f"{commit.committed_at.timestamp()} +0900\n"
    formatted_str += f"\n{commit.message}"
    return formatted_str
