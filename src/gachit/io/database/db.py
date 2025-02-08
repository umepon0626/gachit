import zlib
from hashlib import sha1
from pathlib import Path

from gachit.domain.entity import Sha

from .object_header import ObjectHeader


class DataBase:
    def __init__(self, git_dir: Path) -> None:
        self.git_dir = git_dir

    def read_object(self, sha: Sha) -> tuple[ObjectHeader, bytes]:
        """Read an object from the database

        Args:
            sha (Sha): object sha

        Raises:
            FileNotFoundError: if the object is not found
            ValueError: if the object is malformed

        Returns:
            tuple[ObjectHeader, bytes]: object header and content
        """
        file_path = self.git_dir / "objects" / sha.value[:2] / sha.value[2:]

        # check if the file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # read the file and decompress it
        with open(file_path, "rb") as f:
            raw = zlib.decompress(f.read())

        # find the end of the header
        header_end = raw.find(b"\x00")

        # parse the header
        header = ObjectHeader.from_data(raw[: header_end + 1])

        if header.content_size != len(raw) - header_end - 1:
            raise ValueError(f"Malformed object {file_path}")

        return header, raw[header_end + 1 :]

    def write_object(
        self, header: ObjectHeader, data: bytes, raise_on_exist: bool = True
    ) -> Sha:
        written_data = zlib.compress(header.value + data, zlib.Z_BEST_SPEED)
        sha = Sha(sha1(written_data).hexdigest())
        object_path = self.git_dir / "objects" / sha.value[:2] / sha.value[2:]
        if object_path.exists():
            if raise_on_exist:
                raise FileExistsError(f"Object already exists: {object_path}")
            return sha
        object_path.parent.mkdir(parents=True, exist_ok=True)
        object_path.write_bytes(written_data)
        return sha
