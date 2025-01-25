import zlib
from pathlib import Path

from gachit.domain.entity import Sha

from .object_header import ObjectHeader


class DataBase:
    def __init__(self, git_dir: Path) -> None:
        self.git_dir = git_dir

    def read_object(self, sha: Sha) -> tuple[ObjectHeader, bytes]:
        file_path = self.git_dir / "objects" / sha.value[:2] / sha.value[2:]
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            raw = zlib.decompress(f.read())

        null_byte_end = raw.find(b"\x00")
        header = ObjectHeader.from_data(raw[: null_byte_end + 1])

        if header.content_size != len(raw) - null_byte_end - 1:
            raise ValueError(f"Malformed object {file_path}")

        return header, raw[null_byte_end + 1 :]

    def write_object(
        self, header: ObjectHeader, data: bytes, sha: Sha, raise_on_exist: bool = True
    ) -> None:
        object_path = self.git_dir / "objects" / sha.value[:2] / sha.value[2:]
        if object_path.exists():
            if raise_on_exist:
                raise FileExistsError(f"Object already exists: {object_path}")
            return
        object_path.parent.mkdir(parents=True, exist_ok=True)
        object_path.write_bytes(zlib.compress(header.value + data))
