from gachit.domain.entity import Blob, Commit, Repository, Sha, Tree
from gachit.io.database import DataBase


def cat_file_use_case(sha_str: str) -> Blob | Tree | Commit:
    repo = Repository()
    db = DataBase(repo.git_dir)
    sha = Sha(sha_str)
    return db.read_object(sha)
