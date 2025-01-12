from pathlib import Path

from gachit.domain.entity import Index
from gachit.io.serializer import IndexSerializer


class IndexIO:
    def __init__(self, git_dir: Path) -> None:
        self.index_file_path = git_dir / "index"
        if not self.index_file_path.exists():
            raise FileNotFoundError(f"Index file not found: {self.index_file_path}")

    def read(self) -> Index:
        return IndexSerializer.deserialize(self.index_file_path.read_bytes())

    def write(self, index: Index) -> None:
        self.index_file_path.write_bytes(IndexSerializer.serialize(index))
