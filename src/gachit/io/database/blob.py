from pathlib import Path

from gachit.domain.entity import Blob, Sha
from gachit.io.serializer import BlobSerializer

from .db import DataBase
from .object_header import ObjectHeader


class BlobIO:
    def __init__(self, git_dir: Path) -> None:
        self.db = DataBase(git_dir)

    def get(self, sha: Sha) -> Blob:
        header, data = self.db.read_object(sha)
        if header.object_type != Blob:
            raise ValueError(f"Object type is not Blob: {header.object_type}")
        return BlobSerializer.deserialize(data)

    def write(self, blob: Blob) -> Sha:
        blob_data = BlobSerializer.serialize(blob)
        header = ObjectHeader(Blob, len(blob_data))
        return self.db.write_object(header, blob_data)
