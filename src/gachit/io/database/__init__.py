from pathlib import Path

from gachit.domain.entity import Sha

from .object_header import ObjectHeader
from .read_object import read_object
from .write_object import write_object


class DataBase:
    def __init__(self, git_dir: Path) -> None:
        self.git_dir = git_dir

    def read_object(self, sha: Sha) -> tuple[ObjectHeader, bytes]:
        return read_object(self.git_dir / "objects" / sha.value[:2] / sha.value[2:])

    def write_object(
        self, header: ObjectHeader, data: bytes, sha: Sha, exist_ok: bool = True
    ) -> None:
        return write_object(header, data, sha, self.git_dir / "objects", exist_ok)


__all__ = ["ObjectHeader", "DataBase"]
