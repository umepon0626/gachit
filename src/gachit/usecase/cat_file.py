from pathlib import Path

from gachit.domain.entity import Blob, Commit, Repository, Sha, Tree
from gachit.io.database import DataBase
from gachit.io.serializer import BlobSerializer, CommitSerializer, TreeSerializer


def cat_file_use_case(
    sha_str: str, current_dir: Path = Path(".")
) -> Blob | Tree | Commit:
    repo = Repository(current_dir=current_dir)
    db = DataBase(repo.git_dir)
    sha = Sha(sha_str)
    header, body = db.read_object(sha)
    if header.object_type == Blob:
        return BlobSerializer.deserialize(body)
    elif header.object_type == Tree:
        return TreeSerializer.deserialize(body, db)
    elif header.object_type == Commit:
        return CommitSerializer.deserialize(body)
    else:
        raise ValueError(f"Unknown object type: {header.object_type}")
