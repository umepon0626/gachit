from pathlib import Path

from gachit.domain.entity import Blob, Commit, Sha, Tree

from .read_object import read_object


class DataBase:
    def __init__(self, git_dir: Path) -> None:
        self.git_dir = git_dir

    def read_object(self, sha: Sha) -> Blob | Tree | Commit:
        return read_object(self.git_dir / "objects" / sha.value[:2] / sha.value[2:])
