from pathlib import Path

from gachit.domain.entity import Blob, Sha, Tree

from .read_object import read_object


class DataBase:
    def __init__(self, git_dir: Path) -> None:
        self.git_dir = git_dir

    def read_object(self, sha: Sha) -> Blob | Tree:
        obj = read_object(self.git_dir / "objects" / sha.value[:2] / sha.value[2:])
        if isinstance(obj, Blob):
            return obj
        elif isinstance(obj, Tree):
            return obj
        raise ValueError(f"Expected Blob or Tree, but got {obj}")
