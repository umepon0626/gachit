from gachit.domain.entity import Blob, Commit, Repository, Sha, Tree
from gachit.io.database import DataBase
from gachit.io.serializer import BlobSerializer, CommitSerializer, TreeSerializer


def cat_file_use_case(sha_str: str) -> Blob | Tree | Commit:
    repo = Repository()
    db = DataBase(repo.git_dir)
    sha = Sha(sha_str)
    header, data = db.read_object(sha)
    if header.object_type == Blob:
        return BlobSerializer.deserialize(data)
    elif header.object_type == Tree:
        return TreeSerializer.deserialize(data)
    elif header.object_type == Commit:
        return CommitSerializer.deserialize(data)
    else:
        raise ValueError(
            f"Unknown data type: {header.object_type} and data: {data.decode("ascii")}"
        )
