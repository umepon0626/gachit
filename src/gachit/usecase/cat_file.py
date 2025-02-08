from pathlib import Path

from gachit.domain.entity import Blob, Commit, Repository, Sha, Tree, TreeShallow
from gachit.io.database import DataBase
from gachit.io.serializer import BlobSerializer, CommitSerializer, TreeShallowSerializer


def cat_file_use_case(
    # TODO: rename use_case name
    sha_str: str,
    current_dir: Path = Path("."),
) -> Blob | TreeShallow | Commit:
    """Read an object from the database

    Args:
        sha_str (str): object sha
        current_dir (Path, optional): current directory. Defaults to Path(".").

    Raises:
        ValueError: if the object is not found

    Returns:
        Blob | TreeShallow | Commit: object
    """
    repo = Repository(current_dir=current_dir)
    db = DataBase(repo.git_dir)

    sha = Sha(sha_str)
    header, content = db.read_object(sha)

    # deserialize the object content
    if header.object_type == Blob:
        return BlobSerializer.deserialize(content)
    elif header.object_type == Tree:
        return TreeShallowSerializer.deserialize(content)
    elif header.object_type == Commit:
        return CommitSerializer.deserialize(content)
    else:
        raise ValueError(f"Unknown object type: {header.object_type}")
